# !/usr/bin/env python3
"""
==============================================================
Description  : 工具函数模块初始化
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-11-05 10:45:00
LastEditTime : 2024-11-05 10:45:00
FilePath     : d:/CODE/xjlib/xt_sqlorm/utils/__init__.py
Github       : https://github.com/sandorn/home

本模块包含各种ORM相关的工具函数，包括数据验证、类型转换、
字符串处理等实用功能，为SQLORM提供辅助支持。
==============================================================
"""

from __future__ import annotations

# 导出工具函数
from .validators import ValidationError, validate_datetime, validate_dict, validate_email, validate_enum, validate_json, validate_length, validate_phone, validate_range, validate_required

__all__ = [
    'ValidationError',
    'validate_datetime',
    'validate_dict',
    'validate_email',
    'validate_enum',
    'validate_json',
    'validate_length',
    'validate_phone',
    'validate_range',
    'validate_required',
]

# 版本信息
__version__ = '1.0.0'
__author__ = 'sandorn'
__email__ = 'sandorn@live.cn'