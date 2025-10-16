#!/usr/bin/env python3
"""
==============================================================
Description  : UTC时间工具混入类
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-11-05 10:45:00
LastEditTime : 2024-11-05 10:45:00
FilePath     : d:/CODE/xjlib/xt_sqlorm/models/mixins/utctime_mixin.py
Github       : https://github.com/sandorn/home

提供时区感知的时间处理工具方法，确保所有时间操作都基于UTC时区，避免时区问题。
主要用于数据库模型中统一时间处理逻辑，确保跨时区应用的数据一致性。
==============================================================
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta


class UTCTimeMixin:
    """UTC时间工具混入类

    提供时区感知的时间处理工具方法，确保所有时间操作都基于UTC时区，避免时区问题。
    主要用于数据库模型中统一时间处理逻辑，确保跨时区应用的数据一致性。
    """

    @staticmethod
    def utc_now() -> datetime:
        """获取当前UTC时间"""
        return datetime.now(UTC)

    @staticmethod
    def utc_today() -> datetime:
        """获取UTC当天的开始时间"""
        now = datetime.now(UTC)
        return datetime(now.year, now.month, now.day, tzinfo=UTC)

    @staticmethod
    def days_ago(days: int) -> datetime:
        """获取days天前的UTC时间"""
        return datetime.now(UTC) - timedelta(days=days)

    @staticmethod
    def hours_ago(hours: int) -> datetime:
        """获取hours小时前的UTC时间"""
        return datetime.now(UTC) - timedelta(hours=hours)