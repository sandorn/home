# !/usr/bin/env python3
"""
==============================================================
Description  : 混入类模块初始化
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-11-05 10:45:00
LastEditTime : 2024-11-05 10:45:00
FilePath     : d:/CODE/xjlib/xt_sqlorm/models/mixins/__init__.py
Github       : https://github.com/sandorn/home

本模块包含各种ORM混入类，用于为模型添加特定功能
==============================================================
"""

from __future__ import annotations

# 导出混入类
from .id_mixin import IdMixin
from .softdelete_mixin import SoftDeleteMixin
from .timestamp_mixin import TimestampMixin
from .utctime_mixin import UTCTimeMixin
from .versioned_mixin import VersionedMixin

__all__ = [
    'IdMixin',
    'SoftDeleteMixin',
    'TimestampMixin',
    'UTCTimeMixin',
    'VersionedMixin',
]

# 版本信息
__version__ = '1.0.0'
__author__ = 'sandorn'
__email__ = 'sandorn@live.cn'