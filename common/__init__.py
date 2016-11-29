# -*- coding: utf-8 -*-
import os
import time
import traceback
from datetime import datetime

import config
import settings

__version__ = "1.0"


def get_time():
    date_time = time.localtime()
    return time.strftime("%Y-%m-%d", date_time)


def valid_date_string(string):
    try:
        datetime.strptime(string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def save_raw_to_file(text,
                     path=config.local_storage_raw_file_path,
                     file_name=time.strftime('%Y-%m-%d_%H:%M:%S__') + str(time.time()) + '.raw'):
    if not os.path.exists(path):
        os.makedirs(path)
    ff = open(path + file_name, 'w')
    ff.writelines(text)
    ff.close()


def save_raw_error_log(raw_text=None, exception=None):
    file_name = time.strftime('%Y-%m-%d_%H:%M:%S__') + str(time.time())
    if raw_text:
        save_raw_to_file(raw_text, file_name=file_name + '.html')
    if exception:
        if isinstance(exception, Exception):
            save_raw_to_file(traceback.format_exc(), file_name=file_name + '.log')
        else:
            save_raw_to_file(exception, file_name=file_name + '.log')


def replace_html(s):
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
