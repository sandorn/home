# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-03 12:52:03
LastEditTime : 2024-08-19 16:01:40
FilePath     : /CODE/项目包/ProessPool-8星.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Pool as ProcPool
from os import cpu_count

from xt_file import savefile
from xt_ls_bqg import get_contents, get_download_url
from xt_time import fn_timer


@fn_timer
def Poolapply_async(url):
    bookname, urls, _ = get_download_url(url)

    p = ProcPool(32)  # 设置进程池的最大进程数量
    task_list = []

    for i, url in enumerate(urls, 1):
        res = p.apply_async(get_contents, args=(i, url))  # 异步执行任务
        task_list.append(res)
    p.close()
    p.join()
    res_list = [res.get() for res in task_list]
    res_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(f"{files}&{bookname}&Poolapply_async.txt", res_list, br="\n")


@fn_timer
def ProcessPool(url):
    bookname, urls, _ = get_download_url(url)
    _count = (cpu_count() or 4) * 4
    _count = 61 if _count > 61 else _count
    _count = len(urls) if len(urls) < _count else _count

    with ProcessPoolExecutor(max_workers=_count) as executor:
        task_list = [
            executor.submit(get_contents, i, url) for i, url in enumerate(urls, 1)
        ]
        res_list = [task.result() for task in task_list]

    res_list.sort(key=lambda x: x[0])
    files = os.path.splitext(os.path.basename(__file__))[0]
    savefile(f"{files}&{bookname}&Poolapply_async.txt", res_list, br="\n")


if __name__ == "__main__":
    url = "https://www.bigee.cc/book/6909/"
    # Poolapply_async(url)  # |<perf_counter: 70.98s>
    ProcessPool(url)  # |<perf_counter: 72.30s>
