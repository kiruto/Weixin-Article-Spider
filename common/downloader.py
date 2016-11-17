# -*- coding: utf-8 -*-
import random

import requests

from common import settings
from wechatsogou import WechatCache
import config
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Downloader:

    def __init__(self):
        self._agent = settings.agent
        self._cache = WechatCache(config.cache_dir, 60 * 60)
        self._session = requests.session()
        pass

    def request(self, url, host=None, referer=None, **kwargs):
        headers = {
            "User-Agent": self._agent[random.randint(0, len(self._agent) - 1)],
            "Referer": referer if referer else "http://weixin.sogou.com/",
            "Host": host if host else "mp.weixin.qq.com",
        }
        result = self._session.get(url, headers=headers, **kwargs)
        result.encoding = self._get_encoding_from_response(result)
        self.save(result)
        return result

    def save(self, response):
        ff = open(settings.local_storage_path + "temp.txt", 'w')
        ff.writelines(response.text)
        ff.close()
        pass

    def _get_encoding_from_response(self, r):
        """获取requests库get或post返回的对象编码

        Args:
            r: requests库get或post返回的对象

        Returns:
            对象编码
        """
        encoding = requests.utils.get_encodings_from_content(r.text)
        return encoding[0] if encoding else requests.utils.get_encoding_from_headers(r.headers)
