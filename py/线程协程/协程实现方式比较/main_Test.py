# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-22 11:18:34
@LastEditors: Even.Sand
@LastEditTime: 2020-03-12 11:15:50
'''
import matplotlib.pyplot as plt

import asyncio_Test
import gevent_Test

asyncio_list = []
gevent_list = []

N = 100
Begin = 1
url = 'http://www.python.org'
for i in range(N):
    asyncio_list.append(asyncio_Test.f(Begin + i, url))
    gevent_list.append(gevent_Test.f(Begin + i, url))

plt.plot(asyncio_list, label='asyncio')
plt.plot(gevent_list, label='gevent')

plt.legend()
plt.savefig('1.png')
plt.show()
