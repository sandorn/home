# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:57
LastEditTime : 2023-01-08 01:31:12
FilePath     : /项目包/线程小成果/自定义库futures.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import os

from xt_Ahttp import ahttpGetAll
from xt_File import savefile
from xt_Ls_Bqg import get_biqugse_download_url, get_contents, 结果处理
from xt_Thread import ProcessPool, ThreadPool
from xt_Time import fn_timer


@fn_timer
def ahttp_All(url):
    bookname, urls, _ = get_biqugse_download_url(url)
    resps = ahttpGetAll(urls)
    text_list = 结果处理(resps)
    text_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.basename(__file__).split(".")[0]
    savefile(f'{files}&{bookname}ahttp_All.txt', text_list, br='\n')


def thrPool_ahttp(urls):  # # 无效
    mypool = ThreadPool()
    mypool.add_map(ahttp_All, urls)
    mypool.wait_completed()


@fn_timer
def multpool_ahttp(urls):
    mypool = ProcessPool()
    mypool.add_map(ahttp_All, urls)
    mypool.wait_completed()


def thr_sub(url):
    mypool = ThreadPool()
    bookname, urls, _ = get_biqugse_download_url(url)
    args = [[i, u] for i, u in enumerate(urls)]
    mypool.add_sub(get_contents, *args)
    text_list = mypool.wait_completed()
    # text_list = 结果处理(resps)
    text_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(f'{files}&{bookname}&Thrtpool.txt', text_list, br='\n')


@fn_timer
def multpool_thrsub(urls):
    mypool = ProcessPool()
    mypool.add_map(thr_sub, urls)
    mypool.wait_completed()


@fn_timer
def thrPool_thrsub(urls):
    mypool = ThreadPool()
    mypool.add_map(thr_sub, urls)
    mypool.wait_completed()


if __name__ == '__main__':
    urls = [
        'http://www.biqugse.com/96703/',
        # 'http://www.biqugse.com/96717/',
        # 'http://www.biqugse.com/76169/',
        # 'http://www.biqugse.com/82744/',
        # 'http://www.biqugse.com/96095/',
        # 'http://www.biqugse.com/92385/',
    ]

    ahttp_All(urls[0])
    # thr_sub(urls[0])
    # thrPool_ahttp(urls)   # # 无效
    # multpool_ahttp(urls)  # 68sec
    # thrPool_thrsub(urls)  # 148sec
    # multpool_thrsub(urls) # 110sec
