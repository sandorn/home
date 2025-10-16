# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:57
LastEditTime : 2025-09-06 18:55:56
FilePath     : /CODE/项目包/自定义库thread_CustomThread-7星.py
Github       : https://github.com/sandorn/home
==============================================================
"""
from __future__ import annotations

import os

from xt_bqg import get_contents, get_download_url
from xt_file import savefile
from xt_thread import ThreadBase, ThreadPoolWraps
from xt_time import fn_timer


@fn_timer
def ByThreadPoolWraps(target):
    tpool = ThreadPoolWraps(160)
    bookname, urls, _ = get_download_url(target)
    for index, url in enumerate(urls):
        tpool(get_contents)(index, url)
    text_list = tpool.wait_completed()
    text_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(f"{files}&{bookname}&ByThreadPoolWraps.txt", text_list, br="\n")


@fn_timer
def ByCustomThread(target):
    bookname, urls, _ = get_download_url(target)
    _ = [ThreadBase(get_contents, index, urls[index]) for index in range(len(urls))]
    text_list = ThreadBase.getAllResult()
    text_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(f"{files}&{bookname}&ByCustomThread.txt", text_list, br="\n")


if __name__ == "__main__":
    ByThreadPoolWraps("https://www.bigee.cc/book/6909/")  # |perf_counter: 77.40s
    # ByCustomThread("https://www.bigee.cc/book/6909/")  # |perf_counter: 83.58s
