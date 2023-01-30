# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-21 00:08:37
LastEditTime : 2023-01-21 00:18:30
FilePath     : /CODE/xjLib/xt_DAO/xt_asycsqlalchemy.py
Github       : https://github.com/sandorn/home
==============================================================
'''

from copy import deepcopy

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta  # 类;declarative_base类工厂
from sqlalchemy.orm import scoped_session, sessionmaker
from xt_Class import typed_property
from xt_DAO.cfg import DB_CONFIG, connect_str
from xt_DAO.xt_chemyMeta import Orm_Meta


def get_engine(key='default', dbmodel=None):
    engine = create_async_engine(connect_str(key, odbc='aiomysql'), echo=True, future=True)
    # @实现user.query.xxxx  # FROM tablename
    # if dbmodel is not None: dbmodel.query = session.query_property()
    session = sessionmaker(class_=AsyncSession, autocommit=False, autoflush=False, bind=engine)
    return engine, session


async def async_main():
    async with engine.connect() as conn:
        tables = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())


class SqlConnection(Orm_Meta):

    # #限定参数类型
    dbmodel = typed_property('dbmodel', DeclarativeMeta)

    def __init__(self, dbmodel, key='default'):
        self.dbmodel = dbmodel  # #orm基类
        # #设置self.params参数
        self.params = {attr: getattr(self.dbmodel, attr) for attr in self.dbmodel.columns()}
        self.engine = create_engine(
            connect_str(key),
            max_overflow=0,  # 超过连接池大小外最多创建的连接
            pool_size=5,  # 连接池大小
            pool_timeout=30,  # 池中没有线程最多等待的时间,否则报错
            pool_recycle=-1,  # 多久之后对线程池中的线程进行一次连接的回收（重置）
            echo=False,  # echo参数为True时,会显示每条执行的SQL语句
            # poolclass=NullPool, # 禁用池
        )
        self.conn = self.engine.connect()
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.dbmodel.metadata.create_all(self.engine)

        # @实现 user.query.xxxx  # FROM tablename
        # @self.dbmodel.query_property = self.session.query_property()
        # @self.dbmodel.query = self.session.query()

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
        return not exc_type


'''
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

#参数 echo：打印执行日志，future：使用2.0新特性，也可以使用async_engine_from_config创建,engine直到第一次请求数据库才会真正连接到数据库，称为延迟初始化
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

if __name__ == "__main__":
    # Data_Model_2_py('uuu', 'd:/1.py', 'TXbook')  # 待测试
    from xt_DAO.xt_chemyMeta import getModel
    engine, session = get_engine('TXbx')
    t = getModel('users2', engine)  # , 'users99')
    print(t)
    # print(t.columns())
    # sqlhelper = SqlConnection(t, 'TXbx')
    # res = sqlhelper.select()
    # print(res)
