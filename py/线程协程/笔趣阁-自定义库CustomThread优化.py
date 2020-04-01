# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-31 12:12:40
@LastEditors: Even.Sand
@LastEditTime: 2020-04-01 16:01:36
'''


import os


from xjLib.mystr import (fn_timer, savefile)
import threading
from xjLib.CustomThread import (SingletonThread, SingletonThread_Queue, CustomThread, Custom_Thread_Queue, WorkManager, thread_pool_maneger)
from xjLib.ls import get_download_url, get_contents
# from multiprocessing import Queue
from queue import Queue
import time
'''
import pdb
pdb.set_trace()  # 运行到这里会自动暂停
'''


@fn_timer
def st(bookname, urls):
    _ = [SingletonThread(get_contents, (index, url)) for index, url in enumerate(urls)]
    texts = SingletonThread.wait_completed()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'SingletonThread.txt', texts, br='\n')


@fn_timer
def ct(bookname, args):
    _ = [CustomThread(get_contents, [index, url])for index, url in enumerate(urls)]
    texts = CustomThread.wait_completed()
    texts.sort(key=lambda x: x[0])
    # aftertexts = [[row[i] for i in range(1, 3)] for row in texts]
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(files + '＆' + bookname + 'CustomThread.txt', texts, br='\n')


if __name__ == "__main__":
    bookname, urls = get_download_url('http://www.biqukan.com/2_2714/')  # 38_38836  #2_2714

    st(bookname, urls)
    ct(bookname, urls)

    print('#' * 33, 'threading.active_count():', threading.active_count(), threading.enumerate())
