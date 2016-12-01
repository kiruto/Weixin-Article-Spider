# -*- coding: utf-8 -*-
import os
import shutil

import subprocess

import sys

import config

source_path = config.web_source_path
web_path = config.web_path
tsc_path = os.path.join(config.node_modules_path, "typescript", "bin", "tsc")


def pre_start():
    # compile ts
    child = subprocess.Popen(tsc_path, stdout=subprocess.PIPE, shell=True)
    while True:
        out = child.stdout.read(1)
        if out == '' and child.poll() is not None:
            break
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()
    if child.returncode:
        raise RuntimeError('TS files may have error.')
    else:
        print('TS compiled.')
        print('Deploying Javascript to static paths...')
    shutil.rmtree(path=web_path)
    ignore_patterns = (
        '*.ts',  # source file
        # '*.js.map', # only for debug
        '*.md', '*.yml', 'LICENSE', '.gitignore',  # text files
        'package.json', 'tsconfig.json', 'tslint.json', '.editorconfig'  # project level settings
    )
    print('ignore types: {array}'.format(array=ignore_patterns))
    shutil.copytree(src=source_path, dst=web_path, ignore=shutil.ignore_patterns(*ignore_patterns))
    print('Javascript deployed.')
