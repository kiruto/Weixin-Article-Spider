# -*- coding: utf-8 -*-

import flask
from flask import Flask

from common.downloader import Downloader
import config
from wechatsogou import WechatSogouApi

app = Flask(__name__)
_api = WechatSogouApi()


@app.route('/')
def homepage():
    return 'HP'


@app.route('/rest/name/<account_name>')
def search_account_by_name(account_name):
    account_name = account_name.encode('UTF-8')
    api = get_wx_api()
    result = api.search_gzh_info(account_name)
    return flask.jsonify(result)


@app.route('/rest/id/<account_id>')
def search_account_by_id(account_id):
    account_id = account_id.encode('UTF-8')
    api = get_wx_api()
    result = api.search_gzh_info(account_id)
    return flask.jsonify(result)


@app.route('/rest/article/<keywords>')
def search_article_by_keywords(keywords):
    keywords = keywords.encode('UTF-8')
    api = get_wx_api()
    result = api.search_article_info(keywords)
    return flask.jsonify(result)


@app.route('/rest/message/<account_id>')
def search_message_by_id(account_id):
    account_id = account_id.encode('UTF-8')
    api = get_wx_api()
    result = api.get_gzh_message(wechatid=account_id)
    return flask.jsonify(result)


@app.route('/rest/article/all/<account_id>')
def list_all_articles_by_id(account_id):
    account_id = account_id.encode('UTF-8')
    api = get_wx_api()
    articles = api.get_gzh_message(wechatid=account_id)
    result = []
    for a in articles:
        if a['type'] == '49':
            result.append(a)
    return flask.jsonify(result)


@app.route('/save')
def save_page():
    return Downloader().request('http://mp.weixin.qq.com/s?timestamp=1479366299&src=3&ver=1&signature=Hgvz-IGx2pIJPosLHdR8yqwE8wo1jDbAOGZxFavHFvgo133ujBz7OhOogEJsz5J85pFSj7y4yeGTNb5dkgJ0xm6Jxx4kKgBsIE8ri6F9r8JFG7Gsfqzd9qpdJCTCyblwYZtb9MxAyV8c36SvmvE5mbvcXZ7LeQ4aaP2qZYg1B4k=').text


def get_wx_api():
    return _api


if __name__ == '__main__':
    app.run()
