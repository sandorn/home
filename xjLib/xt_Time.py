# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-05 10:04:55
#FilePath     : /xjLib/xt_Time.py
#LastEditTime : 2020-06-25 13:45:24
#Github       : https://github.com/sandorn/home
#==============================================================
'''
import datetime
import time
from functools import wraps
import traceback


def fn_timer(function):
    '''定义一个装饰器来测量函数的执行时间'''
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t = time.time() - t0
        print(
            f"{stack[0][0]} ,line:<{stack[0][1]}>; function:<{function.__name__}> total run:{t: .2f} seconds"
        )
        return result

    stack = traceback.extract_stack()
    return function_timer


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
