# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-16 00:02:39
@LastEditors  : Even.Sand
@LastEditTime : 2020-02-09 16:15:19
'''
from concurrent.futures import ProcessPoolExecutor as ppool  # 进程池模块
from concurrent.futures import ThreadPoolExecutor as tpool  # 线程池模块
import os
import time
import random


def 被调用子程序(name):
    time.sleep(random.randint(1, 5))
    print('name: %s  pis:%s  run' % (name, os.getpid()), flush=True)


def pro():
    pool = ppool(4)
    for i in range(10):
        pool.submit(被调用子程序, '进程%s' % i)  # 异步调用，不需要等待
    # 作用1：关闭进程池入口不能再提交了
    # 作用2：相当于jion 等待进程池全部运行完毕
    pool.shutdown(wait=True)
    print('进程池主进程')


def 回调子函数(res):
    res1 = res.result()  # !取到res结果 【回调函数】带参数需要这样
    print('回调函数返回值 is %s' % res1)


def thr():
    pool = tpool(4)
    for i in range(10):
        # pool.submit(被调用子程序, '线程%s' % i).result()  # 同步调用，result()，相当于join,get()
        pool.submit(被调用子程序, '线程%s' % i).add_done_callback(回调子函数)
        # 【回调函数】执行完线程后，跟一个函数

    # 作用1：关闭进程池入口不能再提交了
    # 作用2：相当于jion 等待进程池全部运行完毕
    pool.shutdown(wait=True)
    print('回调主线程')


if __name__ == '__main__':
    pro()  # 进程池方式
    thr()  # 回调方式
'''
---------------------
作者：番茄西瓜汤
来源：CSDN
原文：https://blog.csdn.net/weixin_42329277/article/details/80741589
版权声明：本文为博主原创文章，转载请附上博文链接！
'''
