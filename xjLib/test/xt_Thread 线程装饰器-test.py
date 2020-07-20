# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-19 13:52:24
#FilePath     : /xjLib/test/xt_Thread 线程装饰器-test.py
#LastEditTime : 2020-07-17 11:27:28
#Github       : https://github.com/sandorn/home
#==============================================================
'''
import time
from xt_Thread import thread_wrap_class, thread_wraps_class
from xt_Thread import thread_safe, thread_wraps, thread_wrap
from threading import currentThread

# @thread_async
# @thread_wraps()
g_a = 100


def click(callback, *args, **kwargs):
    # print('in main func with <', callback.__name__, '>', *args, **kwargs)
    return callback(*args, **kwargs)


@thread_wrap_class
def event(s):
    time.sleep(s)
    global g_a
    g_a += s
    print(f'{currentThread()} < event > finished! {s} {g_a}')
    return 'event Result ：' + str(s) + '|' + str(g_a)


@thread_wrap_class
def another_event(s):
    time.sleep(s)
    global g_a
    g_a += s
    print(f'{currentThread()} < another event > finished! {s} {g_a}')
    return 'another event Result ：' + str(s) + '|' + str(g_a)


event(4)
a = event(5, daemon=True)
print('a.name:', a.name, a._name, a)
print('a:', a.getResult())
click(event, 3)
click(event, 6)
print('实例获取 event all result:', a.getAllResult())

b = another_event(7)
c = another_event(5)
print('b.name:', b.name, b._name, b)
print('b:', b.getResult())
click(another_event, 6)
click(another_event, 4)
print('c:', c.getResult())
print('实例获取 another_event all result:', b.getAllResult())
