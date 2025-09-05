# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-01 08:40:27
LastEditTime : 2025-09-02 09:54:05
FilePath     : /CODE/xjLib/xt_wraps/executor.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial, wraps
from typing import Any, Callable, Optional, TypeVar

from .exception import handle_exception
from .log import create_basemsg

# 类型变量
T = TypeVar("T")
R = TypeVar("R")

# 默认线程池执行器
_default_executor = ThreadPoolExecutor(max_workers=10, thread_name_prefix="XtExecutor")


def executor_wraps(
    fn: Optional[Callable[..., Any]] = None,
    *,
    background: bool = False,
    executor: Optional[ThreadPoolExecutor] = None,
) -> Callable[..., Any]:
    """异步执行器装饰器"""

    def decorator(func: Callable[..., R]) -> Callable[..., Any]:
        used_executor = executor or _default_executor

        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    if background:
                        return asyncio.create_task(func(*args, **kwargs))
                    else:
                        return await func(*args, **kwargs)
                except Exception as err:
                    return handle_exception(err, create_basemsg(func))

            return async_wrapper
        else:

            @wraps(func)
            async def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    loop = asyncio.get_event_loop()
                    task_func = partial(func, *args, **kwargs)

                    if background:
                        return loop.run_in_executor(used_executor, task_func)
                    else:
                        return await loop.run_in_executor(used_executor, task_func)
                except Exception as err:
                    return handle_exception(err, create_basemsg(func))

            return sync_wrapper

    # 处理装饰器调用方式
    return decorator(fn) if fn else decorator


def run_executor_wraps(fn: Optional[Callable[..., Any]] = None) -> Callable[..., Any]:
    """
    同步运行异步函数的装饰器

    Args:
        func: 要装饰的函数（同步或异步）

    Returns:
        同步函数，可以直接调用

    Example:
        @run_executor_wraps
        async def async_function():
            await asyncio.sleep(1)
            return "done"

        result = async_function()  # 直接返回结果，不需要 await
    """

    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> R:
            if asyncio.iscoroutinefunction(func):
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    return loop.run_until_complete(func(*args, **kwargs))
                except Exception as err:
                    return handle_exception(err, create_basemsg(func))
                finally:
                    loop.close()
            else:
                return func(*args, **kwargs)

        return sync_wrapper

    # 处理装饰器调用方式
    return decorator(fn) if fn else decorator


def future_wraps(
    fn: Optional[Callable[..., Any]] = None,
    *,
    executor: Optional[ThreadPoolExecutor] = None,
) -> Callable[..., Any]:
    """将同步函数包装成返回 Future 对象的装饰器"""

    def decorator(func: Callable[..., R]) -> Callable[..., asyncio.Future[R]]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> asyncio.Future[R]:
            try:
                loop = asyncio.get_event_loop()
                used_executor = executor or _default_executor
                return loop.run_in_executor(
                    used_executor, lambda: func(*args, **kwargs)
                )
            except Exception as err:
                return handle_exception(err, create_basemsg(func))

        return wrapper

    return decorator(fn) if fn else decorator


async def future_wraps_result(future: asyncio.Future[T]) -> T:
    """等待 Future 完成并返回结果"""
    try:
        # return await future
        # 添加超时机制，避免永久等待
        return await asyncio.wait_for(future, timeout=30.0)
    except asyncio.TimeoutError as timerr:
        # 如果超时，取消任务并抛出异常
        if not future.done():
            future.cancel()
        return handle_exception(timerr, create_basemsg(future), re_raise=True)
    except asyncio.CancelledError as cancerr:
        return handle_exception(cancerr, create_basemsg(future), re_raise=True)
    except Exception as err:
        return handle_exception(err, create_basemsg(future), re_raise=True)


if __name__ == "__main__":
    # 测试 executor_wraps

    import time

    @executor_wraps
    def sync_multiply(x: int, y: int) -> int:
        print(f"同步函数执行: {x} * {y}")
        return x * y

    @executor_wraps(background=True)
    def sync_background_task(x: int) -> int:
        print(f"后台同步任务执行: {x}")
        return x * 2

    @executor_wraps
    async def async_multiply(x: int, y: int) -> int:
        print(f"异步函数执行: {x} * {y}")
        await asyncio.sleep(0.1)
        return x * y

    @executor_wraps(background=True)
    async def async_background_task(x: int) -> int:
        print(f"后台异步任务执行: {x}")
        await asyncio.sleep(0.1)
        return x * 2

    async def test_executor_wraps():
        print("=== 测试 executor_wraps ===")

        # 测试同步函数
        result1 = await sync_multiply(5, 6)
        print(f"同步函数结果: {result1}")

        # 测试后台同步任务
        future1 = await sync_background_task(10)  # 注意：这里返回的是 Future
        result2 = await future1
        print(f"后台同步任务结果: {result2}")

        # 测试异步函数
        result3 = await async_multiply(7, 8)
        print(f"异步函数结果: {result3}")

        # 测试后台异步任务
        future2 = await async_background_task(15)  # 注意：这里返回的是 Task
        result4 = await future2
        print(f"后台异步任务结果: {result4}")

    # 测试 run_executor_wraps
    @run_executor_wraps
    async def async_function() -> str:
        await asyncio.sleep(0.2)
        return "异步函数完成"

    @run_executor_wraps
    def sync_function() -> str:
        time.sleep(0.2)
        return "同步函数完成"

    def test_run_executor_wraps():
        print("\n=== 测试 run_executor_wraps ===")

        # 测试异步函数同步调用
        result1 = async_function()
        print(f"异步函数同步调用结果: {result1}")

        # 测试同步函数
        result2 = sync_function()
        print(f"同步函数调用结果: {result2}")

    # 运行测试
    asyncio.run(test_executor_wraps())
    test_run_executor_wraps()

    import asyncio

    from xt_ahttp import ACResponse, ClientSession
    from xt_requests import get

    def get_a_html(url):
        return get(url)

    async def get_a_html_bg(url):
        await asyncio.sleep(1)  # 模拟延迟
        return get(url)

    @future_wraps
    def add(a, b):
        time.sleep(32)
        return a / b

    async def main():
        fn1 = executor_wraps(get_a_html)
        res = await fn1("https://www.baidu.com")
        print("1111111111|Result length:", len(res), res.status, res.url)
        # 后台执行，返回Future对象（对于同步函数）
        fn2 = executor_wraps(get_a_html_bg, background=True)
        future = await fn2("https://www.baidu.com")
        # 等待后台任务完成
        bg_res = await future
        print(
            "222222222|Background result length:",
            len(bg_res),
            bg_res.status,
            bg_res.url,
        )

        # 等待 Future 完成并获取结果
        add_result = await add(3, 5)
        print("333333333|Add result:", add_result)
        add_result2 = await future_wraps_result(add(99, 0))
        print(f"444444444|Add result: {add_result2}")

    asyncio.run(main())

    print(
        55555555,
        fn4 := run_executor_wraps(get_a_html_bg),
        fn4("https://www.126.com"),
    )
    print(66666666, run_executor_wraps(get_a_html)("https://www.sina.com.cn"))

    @run_executor_wraps
    def get_html(url):
        return get(url)

    print(777777777, res := get_html("https://www.163.com"))

    @run_executor_wraps
    def get_b_html(url):
        return get(url)

    print(888888888, res := get_b_html("https://cn.bing.com/"))

    @run_executor_wraps
    async def get_message(url):
        async with ClientSession() as session, session.get(url) as response:
            content = await response.content.read()
            return ACResponse(response, content, 0)

    print(999999999, res := get_message("https://httpbin.org/get"))

    @executor_wraps
    def normal_function():
        return "Hello, I'm a normal function!"

    async def main2():
        result2 = await normal_function()
        result = await add(8, 8)
        return result, result2

    print(101010101, asyncio.run(main2()))
