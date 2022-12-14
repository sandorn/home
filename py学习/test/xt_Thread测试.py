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
LastEditors  : Please set LastEditors
LastEditTime : 2021-01-04 18:13:32
根据网络资料，写的threadpool
'''

import os

from xt_File import savefile
from xt_Ls_Bqg import (
    ahttp_get_contents,
    get_contents,
    get_download_url,
    map_get_contents,
    map_get_contents_ahttp,
)
from xt_Thread import (
    CustomThread,
    CustomThread_Queue,
    P_Map,
    P_Pool,
    P_Sub,
    SigThread,
    SigThreadQ,
    SingletonThread,
    T_Map,
    T_Pool,
    T_Sub,
    WorkManager,
)
from xt_Time import fn_timer

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
    _ = [SigThreadQ([get_contents, (index + 1, url)]) for index, url in enumerate(urls)]
    # print(id(thr[0]), id(thr[1]), id(thr[2]))get_contents_ahttp
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
def tm(bookname, urls):
    mypool = T_Map(map_get_contents, [[index + 1, url] for index, url in enumerate(urls)])
    texts = mypool.wait_completed()
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'TMap.txt', texts, br='\n')


@fn_timer
def pm(bookname, urls):
    mypool = P_Map(map_get_contents_ahttp, [[index + 1, url] for index, url in enumerate(urls)])
    texts = mypool.wait_completed()
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'PMap.txt', texts, br='\n')


@fn_timer
def ts(bookname, urls):

    def _c_func(task):
        print(1111, task.result())

    mypool = T_Sub(
        get_contents,
        [[index + 1, url] for index, url in enumerate(urls)],
        #  callback=_c_func
    )
    texts = mypool.wait_completed()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'T_Sub.txt', texts, br='\n')


@fn_timer
def ps(bookname, urls):
    mypool = P_Sub(ahttp_get_contents, [[index + 1, url] for index, url in enumerate(urls)])
    texts = mypool.wait_completed()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'P_Sub.txt', texts, br='\n')


@fn_timer
def tp(bookname, urls):
    mypool = T_Pool()
    # mypool.add_sub(get_contents, [[index + 1, url] for index, url in enumerate(urls)])
    mypool.add_map(map_get_contents, [[index + 1, url] for index, url in enumerate(urls)])
    texts = mypool.wait_map()
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'TPool-m.txt', texts, br='\n')

    mypool.add_sub(get_contents, [[index + 1, url] for index, url in enumerate(urls)])
    texts = mypool.wait_sub()
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'TPool-s.txt', texts, br='\n')


@fn_timer
def pp(bookname, urls):
    # #无法获取数据
    mypool = P_Pool()
    mypool.add_map(map_get_contents, [[index + 1, url] for index, url in enumerate(urls)])
    texts = mypool.wait_map()
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'TPool-m.txt', texts, br='\n')

    mypool.add_sub(ahttp_get_contents, [[index + 1, url] for index, url in enumerate(urls)])
    texts = mypool.wait_sub()
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'TPool-s.txt', texts, br='\n')


if __name__ == "__main__":

    bookname, urls, _ = get_download_url('http://www.biqukan.com/2_2760/')
    # #38_38836  #2_2714  #2_2760  #76_76519

    # st(bookname, urls)
    sq(bookname, urls)
    # stm(bookname, urls)
    # ct(bookname, urls)
    # cq(bookname, urls)
    # wm(bookname, urls)
    # tm(bookname, urls)
    # pm(bookname, urls)
    # ts(bookname, urls)
    # ps(bookname, urls)
    # tp(bookname, urls)
    # pp(bookname, urls)

    # for f in ['st', 'sq', 'stm', 'ct', 'cq', 'wm']:
    #     eval(f)(bookname, urls)
    # locals()[func](bookname, urls)
    # globals()[func](bookname, urls)
'''
    [2_2760] size: 10.07 MB。
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

    [2_2714 ] size: 47.54 MB。
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
