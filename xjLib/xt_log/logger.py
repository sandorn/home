#!/usr/bin/env python3
"""
日志类模块

包含主要的日志类实现
"""
from __future__ import annotations

import os
import sys
from datetime import datetime
from typing import Any

from loguru import logger
from xt_wraps.singleton import SingletonMixin

from .config import DEFAULT_LOG_LEVEL, IS_DEV, LOG_FILE_RETENTION_DAYS, LOG_FILE_ROTATION_SIZE, OPTIMIZED_FORMAT
from .utils import format_record


class LogCls(SingletonMixin):
    """
    简化版日志配置类 - 利用loguru的record对象获取调用信息
    
    特性：
    - 单例模式，确保全局只有一个日志实例
    - 支持文件和控制台双输出
    - 自动处理日志文件轮转和保留
    - 支持callfrom参数扩展功能
    """
    
    def __init__(self, level: int = DEFAULT_LOG_LEVEL, serialize: bool = False) -> None:
        """
        初始化日志配置
        
        Args:
            level: 日志级别，默认为DEBUG级别
            serialize: 是否序列化日志，默认为False
        """
        self.loger = logger
        self.loger.remove()
        
        # 应用格式处理
        self.loger = self.loger.patch(format_record)
        
        # 设置工作目录和日志文件
        workspace_root: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logs_dir: str = os.path.join(workspace_root, 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        log_file: str = os.path.join(logs_dir, f'xt_{datetime.now().strftime("%Y%m%d")}.log')
        
        # 保存配置信息
        self.current_level = level
        self.log_file = log_file
        self._file_id = None
        self._console_id = None
        
        # 文件日志配置
        self._file_id = self.loger.add(
            log_file,
            rotation=LOG_FILE_ROTATION_SIZE,
            retention=LOG_FILE_RETENTION_DAYS,
            level=level,
            encoding='utf-8',
            format=OPTIMIZED_FORMAT,
            serialize=serialize,
            backtrace=True,
            diagnose=True,
            catch=True,
        )

        # 控制台日志配置（仅开发环境）
        if IS_DEV:
            self._console_id = self.loger.add(
                sys.stderr, 
                level=level, 
                format=OPTIMIZED_FORMAT,
                serialize=serialize,
                backtrace=True,
                diagnose=True,
                catch=True,
            )
            
    def __call__(self, *args: Any, **kwargs: Any) -> list[None]:
        """
        支持实例直接调用，将多个参数作为多条日志记录
        
        Args:
            *args: 要记录的参数
            **kwargs: 传递给loguru的额外参数
            
        Returns:
            list[None]: 每条日志的记录结果列表
        """
        return [self.loger.info(arg, **kwargs) for arg in args]

    def __getattr__(self, attr: str) -> Any:
        """
        动态获取属性，支持直接调用loguru的方法
        
        Args:
            attr: 属性名
            
        Returns:
            Any: loguru的对应方法或默认日志函数
        """
        try:
            return getattr(self.loger, attr)
        except AttributeError:
            # 如果属性不存在，返回一个默认的日志函数
            def fallback_log(*arg: Any, **kwargs: Any) -> None:
                """默认的日志函数，用于处理不存在的日志方法"""
                self.loger.info(*arg, **kwargs)
            return fallback_log
            
    def set_level(self, level: int | str) -> None:
        """
        动态设置日志级别
        
        Args:
            level: 日志级别，可以是整数或字符串
            
        Example:
            >>> mylog.set_level("DEBUG")  # 设置为DEBUG级别
            >>> mylog.set_level(30)       # 设置为WARNING级别
        """
        from .config import LOG_LEVELS
        
        # 转换字符串级别为整数
        if isinstance(level, str):
            level = LOG_LEVELS.get(level.upper(), DEFAULT_LOG_LEVEL)
            
        self.current_level = level
        
        # 更新所有日志处理器的级别
        if self._file_id is not None:
            self.loger.configure(self._file_id, level=level)
        if self._console_id is not None:
            self.loger.configure(self._console_id, level=level)