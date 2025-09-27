#!/usr/bin/env python3
"""
xt_log - 基于loguru的日志库

特性：
- 单例模式，确保全局只有一个日志实例
- 支持文件和控制台双输出
- 自动处理日志文件轮转和保留
- 支持callfrom参数扩展功能
- 模块化设计，功能分离清晰
"""
from __future__ import annotations

from .logger import LogCls

# 创建全局日志实例
mylog = LogCls()

# 导出主要类和函数
__all__ = ['LogCls', 'mylog']

