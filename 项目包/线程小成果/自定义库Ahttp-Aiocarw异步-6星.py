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


if __name__ == "__main__":

    bookname, urls, _ = get_biqugse_download_url("http://www.biqugse.com/96703/")
    # 'http://www.biqugse.com/69761/'
    Aio_feach_run(bookname, urls)
    Aio_feach_run_back(bookname, urls)
    ahttp_run(bookname, urls)
'''
Aio_ahttp(bookname, urls)           68.30 seconds
Aio_feach_run(bookname, urls)       75.70 seconds
ahttp_run(bookname, urls)           75.25 seconds
'''
