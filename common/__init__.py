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
