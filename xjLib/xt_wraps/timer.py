# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-08-28 10:56:45
LastEditTime : 2025-09-02 13:32:43
FilePath     : /CODE/xjLib/xt_wraps/timer.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import asyncio
from functools import wraps
from time import perf_counter
from typing import Any, Callable

from .exception import handle_exception
from .log import create_basemsg, mylog


def timer_wraps(fn: Callable = None):
    """耗时记录装饰器 - 同时支持同步和异步函数"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = perf_counter()
            try:
                return func(*args, **kwargs)
            except Exception as err:
                return handle_exception(err, _basemsg, re_raise=True)
            finally:
                mylog.debug(
                    f"{_basemsg} | Timer-Consuming <{perf_counter() - start_time:.4f} s>"
                )

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = perf_counter()
            try:
                return await func(*args, **kwargs)
            except Exception as err:
                return handle_exception(err, _basemsg, re_raise=True)
            finally:
                mylog.debug(
                    f"{_basemsg} | Timer-Consuming <{perf_counter() - start_time:.4f} s>"
                )

        _basemsg = create_basemsg(func)
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator(fn) if fn else decorator


timer = timer_wraps
