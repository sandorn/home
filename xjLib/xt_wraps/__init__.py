# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-08-28 10:53:57
LastEditTime : 2025-09-14 19:59:20
FilePath     : /CODE/xjlib/xt_wraps/__init__.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能:
- 统一的装饰器接口,简化同步/异步函数的装饰器实现
- 日志记录装饰器,提供函数调用的详细日志
- 函数执行计时器,监控同步/异步函数的执行时间
- 自动重试机制,优化网络请求和不稳定操作的成功率
- 线程池执行器包装器,简化异步执行同步函数
- 单例模式实现,提供多种单例装饰器和混入类

主要特性:
- 统一的API设计,简化装饰器使用体验
- 自动识别并适配同步和异步函数
- 完整的异常捕获和处理机制
- 与项目其他模块保持一致的文档风格
- 支持多种组合使用场景
==============================================================
"""

from __future__ import annotations

from .core import decorate_sync_async
from .exception import handle_exception
from .executor import (
    executor_wraps,
    future_wraps,
    future_wraps_result,
    run_executor_wraps,
)
from .log import LogCls, create_basemsg, log_wraps, mylog
from .retry import TRETRY, retry_wraps
from .singleton import SingletonMeta, SingletonMixin, SingletonWraps, singleton
from .timer import timer, timer_wraps
from .validate import TypedProperty, ensure_initialized, readonly, typeassert, typed_property

__all__ = [
    'TRETRY',
    'LogCls',
    'SingletonMeta',
    'SingletonMixin',
    'SingletonWraps',
    'TypedProperty',
    'create_basemsg',
    'decorate_sync_async',
    'ensure_initialized',
    'executor_wraps',
    'future_wraps',
    'future_wraps_result',
    'handle_exception',
    'log_wraps',
    'mylog',
    'readonly',
    'retry_wraps',
    'run_executor_wraps',
    'singleton',
    'timer',
    'timer_wraps',
    'typeassert',
    'typed_property',
]
