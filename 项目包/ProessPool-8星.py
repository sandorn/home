# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-03 12:52:03
LastEditTime : 2024-08-21 15:46:48
FilePath     : /CODE/项目包/ProessPool-8星.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Pool as ProcPool

from xt_file import savefile
from xt_ls_bqg import get_contents, get_download_url
from xt_time import fn_timer


def new_get_contents(args):
    return get_contents(*args)


@fn_timer
def MPpool(bookname, urls):
    with ProcPool(32) as propool:
        res_list = propool.map(new_get_contents, enumerate(urls, 1))
        # task_list = [
        #     propool.apply_async(get_contents, args=(index, url))
        #     for index, url in enumerate(urls, 1)
        # ]
        # res_list = [res.get() for res in task_list]

    res_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(f"{files}&{bookname}&MPpool.txt", res_list, br="\n")


@fn_timer
def PPoolExecutor(bookname, urls):
    with ProcessPoolExecutor(32) as executor:
        task_list = [
            executor.submit(get_contents, i, url) for i, url in enumerate(urls, 1)
        ]
        res_list = [task.result() for task in task_list]

    res_list.sort(key=lambda x: x[0])
    files = os.path.splitext(os.path.basename(__file__))[0]
    savefile(f"{files}&{bookname}&PPoolExecutor.txt", res_list, br="\n")


if __name__ == "__main__":
    url = "https://www.bigee.cc/book/6909/"
    bookname, urls, _ = get_download_url(url)
    MPpool(bookname, urls)  # |<perf_counter: 70.98s>
    # PPoolExecutor(bookname, urls)  # |<perf_counter: 72.30s>
