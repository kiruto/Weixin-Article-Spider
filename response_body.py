# -*- coding: utf-8 -*-
import traceback

import flask


def get_success_response():
    return ResponseBody(1, 'ok')


def get_error_response(msg, should_print=True):
    if should_print:
        print(msg)
        print(traceback.format_exc())
    return ResponseBody(-1, msg)


class ResponseBody(dict):

    def __init__(self, flag=1, msg='ok', **kwargs):
        super(ResponseBody, self).__init__(flag=flag, msg=msg, **kwargs)

    @classmethod
    def __call__(cls, **kwargs):
        instance = ResponseBody(**kwargs)
        return instance.format()

    def format(self):
        return flask.jsonify(self)
