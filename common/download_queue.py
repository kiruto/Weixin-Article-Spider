# -*- coding: utf-8 -*-
import threading
from time import sleep

from common.downloadtask import DownloadTask

delay_time = 3
_failed_queue = list()
running = False


def resolve(info_list):
    """

    :type info_list: list of dict {
        "author": 作者,
        "content_url": 下载地址,
        "copyright_stat": 授权信息,
        "cover": 封面图,
        "datetime": 发布时间,
        "digest": 简介,
        "fileid": 文件id,
        "main": 1,
        "qunfa_id": 群发消息id,
        "source_url": 外链,
        "title": 标题,
        "type": 消息类型(49是文章)
    }
    """
    if not info_list:
        return
    else:
        for info in range(0, len(info_list)):
            task = DownloadTask(info_list.pop(0))
            delay()
            request = task.request()
            if not request:
                continue
            success = request.save()
            if not success:
                _failed_queue.append(info)


def delay():
    return sleep(delay_time)


def is_running():
    return running
