# -*- coding: utf-8 -*-
import traceback

import flask


def get_success_response():
    return ResponseBody(1, 'ok')


def get_error_response(msg):
    print(msg)
    print(traceback.format_exc())
    return ResponseBody(-1, msg)


class ResponseBody(dict):

    def __init__(self, flag, msg, **kwargs):
        super(ResponseBody, self).__init__(flag=flag, msg=msg, **kwargs)

    def format(self):
        return flask.jsonify(self)
