# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-22 11:18:57
@LastEditors: Even.Sand
@LastEditTime: 2019-05-22 11:18:57
'''
import aiohttp
import asyncio
import time


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main(Target_url):
    async with aiohttp.ClientSession() as session:
        await fetch(session, Target_url)


def f(Times, Target_url):
    st = time.time()
    loop = asyncio.get_event_loop()
    task = [main(Target_url)] * Times
    loop.run_until_complete(asyncio.wait(task))
    et = time.time()
    return et - st
