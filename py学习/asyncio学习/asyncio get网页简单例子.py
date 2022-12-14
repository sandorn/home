# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-28 20:12:54
#FilePath     : /asyncio学习/asyncio get网页简单例子.py
#LastEditTime : 2020-06-28 20:13:22
#Github       : https://github.com/sandorn/home
#==============================================================
'''
import asyncio
import aiohttp


async def get(url):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        result = await response.text()
    return result


async def request():
    url = 'https://httpbin.org/get'
    print('Waiting for', url)
    result = await get(url)
    print('Get response from', url, 'Result:', result)


tasks = [asyncio.ensure_future(request()) for _ in range(2)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
