# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-06-15 21:01:29
LastEditTime : 2024-06-15 21:01:29
FilePath     : /CODE/项目包/线程小成果/自定义库futures.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os

from xt_Ahttp import ahttpGetAll
from xt_File import savefile
from xt_Ls_Bqg import get_contents, get_download_url, 结果处理
from xt_Thread import ProcessPool, ThreadPool
from xt_Time import fn_timer


@fn_timer
def ahttp_All(url):
    bookname, urls, _ = get_download_url(url)
    resps = ahttpGetAll(urls[:20])
    text_list = 结果处理(resps)
    text_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.basename(__file__).split('.')[0]
    savefile(f'{files}&{bookname}ahttp_All.txt', text_list, br='\n')


@fn_timer
def thr_sub(url):
    mypool = ThreadPool()
    bookname, urls, _ = get_download_url(url)
    args = [[i, u] for i, u in enumerate(urls[:20])]
    mypool.add_tasks(get_contents, *args)
    text_list = mypool.wait_completed()
    # text_list = 结果处理(resps)
    text_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.split(__file__)[-1].split('.')[0]
    savefile(f'{files}&{bookname}&Thrtpool.txt', text_list, br='\n')


@fn_timer
def multpool_thrsub(urls):
    mypool = ProcessPool()
    mypool.add_tasks(thr_sub, urls)
    mypool.wait_completed()


@fn_timer
def thrPool_thrsub(urls):
    mypool = ThreadPool()
    mypool.add_tasks(thr_sub, urls)
    mypool.wait_completed()


if __name__ == '__main__':
    urls = [
        'https://www.bigee.cc/book/6909/',
    ]

    # ahttp_All(urls[0])
    thr_sub(urls[0])
    # multpool_thrsub(urls)
    # thrPool_thrsub(urls)
