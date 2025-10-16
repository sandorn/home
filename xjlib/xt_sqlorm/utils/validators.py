#!/usr/bin/env python3
"""
==============================================================
Description  : 数据验证工具模块
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-11-05 10:45:00
LastEditTime : 2024-11-05 10:45:00
FilePath     : d:/CODE/xjlib/xt_sqlorm/utils/validators.py
Github       : https://github.com/sandorn/home

本模块提供各种数据验证工具函数，用于验证数据库字段的合法性，
包括邮箱、手机号、日期时间、JSON、枚举值等常见数据类型的验证。
==============================================================
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from enum import Enum
from typing import Any


class ValidationError(Exception):
    """验证错误异常类

    当数据验证失败时抛出，包含详细的错误信息和验证失败的字段信息。
    """

    def __init__(self, message: str, field: str | None = None, value: Any = None) -> None:
        """初始化验证错误

        Args:
            message: 错误消息
            field: 验证失败的字段名（可选）
            value: 验证失败的值（可选）
        """
        self.message = message
        self.field = field
        self.value = value
        super().__init__(message)

    def __str__(self) -> str:
        """格式化错误信息"""
        if self.field:
            return f"字段 '{self.field}' 验证失败: {self.message} (值: {self.value})"
        return f'验证失败: {self.message}'


def validate_dict(value: Any, field: str | None = None) -> Any:
    """验证JsonEncodedDict类型

    Args:
        value: 要验证的值
        field: 字段名（用于错误消息）

    Returns:
        Any: 验证通过的值

    Raises:
        ValidationError: 如果值不是JsonEncodedDict类型
    """
    if value is not None and not isinstance(value, dict):
        raise ValidationError('值不是字典类型', field, value)
    return value


def validate_email(email: str, field: str | None = None) -> str:
    """验证邮箱地址格式

    Args:
        email: 要验证的邮箱地址
        field: 字段名（用于错误消息）

    Returns:
        str: 验证通过的邮箱地址

    Raises:
        ValidationError: 如果邮箱格式无效
    """
    if not email:
        raise ValidationError('邮箱地址不能为空', field, email)

    # 简单的邮箱格式验证
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError('邮箱格式无效', field, email)

    return email


def validate_phone(phone: str, field: str | None = None) -> str:
    """验证手机号格式（支持中国大陆手机号）

    Args:
        phone: 要验证的手机号
        field: 字段名（用于错误消息）

    Returns:
        str: 验证通过的手机号

    Raises:
        ValidationError: 如果手机号格式无效
    """
    if not phone:
        raise ValidationError('手机号不能为空', field, phone)

    # 中国大陆手机号验证（1开头，11位数字）
    pattern = r'^1[3-9]\d{9}$'
    if not re.match(pattern, phone):
        raise ValidationError('手机号格式无效', field, phone)

    return phone


def validate_datetime(dt_str: str, field: str | None = None) -> datetime:
    """验证日期时间字符串并转换为datetime对象

    Args:
        dt_str: 日期时间字符串
        field: 字段名（用于错误消息）

    Returns:
        datetime: 解析后的datetime对象

    Raises:
        ValidationError: 如果日期时间格式无效
    """
    if not dt_str:
        raise ValidationError('日期时间不能为空', field, dt_str)

    try:
        # 尝试解析ISO格式日期时间
        return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    except (ValueError, TypeError) as e:
        raise ValidationError('日期时间格式无效', field, dt_str) from e


def validate_json(json_str: str, field: str | None = None) -> dict | list:
    """验证JSON字符串并解析为Python对象

    Args:
        json_str: JSON字符串
        field: 字段名（用于错误消息）

    Returns:
        dict | list: 解析后的Python对象

    Raises:
        ValidationError: 如果JSON格式无效
    """
    if not json_str:
        raise ValidationError('JSON字符串不能为空', field, json_str)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValidationError('JSON格式无效', field, json_str) from e


def validate_enum(value: Any, enum_class: type[Enum], field: str | None = None) -> Enum:
    """验证值是否为有效的枚举值

    Args:
        value: 要验证的值
        enum_class: 枚举类
        field: 字段名（用于错误消息）

    Returns:
        Enum: 验证通过的枚举值

    Raises:
        ValidationError: 如果值不是有效的枚举值
    """
    if value is None:
        raise ValidationError('枚举值不能为空', field, value)

    try:
        if isinstance(value, str):
            return enum_class(value)
        if isinstance(value, int):
            # 尝试通过值查找枚举
            for enum_member in enum_class:
                if enum_member.value == value:
                    return enum_member
            raise ValueError
        return enum_class(value)
    except (ValueError, TypeError) as e:
        valid_values = [e.value for e in enum_class]
        raise ValidationError(f'无效的枚举值，有效值为: {valid_values}', field, value) from e


def validate_required(value: Any, field: str | None = None) -> Any:
    """验证值是否为非空

    Args:
        value: 要验证的值
        field: 字段名（用于错误消息）

    Returns:
        Any: 验证通过的值

    Raises:
        ValidationError: 如果值为空
    """
    if value is None or value == '':
        raise ValidationError('该字段为必填项', field, value)
    return value


def validate_length(value: str, min_len: int | None = None, max_len: int | None = None, field: str | None = None) -> str:
    """验证字符串长度

    Args:
        value: 要验证的字符串
        min_len: 最小长度（可选）
        max_len: 最大长度（可选）
        field: 字段名（用于错误消息）

    Returns:
        str: 验证通过的字符串

    Raises:
        ValidationError: 如果长度不符合要求
    """
    if value is None:
        raise ValidationError('字符串不能为空', field, value)

    length = len(value)
    
    if min_len is not None and length < min_len:
        raise ValidationError(f'长度不能小于 {min_len} 个字符', field, value)
    
    if max_len is not None and length > max_len:
        raise ValidationError(f'长度不能超过 {max_len} 个字符', field, value)
    
    return value


def validate_range(value: int | float, min_val: int | float | None = None, max_val: int | float | None = None, field: str | None = None) -> int | float:
    """验证数值范围

    Args:
        value: 要验证的数值
        min_val: 最小值（可选）
        max_val: 最大值（可选）
        field: 字段名（用于错误消息）

    Returns:
        int | float: 验证通过的数值

    Raises:
        ValidationError: 如果数值不在指定范围内
    """
    if value is None:
        raise ValidationError('数值不能为空', field, value)

    if min_val is not None and value < min_val:
        raise ValidationError(f'值不能小于 {min_val}', field, value)
    
    if max_val is not None and value > max_val:
        raise ValidationError(f'值不能超过 {max_val}', field, value)
    
    return value


# 导出所有验证函数
__all__ = [
    'ValidationError',
    'validate_datetime',
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