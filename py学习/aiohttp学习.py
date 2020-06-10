# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-09 15:37:25
#FilePath     : /py学习/aiohttp学习.py
#LastEditTime : 2020-06-09 15:40:41
#Github       : https://github.com/sandorn/home
#==============================================================
Welcome to AIOHTTP — aiohttp 3.6.2 documentation
https://docs.aiohttp.org/en/stable/
'''
import aiohttp
import asyncio


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
    help(aiohttp)
