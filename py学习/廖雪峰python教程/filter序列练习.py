# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-02-07 09:13:56
LastEditTime : 2023-02-07 10:16:05
FilePath     : /CODE/py学习/廖雪峰python教程/迭代习题.py
Github       : https://github.com/sandorn/home
==============================================================
'''


def _odd_iter():
    n = 1
    while True:
        n = n + 2
        yield n


def _not_divisible(n):
    return lambda x: x % n > 0


def primes():
    yield 2
    it = _odd_iter()  # 初始序列
    while True:
        n = next(it)  # 返回序列的第一个数
        yield n
        it = filter(_not_divisible(n), it)  # 构造新序列


def run(n):
    # 打印 n 以内的素数:
    for x in primes():
        if x < n:
            print(x)
        else:
            break


if __name__ == '__main__':
    ...
    # run(50)
    import unittest

    class TestRun(unittest.TestCase):

        def test_run(self):
            self.assertIsNone(run(50))

    unittest.main()
