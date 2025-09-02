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
from typing import Any, Callable, Optional

# 默认线程池执行器
default_executor = ThreadPoolExecutor(max_workers=10, thread_name_prefix="XtExecutor")

def executor_wraps(
    fn: Optional[Callable[..., Any]] = None, background: bool = False
) -> Callable[..., Any]:
    """
    异步执行器装饰器 - 包装同步和异步函数，支持后台执行

    Args:
        fn (Optional[Callable[..., Any]]): 要装饰的函数（同步或异步）
        background (bool): 是否作为后台任务执行，默认为 False

    Returns:
        Callable[..., asyncio.Future[Any]]: 装饰后的异步函数
    """

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # 处理异步函数
            if background:
                # 后台执行异步函数，不等待结果
                return asyncio.create_task(func(*args, **kwargs))
            else:
                # 正常等待异步函数执行完成
                return await func(*args, **kwargs)

        @wraps(func)
        async def sync_wrapper(*args, **kwargs):
            # 处理同步函数，在线程池中执行
            loop = asyncio.get_event_loop()
            task_func = partial(func, *args, **kwargs)

            if background:
                # 后台执行同步函数，直接返回 Future 对象
                # loop.run_in_executor 返回的是 Future，不需要包装成 Task
                return loop.run_in_executor(default_executor, task_func)
            else:
                # 正常等待同步函数执行完成
                return await loop.run_in_executor(default_executor, task_func)

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator(fn) if fn else decorator

def run_executor_wraps(func: Optional[Callable[..., Any]] = None) -> Callable[..., Any]:
    @wraps(func)
    def decorator(*args, **kwargs):
        async def main(*args, **kwargs):
            return func(*args, **kwargs)

        if asyncio.iscoroutinefunction(func):
            return asyncio.run(func(*args, **kwargs))
        return asyncio.run(main(*args, **kwargs))

    return decorator

def future_wraps(fn : Callable[..., Any] = None) -> Callable[..., asyncio.Future[Any]]:
    """
    装饰器，将同步函数包装成返回Future对象的异步函数。

    Args:
        func (Callable): 要装饰的同步函数。

    Returns:
        Callable: 装饰后的异步函数，返回Future对象。
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., asyncio.Future[Any]]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            future = asyncio.Future()
            try:
                result = func(*args, **kwargs)
                future.set_result(result)
            except Exception as e:
                future.set_exception(e)
            return future

        return wrapper
    return decorator(fn) if fn else decorator

async def future_wraps_result(in_future: asyncio.Future) -> Any:
    done_future =  await in_future
    return done_future.result()


if __name__ == "__main__":
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
        return a * b
    
    async def main():
        fn1 = executor_wraps(get_a_html)
        res = await fn1("https://www.baidu.com")
        print("1111111111|Result length:", len(res), res.status, res.url)
        # 后台执行，返回Future对象（对于同步函数）
        fn2 = executor_wraps(get_a_html_bg,background=True)
        future = await fn2("https://www.baidu.com")
        # 等待后台任务完成
        bg_res = await future
        print("222222222|Background result length:", len(bg_res), bg_res.status, bg_res.url)
        add_res = await add(3, 5)
        print("333333333|Add result:", add_res, add_res.result())

    # 运行测试
    asyncio.run(main())
    print(
        444444444,
        fn4 := run_executor_wraps(get_a_html_bg),
        fn4("https://www.126.com"),
    )

    print(555555555, res := asyncio.run(add(5, 5)), res.result())

    print(666666666, res := asyncio.run(future_wraps_result(add(6, 6))))

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

    async def main():
        result = await normal_function()
        return result

    print(101010101, asyncio.run(main()))

