# !/usr/bin/env python3
"""
==============================================================
Description  : XT-SQLORM主模块初始化
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-09-22 10:50:00
LastEditTime : 2025-09-23 10:30:00
FilePath     : /CODE/xjlib/xt_sqlorm/__init__.py
Github       : https://github.com/sandorn/home

XT-SQLORM是一个基于SQLAlchemy的ORM框架，采用模型定义与数据库操作逻辑分离的三层架构设计
==============================================================
"""

# 导出核心模块和类
from __future__ import annotations

from .core import AsyncOrmOperations, AsyncSqlConnection, OrmOperations, SqlConnection, copy_table_model, create_orm_operations, create_sqlconnection, db_to_model, reflect_table
from .models import Base, BaseModel, JsonEncodedDict, ModelExt

__all__ = (
    'AsyncOrmOperations',
    'AsyncSqlConnection',
    'Base',
    'BaseModel',
    'JsonEncodedDict',
    'ModelExt',
    'OrmOperations',
    'SqlConnection',
    'copy_table_model',
    'create_orm_operations',
    'create_sqlconnection',
    'db_to_model',
    'reflect_table',
)

# 版本信息
__version__ = '1.0.0'
__author__ = 'sandorn'
__email__ = 'sandorn@live.cn'
__description__ = 'XT-SQLORM - A SQLAlchemy-based ORM framework with separated model and operation layers'