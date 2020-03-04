# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-20 20:03:57
@LastEditors: Even.Sand
@LastEditTime: 2019-05-20 20:08:52
'''
from pyquery import PyQuery as pq
doc = pq(url='http://www.baidu.com/s?wd=减肥&&pn=20', encoding="utf-8")
print(doc('title'))
