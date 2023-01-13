# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2022-12-30 11:19:53
FilePath     : /py学习/线程协程/实际使用多进程完整模板deco--2.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import os
import time

from deco import concurrent, synchronized

temp_dict = {i: f'{i}pid' for i in range(10)}


@concurrent
def test_concurrent(input_):
    print(input_, os.getpid())
    time.sleep(5)
    return input_, os.getpid()


@synchronized
def test_synchronized():
    for k, v in temp_dict.items():
        temp_dict[k] = test_concurrent(v)
    return temp_dict


if __name__ == '__main__':
    print(test_synchronized())
