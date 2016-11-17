# -*- coding: utf-8 -*-
import sqlite3

from storage import db


class SQLiteStorage:

    def __init__(self):
        self._connect = sqlite3.connect(db)

        pass
