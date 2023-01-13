# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-13 21:22:27
FilePath     : /CODE/py学习/线程协程/装饰器用队列和多线程执行的方法.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import queue
import threading
import time

from xt_Thread import print_lock


def create_threading(func, *data):
    threading.Thread(target=func, args=data).start()


def q_get_do(func):
    while True:
        if q.qsize() > 0:
            get_data = q.get()
            return create_threading(func, get_data)
        else:
            time.sleep(1)


def set_func():

    def de_func(func):

        def blu_func(*args, **kwargs):
            del_data = q_get_do(func=func)
            # ret = func(*args,**kwargs)
            return del_data

        return blu_func

    return de_func


@set_func()
def run_func(num):
    print_lock('func:', num)


q = queue.Queue(maxsize=10)

for i in range(1, 21):
    q.put(i * 10)  # 此为 run_func 的参数
    run_func(i * 10000)  # 此参数无效
