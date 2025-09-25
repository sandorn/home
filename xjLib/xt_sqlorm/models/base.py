#!/usr/bin/env python3
"""
==============================================================
Description  : SQLORM基础模型定义模块
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-09-22 10:15:00
LastEditTime : 2024-11-05 10:45:00
FilePath     : /code/xt_sqlorm/models/base.py
Github       : https://github.com/sandorn/home

本模块提供SQLAlchemy ORM模型的基础定义和扩展功能，主要包括以下核心组件:

- **ModelExt**: SQLAlchemy模型扩展类，提供字典转换、字段获取等增强功能
- **Base**: SQLAlchemy 2.0+ 声明式基类，集成扩展功能
- **BaseModel**: 所有数据库模型的抽象基类，提供通用配置和基础功能

注意：混入类（IdMixin、TimestampMixin、SoftDeleteMixin、VersionedMixin、UTCTimeMixin）
已迁移到 models/mixins/ 目录下的单独文件中，请从该目录导入使用。

本模块设计用于支持时区感知的数据库操作、软删除机制和并发控制，适合构建健壮的数据库应用。
==============================================================
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from sqlalchemy.orm import DeclarativeBase
from xt_class import ItemMixin
from xt_sqlorm.models.mixins.utctime_mixin import UTCTimeMixin


class ModelExt(ItemMixin, UTCTimeMixin):
    """SQLAlchemy ORM 模型扩展基类

    提供字典转换、字段获取、对象表示等增强功能，作为所有ORM模型的基础扩展。
    继承自ItemMixin和UTCTimeMixin，结合了数据访问和时间处理能力。
    """

    def __str__(self) -> str:
        """对象字符串表示，仅显示非None字段的值

        Returns:
            str: 包含类名和非空字段的字符串表示
        """
        return self.__class__.__name__ + str({key: getattr(self, key) for key in self.keys() if getattr(self, key) is not None})

    __repr__ = __str__

    @classmethod
    def columns(cls) -> list[str]:
        """获取所有列名（排除SQLAlchemy内部属性）"""
        return [col.name for col in cls.__table__.c if not col.name.startswith('_sa_')]

    @classmethod
    def keys(cls) -> list[str]:
        """获取所有映射属性名（包括关系属性）"""
        return list(cls.__mapper__.attrs.keys())

    @classmethod
    def make_dict(cls, result: Any) -> Any:
        """批量转换数据库查询结果为字典列表

        支持单条记录、记录列表或查询结果集的自动识别和转换，简化数据处理流程。

        Usage:
            dbmode.make_dict(records)  # 自动处理单条记录或记录列表

        Args:
            result: 数据库查询结果，可以是单个对象、对象列表或查询结果集

        Returns:
            dict | list[dict] | None: 转换后的字典、字典列表，如果输入为None则返回None

        Raises:
            TypeError: 当输入类型不支持转换时
        """
        if result is None:
            return None

        if isinstance(result, cls):
            return result.to_dict()

        if isinstance(result, Sequence) and result and isinstance(result[0], cls):
            return [item.to_dict() for item in result]

        raise TypeError(f'不支持的转换类型: {type(result).__name__}')

    def to_dict(self, alias_dict: dict[str, str] | None = None, exclude_none: bool = False) -> dict[str, Any]:
        """将单一记录对象转换为字典

        支持字段别名映射和空值过滤，灵活满足不同数据输出需求。

        Usage:
            record.to_dict()  # 转换所有字段
            record.to_dict(exclude_none=True)  # 排除None值字段
            record.to_dict(alias_dict={"id": "user_id"})  # 使用别名

        Args:
            alias_dict: 字段别名字典，用于重命名字段
                示例: {"id": "user_id"} - 将id字段名替换为user_id
            exclude_none: 是否排除值为None的字段，默认为False

        Returns:
            dict[str, Any]: 转换后的字典，键为字段名(或别名)，值为字段值

        Raises:
            ValueError: 当提供的别名字典中存在别名冲突时
        """
        alias_dict = alias_dict or {}
        # 添加别名冲突检测
        if alias_dict:
            reversed_aliases = {}
            for field, alias in alias_dict.items():
                if alias in reversed_aliases:
                    raise ValueError(f'别名冲突: {alias} 已映射到多个字段')
                reversed_aliases[alias] = field

        if exclude_none:
            return {alias_dict.get(col.name, col.name): self[col.name] for col in self.__table__.columns if self[col.name] is not None}

        return {alias_dict.get(col.name, col.name): self[col.name] for col in self.__table__.columns}


class Base(DeclarativeBase, ModelExt):
    """SQLAlchemy 2.0+ 声明式基类

    继承自SQLAlchemy的DeclarativeBase和自定义的ModelExt，整合了SQLAlchemy核心功能和扩展功能。
    作为所有具体数据库模型的直接基类，提供一致的模型行为和扩展能力。
    """

    pass


class BaseModel(Base):
    """所有数据库模型的抽象基类

    提供通用的模型配置和基础功能，定义了数据库模型的共同行为。
    作为项目中所有具体数据库表模型的基类，确保模型的一致性和可维护性。
    """

    __abstract__ = True
    __extend_existing__ = True  # 允许表已存在

    @classmethod
    def before_create(cls, mapper: Any, connection: Any, target: Any) -> None:
        """创建前的业务钩子

        数据库记录创建前的回调方法，可在子类中重写以实现自定义业务逻辑。
        常用于设置默认值、验证数据等预创建操作。

        Args:
            mapper: SQLAlchemy映射器对象
            connection: 数据库连接对象
            target: 待创建的模型实例
        """
        pass

    @classmethod
    def after_update(cls, mapper: Any, connection: Any, target: Any) -> None:
        """更新后的审计钩子

        数据库记录更新后的回调方法，可在子类中重写以实现审计日志等功能。
        常用于记录变更历史、触发后续操作等。

        Args:
            mapper: SQLAlchemy映射器对象
            connection: 数据库连接对象
            target: 已更新的模型实例
        """
        pass
