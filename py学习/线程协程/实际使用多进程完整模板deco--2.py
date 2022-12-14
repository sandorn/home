# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:55
LastEditTime : 2022-12-13 15:20:07
FilePath     : /线程协程/实际使用多进程完整模板deco--2.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import os
import time

from deco import concurrent, synchronized


@concurrent  # (processes=24)
def test_concurrent(input_):
    print(input_, os.getpid())
    time.sleep(0.1)
    return os.getpid()


@synchronized
def test_synchronized():
    result = {}
    for i in range(100):
        result[i] = test_concurrent('{} pid'.format(i))
    return result


if __name__ == '__main__':
    print(test_synchronized())
