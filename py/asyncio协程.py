# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-16 01:04:34
@LastEditors: Even.Sand
@LastEditTime: 2019-05-22 10:44:58
'''
import aiohttp
import asyncio
import time
import requests


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    async with aiohttp.ClientSession() as session:
        await fetch(session, 'http://python.org')


st = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait([main(), main()]))
et = time.time()
print(et - st)

st = time.time()
res_text = requests.get('http://python.org').text
res_text_2 = requests.get('http://python.org').text
et = time.time()
print(et - st)
'''
---------------------
作者：肥宅_Sean
来源：CSDN
原文：https://blog.csdn.net/a19990412/article/details/82218826
版权声明：本文为博主原创文章，转载请附上博文链接！'''
