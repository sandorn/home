# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-02-04 22:34:26
LastEditTime : 2023-02-04 22:36:18
FilePath     : /CODE/xjLib/xt_DAO/untilsql.py
Github       : https://github.com/sandorn/home
==============================================================
"""


def make_insert_sql(item, table_name):
    cols = ", ".join(f"`{k}`" for k in item.keys())
    vals = ", ".join(f"'{v}'" for v in item.values())
    sql = f"INSERT INTO `{table_name}`({cols}) VALUES({vals})"
    sql = sql.replace("%", "%%")
    return sql  # text() 用于防止sql注入


def make_update_sql(item, condition, table_name):
    item_kv = ", ".join([f"`{k}`='{item[k]}'" for k in item])
    cond_k = ", ".join([f"`{k}`" for k in condition.keys()])
    cond_v = ", ".join([f"'{v}'" for v in condition.values()])
    sql = f"UPDATE `{table_name}` SET {item_kv} WHERE ({cond_k})=({cond_v})"
    sql = sql.replace("%", "%%")
    return sql  # text() 用于防止sql注入
