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

from __future__ import annotations

import os

from xt_bqg import get_contents, get_download_url
from xt_utils.files import save_file
from xtthread.process import run_custom_process
from xtwraps import timer


def new_get_contents(args):
    return get_contents(*args)


@timer
def cmpro(bookname, urls):
    res_list = run_custom_process(new_get_contents, [(i, url) for i, url in enumerate(urls, 1)])
    res_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.splitext(os.path.basename(__file__))[0]
    save_file(f'{files}&{bookname}&cmpro.txt', res_list, br='\n')


if __name__ == '__main__':
    url = 'https://www.bigee.cc/book/6909/'
    bookname, urls, _ = get_download_url(url)
    cmpro(bookname, urls[0:10])  # |<perf_counter: s>
