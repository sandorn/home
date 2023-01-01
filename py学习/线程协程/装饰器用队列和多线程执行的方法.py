# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-01 16:31:31
FilePath     : /py学习/线程协程/装饰器用队列和多线程执行的方法.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import queue
import threading
import time


def create_threading(func, *data):
    t = threading.Thread(target=func, args=data)
    t.start()


def q_get_do(num, func):
    while True:
        if q.qsize() > 0:
            get_data = q.get()
            return create_threading(func, get_data)
        else:
            time.sleep(1)


def set_func(thread_num):

    def de_func(func):

        def blu_func(*args, **kwargs):
            print("a")
            del_data = q_get_do(num=thread_num, func=func)
            q.put(del_data)
            # ret = func(*args,**kwargs)
            print("b")
            return del_data

        return blu_func

    return de_func


@set_func(thread_num=2)
def func(num):
    print('func:', num)


q = queue.Queue(maxsize=10)

for _ in range(10):
    q.put(1)
func(2)
