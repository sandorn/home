# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-14 23:30:44
LastEditTime : 2024-06-14 15:59:47
FilePath     : /CODE/项目包/线程小成果/自定义库Ahttp-Aiocarw异步-6星.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os

from xt_Ahttp import ahttpGetAll
from xt_Asyncio import AioCrawl
from xt_File import savefile
from xt_Ls_Bqg import clean_Content, get_contents, get_download_url, 结果处理
from xt_Response import htmlResponse
from xt_Thread import FuncInThreadPool
from xt_Time import fn_timer


@fn_timer
def Aio_feach_run(bookname, urls):
    myaio = AioCrawl()
    myaio.add_tasks(urls)
    resps = myaio.wait_completed()
    texts = 结果处理(resps)
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split('.')[0]
    savefile(f'{files}&{bookname}Aio_feach_run.txt', texts, br='\n')


def handle_back_ait(resp):
    if not isinstance(resp, htmlResponse) and resp is not None:
        return [resp.text]

    index = resp.index

    _title = resp.pyquery('h1').text()
    title = _title.strip('\r\n').replace('\u3000', ' ').replace('\xa0', ' ')
    _showtext = resp.pyquery('#chaptercontent').text()
    content = clean_Content(_showtext)
    return [index, title, content]


@fn_timer
def Aio_feach_back(bookname, urls):
    myaio = AioCrawl()
    myaio.add_tasks(urls, callback=handle_back_ait)
    texts = myaio.wait_completed()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split('.')[0]
    savefile(f'{files}&{bookname}Aio_feach_back.txt', texts, br='\n')


@fn_timer
def ahttp_run(bookname, urls):
    texts = ahttpGetAll(urls, callback=handle_back_ait)
    # #callback=handle_resp处理以后的结果
    texts.sort(key=lambda x: x[0])
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


@fn_timer
def func_ThreadPool(bookname, urls):
    indexes = list(range(len(urls)))
    texts = FuncInThreadPool(get_contents, indexes, urls).result
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split('.')[0]
    savefile(f'{files}&{bookname}func_ThreadPool.txt', texts, br='\n')


if __name__ == '__main__':
    url = 'https://www.biquge11.cc/read/11159/'
    bookname, urls, _ = get_download_url(url)
    # Aio_feach_run(bookname, urls)
    # Aio_feach_back(bookname, urls)
    ahttp_run(bookname, urls)
    # Aio_add_func(bookname, urls)
    # func_ThreadPool(bookname, urls)
