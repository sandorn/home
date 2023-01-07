# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2023-01-07 20:55:15
LastEditTime : 2023-01-07 20:55:29
FilePath     : /py学习/线程协程/生成协程的装饰器.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import asyncio
from asyncio.coroutines import iscoroutine
from asyncio.proactor_events import _ProactorBasePipeTransport
from functools import wraps

import aiohttp


def silence_event_loop_closed(func):

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise

    return wrapper


_ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)


def asyncio_wrapper(func):

    @wraps(func)
    async def __wrapper(*args, **kwargs):
        result = await asyncio.create_task(func(*args, **kwargs))  # 执行传入的函数
        return result

    return __wrapper


def asyncio_wrapper(func):
    '''异步装饰器'''

    @wraps(func)
    def _wrapper(*args, **kwargs):

        async def __wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if iscoroutine(result):
                result = await asyncio.create_task(result)
            return result

        return asyncio.run(__wrapper(*args, **kwargs))

    return _wrapper


@asyncio_wrapper
async def get_message():
    # print('开始访问')
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get') as response:
            # print('访问结束')
            return await response.text()


if __name__ == '__main__':
    s = get_message()
    print(s)
