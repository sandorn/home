#!/usr/bin/env python3
"""
日志工具函数模块

包含路径处理、函数定位等工具函数
"""
from __future__ import annotations

import os
from collections.abc import Callable
from typing import Any


def get_function_location(func: Callable) -> dict[str, Any]:
    """
    获取函数的位置信息（文件、行号、函数名）
    
    Args:
        func: 要获取位置信息的函数
        
    Returns:
        dict: 包含文件路径、行号和函数名的字典
        
    Example:
        >>> location = get_function_location(some_function)
        >>> print(location)
        {'file': '/path/to/file.py', 'line': 10, 'function': 'some_function'}
    """
    try:
        # 获取原始函数（处理装饰器情况）
        original_func: Callable = func
        while hasattr(original_func, '__wrapped__'):
            original_func = original_func.__wrapped__
        
        code = original_func.__code__

        return {
            'file': code.co_filename,
            'line': code.co_firstlineno,
            'function': original_func.__name__
        }
    except Exception:
        return {
            'file': 'unknown',
            'line': 0,
            'function': getattr(func, '__name__', 'unknown')
        }


def simplify_file_path(file_path: str, line_no: int, func_name: str) -> str:
    """
    简化文件路径，提取有意义的模块信息
    
    Args:
        file_path: 原始文件路径
        line_no: 行号
        func_name: 函数名
        
    Returns:
        str: 简化后的路径格式（如：module.file:line@function）
        
    Example:
        >>> path = simplify_file_path('/project/src/module/file.py', 10, 'test_func')
        >>> print(path)  # 输出: module.file:10@test_func
    """
    if not file_path or file_path == 'unknown':
        return f'unknown:{line_no}@{func_name}'
    
    try:
        # 获取当前文件的目录路径，用于相对路径计算
        current_dir: str = os.path.dirname(os.path.abspath(__file__))
        project_root: str = os.path.dirname(os.path.dirname(current_dir))
        
        # 将路径转换为相对路径（相对于项目根目录）
        relative_path: str = (
            os.path.relpath(file_path, project_root) 
            if file_path.startswith(project_root) 
            else file_path
        )
        
        # 处理路径部分
        parts: list[str] = relative_path.split(os.sep)
        filename: str = parts[-1] if parts else 'unknown'
        
        # 构建模块路径（最多显示3级）
        if len(parts) > 1:
            # 取最后3级目录（如果存在）
            display_parts: list[str] = parts[-4:-1] if len(parts) >= 4 else parts[:-1]
            module_path: str = '.'.join(display_parts[-2:])  # 最多显示2级目录
            if module_path:
                return f'{module_path}.{filename}:{line_no}@{func_name}'
        
        return f'{filename}:{line_no}@{func_name}'
        
    except Exception:
        base_name: str = os.path.splitext(os.path.basename(file_path))[0]
        return f'{base_name}:{line_no}@{func_name}'


def format_record(record: dict[str, Any]) -> None:
    """
    格式化日志记录，处理callfrom参数
    
    这个函数作为loguru的record处理器，负责：
    1. 检查是否有callfrom参数
    2. 根据callfrom参数或默认信息生成简化路径
    3. 设置simplified_path到record的extra中
    4. 清理callfrom参数避免格式化冲突
    
    Args:
        record: loguru的日志记录字典
        
    Note:
        callfrom参数用于指定日志的调用来源，可以覆盖默认的调用栈信息
    """
    try:
        # 检查是否有callfrom参数
        callfrom: Callable | None = record['extra'].get('callfrom')
        if callfrom is not None:
            # 从callfrom函数获取位置信息
            location: dict[str, Any] = get_function_location(callfrom)
            file_path: str = location['file']
            line_no: int = location['line']
            func_name: str = location['function']
            
            # 生成简化路径
            simplified_path: str = simplify_file_path(file_path, line_no, func_name)
            record['extra']['simplified_path'] = simplified_path
            
            # 移除callfrom参数，避免loguru尝试格式化它
            if 'callfrom' in record['extra']:
                del record['extra']['callfrom']
        else:
            # 使用默认的调用位置信息
            file_path: str = (
                record['file'].path 
                if hasattr(record['file'], 'path') 
                else str(record['file'])
            )
            line_no: int = record['line']
            func_name: str = record['function']
            simplified_path: str = simplify_file_path(file_path, line_no, func_name)
            record['extra']['simplified_path'] = simplified_path
    except Exception:
        record['extra']['simplified_path'] = 'unknown:0@unknown'