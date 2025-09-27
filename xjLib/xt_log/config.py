#!/usr/bin/env python3
"""
日志配置模块

包含日志相关的常量定义和配置设置
"""
from __future__ import annotations

import os

# 环境配置
IS_DEV: bool = os.getenv('ENV', 'dev').lower() == 'dev'
DEFAULT_LOG_LEVEL: int = 10  # DEBUG级别
LOG_FILE_ROTATION_SIZE: str = '16 MB'
LOG_FILE_RETENTION_DAYS: str = '30 days'

# 日志级别映射
LOG_LEVELS: dict[str, int] = {
    'TRACE': 5,
    'DEBUG': 10,
    'INFO': 20,
    'SUCCESS': 25,
    'WARNING': 30,
    'ERROR': 40,
    'CRITICAL': 50
}

# 日志图标
LOG_ICONS: dict[str, str] = {
    'TRACE': '\u270F\uFE0F',    # ✏️ - 跟踪日志
    'START': '\u25B6\uFE0F',    # ▶️ - 开始执行
    'STOP': '\u23F9\uFE0F',     # ⏹️ - 停止执行
    'DEBUG': '\U0001F41E',      # 🐞 - 调试信息
    'INFO': '\u2139\uFE0F',     # ℹ️ - 普通信息
    'SUCCESS': '\u2705\uFE0F',  # ✅ - 成功信息
    'WARNING': '\u26A0\uFE0F',  # ⚠️ - 警告信息
    'ERROR': '\u274C\uFE0F',    # ❌ - 错误信息
    'CRITICAL': '\u2620\uFE0F',  # ☠️ - 严重错误
    'DENIED': '\u26D4\uFE0F'  # ⛔ - 拒绝操作
}

# 日志格式
OPTIMIZED_FORMAT: str = (
    '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | '
    '<level>{level: <8}</level> <level>{level.icon}</level> | '
    '<magenta>{process: >6}</magenta>:<yellow>{thread: <6}</yellow> | '
    '<cyan>{extra[simplified_path]: <35}</cyan> | '
    '<level>{message}</level>'
)