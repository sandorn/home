# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-11-11 09:23:51
LastEditTime : 2024-11-13 09:03:50
FilePath     : /CODE/test/testpy.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import asyncio
import functools

from xt_requests import get


def get_html(url, **kwargs):
    return get(url, **kwargs)


async def main1():
    loop = asyncio.get_running_loop()

    # 使用 functools.partial  传递关键字参数
    partial_func = functools.partial(get_html, "https://www.baidu.com", index=30)

    # 在执行器中运行同步函数
    return await loop.run_in_executor(None, partial_func)


# 运行异步主函数
# print(1111111111, asyncio.run(main1()))

import datetime

import ulid

res = ulid.from_timestamp(datetime.datetime(1999, 1, 1))
print(res)
