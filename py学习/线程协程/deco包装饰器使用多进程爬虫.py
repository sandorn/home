# !/usr/bin/env python
"""
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-29 23:19:42
LastEditTime : 2023-01-12 16:29:18
FilePath     : /py学习/线程协程/deco包装饰器使用多进程爬虫.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os

from deco import concurrent, synchronized
from xt_file import savefile
from xt_ls_bqg import clean_Content
from xt_requests import get
from xt_response import htmlResponse
from xt_str import Str_Replace


@concurrent.threaded(processes=16)
def test_concurrent(index, target):
    # print(f'进程{os.getpid()}正在处理{index}')
    resp = get(target)
    _xpath = ("//h1/text()", '//*[@id="content"]/text()')
    assert isinstance(resp, htmlResponse)
    _title, _showtext = resp.xpath(_xpath)
    title = Str_Replace("".join(_title), [("\u3000", " "), ("\xa0", " "), ("\u00a0", " ")])
    content = clean_Content(_showtext)
    return [index, title, content]


@synchronized
def test_synchronized(target):
    # sourcery skip: for-append-to-extend, inline-immediately-returned-variable, list-comprehension
    resp = get(target)
    _xpath = ('//meta[@property="og:title"]//@content', '//*[@id="list"]/dl/dt[2]/following-sibling::dd/a/@href', '//*[@id="list"]/dl/dt[2]/following-sibling::dd/a/text()')
    assert isinstance(resp, htmlResponse)
    bookname, temp_urls, titles = resp.xpath(_xpath)

    bookname = bookname[0]
    baseurl = "/".join(target.split("/")[:-2])
    urls = [baseurl + item for item in temp_urls]  # 章节链接
    text_list = []
    for index, url in enumerate(urls):
        text_list.append(test_concurrent(index, url))
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(f"{files}&{bookname}&CustomThread.txt", text_list, br="\n")


if __name__ == "__main__":
    _res = test_synchronized("http://www.biqugse.com/96703/")
    # @concurrent.threaded(processes=16)   11秒  # 24 9秒  # 36 8秒
    # print(_res)
