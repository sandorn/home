# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-20 15:34:54
#FilePath     : /py学习/用装饰器写一个可以用队列和多线程执行的方法.py
#LastEditTime : 2020-06-20 15:36:45
#Github       : https://github.com/sandorn/home
#==============================================================
python 多线程装饰器 用装饰器写一个可以用队列和多线程执行的方法，_ajiong314-CSDN博客_python 线程并发装饰器
https://blog.csdn.net/weixin_41896508/article/details/81276292
'''

import threading
import queue
import time


def create_threading(num, func, data):
    for i in range(num):
        t = threading.Thread(target=func, args=(data, ))
        t.start()


def q_get_do(num, func):
    while True:
        if q.qsize() > 0:
            get_data = q.get()
            data = create_threading(num=num, func=func, data=get_data)
            return data
        else:
            time.sleep(1)


def q_put(data):
    q.put(data)


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
    for i in range(10):
        import time
        print(num)
        time.sleep(1)
        print(i)


q = queue.Queue(maxsize=10)

for i in range(10):
    q.put(1)
func(2)
