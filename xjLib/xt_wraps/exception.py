# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-03-03 10:03:22
LastEditTime : 2025-08-29 18:32:40
FilePath     : /CODE/xjLib/xt_wraps/exception.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import inspect
import traceback
from functools import wraps
from typing import Any, Callable

from xt_wraps.log import LogCls, create_basemsg

mylog = LogCls().logger


def catch_wraps(default_return: Any = None):
    """异常处理装饰器 - 同时支持同步和异步函数的异常处理"""

    def decorator(func: Callable) -> Callable:
        _basemsg = create_basemsg(func)

        # 统一的异常处理逻辑
        def handle_exception(err: Exception) -> Any:
            exc_type, exec_val, exec_tb = type(err), err, traceback.format_exc()
            mylog.error(
                f"{_basemsg} | catch_wraps | Error:{exc_type} | {exec_val!r} | {exec_tb}"
            )
            # 返回默认值
            return default_return


        # 异步函数的装饰器
        @wraps(func)
        async def async_wrapped(*args: Any, **kwargs: Any) -> Any:
            try:
                return await func(*args, **kwargs)
            except Exception as err:
                return handle_exception(err)

        # 同步函数的装饰器
        @wraps(func)
        def sync_wrapped(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as err:
                return handle_exception(err)

        
        # 检查函数是否是异步的
        if inspect.iscoroutinefunction(func):
            return async_wrapped
        else:
            return sync_wrapped

    return decorator

def catch_deco(default_return: Any = None):
    """异常处理装饰器 - 同时支持同步和异步函数的异常处理"""

    def decorator(func: Callable) -> Callable:
        # 定义异常处理逻辑
        def handle_exception(err: Exception) -> Any:
            exc_type, exec_val, exec_tb = type(err), err, traceback.format_exc()
            mylog.error(
                f"{_basemsg} | catch_deco | Error:{exc_type} | {exec_val!r} | {exec_tb}"
            )
            # 返回默认值
            return default_return
            
        # 定义异步异常处理的内部函数
        @wraps(func)
        async def async_wrapped(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as err:
                return handle_exception(err)
        
        # 定义同步异常处理的内部函数
        @wraps(func)
        def sync_wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as err:
                return handle_exception(err)
                
        @wraps(func)
        def catch_decorator(*args: Any, **kwargs: Any) -> Any:
            if inspect.iscoroutinefunction(func):
                return async_wrapped(*args, **kwargs)
            else:
                return sync_wrapped(*args, **kwargs)
        
        # 外部包装函数
        def outer_wrapper(*args: Any, **kwargs: Any) -> Any:
            return catch_decorator(*args, **kwargs)
        
        # 保留原始函数的元数据
        outer_wrapper.__name__ = func.__name__
        outer_wrapper.__doc__ = func.__doc__
        outer_wrapper.__module__ = func.__module__

        _basemsg = create_basemsg(func)

        return outer_wrapper

    return decorator


if __name__ == "__main__":

    import asyncio

    # 测试同步函数
    @catch_deco(default_return="同步默认返回值")
    def sync_function_with_error():
        raise RuntimeError("这是一个同步异常")
        return "同步正常返回值"


    @catch_deco(default_return="同步默认返回值")
    def sync_function_normal():
        return "同步正常返回值"


    # 测试异步函数
    @catch_deco(default_return="异步默认返回值")
    async def async_function_with_error():
        await asyncio.sleep(0.1)
        raise RuntimeError("这是一个异步异常")
        return "异步正常返回值"


    @catch_deco(default_return="异步默认返回值")
    async def async_function_normal():
        await asyncio.sleep(0.1)
        return "异步正常返回值"


    def test_sync_functions():
        """测试同步函数"""

        result = sync_function_normal()
        print(f"同步正常函数结果: {result}")

        result = sync_function_with_error()
        print(f"同步异常函数结果: {result}")


    async def test_async_functions():
        """测试异步函数"""
        result = await async_function_normal()
        print(f"异步正常函数结果: {result}")
        result = await async_function_with_error()
        print(f"异步异常函数结果: {result}")


    async def main():
        """主测试函数"""
        print("开始测试装饰器...")

        # 测试同步函数
        test_sync_functions()

        # 测试异步函数
        await test_async_functions()

        print("测试完成!")


    # 运行测试
    asyncio.run(main())
