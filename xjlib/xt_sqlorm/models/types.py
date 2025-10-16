#!/usr/bin/env python3
"""
==============================================================
Description  : 自定义类型模块
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-11-05 10:45:00
LastEditTime : 2024-11-05 10:45:00
FilePath     : d:/CODE/xjlib/xt_sqlorm/models/types.py
Github       : https://github.com/sandorn/home

本模块提供SQLAlchemy ORM的自定义类型定义，包括JSON编码字典、枚举类型、
时间戳类型等，用于增强数据库字段的功能和灵活性。
==============================================================
"""

from __future__ import annotations

import json
from enum import Enum
from typing import Any

from sqlalchemy import TEXT
from sqlalchemy.types import TypeDecorator


class JsonEncodedDict(TypeDecorator):
    """自定义的 SQLAlchemy 类型
    用于将 Python 字典自动序列化为 JSON 字符串存储在数据库中
    在数据库和Python代码之间自动进行JSON序列化和反序列化
    适合存储结构可能变化、不需要复杂查询或需要高度灵活性的数据
    基于TEXT类型实现，支持非ASCII字符的正确处理

    preferences = Column(JsonEncodedDict)  # 存储用户偏好设置，如 {'theme': 'dark', 'language': 'zh'}
    """

    impl = TEXT

    def process_bind_param(self, value: Any, dialect: Any) -> str | None:
        """在将值存储到数据库前，将Python对象转换为JSON字符串

        Args:
            value: 要存储的Python对象(通常是字典或列表)
            dialect: SQLAlchemy方言对象(未使用)

        Returns:
            str | None: 序列化后的JSON字符串，None值保持不变
        """
        return json.dumps(value, ensure_ascii=False) if value is not None else None

    def process_result_value(self, value: str | None, dialect: Any) -> dict | None:
        """从数据库检索值时，将JSON字符串转换回Python对象

        Args:
            value: 数据库中的JSON字符串
            dialect: SQLAlchemy方言对象(未使用)

        Returns:
            dict | None: 反序列化后的Python字典，None值返回空字典
        """
        return json.loads(value) if value is not None else {}


class EnumType(TypeDecorator):
    """枚举类型装饰器

    将Python枚举类型自动转换为数据库中的字符串存储，
    并在查询时自动转换回枚举类型，简化枚举字段的使用。

    status = Column(EnumType(StatusEnum))  # 存储枚举的字符串表示
    """

    impl = TEXT

    def __init__(self, enum_class: type[Enum], *args: Any, **kwargs: Any) -> None:
        """初始化枚举类型装饰器

        Args:
            enum_class: 要包装的枚举类
            *args: 传递给父类的参数
            **kwargs: 传递给父类的关键字参数
        """
        super().__init__(*args, **kwargs)
        self.enum_class = enum_class

    def process_bind_param(self, value: Enum | None, dialect: Any) -> str | None:
        """在存储到数据库前，将枚举转换为字符串

        Args:
            value: 枚举值
            dialect: SQLAlchemy方言对象(未使用)

        Returns:
            str | None: 枚举的字符串表示，None值保持不变
        """
        if value is None:
            return None
        return value.value if hasattr(value, 'value') else str(value)

    def process_result_value(self, value: str | None, dialect: Any) -> Enum | None:
        """从数据库检索时，将字符串转换回枚举

        Args:
            value: 数据库中的字符串
            dialect: SQLAlchemy方言对象(未使用)

        Returns:
            Enum | None: 对应的枚举值，None值返回None
        """
        if value is None:
            return None
        try:
            return self.enum_class(value)
        except ValueError:
            # 处理枚举值不存在的情况
            return None


class UTCDateTime(TypeDecorator):
    """UTC时间类型装饰器

    确保所有时间戳都以UTC时区存储和检索，避免时区转换问题。
    自动处理时区转换，确保时间数据的一致性。

    created_at = Column(UTCDateTime)  # 自动确保UTC时区
    """

    impl = TEXT

    def process_bind_param(self, value: Any, dialect: Any) -> str | None:
        """在存储到数据库前，确保时间为UTC格式字符串

        Args:
            value: 时间对象
            dialect: SQLAlchemy方言对象(未使用)

        Returns:
            str | None: UTC格式的时间字符串，None值保持不变
        """
        if value is None:
            return None
        # 转换为UTC时间字符串
        if hasattr(value, 'isoformat'):
            return value.isoformat()
        return str(value)

    def process_result_value(self, value: str | None, dialect: Any) -> Any | None:
        """从数据库检索时，解析UTC时间字符串

        Args:
            value: 数据库中的UTC时间字符串
            dialect: SQLAlchemy方言对象(未使用)

        Returns:
            Any | None: 解析后的时间对象，None值返回None
        """
        if value is None:
            return None
        # 这里可以根据需要返回datetime对象或其他时间格式
        return value


# 导出所有类型
__all__ = [
    'EnumType',
    'JsonEncodedDict',
    'UTCDateTime',
]

# 版本信息
__version__ = '1.0.0'
__author__ = 'sandorn'
__email__ = 'sandorn@live.cn'