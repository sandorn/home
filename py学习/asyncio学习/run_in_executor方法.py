# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-15 18:26:52
FilePath     : /CODE/py学习/asyncio学习/run_in_executor方法.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import asyncio
import os

from xt_File import savefile
from xt_Ls_Bqg import get_biqugse_download_url, get_contents


async def run(index, url):
    loop = asyncio.get_event_loop()
    try:
        return await loop.run_in_executor(None, get_contents, index, url)
    except Exception as e:
        print(e)


bookname, url_list, _ = get_biqugse_download_url('http://www.biqugse.com/96703/')

tasks = [asyncio.ensure_future(run(index, url)) for index, url in enumerate(url_list)]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

text_list = [task.result() for task in tasks]
text_list.sort(key=lambda x: x[0])
files = os.path.split(__file__)[-1].split(".")[0]
savefile(f'{files}&{bookname}&ahttp.txt', text_list, br='\n')
