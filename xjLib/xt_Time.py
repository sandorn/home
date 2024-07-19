# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-07-18 15:12:35
FilePath     : /CODE/xjLib/xt_time.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import datetime
import time
from time import perf_counter, process_time

import wrapt


def now():
    return datetime.datetime.now()


@wrapt.decorator
def fn_timer(func, instance, args, kwargs):
    _s_time = perf_counter()
    _s_pro = process_time()

    result = func(*args, **kwargs)

    perf_time = perf_counter() - _s_time
    pro_time = process_time() - _s_pro

    print(f"Function:<{func.__name__}>|perf_counter: {perf_time:.2f}s|process_time: {pro_time:.2f}s")

    return result


timeit = timer = fn_timer


def get_time():
    return now().strftime("%Y-%m-%d %H:%M:%S.%f")


def get_lite_time():
    return now().strftime("%H:%M:%S.%f")


def get_sql_time():
    # return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"{now():%F %X}"
    # #'the time is 2020-06-15 13:28:27'


def get_10_timestamp(timestr=None):
    """获取当前时间的时间戳-10位"""
    if timestr is None:
        timestr = time.time()
        return int(round(timestr))
    else:
        timearray = time.strptime(timestr, "%Y-%m-%d %H:%M:%S")
        return int(time.mktime(timearray))


def get_13_timestamp(timestr=None):
    """获取当前时间的时间戳-13位"""
    return get_10_timestamp(timestr) * 1000


if __name__ == "__main__":
    print(get_time())
    print(get_lite_time())
    print(get_sql_time())
    print(get_10_timestamp())
    print(get_13_timestamp())
    print(get_10_timestamp("2020-06-15 13:28:27"))
    print(get_13_timestamp("2020-06-15 13:28:27"))
    print(get_13_timestamp("2020-06-15 13:28:27"))
