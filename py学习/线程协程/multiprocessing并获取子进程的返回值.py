# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2023-01-02 13:48:35
LastEditTime : 2023-01-02 13:48:36
FilePath     : /py学习/线程协程/multiprocessing并获取子进程的返回值.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import multiprocessing
import random
import time


def worker(name, q):
    t = 0
    for i in range(10):
        print(f"{name} {str(i)}")
        x = random.randint(1, 3)
        t += x
        time.sleep(x * 0.1)
    q.put(t)


if __name__ == '__main__':

    q = multiprocessing.Queue()
    jobs = []
    for i in range(10):
        p = multiprocessing.Process(target=worker, args=(str(i), q))
        jobs.append(p)
        p.start()

    for p in jobs:
        p.join()

    results = [q.get() for _ in jobs]
    print(results)
