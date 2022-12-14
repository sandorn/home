# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:49
LastEditTime : 2022-12-14 17:55:43
FilePath     : /xjLib/xt_Time.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import datetime
import time
import traceback
from functools import wraps


def fn_timer(function):
    '''定义一个装饰器来测量函数的执行时间'''

    @wraps(function)
    def func_timer(*args, **kwargs):
        start_time = time.perf_counter()
        result = function(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"{stack[0][0]} ,line:<{stack[0][1]}>; function:<{function.__name__}> total run:{end_time-start_time: .2f} seconds")
        return result

    stack = traceback.extract_stack()
    return func_timer


def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')


def get_lite_time():
    return datetime.datetime.now().strftime('%H:%M:%S.%f')


def get_sql_time():
    # return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f'{datetime.datetime.now():%F %X}'
    # #'the time is 2020-06-15 13:28:27'


def get_10_timestamp(timestr=None):
    '''获取当前时间的时间戳（10位）'''
    if timestr is None:
        timestr = time.time()
        return int(round(timestr))
    else:
        timearray = time.strptime(timestr, '%Y-%m-%d %H:%M:%S')
        return int(time.mktime(timearray))


def get_13_timestamp(timestr=None):
    '''获取当前时间的时间戳（13位）'''
    return get_10_timestamp(timestr) * 1000


if __name__ == '__main__':
    print(get_time())
    print(get_lite_time())
    print(get_sql_time())
    print(get_10_timestamp())
    print(get_13_timestamp())
    print(get_10_timestamp('2020-06-15 13:28:27'))
    print(get_13_timestamp('2020-06-15 13:28:27'))

    print('我是time()方法：{}'.format(time.time()))
    print('我是perf_counter()方法：{}'.format(time.perf_counter()))
    print('我是process_time()方法：{}'.format(time.process_time()))
    t0 = time.time()
    c0 = time.perf_counter()
    p0 = time.process_time()
    r = 0
    for i in range(10000000):
        r += i
    time.sleep(2)
    print(r)
    t1 = time.time()
    c1 = time.perf_counter()
    p1 = time.process_time()
    spend1 = t1 - t0
    spend2 = c1 - c0
    spend3 = p1 - p0
    print("time()方法用时：{}s".format(spend1))
    print("perf_counter()用时：{}s".format(spend2))
    print("process_time()用时：{}s".format(spend3))
    print("测试完毕")
