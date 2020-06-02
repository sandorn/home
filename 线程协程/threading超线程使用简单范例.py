# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-26 14:04:20
@LastEditors: Even.Sand
@LastEditTime: 2020-03-26 14:07:30
'''


import threading
import time


def context(子线程):
    print('in threadContext.')
    子线程.start()

    # 将阻塞tContext直到threadJoin终止。
    子线程.join()

    # tJoin终止后继续执行。
    print('out threadContext.')


def 子程序():
    print('in 子程序.')
    time.sleep(1)
    print('out 子程序.')


子线程 = threading.Thread(target=子程序)
主线程 = threading.Thread(target=context, args=(子线程,))

主线程.start()
