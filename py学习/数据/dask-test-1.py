# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-24 00:37:07
LastEditTime : 2023-01-04 15:43:39
FilePath     : /py学习/数据/dask-test-1.py
Github       : https://github.com/sandorn/home
==============================================================
'''


def inc(x):
    return x + 1


def double(x):
    return x * 2


def add(x, y):
    return x + y


data = [1, 2, 3, 4, 5]

import dask

output = []
for x in data:
    a = dask.delayed(inc)(x)
    b = dask.delayed(double)(x)
    c = dask.delayed(add)(a, b)
    output.append(c)

total = dask.delayed(sum)(output)
print(total.compute())
print(total.visualize())
