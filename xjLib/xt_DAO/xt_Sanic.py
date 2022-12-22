# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2022-12-22 23:02:26
FilePath     : /xjLib/xt_DAO/xt_Sanic.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import asyncio

from sanicdb import SanicDB


async def index(loop):
    db = SanicDB('cdb-lfp74hz4.bj.tencentcdb.com', 'bxflb', 'sandorn', '123456', loop=loop)
    sql = 'select * from user2'
    data = await db.query(sql)
    print(data)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(index(loop))
'''from sanic import Sanic
from sanic import response
# 导入
from sanicdb import SanicDB

app = Sanic('test')
# 实例化SanicDB
db = SanicDB('cdb-lfp74hz4.bj.tencentcdb.com', 'bxflb', 'sandorn', '123456', sanic=app)


@app.route('/sanicdbTest')
async def sanicdbTest(request):
    sql = 'select * from user2'
    data = await app.db.query(sql)
    return response.json(data)


if __name__ == '__main__':
    app.run()'''
