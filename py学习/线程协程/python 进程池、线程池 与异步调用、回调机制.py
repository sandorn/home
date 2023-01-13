# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-13 21:35:17
FilePath     : /CODE/py学习/线程协程/python 进程池、线程池 与异步调用、回调机制.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import os
import random
import time
from concurrent.futures import ProcessPoolExecutor as ppool  # 进程池模块
from concurrent.futures import ThreadPoolExecutor as tpool  # 线程池模块

from xt_Thread import print_lock


def 子程序(name):
    time.sleep(random.randint(1, 5))
    # print_lock(f'name: {name}  pis:{os.getpid()}  run', flush=True)
    return f'子程序返回值 : {name}'


def pro():
    pool = ppool(4)
    li = [pool.submit(子程序, f'进程{i}') for i in range(10)]
    pool.shutdown(wait=True)  # 关闭进程池，等待进程池全部运行完毕
    print_lock('进程池主进程，开始输出结果：')
    for li1 in li:
        print_lock(li1.result())
    print_lock('进程池主进程')


def 回调函数(res):
    res1 = res.result()
    print_lock(f'回调函数返回值 is {res1}')
    return res


def thr():
    pool = tpool(4)
    li = [pool.submit(子程序, f'线程{i}').add_done_callback(回调函数) for i in range(10)]
    pool.shutdown(wait=True)  # 关闭线程池，等待线程池全部运行完毕
    # print(li[0].result())
    print_lock('回调主线程')


if __name__ == '__main__':
    # pro()  # 进程池方式
    thr()  # 回调方式
'''
---------------------
作者：番茄西瓜汤
来源：CSDN
原文：https://blog.csdn.net/weixin_42329277/article/details/80741589
版权声明：本文为博主原创文章，转载请附上博文链接！
'''
