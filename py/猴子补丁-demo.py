# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-06-03 14:48:23
@LastEditors: Even.Sand
@LastEditTime: 2019-06-03 14:49:17
'''


class Foo(object):
    def bar(self):
        print('Foo.bar')


def vrrr(self):
    print('Modified vrrr')


Foo().bar()
Foo.bar = vrrr

Foo().bar()
