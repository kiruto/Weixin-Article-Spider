# -*- coding: utf-8 -*-
import os

import config

agent = config.agent
local_storage_path = os.path.join(os.path.dirname(__file__) + os.sep, "..", "data", "html") + os.sep


def __init__():
    if not os.path.exists(local_storage_path):
        os.makedirs(local_storage_path)
