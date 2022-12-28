# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:55
LastEditTime : 2022-12-13 15:25:23
FilePath     : /线程协程/实际使用多线程完整模板deco.py
Github       : https://github.com/sandorn/home
==============================================================
带装饰器的Python中的简化多进程、多线程并发（装饰并发-Python多线程、进程神器）_陆壹佛爷Tong_T-CSDN博客_python multiprocess 装饰器装饰
https://blog.csdn.net/Tong_T/article/details/103064827?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.nonecase
'''

import itertools
import os
import random
import time
from collections import defaultdict
from threading import Lock

import deco

mylock = Lock()


@deco.concurrent.threaded(processes=16)
def process_lat_lon(lat, lon, data):
    """
    We add this for the concurrent function
    :param lat:
    :param lon:
    :param data:
    :return:
    """
    with mylock:
        print(lat * 10, lon, data[lat * 10 + lon], 'PID:', os.getpid())
    time.sleep(0.1)
    return data[lat * 10 + lon]


@deco.synchronized
def process_data_set(data):
    """
    And we add this for the function which calls the concurrent function
    :param data:
    :return:
    """
    results = defaultdict(dict)
    for lat, lon in itertools.product(range(10), range(10)):
        results[lat][lon] = process_lat_lon(lat, lon, data)
    return dict(results)


if __name__ == "__main__":
    random.seed(0)
    data = [random.randint(1, 999) for _ in range(200)]
    d = process_data_set(data)
    for k, v in d.items():
        print(k, v)
