# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-16 21:49:56
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-06-24 17:32:17
根据网络资料，写的threadpool
'''

import os

from xt_Thread import CustomThread, CustomThread_Queue, WorkManager, thread_pool_maneger, SingletonThread, SigThread, SigThreadQ
from xt_File import savefile
from xt_Time import fn_timer
from xt_Ls_Bqg import get_download_url, get_contents


@fn_timer
def st(bookname, urls):
    thr = [
        SingletonThread(get_contents, index, url)
        for index, url in enumerate(urls)
    ]
    # print(id(thr[0]), id(thr[1]), id(thr[2]))
    # print('9999:', thr[0].__class__.__name__, SingletonThread.__name__)
    texts = SingletonThread.getAllResult(
    )  # #getAllResult()  # #wait_completed()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'SingletonThread.txt', texts, br='\n')


@fn_timer
def sq(bookname, urls):
    for index, url in enumerate(urls):
        res = SigThreadQ([get_contents, index, url])
    texts = SigThreadQ.wait_completed()  # #getAllResult()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'SigThreadQ.txt', texts, br='\n')


@fn_timer
def stm(bookname, urls):
    thr = [
        SigThread(get_contents, index, url) for index, url in enumerate(urls)
    ]
    # print(id(thr[0]), id(thr[1]), id(thr[2]))
    texts = SigThread.wait_completed()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'SigThread.txt', texts, br='\n')


@fn_timer
def ct(bookname, args):
    _ = [
        CustomThread(get_contents, index, url)
        for index, url in enumerate(urls)
    ]
    texts = CustomThread.wait_completed()
    texts.sort(key=lambda x: x[0])
    # texts = [[row[i] for i in range(1, 3)] for row in texts]
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(files + '＆' + bookname + 'CustomThread.txt', texts, br='\n')


@fn_timer
def cq(bookname, urls):
    for index, url in enumerate(urls):
        CustomThread_Queue([get_contents, index, url])
    texts = CustomThread_Queue.wait_completed()  # #getAllResult()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'CustomThread_Queue.txt', texts, br='\n')


@fn_timer
def wm(bookname, urls):
    mywork = WorkManager([[get_contents, index, url]
                          for index, url in enumerate(urls)
                          ])  # 调用函数,参数:list内tupe,线程数量
    # texts = mywork.wait_allcomplete()
    texts = mywork.queue_join()

    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'WorkManager.txt', texts, br='\n')


@fn_timer
def tp(bookname, urls, MaxSem=99):
    mywork = thread_pool_maneger([[get_contents, index, url]
                                  for index, url in enumerate(urls)],
                                 MaxSem=MaxSem)
    texts = mywork.getAllResult()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'thread_pool_maneger.txt',
             texts,
             br='\n')


if __name__ == "__main__":

    bookname, urls = get_download_url('http://www.biqukan.com/38_38836/')
    # #38_38836  #2_2714  #2_2760

    for index in range(3):
        st(bookname, urls)
        print(1111, index)
    # sq(bookname, urls)
    # stm(bookname, urls)
    # ct(bookname, urls)
    # cq(bookname, urls)
    # wm(bookname, urls)
    # tp(bookname, urls)

    # for func in ['st', 'sq','stm','ct', 'cq',''wm', 'tp']:
    #     eval(func)(bookname, urls)
    # locals()[func](bookname, urls)
    # globals()[func](bookname, urls)
'''
    # 默认线程数量
    [笔趣阁-自定义库CustomThread例子＆武炼巅峰SingletonThread.txt]保存完成	size：46.47 MB
    Total time running with [SingletonThread]: 68.46 seconds
    [笔趣阁-自定义库CustomThread例子＆武炼巅峰SingletonThread_Queue.txt]保存完成	size：46.47 MB
    Total time running with [SingletonThread_Queue]: 75.63 seconds
    [笔趣阁-自定义库CustomThread例子＆武炼巅峰CustomThread.txt]保存完成	size：46.47 MB
    Total time running with [CustomThread]: 91.00 seconds
    [笔趣阁-自定义库CustomThread例子＆武炼巅峰Custom_Thread_Queue.txt]保存完成	size：46.47 MB
    Total time running with [Custom_Thread_Queue]: 67.19 seconds
    [笔趣阁-自定义库CustomThread例子＆武炼巅峰WorkManager.txt]保存完成	size：46.47 MB
    Total time running with [WorkManager]: 66.73 seconds
    [笔趣阁-自定义库CustomThread例子＆武炼巅峰thread_pool_maneger.txt]保存完成	size：46.47 MB
    Total time running with [thread_pool_maneger]: 130.96 seconds
'''
