# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-13 10:26:28
@LastEditors: Even.Sand
@LastEditTime: 2020-03-13 10:34:12
'''
import asyncio

from aiohttp import request
from aiomultiprocess import Pool


async def get(url):
    async with request("GET", url) as response:
        return await response.text("utf-8")


async def main():
    urls = ["http://www.baidu.com",
            'http://www.sina.com.cn']
    async with Pool() as pool:
        result = await pool.map(get, urls)
        '''
        p = Worker(target=get, args=(
            "http://www.baidu.com",
            'http://www.sina.com.cn')
            )
        response = await p
        '''
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
