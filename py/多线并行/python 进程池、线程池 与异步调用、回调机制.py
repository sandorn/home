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
@LastEditors: Even.Sand
@LastEditTime: 2019-05-16 00:18:12
'''
from concurrent.futures import ProcessPoolExecutor as ppool  # 进程池模块
from concurrent.futures import ThreadPoolExecutor as tpool  # 线程池模块
import os, time, random


def talk(name):
    time.sleep(random.randint(1, 5))
    print('name: %s  pis:%s  run' % (name, os.getpid()), flush=True)


def calb(res):
    res1 = res.result()  # !取到res结果 【回调函数】带参数需要这样
    print('res1 is %s' % res1)


def pro():
    pool = ppool(4)
    for i in range(10):
        pool.submit(talk, '进程%s' % i)  # 异步调用，不需要等待

    # 作用1：关闭进程池入口不能再提交了
    # 作用2：相当于jion 等待进程池全部运行完毕
    pool.shutdown(wait=True)
    print('主进程')


def thr():
    pool = tpool(4)
    for i in range(10):
        #pool.submit(talk, '线程%s' % i).result()  # 同步调用，result()，相当于join,get()
        #pool.submit(talk, '线程%s' % i)  # 异步调用，不需要等待
        pool.submit(talk, '线程%s' % i).add_done_callback(calb)
        # 【回调函数】执行完线程后，跟一个函数

    # 作用1：关闭进程池入口不能再提交了
    # 作用2：相当于jion 等待进程池全部运行完毕
    pool.shutdown(wait=True)
    print('主线程')


if __name__ == '__main__':
    pro()
    thr()
'''
---------------------
作者：番茄西瓜汤
来源：CSDN
原文：https://blog.csdn.net/weixin_42329277/article/details/80741589
版权声明：本文为博主原创文章，转载请附上博文链接！
'''
