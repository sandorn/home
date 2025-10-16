# !/usr/bin/env python
"""
==============================================================
Description  : SQL工具模块 - 提供安全的SQL语句构建功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-02-04 22:34:26
LastEditTime : 2025-09-17 15:40:00
FilePath     : /CODE/xjlib/xt_database/untilsql.py
Github       : https://github.com/sandorn/home

本模块提供安全的SQL语句构建功能，防止SQL注入攻击。
主要功能包括：
- 安全的INSERT语句构建
- 安全的UPDATE语句构建
- 支持参数化查询
==============================================================
"""

from __future__ import annotations

from typing import Any


def make_insert_sql(item: dict[str, Any], table_name: str) -> tuple[str, tuple[Any, ...]]:
    """
    生成安全的INSERT SQL语句，使用参数化查询防止SQL注入

    Args:
        item: 包含字段名和值的字典
        table_name: 表名

    Returns:
        Tuple[str, Tuple[Any, ...]]: SQL语句和参数元组
            - 第一个元素: 带占位符的SQL语句
            - 第二个元素: 参数值元组

    Example:
        >>> item = {'name': '张三', 'age': 30}
        >>> sql, params = make_insert_sql(item, 'users')
        >>> # sql: INSERT INTO `users`(`name`, `age`) VALUES(%s, %s)
        >>> # params: ('张三', 30)
    """
    # 安全处理表名和字段名
    safe_table_name = _sanitize_identifier(table_name)
    sanitized_columns = [f'`{_sanitize_identifier(k)}`' for k in item]
    
    # 构建SQL语句组件
    cols = ', '.join(sanitized_columns)
    placeholders = ', '.join(['%s'] * len(item))
    params = tuple(item.values())
    
    # 安全构建SQL语句 - 使用预定义模板并组合安全组件
    sql_template = 'INSERT INTO `{}`({}) VALUES({})'
    sql = sql_template.format(safe_table_name, cols, placeholders)
    
    return sql, params


def make_update_sql(item: dict[str, Any], condition: dict[str, Any], table_name: str) -> tuple[str, tuple[Any, ...]]:
    """
    生成安全的UPDATE SQL语句，使用参数化查询防止SQL注入

    Args:
        item: 包含要更新的字段名和值的字典
        condition: 包含WHERE条件的字段名和值的字典
        table_name: 表名

    Returns:
        Tuple[str, Tuple[Any, ...]]: SQL语句和参数元组
            - 第一个元素: 带占位符的SQL语句
            - 第二个元素: 参数值元组

    Example:
        >>> item = {'name': '张三', 'age': 31}
        >>> condition = {'id': 1}
        >>> sql, params = make_update_sql(item, condition, 'users')
        >>> # sql: UPDATE `users` SET `name`=%s, `age`=%s WHERE `id`=%s
        >>> # params: ('张三', 31, 1)
    """
    # 安全处理表名和字段名
    safe_table_name = _sanitize_identifier(table_name)
    
    # 构建SET部分和WHERE部分，使用%s作为占位符
    set_clause = ', '.join([f'`{_sanitize_identifier(k)}`=%s' for k in item])
    where_clause = ' AND '.join([f'`{_sanitize_identifier(k)}`=%s' for k in condition])
    
    # 合并所有参数值
    params = tuple(item.values()) + tuple(condition.values())
    
    # 安全构建SQL语句 - 使用预定义模板并组合安全组件
    sql_template = 'UPDATE `{}` SET {} WHERE {}'
    sql = sql_template.format(safe_table_name, set_clause, where_clause)
    
    return sql, params


def _sanitize_identifier(identifier: str) -> str:
    """
    安全处理SQL标识符（表名、字段名），防止SQL注入

    Args:
        identifier: 要处理的标识符

    Returns:
        str: 处理后的安全标识符
    """
    # 保留中文字符和基本字符，移除潜在的SQL注入风险字符
    import re

    # 允许字母、数字、下划线和中文字符，移除SQL特殊字符
    return re.sub(r'[;"\'\(\)\[\]\{\}\|\\<>&^\-\+\*/%=\?\,\.\s]', '', str(identifier))

