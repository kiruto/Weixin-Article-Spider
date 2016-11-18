# -*- coding: utf-8 -*-
from __future__ import print_function
from selenium import webdriver

import config

__version__ = "1.0"


def get_driver():
    if config.browser == "chrome":
        return webdriver.Chrome(executable_path=config.chrome_path)
    elif config.browser == "phantomjs":
        return webdriver.PhantomJS(executable_path=config.phantomjs_path)
    else:
        print("%s not found" % config.browser)
        raise Exception()
