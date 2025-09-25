#!/usr/bin/env python3
"""
==============================================================
Description  : 时间戳字段混入类
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-11-05 10:45:00
LastEditTime : 2024-11-05 10:45:00
FilePath     : d:/CODE/xjlib/xt_sqlorm/models/mixins/timestamp_mixin.py
Github       : https://github.com/sandorn/home

提供创建时间和更新时间字段定义，确保所有时间戳都使用UTC时区。
通过数据库默认值和自动更新机制，维护记录的时间信息，无需手动设置。
==============================================================
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, text
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    """时间戳字段混入类

    提供创建时间和更新时间字段定义，确保所有时间戳都使用UTC时区。
    通过数据库默认值和自动更新机制，维护记录的时间信息，无需手动设置。
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text('UTC_TIMESTAMP()'),  # MySQL兼容的UTC时间戳
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text('UTC_TIMESTAMP()'),
        onupdate=text('UTC_TIMESTAMP()'),  # MySQL兼容的UTC时间戳
    )