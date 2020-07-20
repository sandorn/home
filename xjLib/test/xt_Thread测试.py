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
#LastEditTime : 2020-07-17 10:49:05
根据网络资料，写的threadpool
'''

import os

from xt_Thread import CustomThread, CustomThread_Queue, WorkManager, SingletonThread, SigThread, SigThreadQ, ThreadPoolMap, ThreadPoolSub, ProcessPoolMap, ProcessPoolSub, CustomThread_Singleton, ExThreadPool, ExProcesPool
from xt_File import savefile
from xt_Time import fn_timer
from xt_Ls_Bqg import get_download_url, get_contents, map_get_contents, map_get_contents_ahttp, get_contents_ahttp, arrangeContent
# from xt_Thread import thread_wrap_class


@fn_timer
def st(bookname, urls):
    thr = [SingletonThread(get_contents, index + 1, url) for index, url in enumerate(urls)]
    print(id(thr[0]), id(thr[1]), id(thr[2]))
    texts = SingletonThread.getAllResult()  # #getAllResult()  # #wait_completed()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'SingletonThread.txt', texts, br='\n')


@fn_timer
def sq(bookname, urls):
    thr = [SigThreadQ([get_contents, index + 1, url]) for index, url in enumerate(urls)]
    # print(id(thr[0]), id(thr[1]), id(thr[2]))
    texts = SigThreadQ.wait_completed()  # #getAllResult()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'SigThreadQ.txt', texts, br='\n')


@fn_timer
def stm(bookname, urls):
    thr = [SigThread(get_contents, index + 1, url) for index, url in enumerate(urls)]
    print(id(thr[0]), id(thr[1]), id(thr[2]))
    texts = SigThread.wait_completed()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'SingletonThread_make.txt', texts, br='\n')


@fn_timer
def ct(bookname, args):
    _ = [CustomThread(get_contents, index + 1, url) for index, url in enumerate(urls)]
    texts = CustomThread.wait_completed()
    texts.sort(key=lambda x: x[0])
    # texts = [[row[i] for i in range(1, 3)] for row in texts]
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(files + '＆' + bookname + 'CustomThread.txt', texts, br='\n')


@fn_timer
def cq(bookname, urls):
    for index, url in enumerate(urls):
        CustomThread_Queue([get_contents, index + 1, url])
    texts = CustomThread_Queue.wait_completed()  # #getAllResult()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'CustomThread_Queue.txt', texts, br='\n')


@fn_timer
def wm(bookname, urls):
    mywork = WorkManager()
    mywork.add_work_queue([get_contents, index + 1, url] for index, url in enumerate(urls))
    texts = mywork.getAllResult()

    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'WorkManager.txt', texts, br='\n')

    mywork.add_work_queue([
        [get_contents, 9999, 'https://www.biqukan.com/26_26819/13059420.html'],
    ])
    mywork.add_work_queue([
        [get_contents, 8888, 'https://www.biqukan.com/26_26819/2199.html'],
    ])
    texts = mywork.wait_completed()

    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + '司机' + 'WorkManager.txt', texts, br='\n')


@fn_timer
def pm(bookname, urls):
    mypool = ThreadPoolMap(map_get_contents, [[index + 1, url] for index, url in enumerate(urls)])
    texts = mypool.wait_completed()
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'ThreadPoolMap.txt', texts, br='\n')

    # # ------------------------------------------------------------------------
    mypool = ExThreadPool()
    mypool.add_map(map_get_contents, [[index + 1, url] for index, url in enumerate(urls)])
    texts = mypool.getAllResult()
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'ExThreadPool.map.txt', texts, br='\n')

    # # ------------------------------------------------------------------------
    mypool.add_sub(
        get_contents,
        [[index + 1, url] for index, url in enumerate(urls)],
        #  callback=_c_func
    )
    texts = mypool.wait_completed()
    texts.sort(key=lambda x: x[0])  # @map默认有序
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'ExThreadPool.submit.txt', texts, br='\n')


@fn_timer
def ps(bookname, urls):
    def _c_func(task):
        print(1111, task.result())

    mypool = ThreadPoolSub(
        get_contents,
        [[index + 1, url] for index, url in enumerate(urls)],
        #  callback=_c_func
    )
    texts = mypool.wait_completed()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'ThreadPoolSub.txt', texts, br='\n')


@fn_timer
def cpm(bookname, urls):
    mypool = ExProcesPool()
    mypool.add_map(map_get_contents_ahttp, [[index + 1, url] for index, url in enumerate(urls)])
    texts = mypool.getAllResult()
    # mypool = ProcessPoolMap(map_get_contents_ahttp, [[index + 1, url] for index, url in enumerate(urls)])
    # texts = mypool.wait_completed()
    # texts.sort(key=lambda x: x[0])  # @map默认有序
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'ProcessPoolMap.txt', texts, br='\n')


@fn_timer
def cps(bookname, urls):
    mypool = ProcessPoolSub(get_contents_ahttp, [[index + 1, url] for index, url in enumerate(urls)])
    texts = mypool.wait_completed()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'ProcessPoolSub.txt', texts, br='\n')


if __name__ == "__main__":

    bookname, urls = get_download_url('http://www.biqukan.com/38_38836/')
    # #38_38836  #2_2714  #2_2760  #76_76519

    # st(bookname, urls)
    # sq(bookname, urls)
    stm(bookname, urls)
    # ct(bookname, urls)
    # cq(bookname, urls)
    # wm(bookname, urls)
    # pm(bookname, urls)
    # ps(bookname, urls)
    # cpm(bookname, urls)
    # cps(bookname, urls)

    # for f in ['st', 'sq', 'stm', 'ct', 'cq', 'wm', 'pm', 'ps', 'cpm', 'cps']:
    #     eval(f)(bookname, urls)
    # locals()[func](bookname, urls)
    # globals()[func](bookname, urls)
'''
    [笔趣阁-庆余年 2_2760] size: 10.07 MB。
    <st> total run: 10.89 seconds
    <sq> total run: 13.12 seconds
    <stm> total run: 11.72 seconds
    <ct> total run: 12.78 seconds
    <cq> total run: 12.42 seconds
    <wm> total run: 12.69 seconds
    <pm> total run: 11.18 seconds
    <ps> total run: 11.02 seconds
    <cpm> total run: 34.88 seconds
    <cps> total run: 41.62 seconds

    [笔趣阁-庆余年 2_2714 ] size: 47.54 MB。
    <st> total run: 74.09 seconds
    <sq> total run: 81.81 seconds
    <stm> total run: 98.75 seconds
    <ct> total run: 89.89 seconds
    <cq> total run: 84.27 seconds
    <wm> total run: 89.94 seconds
    <pm> total run: 78.95 seconds
    <ps> total run: 78.91 seconds
    <cpm> total run: 170.07 seconds
    <cps> total run: 185.84 seconds

'''
