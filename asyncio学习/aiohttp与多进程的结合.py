# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-16 23:13:37
@LastEditors: Even.Sand
@LastEditTime: 2020-04-17 20:29:54
'''
# 与多进程的结合

import asyncio
import aiohttp
import time
from aiomultiprocess import Pool


async def get(url):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    result = await response.text()
    session.close()
    return result


async def get_html():
    url = 'http://www.baidu.com'
    urls = [url for _ in range(100)]
    async with Pool() as pool:
        result = await pool.map(get, urls)
        return result


if __name__ == '__main__':
    start = time.time()
    coroutine = get_html()
    task = asyncio.ensure_future(coroutine)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)

    end = time.time()
    print('Cost time:', end - start)
