# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2020-02-12 15:30:36
@LastEditors: Even.Sand
@LastEditTime: 2020-03-18 02:27:28
'''

import os
import sys

from scrapy.cmdline import execute


def ScrapyRun(dirpath, spilername):
    # 添加环境变量
    sys.path.append(dirpath)
    # 切换工作目录
    os.chdir(dirpath)
    print(dirpath, 'Scrapy爬虫启动中.......')

    # 启动爬虫,第三个参数为爬虫name
    execute(['scrapy', 'crawl', spilername])


if __name__ == '__main__':
    import logging
    # 调用调试输出
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
