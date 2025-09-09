# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-14 23:30:44
LastEditTime : 2024-11-06 15:00:42
FilePath     : /CODE/项目包/自定义库AioHttpClient&Carw异步-9星.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os

from xt_ahttp import ahttpGetAll
from xt_ahttpclent import AioHttpClient
from xt_aiocrawl import AioCrawl
from xt_bqg import get_contents, get_download_url, 结果处理
from xt_file import savefile
from xt_wraps import timer


@timer
def AioHttpCrawl_pool(book_name, urls_list):
    myaio = AioCrawl()
    args_list = [[(index, url), {}] for index, url in enumerate(urls_list, 1)]
    texts = myaio.add_pool(get_contents, args_list)
    texts.sort(key=lambda x: x[0])
    # sorted(texts, key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(f"{files}&{book_name}AioHttpCrawl_pool.txt", texts, br="\n")


@timer
def ahttp_GetAll(book_name, urls):
    resps = ahttpGetAll(urls)
    texts = 结果处理(resps)
    files = os.path.basename(__file__).split(".")[0]
    savefile(f"{files}&{book_name}ahttpGetAll.txt", texts, br="\n")


@timer
def AioHttpClient_run(book_name, urls):
    texts = []
    AHC = AioHttpClient()
    resps = AHC.getall(urls)
    texts = 结果处理(resps)
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(f"{files}&{book_name}AioHttpClient_run.txt", texts, br="\n")


if __name__ == "__main__":
    url = "https://www.bigee.cc/book/6909/"
    book_name, urls, _ = get_download_url(url)
    AioHttpCrawl_pool(book_name, urls[0:10])  # |perf_counter: 68.29s
    # ahttp_GetAll(book_name, urls[0:10])  # |perf_counter: 56.20s
    # AioHttpClient_run(book_name, urls)  # |perf_counter: 42.20s
