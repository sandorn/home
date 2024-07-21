# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-03 12:52:03
LastEditTime : 2024-07-21 12:00:34
FilePath     : /CODE/项目包/自定义库ProessPool_apply_async-8星.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os
from multiprocessing import Pool as ProcPool

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
    # aftertexts = [[row[i] for i in range(1, 3)] for row in texts]
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(f"{files}&{bookname}&Poolapply_async.txt", res_list, br="\n")


if __name__ == "__main__":
    url = "https://www.bigee.cc/book/6909/"
    Poolapply_async(url)  # |time: 57.40 sec|processtime: 3.17 sec
