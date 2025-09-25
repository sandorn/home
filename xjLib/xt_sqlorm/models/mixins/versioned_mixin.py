#!/usr/bin/env python3
"""
==============================================================
Description  : 版本控制混入类
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-11-05 10:45:00
LastEditTime : 2024-11-05 10:45:00
FilePath     : d:/CODE/xjlib/xt_sqlorm/models/mixins/versioned_mixin.py
Github       : https://github.com/sandorn/home

提供乐观锁功能，防止并发更新冲突。通过版本号机制，确保在多用户环境下数据的一致性。
当多个用户同时修改同一条记录时，只有第一个提交的修改会成功，后续修改将失败。
==============================================================
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column


class VersionedMixin:
    """版本控制混入类

    提供乐观锁功能，防止并发更新冲突。通过版本号机制，确保在多用户环境下数据的一致性。
    当多个用户同时修改同一条记录时，只有第一个提交的修改会成功，后续修改将失败。
    """

    version_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    @property
    def __mapper_args__(self) -> dict[str, Any]:
        """动态返回版本控制配置

        配置SQLAlchemy使用version_id_col作为乐观锁的版本控制列，并禁用自动版本生成
        以支持手动控制版本号的增量逻辑。

        Returns:
            dict[str, Any]: 包含版本控制配置的字典
        """
        return {
            'version_id_col': self.__table__.c.version_id,
            'version_id_generator': False,  # 手动管理版本号
        }

    def increment_version(self) -> None:
        """手动增加版本号

        在更新记录前调用此方法，确保版本号正确递增，维持乐观锁的有效性。
        """
        self.version_id += 1