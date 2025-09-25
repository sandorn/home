#!/usr/bin/env python3
"""
==============================================================
Description  : ID字段混入类
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-11-05 10:45:00
LastEditTime : 2024-11-05 10:45:00
FilePath     : d:/CODE/xjlib/xt_sqlorm/models/mixins/id_mixin.py
Github       : https://github.com/sandorn/home

提供数据库表的主键ID字段定义，简化主键字段的重复定义。
通过混入方式使用，可以与其他混入类组合，构建完整的数据模型。
==============================================================
"""

from __future__ import annotations

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column


class IdMixin:
    """ID字段混入类

    提供数据库表的主键ID字段定义，简化主键字段的重复定义。
    通过混入方式使用，可以与其他混入类组合，构建完整的数据模型。
    """

    ID: Mapped[int] = mapped_column(Integer, primary_key=True)