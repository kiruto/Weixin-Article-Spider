# -*- coding: utf-8 -*-
from __future__ import print_function
import hashlib
import os
import random
import traceback

import requests
import time

import botdriver
import common
import constants
from common import settings
from storage.sqlite_storage import SQLiteStorage
from wechatsogou import WechatCache
import config
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def _get_encoding_from_response(r):
    """获取requests库get或post返回的对象编码

    Args:
        r: requests库get或post返回的对象

    Returns:
        对象编码
    """
    encoding = requests.utils.get_encodings_from_content(r.text)
    return encoding[0] if encoding else requests.utils.get_encoding_from_headers(r.headers)


def get_article_id(info):
    m = hashlib.md5()
    m.update(info['title'])
    return m.hexdigest()


class DownloadTask:

    def __init__(self, info, subscribe=None):
        """

        :type subscribe: dict {
            "name": 微信号
        }
        :type info: {
            "author": 作者,
            "content_url": 下载地址,
            "copyright_stat": 授权信息,
            "cover": 封面图,
            "datetime": 发布时间,
            "digest": 简介,
            "fileid": 文件id,
            "main": 1,
            "qunfa_id": 群发消息id,
            "source_url": 外链,
            "title": 标题,
            "type": 消息类型(49是文章)
        }
        """
        self._agent = settings.agent
        self._cache = WechatCache(config.cache_dir, 60 * 60)
        self._session = requests.session()
        self.subscribe = subscribe

        self.info = info

    def request(self, url=None, host=None, referer=None, **kwargs):
        db_helper = SQLiteStorage()
        article_id = get_article_id(self.info)
        if db_helper.get_article(article_id) is not None:
            return None, "article %s has already exist." % article_id
        if not url:
            url = self.info['content_url']
        result = None
        if config.engine == constants.request:
            result = self._get_page_by_request(url=url)
        elif config.engine == constants.browser:
            result = self._get_page_by_web_driver(url=url)
        return DownloadedDocument(result, self), '%s download success' % url

    def _get_page_by_request(self, url=None, host=None, referer=None, **kwargs):
        headers = {
            "User-Agent": self._agent[random.randint(0, len(self._agent) - 1)],
            "Referer": referer if referer else "http://weixin.sogou.com/",
            "Host": host if host else "mp.weixin.qq.com",
        }
        result = self._session.get(url, headers=headers, **kwargs)
        result.encoding = _get_encoding_from_response(result)
        return result

    def _get_page_by_web_driver(self, url=None, host=None, referer=None, **kwargs):
        driver = botdriver.get_driver()
        driver.get(url)
        time.sleep(3)
        text = common.replace_html(driver.page_source)
        driver.close()
        return text


class DownloadedDocument:

    def __init__(self, content_text, download_task):
        self.content_text = content_text
        self.download_info = download_task.info
        self.subscribe = download_task.subscribe

    def get_save_path(self):
        return config.local_storage_path + common.get_time() + os.sep, common.get_time() + os.sep

    def get_file_name(self):
        return get_article_id(self.download_info) + ".html"

    def write_to_file(self):
        path, url = self.get_save_path()
        file_name = self.get_file_name()
        common.save_raw_to_file(self.content_text, path, file_name)
        return url + file_name

    def insert_into_db(self):
        db_helper = SQLiteStorage()
        article_id = get_article_id(self.download_info)
        if db_helper.get_article(article_id) is None:
            author = '' if not self.subscribe else self.subscribe["name"]
            db_helper.insert_article(self.download_info, self.write_to_file(), author)
        else:
            print("article %s has already exist." % article_id)

    def save(self):
        try:
            self.insert_into_db()
            return True, 'saved'
        except Exception as e:
            print(e.message, traceback.format_exc())
            return False, e.message
