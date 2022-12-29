# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2022-12-29 12:06:48
FilePath     : /py学习/线程协程/pyquery爬虫库demo.py
Github       : https://github.com/sandorn/home
==============================================================
'''
from pyquery import PyQuery as pq

# response = pq(url='https://www.baidu.com', encoding="utf-8")
# print(type(response))
# print(response)
response = pq(url='https://www.baidu.com', encoding="utf-8")
print(type(response))
print(response)
print(response('title').text())
