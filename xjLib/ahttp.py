# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-04 09:01:10
@LastEditors: Even.Sand
@LastEditTime: 2020-03-04 20:21:40
'''


import ahttp


def ahttpGet(url, params=None, **kwargs):
    task = ahttp.get(url, params=params, **kwargs)
    clientResponse = task.run()
    return clientResponse


def ahttpGetAll(urls, pool=2, callback=None, params=None, **kwargs):
    tasks = [ahttp.get(url, params=params, **kwargs) for url in urls]
    resps = ahttp.run(tasks, pool=pool, callback=callback)
    return resps
