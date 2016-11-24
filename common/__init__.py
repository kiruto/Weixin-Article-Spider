# -*- coding: utf-8 -*-
import os
import time
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


def save_row_to_file(text,
                     path=config.local_storage_raw_file_path,
                     file_name=time.strftime('%Y-%m-%d_%H:%M:%S__') + str(time.time()) + '.raw'):
    if not os.path.exists(path):
        os.makedirs(path)
    ff = open(path + file_name, 'w')
    ff.writelines(text)
    ff.close()


def save_page_error_log(text, exception):
    file_name = time.strftime('%Y-%m-%d_%H:%M:%S__') + str(time.time())
    save_row_to_file(text, file_name=file_name + '.html')
    save_row_to_file(exception, file_name=file_name + '.log')
