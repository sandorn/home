# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-08-28 10:53:57
LastEditTime : 2025-08-28 10:54:39
FilePath     : /CODE/xjLib/xt_decorators/__init__.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from xt_wraps.core import decorate_sync_async, func_sync_async
from xt_wraps.exception import catch_deco, catch_wraps
from xt_wraps.log import LogCls, create_basemsg, log_wraps
from xt_wraps.retry import retry_deco, retry_wraps
from xt_wraps.timer import TimeContextManager, timer_deco, timer_wraps

__all__ = [
    "retry_wraps",
    "retry_deco",
    "log_wraps",
    "log_deco",
    "LogCls",
    "create_basemsg",
    "timer_wraps",
    "timer_deco",
    "TimeContextManager",
    "catch_wraps",
    "catch_deco",
    "decorate_sync_async",
    "func_sync_async",
]


if __name__ == "__main__":
    from functools import wraps

    def with_retry_logging(max_attempts=3):
        """自定义装饰器组合：重试+日志+异常处理"""

        def decorator(func):
            @wraps(func)
            @log_wraps()
            @timer_wraps()
            def wrapper333(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper333

        return decorator


    # 使用自定义组合装饰器
    @with_retry_logging(max_attempts=2)
    def my_function(x):
        if x < 0:
            raise ValueError("值太小")
        return x ** 2
    
    my_function(3)

