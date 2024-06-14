# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-06-13 13:07:45
FilePath     : /CODE/xjLib/xt_DAO/xt_Sanic.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import asyncio

from sanicdb import SanicDB


async def index(loop=None, sql=None):
    loop = loop or asyncio.get_event_loop()
    db = SanicDB(
        host='localhost',
        database='bxflb',
        user='sandorn',
        password='123456',
        loop=loop,
        port=3306,  # 非默认，需明确
    )
    sql = 'select * from users2' if not sql else sql
    data = await db.query(sql)
    print(data)


if __name__ == '__main__':
    asyncio.run(index(sql='select * from users2 limit 2'))
