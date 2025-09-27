# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-06 07:39:54
LastEditTime : 2025-09-06 07:41:21
FilePath     : /CODE/xjLib/xt_wraps/test/test_task_type.py
Github       : https://github.com/sandorn/home
==============================================================
"""
from __future__ import annotations

import asyncio

from xt_wraps.executor import executor_wraps
from xt_wraps.timer import timer_wraps


# 测试异步函数 - 后台执行
@executor_wraps(background=True)
@timer_wraps
async def async_background_function():
    """测试异步函数的后台执行"""
    await asyncio.sleep(1)  # 模拟较长时间操作
    return '后台异步函数执行结果'


async def main():
    task = async_background_function()
    
    # 等待任务完成
    await task


if __name__ == '__main__':
    asyncio.run(main())