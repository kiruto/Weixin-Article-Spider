# -*- coding: utf-8 -*-
from __future__ import print_function

import json
import os
from logging.handlers import RotatingFileHandler

import flask
from flask import Flask, request, abort
import logging

from flask import redirect
from flask import render_template
from flask import send_file
from flask import send_from_directory
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

import common
import constants
import web_service
from common import download_queue
import config
from common import sogou_api
from response_body import get_success_response, get_error_response, ResponseBody
from storage.sqlite_storage import SQLiteStorage

app = Flask(__name__)

if not os.path.exists(config.local_storage_path):
    os.makedirs(config.local_storage_path)

if not os.path.exists(config.db_path):
    os.makedirs(config.local_storage_path)

if not os.path.exists(config.log_path):
    os.makedirs(config.log_path)

if not os.path.exists(config.local_storage_raw_file_path):
    os.makedirs(config.local_storage_raw_file_path)


sqlite_helper = SQLiteStorage()


@app.before_request
def reject_head_request():
    if request.method == 'HEAD':
        abort(400)


@app.errorhandler(404)
def page_not_found(e):
    return get_error_response('Not found', should_print=False).format(), 404


@app.route('/')
def hp():
    return redirect('/s/index.html')


# node module dependencies
@app.route('/node_modules/<path:path>')
def node_modules(path):
    return send_from_directory(config.node_modules_path, path)


@app.route('/log/files/', defaults={'path': None})
@app.route('/log/files/<path:path>')
def show_log_files(path):
    base_dir = config.local_storage_raw_file_path
    abs_path = base_dir if not path else os.path.join(base_dir, path)

    if not os.path.exists(abs_path):
        return abort(404)

    if os.path.isfile(abs_path):
        return send_file(abs_path)

    files = os.listdir(abs_path)
    return render_template('files.html', files=files)


@app.route('/cache/html/<path:path>')
def get_page(path):
    return send_from_directory(config.local_storage_path, path)


# redirect to homepage
@app.route('/s', defaults={'path': None})
@app.route('/s/', defaults={'path': None})
# routing by Angular
@app.route('/s/articles', defaults={'path': None})
@app.route('/s/articles/<path:path>')
@app.route('/s/settings', defaults={'path': None})
@app.route('/s/settings/<path:path>')
@app.route('/s/status', defaults={'path': None})
@app.route('/s/status/<path:path>')
@app.route('/s/logs', defaults={'path': None})
@app.route('/s/logs/<path:path>')
def web_hp_default(path):
    return web_resource('index.html')


# dist web contents
@app.route('/s/<path:path>')
def web_resource(path):
    path = 'dist/' + path
    return app.send_static_file(path)


# only for test
@app.route('/rest/name/<account_name>')
def search_account_by_name(account_name):
    account_name = account_name.encode('UTF-8')
    api = sogou_api.get_wx_api()
    result = api.search_gzh_info(account_name)
    return flask.jsonify(result)


# only for test
@app.route('/rest/id/<account_id>')
def search_account_by_id(account_id):
    account_id = account_id.encode('UTF-8')
    api = sogou_api.get_wx_api()
    result = api.search_gzh_info(account_id)
    return flask.jsonify(result)


# only for test
@app.route('/rest/article/search/<keywords>')
def search_article_by_keywords(keywords):
    keywords = keywords.encode('UTF-8')
    api = sogou_api.get_wx_api()
    result = api.search_article_info(keywords)
    return flask.jsonify(result)


# only for test
@app.route('/rest/message/<account_id>')
def search_message_by_id(account_id):
    account_id = account_id.encode('UTF-8')
    api = sogou_api.get_wx_api()
    result = api.get_gzh_message(wechatid=account_id)
    return flask.jsonify(result)


# only for test
@app.route('/rest/article/all/<account_id>')
def list_all_articles_by_id(account_id):
    return flask.jsonify(sogou_api.get_articles_by_id(account_id))


@app.route('/rest/wxid/add/<wxid>')
def add_wxid(wxid):
    try:
        sqlite_helper.subscribe(wxid)
        return get_success_response().format()
    except Exception as e:
        return get_error_response(e.message).format()


@app.route('/rest/wxid/batch/', methods=['POST'])
def batch_wxid():
    data = request.data
    lst = json.loads(data)
    if isinstance(lst, list):
        sqlite_helper.batch_subscribe(lst)
        return get_success_response().format()
    else:
        return get_error_response(data + 'is not a list').format()


@app.route('/rest/exid/remove/<wxid>')
def remove_wxid(wxid):
    wxid = wxid.strip()
    sqlite_helper.unsubscribe(wxid)
    return get_success_response().format()


@app.route('/rest/status')
def get_status():
    return ResponseBody(1, download_queue.get_status()).format()


@app.route('/start')
def start():
    return get_success_response().format() if download_queue.start() else get_error_response('spider is running').format()


@app.route('/stop')
def stop():
    download_queue.stop()
    return get_success_response().format()


@app.route('/rest/progress')
def progress():
    if download_queue.get_status() == constants.BUSY:
        p = download_queue.get_thread_progress()
        return ResponseBody(**p).format()
    if download_queue.get_status() == constants.IDLE:
        return ResponseBody(total=0, progress=-1, sub_task_total=0, sub_task_progress=-1).format()


@app.route('/rest/log/<line>')
def get_log(line):
    try:
        line = int(line)
    except ValueError:
        return get_error_response('line must be a int number: %s' % line).format()
    if not line:
        line = 0
    l = download_queue.get_log_from(int(line))
    return ResponseBody(log=l).format()


@app.route('/rest/article/date/written/<date>')
def get_articles_by_date_written(date):
    if not common.valid_date_string(date):
        return get_error_response('%s is not a date' % date).format()
    articles = sqlite_helper.get_articles_by_date_written(date)
    return ResponseBody(articles=articles).format()


@app.route('/rest/article/date/create_at/<date>')
def get_articles_by_date_created(date):
    if not common.valid_date_string(date):
        return get_error_response('%s is not a date' % date).format()
    articles = sqlite_helper.get_articles_by_date_created(date)
    return ResponseBody(articles=articles).format()


@app.route('/rest/date/create_at')
def get_date_by_created():
    return ResponseBody(date=sqlite_helper.get_date_by_created()).format()


@app.route('/rest/date/written')
def get_date_by_written():
    return ResponseBody(date=sqlite_helper.get_date_by_written()).format()


@app.route('/rest/wxid/list')
def get_wxid_list():
    subscribes = sqlite_helper.get_wxid_list()
    return ResponseBody(wxid_list=subscribes).format()


# only for test
@app.route('/save')
def save_page():
    subscribes = sqlite_helper.get_wxid_list()
    print(subscribes)
    try:
        info_list = list()
        for s in subscribes:
            print("processing wxid=%s" % s['name'])
            all_articles = sogou_api.get_articles_by_id(s['name'])
            for a in all_articles:
                info_list.append(a)
            download_queue.resolve(info_list)
        return get_success_response().format()
    except Exception as e:
        return get_error_response(e.message).format()


@app.route('/clean')
def clean_cache_and_db(): pass


def _get_log_path():
    return config.log_path + common.get_time() + '_flask.log'


if __name__ == '__main__':
    web_service.pre_start()
    handler = RotatingFileHandler(_get_log_path(), maxBytes=100000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    # app.run(host='0.0.0.0', port=config.http_port)
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(config.http_port)
    IOLoop.instance().start()
