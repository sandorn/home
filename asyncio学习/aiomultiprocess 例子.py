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
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-06-28 20:43:15
'''
import asyncio

from aiohttp import request
from aiomultiprocess import Pool


async def get(url):
    async with request("GET", url) as response:
        return await response.text("utf-8")


async def main():
    urls = ["http://www.baidu.com", 'http://www.sina.com.cn']
    async with Pool() as pool:
        result = await pool.map(get, urls)

        print(result)
        return result


if __name__ == "__main__":
    asyncio.run(main())
