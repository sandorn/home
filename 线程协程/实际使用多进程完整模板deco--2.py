# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-20 22:30:46
#FilePath     : /线程协程/实际使用多进程完整模板deco--2.py
#LastEditTime : 2020-06-20 22:32:24
#Github       : https://github.com/sandorn/home
#==============================================================
'''
import os

import time
from deco import concurrent, synchronized

temp_dict = {}
for i in range(20):
    temp_dict[i] = '{} pid'.format(i)


@concurrent
def test_concurrent(input_):
    print(input_, os.getpid())
    time.sleep(0.5)
    return input_, os.getpid()


@synchronized
def test_synchronized():
    result = {}
    for k, v in temp_dict.items():
        result[k] = test_concurrent(v)
    return result


if __name__ == '__main__':
    print(test_synchronized())
