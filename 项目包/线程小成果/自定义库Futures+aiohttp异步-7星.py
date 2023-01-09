# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-31 08:03:42
LastEditTime : 2023-01-08 01:12:00
FilePath     : /项目包/线程小成果/自定义库Futures+aiohttp异步-7星.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import os

from xt_Ahttp import ahttpGetAll
from xt_File import savefile
from xt_Ls_Bqg import get_biqugse_download_url, 结果处理
from xt_Thread import ProcessPool, ThreadPool
from xt_Time import fn_timer


@fn_timer
def Aio_ahttp(bookname, urls):
    resps = ahttpGetAll(urls)
    texts = 结果处理(resps)
    files = os.path.basename(__file__).split(".")[0]
    savefile(f'{files}&{bookname}Aio_ahttp.txt', texts, br='\n')


def multpool():
    url_list = [
        'http://www.biqugse.com/96703/',
        'http://www.biqugse.com/96717/',
        'http://www.biqugse.com/76169/',
        'http://www.biqugse.com/82744/',
        'http://www.biqugse.com/96095/',
        'http://www.biqugse.com/92385/',
    ]

    mypool = ProcessPool()
    # mypool = ProcessPool() # 38.926 seconds
    # mypool = ThreadPool() # 56.509 seconds

    for url in url_list:
        bookname, urls, titles = get_biqugse_download_url(url)
        booknames = [bookname] * len(urls)
        mypool.add_sub(Aio_ahttp, [bookname, urls])
    mypool.wait_completed()


def Aio():
    target = 'http://www.biqugse.com/96703/'
    bookname, urls, _ = get_biqugse_download_url(target)
    Aio_ahttp(bookname, urls)


if __name__ == "__main__":

    Aio()
    # multpool()  # 40s
