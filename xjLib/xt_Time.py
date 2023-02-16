# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-02-15 21:02:59
FilePath     : /CODE/xjLib/xt_Time.py
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
        _st = traceback.extract_stack()
        _s_time = nowsec()
        _s_pro = nowpro()

        result = func(*args, **kwargs)

        print(f"{_st[0][0]}|{_st[0][1]}|{func.__name__}|time:{nowsec() - _s_time: .2f} sec|processtime:{nowpro() - _s_pro: .2f} sec")
        return result

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
