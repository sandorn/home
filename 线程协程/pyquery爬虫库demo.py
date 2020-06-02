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
@LastEditTime: 2020-03-27 11:18:30
'''
from pyquery import PyQuery as pq
# response = pq(url='https://www.baidu.com', encoding="utf-8")
# print(type(response))
# print(response)
response = pq(url='http://www.baidu.com/s?wd=减肥&pn=10&oq=减肥&ie=utf-8&usm=1&rsv_pq=b58cbecf0001c4b9&rsv_t=4c4aEgaUKptWNHVGpVHRqWs13bTEoZ%2BBOrZvjwsDu1LE25Ll3Tl1J%2BHi8kc', encoding="utf-8")
print(type(response))
print(response)
