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
#LastEditTime : 2020-06-22 11:45:37
#Github       : https://github.com/sandorn/home
#==============================================================
'''
import time
from xt_Thread import thread_wrap_class, thread_wraps_class, thread_safe, Lock, thread_wraps, thread_wrap, print
from threading import currentThread

from pysnooper import snoop
from xt_Log import log
log = log()
snooper = snoop(log.filename)
# print = log.debug
# import dis
# dis.dis(event) # 反汇编
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


@thread_wraps_class()
def another_event(s):
    time.sleep(s)
    global g_a
    g_a += s
    print(f'{currentThread()} < another event > finished! {s} {g_a}')
    return 'another event Result ：' + str(s) + '|' + str(g_a)


# a = event(5)
# click(event, 2)
# print(a.getResult())
# print(a.getAllResult())

b = another_event(4)
c = another_event(5)
print('b:', b.getResult())
click(another_event, 6)
click(another_event, 4)
print('all:', b.getResult())
