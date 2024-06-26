# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-06-25 17:11:57
FilePath     : /CODE/py学习/线程协程/2k小说-ahttp异步.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import asyncio


# 普通函数1
def func1():
    return 'Function 1 executed'


# 普通函数2
def func2():
    return 'Function 2 executed'


# 异步装饰器
def async_wrapper(func):
    async def _wrapper():
        return func()

    return _wrapper


# 转换为coroutine
async_func1 = async_wrapper(func1)
async_func2 = async_wrapper(func2)


async def main():
    # 并发执行多个 coroutine
    result = await asyncio.gather(async_func1(), async_func2())
    print(result)


# 运行事件循环
asyncio.run(main())
