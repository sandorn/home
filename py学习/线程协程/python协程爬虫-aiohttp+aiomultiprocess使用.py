# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-13 00:49:00
LastEditTime : 2022-12-13 00:49:01
FilePath     : /线程协程/python协程爬虫-aiohttp+aiomultiprocess使用.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import asyncio

from aiohttp import request
from aiomultiprocess import Pool, Worker


async def get(url):
    async with request("GET", url) as response:
        return await response.text("utf-8")


async def main():
    p = Worker(target=get, args=("https://www.wuzhuiso.com/", ))
    response = await p
    print(2222222222222222, response)


async def main_pool():
    urls = [
        "https://www.wuzhuiso.com/",
        "https://www.bing.com/",
    ]
    async with Pool() as pool:
        result = await pool.map(get, urls)
        print(11111111111111, result)


if __name__ == "__main__":

    asyncio.run(main_pool())
    # asyncio.run(main())
