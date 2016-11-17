# -*- coding: utf-8 -*-


class DownloadQueue:
    def __init__(self):
        self._queue = list()

    def add(self, info):
        self._queue.append(info)

    def resolve(self):
        if not self._queue:
            return
        else:
            pass
