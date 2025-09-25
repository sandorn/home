#!/usr/bin/env python3
"""
测试更新后的log_wraps装饰器是否正常工作
验证特殊符号快捷方法的集成
"""

import asyncio
from xt_wraps.log import log_wraps, mylog


@log_wraps
def sync_example(x: int, y: int) -> int:
    """同步函数示例"""
    return x + y


@log_wraps(log_result=False)
def sync_without_result(x: str) -> str:
    """不记录返回结果的同步函数示例"""
    return f"Processed: {x}"


@log_wraps(log_args=False)
def sync_without_args() -> str:
    """不记录参数的同步函数示例"""
    return "No arguments function"


@log_wraps
async def async_example(data: list) -> dict:
    """异步函数示例"""
    await asyncio.sleep(0.1)  # 模拟异步操作
    return {"processed_count": len(data), "success": True}


@log_wraps
async def async_with_error() -> None:
    """会抛出异常的异步函数示例"""
    await asyncio.sleep(0.1)  # 模拟异步操作
    raise ValueError("模拟错误发生")


async def main() -> None:
    """主函数，运行所有测试"""
    mylog.info("开始测试更新后的log_wraps装饰器")
    
    # 测试同步函数
    mylog.info("\n测试同步函数:")
    result1 = sync_example(5, 3)
    mylog.info(f"同步函数结果: {result1}")
    
    result2 = sync_without_result("test data")
    mylog.info(f"不记录结果的同步函数结果: {result2}")
    
    result3 = sync_without_args()
    mylog.info(f"不记录参数的同步函数结果: {result3}")
    
    # 测试异步函数
    mylog.info("\n测试异步函数:")
    result4 = await async_example([1, 2, 3, 4, 5])
    mylog.info(f"异步函数结果: {result4}")
    
    # 测试异常情况
    mylog.info("\n测试异常处理:")
    try:
        await async_with_error()
    except ValueError:
        mylog.info("捕获到预期的ValueError异常")
    
    mylog.info("\n所有测试完成")


if __name__ == "__main__":
    asyncio.run(main())