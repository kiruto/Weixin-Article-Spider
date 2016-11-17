# -*- coding: utf-8 -*-
import config

db = config.db_path + config.db_file

create_table_article = "CREATE TABLE article (date text, title text, info text, extra text, content text)"
create_table_wxid = "CREATE TABLE WXID (name text)"
