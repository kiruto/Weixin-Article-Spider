# -*- coding: utf-8 -*-
import logging
import requests
import random
import time
import re
from lxml import etree
from PIL import Image

import common


def get_gzh_article_gzh_by_url_dict(text, url):
    """最近文章页  公众号信息

    Args:
        text: 最近文章文本

    Returns:
        字典{'name':name,'wechatid':wechatid,'introduction':introduction,'authentication':authentication,'qrcode':qrcodes,'img':img,'url':url}
        name: 公众号名称
        wechatid: 公众号id
        jieshao: 介绍
        renzhen: 认证，为空表示未认证
        qrcode: 二维码
        img: 头像图片
        url: 最近文章地址
    """
    page = etree.HTML(text)
    profile_info_area = page.xpath("//div[@class='profile_info_area']")[0]
    img = profile_info_area.xpath('div[1]/span/img/@src')[0]
    name = profile_info_area.xpath('div[1]/div/strong/text()')[0]
    name = _replace_space(name)
    wechatid = profile_info_area.xpath('div[1]/div/p/text()')
    if wechatid:
        wechatid = wechatid[0].replace(u'微信号: ', '')
    else:
        wechatid = ''
    introduction = profile_info_area.xpath('ul/li[1]/div/text()')[0]
    authentication = profile_info_area.xpath('ul/li[2]/div/text()')
    authentication = authentication[0] if authentication else ''
    qrcode = page.xpath('//*[@id="js_pc_qr_code_img"]/@src')[0]
    qrcode = 'http://mp.weixin.qq.com/' + qrcode if qrcode else ''
    return {
        'name': name,
        'wechatid': wechatid,
        'introduction': introduction,
        'authentication': authentication,
        'qrcode': qrcode,
        'img': img,
        'url': url
    }


def get_gzh_article_by_url_dict(text):
    """最近文章页 文章信息

    Args:
        text: 最近文章文本

    Returns:
        msgdict: 最近文章信息字典
    """
    msglist = re.findall("var msgList = '(.+?)';", text, re.S)[0]
    msgdict = eval(_replace_html(msglist))
    return msgdict


def _deal_gzh_article_dict(msgdict, **kwargs):
    """解析 公众号 群发消息

    Args:
        msgdict: 信息字典

    Returns:
        列表，均是字典，一定含有一下字段qunfa_id,datetime,type

        当type不同时，含有不同的字段，具体见文档
    """
    biz = kwargs.get('biz', '')
    uin = kwargs.get('uin', '')
    key = kwargs.get('key', '')
    items = list()
    for listdic in msgdict['list']:
        item = dict()
        comm_msg_info = listdic['comm_msg_info']
        item['qunfa_id'] = comm_msg_info.get('id', '')  # 不可判重，一次群发的消息的id是一样的
        item['datetime'] = comm_msg_info.get('datetime', '')
        item['type'] = str(comm_msg_info.get('type', ''))
        if item['type'] == '1':
            # 文字
            item['content'] = comm_msg_info.get('content', '')
        elif item['type'] == '3':
            # 图片
            item[
                'img_url'] = 'https://mp.weixin.qq.com/mp/getmediadata?__biz=' + biz + '&type=img&mode=small&msgid=' + \
                             str(item['qunfa_id']) + '&uin=' + uin + '&key=' + key
        elif item['type'] == '34':
            # 音频
            item['play_length'] = listdic['voice_msg_ext_info'].get('play_length', '')
            item['fileid'] = listdic['voice_msg_ext_info'].get('fileid', '')
            item['audio_src'] = 'https://mp.weixin.qq.com/mp/getmediadata?__biz=' + biz + '&type=voice&msgid=' + \
                                str(item['qunfa_id']) + '&uin=' + uin + '&key=' + key
        elif item['type'] == '49':
            # 图文
            app_msg_ext_info = listdic['app_msg_ext_info']
            url = app_msg_ext_info.get('content_url')
            if url:
                url = 'http://mp.weixin.qq.com' + url if 'http://mp.weixin.qq.com' not in url else url
            else:
                url = ''
            item['main'] = 1
            item['title'] = app_msg_ext_info.get('title', '')
            item['digest'] = app_msg_ext_info.get('digest', '')
            item['fileid'] = app_msg_ext_info.get('fileid', '')
            item['content_url'] = url
            item['source_url'] = app_msg_ext_info.get('source_url', '')
            item['cover'] = app_msg_ext_info.get('cover', '')
            item['author'] = app_msg_ext_info.get('author', '')
            item['copyright_stat'] = app_msg_ext_info.get('copyright_stat', '')
            items.append(item)
            if app_msg_ext_info.get('is_multi', 0) == 1:
                for multidic in app_msg_ext_info['multi_app_msg_item_list']:
                    url = multidic.get('content_url')
                    if url:
                        url = 'http://mp.weixin.qq.com' + url if 'http://mp.weixin.qq.com' not in url else url
                    else:
                        url = ''
                    itemnew = dict()
                    itemnew['qunfa_id'] = item['qunfa_id']
                    itemnew['datetime'] = item['datetime']
                    itemnew['type'] = item['type']
                    itemnew['main'] = 0
                    itemnew['title'] = multidic.get('title', '')
                    itemnew['digest'] = multidic.get('digest', '')
                    itemnew['fileid'] = multidic.get('fileid', '')
                    itemnew['content_url'] = url
                    itemnew['source_url'] = multidic.get('source_url', '')
                    itemnew['cover'] = multidic.get('cover', '')
                    itemnew['author'] = multidic.get('author', '')
                    itemnew['copyright_stat'] = multidic.get('copyright_stat', '')
                    items.append(itemnew)
            continue
        elif item['type'] == '62':
            item['cdn_videoid'] = listdic['video_msg_ext_info'].get('cdn_videoid', '')
            item['thumb'] = listdic['video_msg_ext_info'].get('thumb', '')
            item['video_src'] = 'https://mp.weixin.qq.com/mp/getcdnvideourl?__biz=' + biz + '&cdn_videoid=' + item[
                'cdn_videoid'] + '&thumb=' + item['thumb'] + '&uin=' + uin + '&key=' + key
        items.append(item)

    items_new = []  # 删除搜狗本身携带的空数据
    for item in items:
        if (int(item['type']) == 49) and (not item['content_url']):
            pass
        else:
            items_new.append(item)
    return items_new


def _replace_space(s):
    s = s.replace(' ', '')
    s = s.replace('\r\n', '')
    return s


def _replace_html(s):
    """替换html‘&quot;’等转义内容为正常内容

    Args:
        s: 文字内容

    Returns:
        s: 处理反转义后的文字
    """
    s = s.replace('&#39;', '\'')
    s = s.replace('&quot;', '"')
    s = s.replace('&amp;', '&')
    s = s.replace('&gt;', '>')
    s = s.replace('&lt;', '<')
    s = s.replace('&yen;', '¥')
    s = s.replace('amp;', '')
    s = s.replace('&lt;', '<')
    s = s.replace('&gt;', '>')
    s = s.replace('&nbsp;', ' ')
    s = s.replace('\\', '')
    return s
