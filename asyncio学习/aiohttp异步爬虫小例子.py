# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-07-02 16:46:05
#FilePath     : /asyncio学习/aiohttp异步爬虫小例子.py
#LastEditTime : 2020-07-02 17:26:58
#Github       : https://github.com/sandorn/home
#==============================================================
'''
import aiohttp
import asyncio
from time import time


def spilder():
    async def fetch(client):
        async with client.get('http://httpbin.org/get') as resp:
            assert resp.status == 200
            return await resp.text()

    async def main():
        async with aiohttp.ClientSession() as client:
            html = await fetch(client)
            # print(html)

    loop = asyncio.get_event_loop()
    tasks = []
    for i in range(30):
        task = loop.create_task(main())
        tasks.append(task)

    start = time()
    loop.run_until_complete(main())
    print("aiohttp spilder：", time() - start)


def single():
    async def fetch(client):
        # print("打印 ClientSession 对象", client)
        async with client.get('http://httpbin.org/get') as resp:
            assert resp.status == 200
            return await resp.text()

    async def main():
        async with aiohttp.ClientSession() as client:
            tasks = []
            for i in range(30):
                tasks.append(asyncio.create_task(fetch(client)))
            await asyncio.wait(tasks)

    loop = asyncio.get_event_loop()
    start = time()
    loop.run_until_complete(main())
    print("aiohttp single：", time() - start)


def two():
    async def fetch(client):
        # print("打印 ClientSession 对象", client)
        async with client.get('http://httpbin.org/get') as resp:
            assert resp.status == 200
            return await resp.text()

    async def main():
        async with aiohttp.ClientSession() as client:
            tasks = []
            for i in range(30):
                coro = fetch(client)
                tasks.append(asyncio.ensure_future(coro))
            await asyncio.wait(tasks)

    # #等待纤程结束
    loop = asyncio.get_event_loop()
    start = time()
    loop.run_until_complete(main())
    print("aiohttp two：", time() - start)


spilder()
single()
two()
