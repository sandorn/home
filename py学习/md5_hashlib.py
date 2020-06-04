# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-02-26 10:26:44
@LastEditors: Even.Sand
@LastEditTime: 2020-02-26 16:39:23
'''
import hashlib


def md5(str):
    data = str
    m = hashlib.md5(data.encode("utf-8", 'ignore'))
    return (m.hexdigest())


print(md5('测试中'))
print(md5('测试�0�2 中'))
print(md5('第一千一百一十章薄面'))
