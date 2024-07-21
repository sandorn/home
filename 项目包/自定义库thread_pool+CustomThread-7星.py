# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:57
LastEditTime : 2024-07-19 15:39:49
FilePath     : /CODE/项目包/自定义库thread_pool+CustomThread-7星.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os

from xt_file import savefile
from xt_ls_bqg import get_contents, get_download_url
from xt_thread import CustomThread, ThreadPoolWraps
from xt_time import fn_timer

tpool = ThreadPoolWraps(200)


@fn_timer
def ByThreadPoolWraps(target):
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
    # urls = urls[:100]
    _ = [CustomThread(get_contents, index, urls[index]) for index in range(len(urls))]
    text_list = CustomThread.getAllResult()
    text_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(f"{files}&{bookname}&ByCustomThread.txt", text_list, br="\n")


if __name__ == "__main__":
    ByThreadPoolWraps("https://www.bigee.cc/book/6909/")  # |perf_counter: 65.40s|process_time: 28.03s
    # ByCustomThread("https://www.bigee.cc/book/6909/")  # |perf_counter: 72.39s|process_time: 38.41s
