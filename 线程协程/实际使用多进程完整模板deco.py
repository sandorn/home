# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-20 15:39:02
#FilePath     : /线程协程/实际使用多进程完整模板deco.py
#LastEditTime : 2020-06-20 22:48:45
#Github       : https://github.com/sandorn/home
#==============================================================
带装饰器的Python中的简化多进程、多线程并发（装饰并发-Python多线程、进程神器）_陆壹佛爷Tong_T-CSDN博客_python multiprocess 装饰器装饰
https://blog.csdn.net/Tong_T/article/details/103064827?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.nonecase
'''
import deco
import time
import random
from collections import defaultdict
import os


@deco.concurrent(processes=16)
def process_lat_lon(lat, lon, data):
    """
    We add this for the concurrent function
    :param lat:
    :param lon:
    :param data:
    :return:
    """
    print(1111, 'pid:', os.getpid(), lat * 10, lon, data[lat * 10 + lon])
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
    for lat in range(10):
        for lon in range(10):
            results[lat][lon] = process_lat_lon(lat, lon, data)
    return dict(results)


if __name__ == "__main__":
    """Windows下必须在__main__命名下，所以如果调用，也都遵循这个规则吧"""
    random.seed(0)
    data = [random.random() for _ in range(200)]
    start = time.time()
    # d = process_data_set(data)
    # for k, v in d.items():
    #     print(k, v)
    # !未自动结束
    print(process_data_set(data))
    print(time.time() - start)
