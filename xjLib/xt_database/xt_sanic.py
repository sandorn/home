# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-07-25 16:55:39
FilePath     : /CODE/xjLib/xt_database/xt_sanic.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import asyncio

from sanicdb import SanicDB
from xt_database.cfg import DB_CFG


async def sanic_go(sql, loop=None):
    loop = loop or asyncio.get_event_loop()
    db_key = "TXbx"
    if not hasattr(DB_CFG, db_key):
        raise ValueError(f"错误提示:检查数据库配置:{db_key}")
    cfg = DB_CFG[db_key].value
    cfg.pop("type", None)
    cfg["database"] = cfg.pop("db")

    db = SanicDB(**cfg)
    return await db.query(sql)


if __name__ == "__main__":
    res = asyncio.run(sanic_go(sql="select * from users2"))
    print(res)
