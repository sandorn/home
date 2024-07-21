"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:57
LastEditTime : 2024-07-19 16:22:24
FilePath     : /CODE/项目包/CF-Pool进程池--7星.PY
Github       : https://github.com/sandorn/home
==============================================================
python线程池ThreadPoolExecutor与进程池ProcessPoolExecutor - Harvard_Fly - 博客园
https://www.cnblogs.com/FG123/p/9704233.html
"""

import os
from concurrent.futures import (
    ThreadPoolExecutor,  # 线程池模块  ProcessPoolExecutor
    as_completed,
)

from xt_file import savefile
from xt_ls_bqg import get_contents, get_download_url
from xt_time import fn_timer

texts = []


def callback_func(future):
    index, name, text = future.result()  # 回调函数取得返回值
    texts.append([index, name, text])


@fn_timer
def main_callback(max, bookname, urls):
    with ThreadPoolExecutor(max) as pool:
        [pool.submit(get_contents, index, urls[index]).add_done_callback(callback_func) for index in range(len(urls))]
    texts.sort(key=lambda x: x[0])
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(f"{files}&{bookname}ThreadPoolE_submit_callback.txt", texts, br="\n")


@fn_timer
def main_completed(max, bookname, urls):
    with ThreadPoolExecutor(max) as pool:
        future_tasks = [pool.submit(get_contents, index, urls[index]) for index in range(len(urls))]
    texts = [future.result() for future in as_completed(future_tasks)]
    # $texts = [future.result() for future in wait(future_tasks)[0]]
    textssord = sorted(texts, key=lambda x: x[0])
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(f"{files}&{bookname}ThreadPoolE_submit.txt", textssord, br="\n")


@fn_timer
def main_map(max, bookname, urls):
    indexs = list(range(len(urls)))
    # 创建多进程队列
    with ThreadPoolExecutor(max) as pool:
        future_tasks = pool.map(get_contents, indexs, urls)
    texts = list(future_tasks)
    texts.sort(key=lambda x: x[0])
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(f"{files}&{bookname}ThreadPoolE_map.txt", texts, br="\n")


if __name__ == "__main__":
    url = "https://www.bigee.cc/book/6909/"
    bookname, urls, _ = get_download_url(url)
    # main_map(60, bookname, urls)  # |perf_counter: 72.30s|process_time: 39.91s
    # main_completed(60, bookname, urls)  # |perf_counter: 73.01s|process_time: 40.36s
    main_callback(60, bookname, urls)  # |perf_counter: 72.73s|process_time: 41.64s
