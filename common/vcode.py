# -*- coding: utf-8 -*-
import os
import traceback

from PIL import Image

import config
from common import download_queue

VCODE_LOCKED_IP = 'locked_ip'
VCODE_FROM_ARTICLE_LIST = 'article_list'
temp_driver = None
solved = False
vcode_type = None


def generate_code(vcode_from=VCODE_FROM_ARTICLE_LIST):
    if not temp_driver:
        raise VCodeSessionException('session not created.')
    if vcode_from == VCODE_FROM_ARTICLE_LIST:
        filename = 'article_list_vcode'
        element_id = 'verify_img'
        global vcode_type
        vcode_type = VCODE_FROM_ARTICLE_LIST
    elif vcode_from == VCODE_LOCKED_IP:
        filename = 'locked_ip_vcode'
        element_id = 'seccodeImage'
        global vcode_type
        vcode_type = VCODE_LOCKED_IP
    else:
        return
    try:
        element = temp_driver.find_element_by_id(element_id)  # find part of the page you want image of
        location = element.location
        size = element.size
        temp_driver.save_screenshot(config.cache_path + filename + '.png')  # saves screenshot of entire page
        im = Image.open(config.cache_path + filename + '.png')  # uses PIL library to open image in memory

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        print('p1x%s, p1y%s, p2x%s, p2y%s' % (left, top, right, bottom))

        im = im.crop((left, top, right, bottom))  # defines crop points
        im.save(config.cache_path + filename + '.png')  # saves new cropped image
        print('saved')
    except Exception as e:
        print('failed while create vcode session.')
        print(e)
        print(traceback.format_exc())
        close_session()


def get_vcode_img_file():
    return config.cache_path + 'article_list_vcode.png'


def resolve_vcode(code, vcode_from):
    if not temp_driver:
        raise VCodeSessionException('session not created.')
    if not vcode_from == vcode_type:
        raise VCodeSessionException('try to resolve a wrong vcode')
    if vcode_from == VCODE_FROM_ARTICLE_LIST:
        input_element_id = 'input'
        submit_element_id = 'bt'
    elif vcode_from == VCODE_LOCKED_IP:
        input_element_id = 'seccodeInput'
        submit_element_id = 'submit'
    else:
        return False
    form = temp_driver.find_element_by_id(input_element_id)
    form.clear()
    form.send_keys(code)
    submit = temp_driver.find_element_by_id(submit_element_id)
    submit.click()
    global solved
    solved = True
    return True


def create_session(driver, vcode_from=VCODE_FROM_ARTICLE_LIST):
    print('need input vcode')
    download_queue.log_to_bot_process(flag='error', msg='需要输入验证码(时限1分钟)')
    global temp_driver
    global solved
    solved = False
    print('temp_driver')
    print(temp_driver)
    print('driver')
    print(driver)
    if temp_driver:
        close_session()
    if driver:
        temp_driver = driver
        generate_code(vcode_from)


def close_session():
    global temp_driver
    if temp_driver:
        try:
            temp_driver.close()
        except:
            pass
        temp_driver = None
    try:
        os.remove(config.cache_path + 'article_list_vcode.png')
    except Exception as e:
        print('error at delete file')
        print(e)
        print(traceback.format_exc())


class VCodeSessionException(Exception):
    """
    验证码对话错误
    """
