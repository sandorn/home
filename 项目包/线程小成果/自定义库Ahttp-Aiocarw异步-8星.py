# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-14 23:30:44
LastEditTime : 2024-07-17 16:02:42
FilePath     : /CODE/项目包/线程小成果/自定义库Ahttp-Aiocarw异步-8星.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os

from xt_ahttp import ahttpGetAll
from xt_ahttpclent import AioHttpClient
from xt_ahttpcrawl import AioHttpCrawl
from xt_file import savefile
from xt_ls_bqg import clean_Content, get_contents, get_download_url, 结果处理
from xt_response import htmlResponse
from xt_time import fn_timer


@fn_timer
def Aio_add_task(bookname, urls):
    myaio = AioHttpCrawl()
    myaio.add_tasks(urls)
    resps = myaio.wait_completed()
    texts = 结果处理(resps)
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(f"{files}&{bookname}Aio_add_task.txt", texts, br="\n")


@fn_timer
def Aio_add_pool(bookname, urls):
    myaio = AioHttpCrawl()
    myaio.add_pool(get_contents, list(range(len(urls))), urls)
    texts = myaio.wait_completed()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(f"{files}&{bookname}Aio_add_func.txt", texts, br="\n")


def handle_back_ait(resp):
    if not isinstance(resp, htmlResponse):
        return [0, resp, ""]

    index = resp.index
    _title = resp.query("h1").text()
    title = _title.strip("\r\n").replace("\u3000", " ").replace("\xa0", " ")
    _showtext = resp.query("#chaptercontent").text()
    content = clean_Content(_showtext)
    return [index, title, content]


@fn_timer
def Aio_add_task_back(bookname, urls):
    myaio = AioHttpCrawl()
    myaio.add_tasks(urls, callback=handle_back_ait)
    texts = myaio.wait_completed()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(f"{files}&{bookname}Aio_add_task_back.txt", texts, br="\n")


@fn_timer
def ahttp_run(bookname, urls):
    texts = ahttpGetAll(urls, callback=handle_back_ait)
    files = os.path.basename(__file__).split(".")[0]
    savefile(f"{files}&{bookname}ahttp_run.txt", texts, br="\n")


@fn_timer
def AioHttpClient_run(bookname, urls):
    texts = []
    AHC = AioHttpClient()
    resps = AHC.getall(urls)
    texts = 结果处理(resps)
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(f"{files}&{bookname}AioHttpClient_run.txt", texts, br="\n")


if __name__ == "__main__":
    url = "https://www.bigee.cc/book/6909/"
    bookname, urls, _ = get_download_url(url)
    # Aio_add_task(bookname, urls)  # |time: 55.67 sec|processtime: 32.83 sec
    # Aio_add_pool(bookname, urls)  # |time: 87.61 sec|processtime: 38.48 sec
    # Aio_add_task_back(bookname, urls)  # |time: 52.35 sec|processtime: 34.19 sec
    # ahttp_run(bookname, urls)  # |time: 64.91 sec|processtime: 40.31 sec
    AioHttpClient_run(bookname, urls)  # |time: 42.82 sec|processtime: 28.95 sec #@ 8星
