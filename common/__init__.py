# -*- coding: utf-8 -*-
import time

__version__ = "1.0"


def get_time():
    date_time = time.localtime()
    return time.strftime("%Y-%m-%d", date_time)