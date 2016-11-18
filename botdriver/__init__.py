# -*- coding: utf-8 -*-
from __future__ import print_function

import time
from selenium import webdriver

import config

__version__ = "1.0"


def get_driver():
    if config.browser == "chrome":
        return webdriver.Chrome(executable_path=config.chrome_path,
                                service_log_path=config.log_path + time.strftime("%Y-%m-%d") + "_chrome.log")
    elif config.browser == "phantomjs":
        return webdriver.PhantomJS(executable_path=config.phantomjs_path,
                                   service_log_path=config.log_path + time.strftime("%Y-%m-%d") + "_ghost.log")
    else:
        print("%s not found" % config.browser)
        raise Exception()
