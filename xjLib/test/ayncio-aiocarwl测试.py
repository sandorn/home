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
#LastEditTime : 2020-06-30 19:16:55
#Github       : https://github.com/sandorn/home
#==============================================================
'''

import os

from xt_File import savefile
from xt_Time import fn_timer
from xt_Ls_Bqg import get_download_url, arrangeContent
from xt_Asyncio import AioCrawl
from xt_Ahttp import ahttpGetAll
from xt_Response import ReqResult


def handle_result(resps):
    # print('handle_result_4444:', resps)
    texts = []
    for resp in resps:
        # print('handle_result_5555:', resp)
        if resp is None: continue
        if not isinstance(resp, ReqResult):
            texts.append([
                resp.text,
            ])
        index = resp.index
        element = resp.element

        _title = "".join(element.xpath('//h1/text()'))
        title = _title.strip('\r\n').replace(u'\u3000',
                                             u' ').replace(u'\xa0', u' ')
        _showtext = element.xpath('//*[@id="content"]/text()')
        content = arrangeContent(_showtext)
        texts.append([index, title, content])
    return texts


@fn_timer
def aio(bookname, urls):
    aio = AioCrawl()
    aio.add_fetch_tasks([[url, index + 1] for index, url in enumerate(urls)])
    resps = aio.getAllResult()
    texts = handle_result(resps)
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'AioCrawl.txt', texts, br='\n')
    # #38_38836 :4seconds  #2_2714:101seconds  #2_2760:7seconds #76_76519:1seconds


@fn_timer
def aia(bookname, urls):
    texts = []

    def _h_res(resp):
        # print('handle_result_5555:', resp)
        element = resp.element
        index = resp.index

        _title = "".join(element.xpath('//h1/text()'))
        title = _title.strip('\r\n').replace(u'\u3000',
                                             u' ').replace(u'\xa0', u' ')
        _showtext = element.xpath('//*[@id="content"]/text()')
        content = arrangeContent(_showtext)
        texts.append([index, title, content])

        return [index, title, content]

    texts = ahttpGetAll(urls, callback=_h_res)
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'AioCrawlAll.txt', texts, br='\n')


if __name__ == "__main__":

    bookname, urls = get_download_url('http://www.biqukan.com/2_2714/')
    # #38_38836  #2_2714  #2_2760  #76_76519

    aio(bookname, urls)
    # aia(bookname, urls)
'''
    38_38836 <aio> total run: 4.04 seconds
    76_76519 <aio> total run: 0.74 seconds
    2_2760 <aio> total run: 6.60 seconds
    18_18098 <aio> total run: 19.19 seconds
    2_2714 <aio> total run: 61.05 seconds

    38_38836 <aia> total run: 7.6 seconds
    76_76519 <aia> total run: 1.94 seconds
    2_2760 <aia> total run: 4.30 seconds
    18_18098 <aio> total run: 19.19 seconds
    2_2714 <aia> total run: 82.05 seconds

'''
