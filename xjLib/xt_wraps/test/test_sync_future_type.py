# !/usr/bin/env python
"""
==============================================================
Description  : 测试同步函数后台执行返回的对象类型
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-06 07:49:17
LastEditTime : 2025-09-06 08:11:26
FilePath     : /CODE/xjLib/xt_wraps/test/test_sync_future_type.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import asyncio
import time

from xt_wraps.executor import executor_wraps


# 测试同步函数 - 后台执行
@executor_wraps(background=True)
def sync_background_function():
    """测试同步函数的后台执行"""
    print(f"后台同步函数在 {time.strftime('%H:%M:%S')} 开始执行")
    time.sleep(1)  # 模拟较长时间操作
    print(f"后台同步函数在 {time.strftime('%H:%M:%S')} 执行完成")
    return "后台同步函数执行结果"

async def main():
    print("测试同步函数后台执行的返回类型")
    future = sync_background_function()
    print(f"返回的对象类型: {type(future)}")
    print(f"是否为asyncio.Future: {isinstance(future, asyncio.Future)}")
    print(f"类名: {future.__class__.__name__}")
    print(f"基类: {[base.__name__ for base in future.__class__.__bases__]}")
    print(f"是否有done()方法: {hasattr(future, 'done')}")
    print(f"是否有result()方法: {hasattr(future, 'result')}")
    
    # 等待任务完成
    result = await future
    print(f"任务完成后的结果: {result}")

if __name__ == "__main__":
    asyncio.run(main())