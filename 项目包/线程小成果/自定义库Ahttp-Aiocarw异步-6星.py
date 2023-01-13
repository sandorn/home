# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:57
LastEditTime : 2023-01-13 16:43:36
FilePath     : /项目包/线程小成果/自定义库Ahttp-Aiocarw异步-6星.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import os

from xt_Ahttp import ahttpGetAll
from xt_Asyncio import AioCrawl
from xt_File import savefile
from xt_Ls_Bqg import (clean_Content, get_biqugse_download_url, get_contents, 结果处理)
from xt_Response import htmlResponse
from xt_Time import fn_timer


@fn_timer
def Aio_feach_run(bookname, urls):
    myaio = AioCrawl()
    myaio.add_tasks(urls)
    resps = myaio.wait_completed()
    texts = 结果处理(resps)
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(f'{files}&{bookname}Aio_feach_run.txt', texts, br='\n')


def handle_back_ait(resp):
    if not isinstance(resp, htmlResponse) and resp is not None:
        return [resp.text]

    index = resp.index
    element = resp.element

    _title = "".join(element.xpath('//h1/text()'))
    title = _title.strip('\r\n').replace(u'\u3000', u' ').replace(u'\xa0', u' ')
    _showtext = element.xpath('//*[@id="content"]/text()')
    content = clean_Content(_showtext)
    return [index, title, content]


@fn_timer
def Aio_feach_run_back(bookname, urls):
    myaio = AioCrawl()
    myaio.add_tasks(urls, callback=handle_back_ait)
    texts = myaio.wait_completed()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(f'{files}&{bookname}Aio_feach_run_back.txt', texts, br='\n')


@fn_timer
def ahttp_run(bookname, urls):
    texts = ahttpGetAll(urls, callback=handle_back_ait)
    # #callback=handle_resp处理以后的结果
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(f'{files}&{bookname}ahttp_run.txt', texts, br='\n')


@fn_timer
def run_in_pool(bookname, urls):
    myaio = AioCrawl()
    indexes = list(range(len(urls)))
    myaio.add_func(get_contents, indexes, urls)
    texts = myaio.wait_completed()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(f'{files}&{bookname}run_in_pool.txt', texts, br='\n')


if __name__ == "__main__":
    url = 'http://www.biqugse.com/28542/'
    # url = "http://www.biqugse.com/96703/"
    bookname, urls, _ = get_biqugse_download_url(url)
    # 'http://www.biqugse.com/28542/'
    # Aio_feach_run(bookname, urls)
    # Aio_feach_run_back(bookname, urls)
    # ahttp_run(bookname, urls)
    # run_in_pool(bookname, urls)
'''
Aio_feach_run(bookname, urls)       151sec
Aio_feach_run_back(bookname, urls)  166sec
ahttp_run(bookname, urls)           154sec
run_in_pool(bookname, urls)         335sec
'''
