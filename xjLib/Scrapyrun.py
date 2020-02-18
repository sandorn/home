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
@LastEditors  : Even.Sand
@LastEditTime : 2020-02-13 03:03:21
'''


from scrapy.cmdline import execute
import sys
import os
# 获取当前脚本路径
dirpath = os.path.dirname(os.path.abspath(__file__))
# 运行文件绝对路径
print(os.path.abspath(__file__))
# 运行文件父路径
print(dirpath)
# 添加环境变量
sys.path.append(dirpath)
# 切换工作目录
os.chdir(dirpath)
# 启动爬虫,第三个参数为爬虫name
execute(['scrapy', 'crawl', '爬虫name', '-o', 'items.json', '-s', 'FEED_EXPORT_ENCODING=utf-8'])