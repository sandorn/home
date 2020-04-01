# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-26 16:19:29
@LastEditors: Even.Sand
@LastEditTime: 2020-03-26 16:19:31
'''


# *允许你传入0个或任意个参数，这些可变参数在函数调用时自动组装为一个tuple。
def f(a, *args):
    print(args)


f(1, 2, 3, 4)


def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    print(sum)


calc(1, 2, 3, 4)


# **,关键字参数允许你传入0个或任意个含参数名的参数,这些关键字参数在函数内部自动组装为一个dict。
def d(**kargs):
    print(kargs)


d(a=1, b=2)

# 在函数混合使用*以及**。


def h(a, *args, **kargs):
    print(a, args, kargs)


h(1, 2, 3, x=4, y=5)


def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)


person('Adam', 45, gender='M', job='Engineer')
