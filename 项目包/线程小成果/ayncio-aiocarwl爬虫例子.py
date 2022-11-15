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

from xt_Ahttp import Async_run, ahttpGetAll, get, multi_req
from xt_Asyncio import AioCrawl
from xt_File import savefile
from xt_Ls_Bqg import clean_Content, 结果处理, get_biqugse_download_url
from xt_Response import ReqResult
from xt_Time import fn_timer


def handle_back_ait(resp):
    if not isinstance(resp, ReqResult) and resp is not None:
        return [resp.text]

    index = resp.index
    element = resp.element

    _title = "".join(element.xpath('//h1/text()'))
    title = _title.strip('\r\n').replace(u'\u3000', u' ').replace(u'\xa0', u' ')
    _showtext = element.xpath('//*[@id="content"]/text()')
    content = clean_Content(_showtext)
    return [index, title, content]


@fn_timer
def Aio_run_Task(bookname, urls):
    asynctasks = []
    for index, url in enumerate(urls, 1):
        task = get(url)
        task.index = index
        asynctasks.append(task)
    tasks = [Async_run(task) for task in asynctasks]

    myaio = AioCrawl()
    myaio.add_tasks(tasks)
    resps = myaio.getAllResult()  # #callback=handle_resp处理以后的结果
    texts = 结果处理(resps)
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'Aio_run_Task.txt', texts, br='\n')


@fn_timer
def Aio_run_Task_Back(bookname, urls):
    asynctasks = []
    for index, url in enumerate(urls, 1):
        task = get(url, callback=handle_back_ait)
        task.index = index
        asynctasks.append(task)
    tasks = [Async_run(task) for task in asynctasks]

    myaio = AioCrawl()
    myaio.add_tasks(tasks)
    texts = myaio.getAllResult()  # #callback=handle_resp处理以后的结果
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'Aio_run_Task_Back.txt', texts, br='\n')


@fn_timer
def Aio_ahttpGetAll(bookname, urls):
    resps = ahttpGetAll(urls)
    texts = 结果处理(resps)
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'ahttpGetAll.txt', texts, br='\n')


@fn_timer
def Aio_multi_req(bookname, urls):
    asynctasks = [get(url) for url in urls]
    res_list = []
    myaio = AioCrawl()
    myaio.add_tasks([multi_req(asynctasks, 100, res_list)])
    resps = myaio.getAllResult()
    texts = 结果处理(resps[0])
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'Aio_multi_req.txt', texts, br='\n')


if __name__ == "__main__":

    bookname, urls, titles = get_biqugse_download_url('http://www.biqugse.com/96703/')
    Aio_run_Task(bookname, urls)
    Aio_run_Task_Back(bookname, urls)
    Aio_ahttpGetAll(bookname, urls)
    Aio_multi_req(bookname, urls)
'''
<Aio_run_Task>        total run: 2.02 seconds
<Aio_run_Task_Back>        total run: 2.31 seconds
<Aio_ahttpGetAll>   total run: 3.15 seconds
<Aio_multi_req>       total run: 1.70 seconds
'''
