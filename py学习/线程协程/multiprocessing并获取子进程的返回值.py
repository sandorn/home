# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-02 13:48:35
LastEditTime : 2023-01-13 21:40:31
FilePath     : /CODE/py学习/线程协程/multiprocessing并获取子进程的返回值.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import multiprocessing
import random
import time


def worker(name, que):
    t = 0
    for i in range(10):
        print(f"{name} {str(i)}")
        x = random.randint(1, 3)
        t += x
        time.sleep(x * 0.1)
    que.put(t)


if __name__ == '__main__':

    que = multiprocessing.Queue()
    jobs = []
    for i in range(10):
        p = multiprocessing.Process(target=worker, args=(str(i), que))
        jobs.append(p)
        p.start()

    for p in jobs:
        p.join()

    results = [que.get() for _ in jobs]
    print(results)
