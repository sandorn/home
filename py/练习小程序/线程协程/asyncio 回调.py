# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-01 16:33:59
@LastEditors: Even.Sand
@LastEditTime: 2020-03-01 16:35:58
'''
import asyncio
import aiofiles


async def myopen():
    async with aiofiles.open('README.md', encoding='utf8') as file:
        contents = await file.read()
        print('my read done, file size is {}'.format(len(contents)))


async def test_read():
    print('begin readfile')
    await myopen()
    print('end readfile')


async def test_cumpute(x, y):
    print("begin cumpute")
    await asyncio.sleep(0.2)
    print('end cumpute')
    return x + y


def got_result(future):
    print('The result is ', future.result())


loop = asyncio.get_event_loop()
to_do = [asyncio.ensure_future(test_read()), asyncio.ensure_future(test_cumpute(1, 5))]
to_do[1].add_done_callback(got_result)
loop.run_until_complete(asyncio.wait(to_do))
loop.close()
'''
---------------------
作者：Python之禅
来源：CSDN
原文：https://blog.csdn.net/zV3e189oS5c0tSknrBCL/article/details/80906206
版权声明：本文为博主原创文章，转载请附上博文链接！
'''
