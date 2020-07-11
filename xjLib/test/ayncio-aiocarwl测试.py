# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-30 12:50:40
#FilePath     : /xjLib/test/ayncio-aiocarwl测试.py
#LastEditTime : 2020-07-10 18:19:14
#Github       : https://github.com/sandorn/home
#==============================================================
'''

import os

from xt_File import savefile
from xt_Time import fn_timer
from xt_Ls_Bqg import get_download_url, arrangeContent
from xt_Asyncio import AioCrawl, make_future
from xt_Ahttp import ahttpGetAll, get, Async_run, multi_req
from xt_Response import ReqResult
import threading
import asyncio


def handle_result(resps):
    texts = []
    for resp in resps:
        if resp is None: continue
        if not isinstance(resp, ReqResult):
            texts.append([resp.text])
        index = resp.index
        element = resp.element

        _title = "".join(element.xpath('//h1/text()'))
        title = _title.strip('\r\n').replace(u'\u3000', u' ').replace(u'\xa0', u' ')
        _showtext = element.xpath('//*[@id="content"]/text()')
        content = arrangeContent(_showtext)
        texts.append([index, title, content])
    return texts


@fn_timer
def aio(bookname, urls):
    aio = AioCrawl()
    aio.add_fetch_tasks([[url, index + 1] for index, url in enumerate(urls)])
    # aio.add_fetch_tasks(urls)
    resps = aio.getAllResult()
    texts = handle_result(resps)
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'AioCrawl.txt', texts, br='\n')


def handle_resp(resp):
    if not isinstance(resp, ReqResult) and resp is not None:
        return [resp.text]

    index = resp.index
    element = resp.element

    _title = "".join(element.xpath('//h1/text()'))
    title = _title.strip('\r\n').replace(u'\u3000', u' ').replace(u'\xa0', u' ')
    _showtext = element.xpath('//*[@id="content"]/text()')
    content = arrangeContent(_showtext)
    return [index, title, content]


@fn_timer
def ait(bookname, urls):
    asynctasks = []
    for index, url in enumerate(urls):
        task = get(url, callback=handle_resp)
        task.index = index + 1
        asynctasks.append(task)
    tasks = [Async_run(task) for task in asynctasks]

    aio = AioCrawl()
    aio.add_tasks(tasks)
    texts = aio.getAllResult()  # #callback=handle_resp处理以后的结果
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'AioAtthpTask.txt', texts, br='\n')


@fn_timer
def ahttpall(bookname, urls):
    resps = ahttpGetAll(urls)
    texts = handle_result(resps)
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'ahttpGetAll.txt', texts, br='\n')


@fn_timer
def aimq(bookname, urls):
    asynctasks = [get(url) for url in urls]
    res_list = []
    aio = AioCrawl()
    aio.add_tasks([multi_req(asynctasks, 100, res_list)])
    resps = aio.getAllResult()
    texts = handle_result(resps[0])
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'AioAtthpMulti_req.txt', texts, br='\n')


if __name__ == "__main__":

    bookname, urls = get_download_url('http://www.biqukan.com/38_38836/')

    # aio(bookname, urls)
    # ait(bookname, urls)
    # ahttpall(bookname, urls)
    aimq(bookname, urls)
    # @make_future
    # res = asyncio.run(aia(bookname, urls))
    # print(res.result())
'''
    38_38836 <aio> total run: 3.62 seconds
    76_76519 <aio> total run: 0.74 seconds
    2_2760 <aio> total run: 6.60 seconds
    18_18098 <aio> total run: 19.19 seconds
    2_2714 <aio> total run: 58.00 seconds

    38_38836 <aia> total run: 3.28 seconds
    76_76519 <aia> total run: 1.94 seconds
    2_2760 <aia> total run: 4.30 seconds
    18_18098 <aio> total run: 19.19 seconds
    2_2714 <aia> total run: 78.05 seconds

'''
