# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-14 23:30:44
LastEditTime : 2024-06-21 12:28:37
FilePath     : /CODE/项目包/线程小成果/自定义库Ahttp-Aiocarw异步-8星.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os

from xt_Ahttp import ahttpGetAll
from xt_Asyncio import AioCrawl
from xt_File import savefile
from xt_Ls_Bqg import clean_Content, get_contents, get_download_url, 结果处理
from xt_Response import htmlResponse
from xt_Time import fn_timer


@fn_timer
def Aio_add_task(bookname, urls):
    myaio = AioCrawl()
    myaio.add_tasks(urls)
    resps = myaio.wait_completed()
    texts = 结果处理(resps)
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split('.')[0]
    savefile(f'{files}&{bookname}Aio_add_task.txt', texts, br='\n')


def handle_back_ait(resp):
    if not isinstance(resp, htmlResponse):
        return [0, resp, '']

    index = resp.index
    _title = resp.pyquery('h1').text()
    title = _title.strip('\r\n').replace('\u3000', ' ').replace('\xa0', ' ')
    _showtext = resp.pyquery('#chaptercontent').text()
    content = clean_Content(_showtext)
    return [index, title, content]


@fn_timer
def Aio_add_task_back(bookname, urls):
    myaio = AioCrawl()
    myaio.add_tasks(urls, callback=handle_back_ait)
    texts = myaio.wait_completed()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split('.')[0]
    savefile(f'{files}&{bookname}Aio_add_task_back.txt', texts, br='\n')


@fn_timer
def ahttp_run(bookname, urls):
    texts = ahttpGetAll(urls, callback=handle_back_ait)
    files = os.path.basename(__file__).split('.')[0]
    savefile(f'{files}&{bookname}ahttp_run.txt', texts, br='\n')


@fn_timer
def Aio_add_func(bookname, urls):
    myaio = AioCrawl()
    indexes = list(range(len(urls)))
    myaio.add_func(get_contents, indexes, urls)
    texts = myaio.wait_completed()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split('.')[0]
    savefile(f'{files}&{bookname}Aio_add_func.txt', texts, br='\n')


if __name__ == '__main__':
    url = 'https://www.bigee.cc/book/6909/'
    # 'https://www.biquge11.cc/read/11159/'
    bookname, urls, _ = get_download_url(url)
    # Aio_add_task(bookname, urls)  # |time: 56.05 sec|processtime: 37.31 sec
    # Aio_add_task_back(bookname, urls)  # |time: 59.45 sec|processtime: 39.39 sec
    # ahttp_run(bookname, urls)  # |time: 63.03 sec|processtime: 40.23 sec
    # Aio_add_func(bookname, urls)  # |time: 88.85 sec|processtime: 46.36 sec
