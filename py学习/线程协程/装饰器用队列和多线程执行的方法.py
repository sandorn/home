# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-01 21:41:38
FilePath     : /py学习/线程协程/装饰器用队列和多线程执行的方法.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import queue
import threading
import time

from xt_Thread import print_lock


def create_threading(func, *data):
    t = threading.Thread(target=func, args=data)
    t.start()


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
            print_lock("a")
            del_data = q_get_do(func=func)
            # ret = func(*args,**kwargs)
            print_lock("b")
            return del_data

        return blu_func

    return de_func


@set_func()
def func(num):
    print_lock('func:', num)


q = queue.Queue(maxsize=10)

for i in range(6):
    q.put(i)
    func(i * i)
