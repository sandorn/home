# !/usr/bin/env python
"""
==============================================================
Description  : 确保变量已初始化装饰器
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-06 12:54:07
LastEditTime : 2025-09-14 13:37:42
FilePath     : /CODE/xjlib/xt_wraps/validate.py
Github       : https://github.com/sandorn/home
==============================================================
"""
from __future__ import annotations

from functools import lru_cache, wraps


def cache_wrapper(maxsize=128):
    """
    通用缓存装饰器，支持同步函数。
    :param maxsize: 缓存最大数量
    """
    def decorator(func):
        cached_func = lru_cache(maxsize=maxsize)(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            return cached_func(*args, **kwargs)
        return wrapper
    return decorator
