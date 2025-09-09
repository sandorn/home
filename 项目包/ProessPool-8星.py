# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-03 12:52:03
LastEditTime : 2025-09-06 19:03:55
FilePath     : /CODE/项目包/ProessPool-8星.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os

from xt_bqg import get_contents, get_download_url
from xt_file import savefile
from xt_thread import run_custom_process
from xt_wraps import timer


def new_get_contents(args):
    return get_contents(*args)


@timer
def cmpro(bookname, urls):
    res_list = run_custom_process(
        new_get_contents, [(i, url) for i, url in enumerate(urls, 1)]
    )
    res_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.splitext(os.path.basename(__file__))[0]
    savefile(f"{files}&{bookname}&cmpro.txt", res_list, br="\n")


if __name__ == "__main__":
    url = "http://www.bequke.com/xiaoshuo/0/152/"
    bookname, urls, _ = get_download_url(url)
    cmpro(bookname, urls[0:10])  # |<perf_counter: s>
