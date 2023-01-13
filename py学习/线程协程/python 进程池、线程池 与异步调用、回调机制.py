# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-13 16:45:21
FilePath     : /py学习/线程协程/python 进程池、线程池 与异步调用、回调机制.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import os
import random
import time
from concurrent.futures import ProcessPoolExecutor as ppool  # 进程池模块
from concurrent.futures import ThreadPoolExecutor as tpool  # 线程池模块


def 子程序(name):
    time.sleep(random.randint(1, 5))
    # print(f'name: {name}  pis:{os.getpid()}  run', flush=True)
    return f'子程序返回值 : {name}'


def pro():
    pool = ppool(4)
    li = [pool.submit(子程序, f'进程{i}') for i in range(10)]
    pool.shutdown(wait=True)  # 关闭进程池，等待进程池全部运行完毕
    print('进程池主进程，开始输出结果：')
    for li1 in li:
        print(li1.result())
    print('进程池主进程')


def 回调函数(res):
    res1 = res.result()
    # print(f'回调函数返回值 is {res1}')
    return res


def thr():
    pool = tpool(4)
    li = [pool.submit(子程序, f'线程{i}').add_done_callback(回调函数) for i in range(10)]
    pool.shutdown(wait=True)  # 关闭线程池，等待线程池全部运行完毕
    print('回调主线程')


if __name__ == '__main__':
    pro()  # 进程池方式
    # thr()  # 回调方式
'''
---------------------
作者：番茄西瓜汤
来源：CSDN
原文：https://blog.csdn.net/weixin_42329277/article/details/80741589
版权声明：本文为博主原创文章，转载请附上博文链接！
'''
