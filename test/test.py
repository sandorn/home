# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-09-23 17:17:17
LastEditTime : 2024-09-29 11:21:46
FilePath     : /CODE/test/test.py
Github       : https://github.com/sandorn/home
==============================================================
"""


def factorial(n, acc=1):
    """使用尾递归优化计算阶乘"""
    while True:
        if n == 0:
            return acc
        n, acc = n - 1, acc * n


# print(factorial(6))


def add(x):
    """柯里化"""
    return lambda y: x + y


# add_five = add(5)
# result = add_five(10)
# print(result)


def add_one(x):
    return x + 1


def square(x):
    return x**2


print(square(add_one(3)))
