# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-01 15:54:34
@LastEditors: Even.Sand
@LastEditTime: 2020-03-01 15:58:36
'''
import aiohttp
import asyncio
import time


async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(response)


async def request():
    url = 'http://www.163.com'
    await get(url)


def _now(): return time.time()


start = _now()
tasks = [asyncio.ensure_future(request()) for _ in range(10)]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
print(_now() - start)
