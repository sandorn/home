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


import asyncio
import time

from xt_wraps.executor import executor_wraps


# 测试异步函数 - 后台执行
@executor_wraps(background=True)
async def async_background_function():
    """测试异步函数的后台执行"""
    print(f"后台异步函数在 {time.strftime('%H:%M:%S')} 开始执行")
    await asyncio.sleep(1)  # 模拟较长时间操作
    print(f"后台异步函数在 {time.strftime('%H:%M:%S')} 执行完成")
    return "后台异步函数执行结果"

async def main():
    print("测试异步函数后台执行的返回类型")
    task = async_background_function()
    print(f"返回的对象类型: {type(task)}")
    print(f"是否为Task对象: {isinstance(task, asyncio.Task)}")
    print(f"是否为Future对象: {isinstance(task, asyncio.Future)}")
    print(f"Task状态: {'pending' if task.done() is False else 'done'}")
    
    # 等待任务完成
    result = await task
    print(f"任务完成后的结果: {result}")

if __name__ == "__main__":
    asyncio.run(main())