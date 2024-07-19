# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-31 08:03:42
LastEditTime : 2024-06-21 15:09:20
FilePath     : /CODE/项目包/线程小成果/自定义库fninthreadpool异步-5星.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os

from xt_file import savefile
from xt_ls_bqg import clean_Content, get_download_url
from xt_requests import get
from xt_response import htmlResponse
from xt_str import Str_Clean
from xt_thread import FnInThreadPool, ThreadPool
from xt_time import fn_timer


def new_get_contents(args):
    index, target = args
    resp = get(target)
    if not isinstance(resp, htmlResponse):
        return [0, resp, ""]
    _xpath = ["//h1/text()", '//*[@id="chaptercontent"]/text()']
    title, content = resp.xpath(_xpath)
    title = "".join(Str_Clean("".join(title), ["\u3000", "\xa0", "\u00a0"]))
    content = clean_Content(content).strip()
    return [index, title, content]


@fn_timer
def ThreadPool_add_tasks(bookname, urls, fn):
    mypool = ThreadPool()
    args = [[index, url] for index, url in enumerate(urls, start=1)]
    mypool.add_tasks(fn, args)
    texts = mypool.wait_completed()
    files = os.path.basename(__file__).split(".")[0]
    savefile(f"{files}&{bookname}ThreadPool_add_tasks.txt", texts, br="\n")


@fn_timer
def FnInPool(bookname, urls):
    args = [[index, url] for index, url in enumerate(urls, start=1)]
    texts = FnInThreadPool(new_get_contents, args).result
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(f"{files}&{bookname}FnInPool.txt", texts, br="\n")


if __name__ == "__main__":
    url_list = ["https://www.bigee.cc/book/6909/"]
    bookname, urls, _ = get_download_url(url_list[0])
    # ThreadPool_add_tasks(bookname, urls, new_get_contents)  # |perf_counter: 153.21s|process_time: 53.72s
    FnInPool(bookname, urls)  # |perf_counter: 86.14s|process_time: 37.39s
