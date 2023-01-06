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

from xt_Ahttp import ahttpGetAll, asynctask_run, get
from xt_Asyncio import AioCrawl
from xt_File import savefile
from xt_Ls_Bqg import clean_Content, get_biqugse_download_url, 结果处理
from xt_Response import ReqResult
from xt_Time import fn_timer


@fn_timer
def Aio_ahttp(bookname, urls):
    myaio = AioCrawl()
    myaio.add_ahttp_tasks(urls)
    resps = myaio.getAllResult()[0]
    texts = 结果处理(resps)
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(f'{files}&{bookname}Aio_ahttp.txt', texts, br='\n')


@fn_timer
def Aio_feach_run(bookname, urls):
    myaio = AioCrawl()
    myaio.add_fetch_tasks(urls, callback=handle_back_ait)
    texts = myaio.getAllResult()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(f'{files}&{bookname}Aio_feach_run.txt', texts, br='\n')


@fn_timer
def ahttp_run(bookname, urls):
    texts = ahttpGetAll(urls, callback=handle_back_ait)
    # #callback=handle_resp处理以后的结果
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(f'{files}&{bookname}ahttp_run.txt', texts, br='\n')


@fn_timer
def Aio_run_Task(bookname, urls):
    asynctasks = []
    for index, url in enumerate(urls, 1):
        task = get(url)
        task.index = index
        asynctasks.append(task)
    tasks = [asynctask_run(task) for task in asynctasks]

    myaio = AioCrawl()
    myaio.add_tasks(tasks)
    resps = myaio.getAllResult()
    texts = 结果处理(resps)
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(f'{files}&{bookname}Aio_run_Task.txt', texts, br='\n')


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
def Aio_run_Task_Back(bookname, urls):
    asynctasks = []
    for index, url in enumerate(urls, 1):
        task = get(url, callback=handle_back_ait)
        task.index = index
        asynctasks.append(task)
    tasks = [asynctask_run(task) for task in asynctasks]

    myaio = AioCrawl()
    myaio.add_tasks(tasks)
    texts = myaio.getAllResult()  # #callback=handle_resp处理以后的结果
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(f'{files}&{bookname}Aio_run_Task_Back.txt', texts, br='\n')


if __name__ == "__main__":

    bookname, urls, titles = get_biqugse_download_url('http://www.biqugse.com/96703/')
    # Aio_ahttp(bookname, urls)
    # Aio_feach_run(bookname, urls)
    # ahttp_run(bookname, urls)
    # Aio_run_Task(bookname, urls)
    # Aio_run_Task_Back(bookname, urls)
'''
Aio_run_Task(bookname, urls)                4.12s
Aio_ahttp(bookname, urls)                   4.36s
ahttp_run(bookname, urls)                   4.70s
Aio_run_Task_Back(bookname, urls)           4.86s
'''
