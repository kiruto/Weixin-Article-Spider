# -*- coding: utf-8 -*-
import shutil

import config

source_path = config.web_source_path
web_path = config.web_path


def pre_start():
    shutil.rmtree(path=web_path)
    ignore_patterns = (
        '*.ts',  # source file
        #'*.js.map', # only for debug
        '*.md', '*.yml', 'LICENSE', '.gitignore',  # text files
        'package.json', 'tsconfig.json', 'tslint.json', '.editorconfig'  # project level settings
    )
    shutil.copytree(src=source_path, dst=web_path, ignore=shutil.ignore_patterns(*ignore_patterns))
