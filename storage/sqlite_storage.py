# -*- coding: utf-8 -*-
import hashlib
import json
import sqlite3
import time

from storage import db

version = '1.0'


class SQLiteStorage:

    def __init__(self):
        self._connect = sqlite3.connect(db)
        self._create_table()

    def subscribe(self, wxid):
        c = self._connect.cursor()
        c.execute("INSERT INTO wxid VALUES (?)", [wxid])
        self._connect.commit()
        c.close()

    def unsubscribe(self, wxid):
        c = self._connect.cursor()
        c.execute("DELETE FROM wxid WHERE name=?", [wxid])
        self._connect.commit()
        c.close()

    def insert_article(self, article, local_url):
        c = self._connect.cursor()
        m = hashlib.md5()
        m.update(article.title)
        hash_id = m.hexdigest()
        date_time = time.localtime(int(article.datetime))
        date_time = time.strptime(date_time, "%Y-%m-%d")
        extra = json.dumps(article)
        data = (hash_id, date_time, article.title, "", extra, local_url, version)
        c.execute("INSERT INTO article VALUES (?, ?, ?, ?, ?, ?, ?)", data)
        self._connect.commit()
        c.close()

    def close(self):
        self._connect.close()

    def _create_table(self):
        c = self._connect.cursor()
        create_table_article = """CREATE TABLE IF NOT EXISTS article (
        hash_id text PRIMARY KEY,
        date_time text,
        title text,
        info text,
        extra text,
        content text,
        version text)"""
        create_table_wxid = "CREATE TABLE IF NOT EXISTS wxid (name text PRIMARY KEY)"
        c.execute(create_table_article)
        c.execute(create_table_wxid)
        self._connect.commit()
        c.close()
