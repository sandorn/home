# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-31 08:03:42
LastEditTime : 2023-01-01 17:52:08
FilePath     : /项目包/线程小成果/自定义库Futures+Asyncio异步l爬虫.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import os

from xt_Ahttp import Async_run, get
from xt_Asyncio import AioCrawl
from xt_File import savefile
from xt_Ls_Bqg import get_biqugse_download_url, 结果处理
from xt_Thread import ProcessPool, ThreadPool
from xt_Time import fn_timer


@fn_timer
def Aio_run_Task(bookname, urls):
    asynctasks = []
    for index, url in enumerate(urls):
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
    savefile(f'{files}&{bookname}Aio_run_Task.txt', texts, br='\n')


def multpool():
    url_list = [
        'http://www.biqugse.com/96703/',
        'http://www.biqugse.com/96704/',
        'http://www.biqugse.com/96705/',
        'http://www.biqugse.com/96706/',
        'http://www.biqugse.com/96707/',
        'http://www.biqugse.com/96708/',
    ]

    mypool = ProcessPool()
    # mypool = ProcessPool() # 38.926 seconds
    # mypool = ThreadPool() # 56.509 seconds

    for url in url_list:
        bookname, urls, titles = get_biqugse_download_url(url)
        booknames = [bookname] * len(urls)
        mypool.add_sub(Aio_run_Task, [bookname, urls])
    mypool.get_sub_result()


if __name__ == "__main__":

    # Aio_run_Task(bookname, urls)
    # Aio_run_Task_Back(bookname, urls)
    # Aio_ahttpGetAll(bookname, urls)
    # Aio_multi_req(bookname, urls)

    multpool()
