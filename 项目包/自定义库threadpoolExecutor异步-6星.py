# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-31 08:03:42
LastEditTime : 2024-10-28 13:14:47
FilePath     : /CODE/项目包/自定义库threadpoolExecutor异步-6星.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os

from xt_file import savefile
from xt_ls_bqg import get_contents, get_download_url
from xt_thread import FnInPool, ThreadPool
from xt_time import fn_timer


@fn_timer
def ThreadPool_add_tasks(bookname, urls, fn):
    mypool = ThreadPool()
    mypool.add_tasks(fn, list(range(len(urls))), urls)
    texts = mypool.wait_completed()
    files = os.path.basename(__file__).split(".")[0]
    savefile(f"{files}&{bookname}ThreadPool_add_tasks.txt", texts, br="\n")


@fn_timer
def FnInPoolfunc(bookname, urls):
    res = FnInPool(get_contents, list(range(len(urls))), urls)
    texts = res.result
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(f"{files}&{bookname}FnInPool.txt", texts, br="\n")


if __name__ == "__main__":
    url_list = ["https://www.bigee.cc/book/6909/"]
    bookname, urls, _ = get_download_url(url_list[0])
    ThreadPool_add_tasks(bookname, urls, get_contents)  # |perf_counter: 81.59s
    # FnInPoolfunc(bookname, urls)  # |perf_counter: 83.51s|
