# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-13 14:05:41
FilePath     : /xjLib/xt_Time.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import datetime
import time
import traceback
from functools import wraps

nowpro = lambda: time.process_time()
nowsec = lambda: time.time()
now = lambda: datetime.datetime.now()


def fn_timer(func):
    '''装饰器:测量函数执行时长'''

    @wraps(func)
    def func_timer(*args, **kwargs):
        start_time = nowsec()
        result = func(*args, **kwargs)
        se = nowsec() - start_time
        print(f"{stack[0][0]} ,line:<{stack[0][1]}>; func:<{func.__name__}> run time:{se: .2f} seconds")
        return result

    stack = traceback.extract_stack()
    return func_timer


timeit = timer = fn_timer


def get_time():
    return now().strftime('%Y-%m-%d %H:%M:%S.%f')


def get_lite_time():
    return now().strftime('%H:%M:%S.%f')


def get_sql_time():
    # return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f'{now():%F %X}'
    # #'the time is 2020-06-15 13:28:27'


def get_10_timestamp(timestr=None):
    '''获取当前时间的时间戳-10位'''
    if timestr is None:
        timestr = time.time()
        return int(round(timestr))
    else:
        timearray = time.strptime(timestr, '%Y-%m-%d %H:%M:%S')
        return int(time.mktime(timearray))


def get_13_timestamp(timestr=None):
    '''获取当前时间的时间戳-13位'''
    return get_10_timestamp(timestr) * 1000


if __name__ == '__main__':
    print(get_time())
    print(get_lite_time())
    print(get_sql_time())
    print(get_10_timestamp())
    print(get_13_timestamp())
    print(get_10_timestamp('2020-06-15 13:28:27'))
    print(get_13_timestamp('2020-06-15 13:28:27'))
