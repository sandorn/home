# !/usr/bin/env python
"""
==============================================================
Description  : 函数包装器工具集 - 提供常用的函数装饰器和包装器功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-08-28 10:53:57
LastEditTime : 2025-09-06 13:00:00
FilePath     : /CODE/xjLib/xt_wraps/__init__.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能：
- 统一的装饰器接口，简化同步/异步函数的装饰器实现
- 日志记录装饰器，提供函数调用的详细日志
- 函数执行计时器，监控同步/异步函数的执行时间
- 自动重试机制，优化网络请求和不稳定操作的成功率
- 线程池执行器包装器，简化异步执行同步函数
- 单例模式实现，提供多种单例装饰器和混入类

主要特性：
- 统一的API设计，简化装饰器使用体验
- 自动识别并适配同步和异步函数
- 完整的异常捕获和处理机制
- 与项目其他模块保持一致的文档风格
- 支持多种组合使用场景
==============================================================
"""

from .core import decorate_sync_async
from .exception import handle_exception
from .executor import (
    executor_wraps,
    future_wraps,
    future_wraps_result,
    run_executor_wraps,
)
from .log import create_basemsg, log_wraps, mylog
from .retry import retry_wraps
from .singleton import SingletonMeta, SingletonMixin, SingletonWraps, singleton
from .timer import timer, timer_wraps
from .validate import validate_custom, validate_params, validate_ranges, validate_types

# 模块级别文档说明
"""函数包装器工具集 - 提供常用的函数装饰器和包装器功能

使用示例:
    # 导入所有装饰器
    from xjLib.xt_wraps import *
    
    # 使用日志装饰器
    @log_wraps
    def my_function():
        return "执行结果"
    
    # 使用重试装饰器
    @retry_wraps(max_attempts=3)
    def unstable_network_call():
        # 网络请求代码
        pass
    
    # 组合使用装饰器
    @log_wraps
    @timer_wraps
    @retry_wraps()
    async def complex_operation():
        # 复杂异步操作
        await asyncio.sleep(1)
        return "完成"

注意事项:
    - 装饰器可以任意组合使用，但建议按逻辑顺序排列
    - 所有装饰器都同时支持同步和异步函数
    - 单例装饰器可以确保目标类只有一个实例
"""

__all__ = [
    # 基础工具
    "decorate_sync_async",
    "handle_exception",
    "create_basemsg",
    "mylog",
    # 日志相关
    "log_wraps",
    # 计时相关
    "timer",
    "timer_wraps",
    # 重试相关
    "retry_wraps",
    # 验证相关
    "validate_params",
    "validate_types",
    "validate_ranges",
    "validate_custom",
    # 执行器相关
    "executor_wraps",
    "future_wraps",
    "future_wraps_result",
    "run_executor_wraps",
    # 单例相关
    "SingletonMeta",
    "SingletonMixin",
    "SingletonWraps",
    "singleton",
]
