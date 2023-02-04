# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-02-04 22:34:26
LastEditTime : 2023-02-04 22:36:18
FilePath     : /CODE/xjLib/xt_DAO/untilsql.py
Github       : https://github.com/sandorn/home
==============================================================
'''
from sqlalchemy import text  # , MetaData, Table, create_engine,


def get_insert_sql(item, tablename):
    cols = ", ".join(f"`{k}`" for k in item.keys())
    vals = ", ".join(f"'{v}'" for v in item.values())
    sql = f"INSERT INTO `{tablename}`({cols}) VALUES({vals})"
    return text(sql)  # text() 用于防止sql注入


def get_update_sql(item, condition, tablename):
    item_kv = ", ".join([f"`{k}`='{item[k]}'" for k in item])
    cond_k = ", ".join([f"`{k}`" for k in condition.keys()])
    cond_v = ", ".join([f"'{v}'" for v in condition.values()])
    sql = f"UPDATE `{tablename}` SET {item_kv} WHERE ({cond_k})=({cond_v})"
    return text(sql)  # text() 用于防止sql注入
