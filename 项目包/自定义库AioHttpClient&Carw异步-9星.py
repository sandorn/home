# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-14 23:30:44
LastEditTime : 2024-11-06 15:00:42
FilePath     : /CODE/项目包/自定义库AsyncHttpClient&Carw异步-9星.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from __future__ import annotations

import os

from xt_bqg import get_contents, get_download_url, resps_handle
from xt_utils.files import save_file
from xthttp import AsyncHttpClient, ahttp_get, ahttp_get_all
from xtthread import AsyncThreadPool
from xtwraps import timer


@timer
def AioHttpCrawl_pool(book_name, urls_list):
    myaio = AsyncThreadPool()
    args_list = [[(index, url), {}] for index, url in enumerate(urls_list, 1)]
    texts = myaio.submit_tasks(get_contents, args_list)
    texts.sort(key=lambda x: x[0])
    # sorted(texts, key=lambda x: x[0])
    files = os.path.basename(__file__).split('.')[0]
    save_file(f'{files}&{book_name}AioHttpCrawl_pool.txt', texts, br='\n')


@timer
def ahttp_GetAll(book_name, urls):
    resps = ahttp_get_all(urls)
    texts = resps_handle(resps)
    files = os.path.basename(__file__).split('.')[0]
    save_file(f'{files}&{book_name}ahttp_get_all.txt', texts, br='\n')


@timer
def AsyncHttpClient_run(book_name, urls):
    texts = []
    AHC = AsyncHttpClient()
    resps = AHC.multi_request('get', urls)
    texts = [resp.result for resp in resps]
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split('.')[0]
    save_file(f'{files}&{book_name}AsyncHttpClient_run.txt', texts, br='\n')


if __name__ == '__main__':
    url = 'https://www.bigee.cc/book/6909/'
    book_name, urls, _ = get_download_url(url)
    print(f'book_name: {book_name}')
    print(f'urls[0]: {urls[0]}')
    print(f'urls[1]: {urls[1]}')
    print(f'urls[2]: {urls[2]}')
    resp = ahttp_get(urls[0])
    print(f'resp: {resp}')
    # AioHttpCrawl_pool(book_name, urls[0:10])  # |perf_counter: 68.29s
    ahttp_GetAll(book_name, urls[0:10])  # |perf_counter: 56.20s
    # AsyncHttpClient_run(book_name, urls[0:10])  # |perf_counter: 42.20s
