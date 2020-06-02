# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-01 15:59:38
@LastEditors: Even.Sand
@LastEditTime: 2020-03-13 17:47:12
'''
import asyncio

import aiohttp
from aiomultiprocess import Pool, Process, Worker


async def get(url, x='mainbypool'):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(x, response)


async def mainbyprocess():
    p = Process(target=get, args=("https://www.baidu.com", 'mainbyprocess'))
    await p


async def mainbyworker():
    p = Worker(target=get, args=("https://www.baidu.com", 'mainbyworker'))
    response = await p


async def mainbypool():
    urls = ["https://www.163.com", "https://www.baidu.com"]
    async with Pool() as pool:
        result = await pool.map(get, urls)
        print(result)

if __name__ == "__main__":
    asyncio.run(mainbypool())
    asyncio.run(mainbyworker())
    asyncio.run(mainbyprocess())
    # If you want to get results back from that coroutine, Worker makes that available:
    # If you want a managed pool of worker processes, then use Pool:
