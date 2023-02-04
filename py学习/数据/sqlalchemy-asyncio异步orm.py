# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-02-03 16:18:26
LastEditTime : 2023-02-03 16:18:56
FilePath     : /CODE/py学习/数据/sqlalchemy-asyncio异步orm.py
Github       : https://github.com/sandorn/home
==============================================================
https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
'''
import asyncio

from sqlalchemy import Column, MetaData, String, Table, select
from sqlalchemy.ext.asyncio import create_async_engine
from xt_DAO.cfg import DB_CONFIG, connect_str

meta = MetaData()
t1 = Table("t1", meta, Column("name", String(50), primary_key=True))


async def async_main() -> None:
    engine = create_async_engine(
        connect_str('TXbx', 'aiomysql'),
        echo=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)

        await conn.execute(t1.insert(), [{"name": "some1111"}, {"name": "some2222"}])

    async with engine.connect() as conn:
        # select a Result, which will be delivered with buffered
        # results
        result = await conn.execute(select(t1).where(t1.c.name == "some name 1"))

        print(result.fetchall())

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()


asyncio.run(async_main())


'''
https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html

with Session(engine) as session_obj:
    result = sess.execute(select(User).where(User.id == 7))


from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

#参数 echo:打印执行日志,future:使用2.0新特性,也可以使用async_engine_from_config创建,engine直到第一次请求数据库才会真正连接到数据库,称为延迟初始化
engine = create_async_engine(connect_str('default','aiomysql'),
                                echo=True, future=True)
Session = sessionmaker(class_=AsyncSession,autocommit=False,
                    autoflush=False,bind=engine)
Base = declarative_base()
#等价于   from sqlalchemy.orm import registry
#        mapper_registry = registry()
#        Base = mapper_registry.generate_base()

# 简单使用
async def query():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT x, y FROM some_table"))
        for row in result:
            print(f"x: {row.x}  y: {row.y}")

# 手动提交： 使用冒号声明参数
async def insert():
    async with engine.connect() as conn:
        await conn.execute(text("CREATE TABLE some_table (x int, y int)"))
        await conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            {"x": 1, "y": 1}, {"x": 2, "y": 4}
        )
        await conn.commit()

# 自动提交：绑定多个参数
async def connect_insert():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE TABLE some_table (x int, y int)"))
        await conn.execute(
          text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
          [{"x": 1, "y": 1}, {"x": 2, "y": 4}]
        )
        await conn.commit()

# 使用bindparams绑定参数
async def connect_query():
    stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x,y").bindparams(y=6)
    async with engine.connect() as conn:
        result = await conn.execute(stmt)
        for row in result:
            print(f"x: {row.x}  y: {row.y}")
'''
