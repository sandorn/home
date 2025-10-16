# !/usr/bin/env python3
"""
==============================================================
Description  : 模型模块初始化
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-09-22 10:55:00
LastEditTime : 2024-11-05 10:45:00
FilePath     : /code/xt_sqlorm/models/__init__.py
Github       : https://github.com/sandorn/home

本模块导出所有ORM相关的核心组件，包括基础模型、混入类、自定义类型等。
==============================================================
"""

# 导出模型类
from __future__ import annotations

from xt_sqlorm.models.base import Base, BaseModel, ModelExt
from xt_sqlorm.models.mixins import IdMixin, SoftDeleteMixin, TimestampMixin, UTCTimeMixin, VersionedMixin
from xt_sqlorm.models.types import EnumType, JsonEncodedDict, UTCDateTime

__all__ = [
    'Base',
    'BaseModel',
    'EnumType',
    'IdMixin',
    'JsonEncodedDict',
    'ModelExt',
    'SoftDeleteMixin',
    'TimestampMixin',
    'UTCDateTime',
    'UTCTimeMixin',
    'VersionedMixin',
]

# 版本信息
__version__ = '1.0.0'
__author__ = 'sandorn'
__email__ = 'sandorn@live.cn'