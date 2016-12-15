# -*- coding: utf-8 -*-
import hashlib
import json
import re
import sqlite3
import time
import datetime

import common
from storage import db

version = '1.0'


class SQLiteStorage:

    def __init__(self):
        self._connect = sqlite3.connect(db)
        self._connect.text_factory = str
        self._create_table()

    def subscribe(self, wxid):
        c = self._connect.cursor()
        c.execute("INSERT INTO wxid(name) VALUES (?)", [wxid])
        self._connect.commit()
        c.close()

    def unsubscribe(self, wxid):
        c = self._connect.cursor()
        c.execute("DELETE FROM wxid WHERE name=?", [wxid])
        self._connect.commit()
        c.close()

    def batch_subscribe(self, id_list):
        c = self._connect.cursor()
        data = []
        for i in id_list:
            i = i.strip()
            if len(i) == 0:
                continue
            if not common.is_wxid(i):
                continue
            p = (i, )
            data.append(p)
        try:
            c.executemany("INSERT OR REPLACE INTO wxid(name) VALUES (?)", data)
            self._connect.commit()
        except Exception as e:
            print(e)
            common.save_raw_error_log(exception=e)
        c.close()

    def edit_extra(self, wxid, extra_dict):
        """

        :param wxid: string 微信id
        :type extra_dict: dict
            name: 公众号名称
            wechatid: 公众号id
            jieshao: 介绍
            renzhen: 认证，为空表示未认证
            qrcode: 二维码
            img: 头像图片
            url: 最近文章地址
        """
        if not wxid or not extra_dict:
            return
        if isinstance(extra_dict, dict):
            extra_dict['version'] = version
            extra = json.dumps(extra_dict)
            c = self._connect.cursor()
            c.execute("UPDATE wxid SET extra=? WHERE name=?", [extra, wxid])
            self._connect.commit()
            c.close()

    def get_wxid_list(self):
        c = self._connect.cursor()
        result = c.execute("SELECT * FROM wxid").fetchall()
        c.close()
        result_list = list()
        for r in result:
            result_list.append(WXIDRecord(r))
        return result_list

    def insert_article(self, article, local_url, author_name=''):
        c = self._connect.cursor()
        m = hashlib.md5()
        m.update(article['title'])
        hash_id = m.hexdigest()
        date_time = time.localtime(int(article['datetime']))
        date_time = time.strftime("%Y-%m-%d", date_time)
        extra = json.dumps(article)
        data = (hash_id, date_time, article['title'], "", extra, local_url, version, author_name)
        c.execute("""INSERT INTO article(hash_id, date_time, title, info, extra, content, version, author)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", data)
        self._connect.commit()
        c.close()

    def get_article(self, hash_id):
        c = self._connect.cursor()
        result = c.execute("SELECT * FROM article WHERE hash_id=?", [hash_id]).fetchone()
        c.close()
        if not result:
            return None
        else:
            return ArticleRecord(result)

    def get_articles_by_date_created(self, date):
        c = self._connect.cursor()
        result = c.execute("SELECT * FROM article"
                           " WHERE created_at BETWEEN date(?) AND date(?, '+1 day')", [date, date]).fetchall()
        articles = list()
        for r in result:
            articles.append(ArticleRecord(r))
        c.close()
        return articles

    def get_articles_by_date_written(self, date):
        c = self._connect.cursor()
        result = c.execute("SELECT * FROM article WHERE date_time=?", [date]).fetchall()
        articles = list()
        for r in result:
            articles.append(ArticleRecord(r))
        c.close()
        return articles

    def get_articles_by_author(self, author):
        c = self._connect.cursor()
        result = c.execute("SELECT * FROM article WHERE author=?", [author]).fetchall()
        articles = list()
        for r in result:
            articles.append(ArticleRecord(r))
        c.close()
        return articles

    def get_date_by_created(self):
        d = datetime.datetime.now()
        offset = datetime.timedelta(days=7)
        day = d - offset
        date_from = datetime.datetime(day.year, day.month, day.day, 0, 0, 0)
        date = str(date_from)
        c = self._connect.cursor()
        result = c.execute("SELECT strftime('%Y-%m-%d', created_at) FROM article"
                           " WHERE datetime(created_at)>=datetime(?)"
                           " GROUP BY strftime('%Y-%m-%d', created_at)", [date]).fetchall()
        return result

    def get_date_by_written(self):
        d = datetime.datetime.now()
        offset = datetime.timedelta(days=7)
        day = d - offset
        date_from = datetime.datetime(day.year, day.month, day.day, 0, 0, 0)
        date = str(date_from)
        c = self._connect.cursor()
        result = c.execute("SELECT strftime('%Y-%m-%d', date_time) FROM article"
                           " WHERE datetime(date_time)>=datetime(?)"
                           " GROUP BY strftime('%Y-%m-%d', date_time)", [date]).fetchall()
        return result

    def close(self):
        self._connect.close()

    def _create_table(self):
        c = self._connect.cursor()
        create_table_article = """CREATE TABLE IF NOT EXISTS article (
        hash_id text PRIMARY KEY,
        date_time text,
        created_at text NOT NULL DEFAULT (datetime('now', 'localtime')),
        title text,
        info text,
        extra text,
        content text,
        version text,
        author text)"""
        create_table_wxid = "CREATE TABLE IF NOT EXISTS wxid (name text PRIMARY KEY, extra text)"
        c.execute(create_table_article)
        c.execute(create_table_wxid)
        self._connect.commit()
        c.close()


class WXIDRecord(dict):

    def __init__(self, row, **kwargs):
        super(WXIDRecord, self).__init__(name=row[0], extra=row[1], **kwargs)
        if self['extra']:
            try:
                self['extra'] = json.loads(self['extra'])
            except Exception as e:
                print(e)


class ArticleRecord(dict):

    def __init__(self, row, **kwargs):
        """

        :param row: 从SELECT * FROM articles中出来的原始结果
        :param kwargs:
        """
        super(ArticleRecord, self).__init__(
            hash_id=row[0],
            date_time=row[1],
            created_at=row[2],
            title=row[3],
            info=row[4],
            extra=row[5],
            content=row[6],
            version=row[7],
            author=row[8],
            **kwargs)
        self['extra'] = json.loads(self['extra'])
