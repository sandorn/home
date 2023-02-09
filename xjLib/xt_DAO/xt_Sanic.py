# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-18 14:26:14
FilePath     : /CODE/xjLib/xt_DAO/xt_Sanic.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import asyncio

from sanicdb import SanicDB


async def index(loop=None):
    loop = loop or asyncio.get_event_loop()
    db = SanicDB(
        host='cdb-lfp74hz4.bj.tencentcdb.com',
        database='bxflb',
        user='sandorn',
        password='123456',
        loop=loop,
        port=10014,  #非默认，需明确
    )
    sql = 'select * from users2'
    data = await db.query(sql)
    print(data)


if __name__ == '__main__':
    asyncio.run(index())
