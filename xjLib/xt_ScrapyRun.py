# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:49
FilePath     : /xjLib/xt_ScrapyRun.py
LastEditTime : 2022-11-14 22:23:00
Github       : https://github.com/sandorn/home
==============================================================
'''
import os
import sys

from scrapy.cmdline import execute


def ScrapyRun(dirpath, spilername):
    # 添加环境变量
    sys.path.append(dirpath)
    # 切换工作目录
    os.chdir(dirpath)
    print(f'{dirpath} | {str(spilername)} 爬虫启动中.......')
    # 启动爬虫,第三个参数为爬虫name
    execute(['scrapy', 'crawl', spilername])
