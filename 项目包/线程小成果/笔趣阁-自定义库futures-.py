# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:49
LastEditTime : 2022-12-09 11:42:51
FilePath     : /项目包/线程小成果/笔趣阁-自定义库futures-.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import os

from xt_Ahttp import Async_run, ahttpGetAll, get
from xt_Asyncio import AioCrawl
from xt_File import savefile
from xt_Ls_Bqg import get_biqugse_download_url, 结果处理
from xt_Thread import P_Pool, T_Pool
from xt_Time import fn_timer


@fn_timer
def ahttp_All(url):
    bookname, urls, _ = get_biqugse_download_url(url)
    resps = ahttpGetAll(urls)
    text_list = 结果处理(resps)
    text_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'ahttp_All.txt', text_list, br='\n')


def multpool(urls, pool_func=P_Pool):
    mypool = pool_func()
    mypool.add_map(ahttp_All, urls)
    # mypool = pool_func(Aio_run_Task, urls)
    mypool.wait_map_completed()


if __name__ == '__main__':
    url = 'http://www.biqugse.com/2367/'
    # ahttp_All(url)
    # Aio_run_Task(url)

    urls = [
        'http://www.biqugse.com/96703/',
        # 'http://www.biqugse.com/96717/',
        # 'http://www.biqugse.com/2367/',
    ]
    multpool(urls)  #, T_Pool)
