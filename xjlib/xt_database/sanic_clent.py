# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-09-10 14:42:57
FilePath     : /CODE/xjLib/xt_database/sanic.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from __future__ import annotations

import asyncio

from sanic import Sanic, response
from sanicdb import SanicDB
from xt_database.cfg import DB_CFG


async def sanic_go(sql, loop=None):
    loop = loop or asyncio.get_running_loop()
    db_key = 'TXbx'
    if not hasattr(DB_CFG, db_key):
        raise ValueError(f'错误提示:检查数据库配置:{db_key}')
    cfg = DB_CFG[db_key].value
    cfg.pop('type', None)
    cfg['database'] = cfg.pop('db')

    db = SanicDB(**cfg)
    return await db.query(sql)


app = Sanic('demo')
temp_db = SanicDB('localhost', 'bxflb', 'sandorn', '123456', sanic=app)


@app.route('/')
async def index(request):
    sql = 'select * from users2 where id=1'
    data = await app.temp_db.query(sql)
    return response.json(data)


if __name__ == '__main__':
    # res = asyncio.run(sanic_go(sql='select * from users2'))
    # print(res)
    app.run()
