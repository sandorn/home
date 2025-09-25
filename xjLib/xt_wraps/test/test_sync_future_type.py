# !/usr/bin/env python3
"""
==============================================================
Description  : 测试同步函数后台执行返回的对象类型
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-06 07:49:17
LastEditTime : 2025-09-16 11:26:46
FilePath     : /CODE/xjlib/xt_wraps/test/test_sync_future_type.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from __future__ import annotations

import asyncio
import time

from xt_wraps import executor_wraps


# 测试同步函数 - 后台执行
@executor_wraps(background=True)
def sync_background_function():
    """测试同步函数的后台执行"""
    time.sleep(1)  # 模拟较长时间操作
    return '后台同步函数执行结果'


async def main():
    future = sync_background_function()

    # 等待任务完成
    await future


if __name__ == '__main__':
    asyncio.run(main())
