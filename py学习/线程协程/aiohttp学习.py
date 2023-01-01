# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-01 18:51:54
FilePath     : /py学习/线程协程/aiohttp学习.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import asyncio

import aiohttp


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main(url):
    async with aiohttp.ClientSession() as session:
        text = await fetch(session, url)
        print(text)


if __name__ == '__main__':
    url = "https://httpbin.org/get"  # 返回head及ip等信息

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(url))
