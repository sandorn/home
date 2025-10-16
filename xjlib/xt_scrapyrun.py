# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-07-01 13:24:31
FilePath     : /CODE/xjLib/xt_ScrapyRun.py
Github       : https://github.com/sandorn/home
==============================================================
"""
from __future__ import annotations

import os
import sys

from scrapy.cmdline import execute


def ScrapyRun(dirpath, spilername):
    # 添加环境变量
    sys.path.append(dirpath)
    # 切换工作目录
    os.chdir(dirpath)
    print(f"{dirpath} | {spilername!s} 爬虫启动中.......")
    # 启动爬虫,第三个参数为爬虫name
    execute(["scrapy", "crawl", spilername])
