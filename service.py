# -*- coding: utf-8 -*-
from __future__ import print_function
import os
from logging.handlers import RotatingFileHandler

import flask
from flask import Flask, request, abort
import logging

import botdriver
import common
from common import download_queue
import config
from response_body import get_success_response, get_error_response
from wechatsogou import WechatSogouApi
from storage.sqlite_storage import SQLiteStorage

app = Flask(__name__)
_api = WechatSogouApi()

if not os.path.exists(config.local_storage_path):
    os.makedirs(config.local_storage_path)

if not os.path.exists(config.db_path):
    os.makedirs(config.local_storage_path)

if not os.path.exists(config.log_path):
    os.makedirs(config.log_path)


sqlite_helper = SQLiteStorage()


@app.before_request
def reject_head_request():
    if request.method == 'HEAD':
        abort()


@app.errorhandler(404)
def page_not_found(e):
    return get_error_response(e.message), 404


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
    return flask.jsonify(_get_articles_by_id(account_id))


@app.route('/rest/wxid/add/<wxid>')
def add_wxid(wxid):
    try:
        sqlite_helper.subscribe(wxid)
        return get_success_response().format()
    except Exception as e:
        return get_error_response(e.message).format()


@app.route('/save')
def save_page():
    subscribes = sqlite_helper.get_wxid_list()
    print(subscribes)
    try:
        info_list = list()
        for s in subscribes:
            print("processing wxid=%s" % s['name'])
            all_articles = _get_articles_by_id(s['name'])
            for a in all_articles:
                info_list.append(a)
            download_queue.resolve(info_list)
        return get_success_response().format()
    except Exception as e:
        return get_error_response(e.message).format()


def get_wx_api():
    return _api


def _get_articles_by_id(account_id):
    account_id = account_id.encode('UTF-8')
    api = get_wx_api()
    articles = api.get_gzh_message(wechatid=account_id)
    result = []
    for a in articles:
        if a['type'] == '49':
            result.append(a)
    return result


def _get_log_path():
    return config.log_path + common.get_time() + '_flask.log'


if __name__ == '__main__':
    handler = RotatingFileHandler(_get_log_path(), maxBytes=100000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()
