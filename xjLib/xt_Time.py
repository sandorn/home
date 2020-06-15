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
#LastEditTime : 2020-06-15 13:30:06
#Github       : https://github.com/sandorn/home
#==============================================================
'''
import datetime
import time
from functools import wraps


def fn_timer(function):
    '''定义一个装饰器来测量函数的执行时间'''
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print("Function : <%s> Total running time: %.2f seconds" %
              (function.__name__, t1 - t0))
        return result

    return function_timer


def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')


def get_lite_time():
    return datetime.datetime.now().strftime('%H:%M:%S.%f')


def get_sql_time():
    # return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f'{datetime.now():%F %X}'
    # #'the time is 2020-06-15 13:28:27'


def get_10_timestamp(timestr=None):
    '''获取当前时间的时间戳（10位）'''
    if timestr is None:
        timestr = time.time()
        return int(round(timestr))
    else:
        timearray = time.strptime(timestr, '%Y-%m-%d %H:%M:%S')
        return int(time.mktime(timearray))


@fn_timer
def get_13_timestamp(timestr=None):
    '''获取当前时间的时间戳（13位）'''
    return get_10_timestamp(timestr) * 1000


if __name__ == "__main__":
    print(get_13_timestamp())
    print(get_10_timestamp('2020-06-05 11:29:01'))
    print(get_sql_time())
