# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-03 21:31:02
@LastEditors: Even.Sand
@LastEditTime: 2020-03-03 21:31:02
'''
import asyncio
import time


async def run(url):
    print("start ", url)
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(None, time.sleep, 1)
    except Exception as e:
        print(e)
    print("stop ", url)
url_list = ["https://thief.one", "https://home.nmask.cn", "https://movie.nmask.cn", "https://tool.nmask.cn"]
tasks = [asyncio.ensure_future(run(url)) for url in url_list]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
