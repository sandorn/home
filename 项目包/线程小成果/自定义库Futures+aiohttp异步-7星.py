# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-31 08:03:42
LastEditTime : 2024-06-14 16:08:38
FilePath     : /CODE/项目包/线程小成果/自定义库Futures+aiohttp异步-7星.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os

from xt_Ahttp import ahttpGetAll
from xt_Asyncio import AioCrawl
from xt_File import savefile
from xt_Ls_Bqg import get_download_url, 结果处理
from xt_Thread import ProcessPool
from xt_Time import fn_timer


@fn_timer
def Aio_ahttp(bookname, urls):
    resps = ahttpGetAll(urls)
    texts = 结果处理(resps)
    files = os.path.basename(__file__).split('.')[0]
    savefile(f'{files}&{bookname}Aio_ahttp.txt', texts, br='\n')


@fn_timer
def Aio_feach_run(bookname, urls):
    myaio = AioCrawl()
    myaio.add_tasks(urls)
    resps = myaio.wait_completed()
    texts = 结果处理(resps)
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split('.')[0]
    savefile(f'{files}&{bookname}Aio_feach_run.txt', texts, br='\n')


def pool(url_list, func):
    mypool = ProcessPool()

    for url in url_list:
        bookname, urls, _ = get_download_url(url)
        mypool.add_sub(func, [bookname, urls])
    mypool.wait_completed()


if __name__ == '__main__':
    url_list = [
        'https://www.biquge11.cc/read/11159/',
    ]
    # pool(url_list, Aio_ahttp)  # 卡死
    pool(url_list[:1], Aio_feach_run)  # AioCrawl 12s
