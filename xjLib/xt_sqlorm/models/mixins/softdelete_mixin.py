#!/usr/bin/env python3
"""
==============================================================
Description  : 软删除混入类
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-11-05 10:45:00
LastEditTime : 2024-11-05 10:45:00
FilePath     : d:/CODE/xjlib/xt_sqlorm/models/mixins/softdelete_mixin.py
Github       : https://github.com/sandorn/home

提供逻辑删除功能，通过标记删除时间而非物理删除记录，实现数据的可恢复性。
包含软删除、恢复、查询活跃/已删除记录等完整功能，并支持永久清理过期删除记录。
==============================================================
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import DateTime, delete, select
from sqlalchemy.orm import Mapped, mapped_column


class SoftDeleteMixin:
    """软删除混入类 - 时区感知版本

    提供逻辑删除功能，通过标记删除时间而非物理删除记录，实现数据的可恢复性。
    包含软删除、恢复、查询活跃/已删除记录等完整功能，并支持永久清理过期删除记录。
    """

    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment='软删除时间戳（UTC时区）')

    def soft_delete(self) -> None:
        """执行软删除操作，使用UTC时间标记删除

        将记录标记为已删除状态，但不从数据库中物理删除，便于数据恢复和历史查询。
        自动使用当前UTC时间作为删除时间戳。
        """
        self.deleted_at = datetime.now(UTC)

    def restore(self) -> None:
        """恢复已软删除的记录

        清除删除时间戳，将记录恢复为活跃状态，适用于误删除等场景。
        """
        self.deleted_at = None

    @property
    def is_deleted(self) -> bool:
        """检查记录是否已被软删除

        Returns:
            bool: 如果记录已被软删除则返回True，否则返回False
        """
        return self.deleted_at is not None

    @property
    def deletion_age_days(self) -> float | None:
        """获取记录被删除的天数（如未删除则返回None）

        Returns:
            float | None: 记录被删除的天数，未删除时返回None
        """
        if not self.deleted_at:
            return None
        return (datetime.now(UTC) - self.deleted_at).total_seconds() / 86400

    # 类方法查询
    @classmethod
    def get_active(cls, session: Any) -> Any:
        """获取所有活跃（未删除）的记录

        Args:
            session: SQLAlchemy会话对象

        Returns:
            sqlalchemy.ScalarResult: 活跃记录的结果集
        """
        return session.scalars(select(cls).where(cls.deleted_at.is_(None)))

    @classmethod
    def get_deleted(cls, session: Any) -> Any:
        """获取所有已软删除的记录

        Args:
            session: SQLAlchemy会话对象

        Returns:
            sqlalchemy.ScalarResult: 已删除记录的结果集
        """
        return session.scalars(select(cls).where(cls.deleted_at.is_not(None)))

    @classmethod
    def get_all_including_deleted(cls, session: Any) -> Any:
        """获取所有记录（包括活跃和已删除的记录）

        Args:
            session: SQLAlchemy会话对象

        Returns:
            sqlalchemy.ScalarResult: 所有记录的结果集
        """
        return session.scalars(select(cls))

    @classmethod
    def permanent_delete_old_records(cls, session: Any, days: int = 30) -> int:
        """永久删除超过指定天数的软删除记录

        用于清理历史软删除数据，释放数据库空间。默认清理30天前的删除记录。

        Args:
            session: SQLAlchemy会话对象
            days: 保留天数，超过该天数的软删除记录将被永久删除，默认为30天

        Returns:
            int: 永久删除的记录数量
        """

        cutoff_date = datetime.now(UTC) - timedelta(days=days)

        result = session.execute(delete(cls).where(cls.deleted_at.is_not(None), cls.deleted_at < cutoff_date))
        session.commit()
        return result.rowcount