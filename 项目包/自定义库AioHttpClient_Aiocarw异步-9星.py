# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-14 23:30:44
LastEditTime : 2024-08-07 18:11:37
FilePath     : /CODE/项目包/自定义库AioHttpClient_Aiocarw异步-9星.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os

from xt_ahttp import ahttpGetAll
from xt_ahttpclent import AioHttpClient
from xt_ahttpcrawl import AioHttpCrawl
from xt_file import savefile
from xt_ls_bqg import get_contents, get_download_url, handle_back_ait, 结果处理
from xt_time import fn_timer


@fn_timer
def AioHttpCrawl_task(bookname, urls):
    myaio = AioHttpCrawl()
    myaio.add_tasks(urls)
    resps = myaio.wait_completed()
    texts = 结果处理(resps)
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(f"{files}&{bookname}AioHttpCrawl_task.txt", texts, br="\n")


@fn_timer
def AioHttpCrawl_pool(bookname, urls):
    myaio = AioHttpCrawl()
    myaio.add_pool(get_contents, list(range(len(urls))), urls)
    texts = myaio.wait_completed()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(f"{files}&{bookname}AioHttpCrawl_pool.txt", texts, br="\n")


@fn_timer
def ahttp_GetAll(bookname, urls):
    texts = ahttpGetAll(urls, callback=handle_back_ait)
    files = os.path.basename(__file__).split(".")[0]
    savefile(f"{files}&{bookname}ahttpGetAll.txt", texts, br="\n")


@fn_timer
def AioHttpClient_run(bookname, urls):
    texts = []
    AHC = AioHttpClient()
    resps = AHC.getall(urls)
    texts = 结果处理(resps)
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(f"{files}&{bookname}AioHttpClient_run.txt", texts, br="\n")


if __name__ == "__main__":
    url = "https://www.bigee.cc/book/6909/"
    bookname, urls, _ = get_download_url(url)
    # AioHttpCrawl_pool(bookname, urls)  # |perf_counter: 85.29s
    ahttp_GetAll(bookname, urls[:20])  # |perf_counter: 56.20s
    # AioHttpCrawl_task(bookname, urls)  # |perf_counter: 55.75s
    # AioHttpClient_run(bookname, urls)  # |perf_counter: 42.20s #@ 8星
