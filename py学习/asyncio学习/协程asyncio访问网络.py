# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:36:04
LastEditTime : 2022-12-14 23:25:56
FilePath     : /py学习/asyncio学习/协程asyncio访问网络.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import asyncio

import aiohttp


async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(response)


async def request():
    url = 'http://www.163.com'
    await get(url)


tasks = [asyncio.ensure_future(request()) for _ in range(10)]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
