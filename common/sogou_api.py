# -*- coding: utf-8 -*-
from wechatsogou import WechatSogouApi

_api = WechatSogouApi()


def get_wx_api():
    return _api


def get_articles_by_id(account_id):
    account_id = account_id.encode('UTF-8')
    api = get_wx_api()
    articles = api.get_gzh_message(wechatid=account_id)
    result = []
    for a in articles:
        if a['type'] == '49':
            result.append(a)
    return result
