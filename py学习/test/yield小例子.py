# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-28 14:47:15
@LastEditors: Even.Sand
@LastEditTime: 2019-05-28 17:09:51

python中yield的用法详解——最简单，最清晰的解释 - mieleizhi0522的博客 - CSDN博客
https://blog.csdn.net/mieleizhi0522/article/details/82142856
'''


def foo():
    print("starting...")
    while True:
        res = yield 4
        print("res:", res)


g = foo()
print(next(g))
print("*" * 20)
print(g.send(7))


def foo2(num):
    print("starting...")
    while num < 10:
        num = num + 1
        yield num


for n in foo2(0):
    print(n)


def flatten(nested):
    try:
        # 不要迭代类似字符串的对象：
        # if isinstance(variate,list) or isinstance(variate,tuple):
        try:
            nested + ''
        except TypeError:
            pass
        else:
            raise TypeError

        for sublist in nested:
            for element in flatten(sublist):
                yield element
    except TypeError:
        yield nested


res = ([1, 2, 3, 4, 5], [11, 46,
                         87], [125232], [5667, 2356, 26, 6215, 9741, 23525])
res2 = [
    'and', 'B', ['not', 'A'], [1, 2, 1, [2, 1], [1, 1, [2, 2, 1]]],
    ['not', 'A', 'A'], ['or', 'A', 'B', 'A'], 'B'
]

for i in flatten(res2):
    print(i)
