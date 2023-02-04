# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-23 00:23:58
LastEditTime : 2023-02-04 20:42:41
FilePath     : /CODE/xjLib/xt_DAO/xt_asynOrm.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from xt_Class import typed_property
from xt_DAO.cfg import connect_str
from xt_DAO.untilsql import get_insert_sql, get_update_sql
from xt_DAO.xt_chemyMeta import Orm_Meta


class AsynSqlOrm(Orm_Meta):

    # #限定参数类型
    Base = typed_property('Base', DeclarativeMeta)

    def __init__(self, Base, key='default', tablename=None):
        self.coro_list = []
        self.Base = Base  # #orm基类
        self.tablename = tablename or self.Base.__tablename__
        self.loop = asyncio.get_event_loop()
        # #设置self.params参数
        self.params = {attr: getattr(self.Base, attr) for attr in self.Base.columns()}
        self.engine = create_async_engine(
            connect_str(key=key, odbc='aiomysql'),
            max_overflow=0,  # 超过连接池大小外最多创建的连接
            pool_size=5,  # 连接池大小
            pool_timeout=30,  # 池中没有线程最多等待的时间,否则报错
            pool_recycle=-1,  # 多久之后对线程池中的线程进行一次连接的回收（重置）
            # echo=True,  # echo参数为True时,会显示每条执行的SQL语句
            # poolclass=NullPool, # 禁用池
        )
        self.async_session = async_sessionmaker(
            bind=self.engine,
            # class_=AsyncSession,
            # autocommit=False,
            # autoflush=False,
            expire_on_commit=False,
        )
        self.run_in_loop([self.init_db()])

    def run_in_loop(self, coro_list=None):
        coro_list = coro_list or self.coro_list
        return self.loop.run_until_complete(asyncio.gather(*coro_list))

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.create_all)

    async def dropt_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.drop_all)

    def querymany(self, sql_list, autorun=True):
        _coro = [self.__query(sql) for sql in sql_list]
        if autorun: return self.run_in_loop(_coro)
        else: self.coro_list.extend(_coro)

    def query(self, sql, autorun=True):
        _coro = [self.__query(sql)]
        if autorun: return self.run_in_loop(_coro)
        else: self.coro_list.extend(_coro)

    async def __query(self, sql):
        async with self.async_session() as session:
            result = await session.execute(text(sql))
            await session.commit()
            return result.all() if result.returns_rows else result.rowcount

    def insert(self, data_dict_list, tablename=None, autorun=True):
        tablename = tablename or self.tablename
        if isinstance(data_dict_list, dict): data_dict_list = [data_dict_list]
        _coro = [self.__insert(data_dict, tablename) for data_dict in data_dict_list]
        if autorun: return self.run_in_loop(_coro)
        else: self.coro_list.extend(_coro)

    def update(self, data_dict_list, whrere_dict_list, tablename=None, autorun=True):
        tablename = tablename or self.tablename
        if isinstance(data_dict_list, dict): data_dict_list = [data_dict_list]
        _coro = [self.__update(data_dict, whrere_dict, tablename) for data_dict, whrere_dict in zip(data_dict_list, whrere_dict_list)]
        if autorun: return self.run_in_loop(_coro)
        else: self.coro_list.extend(_coro)

    async def __insert(self, data_dict_list, tablename):
        insert_sql = get_insert_sql(data_dict_list, tablename)
        async with self.async_session() as session:
            result = await session.execute(insert_sql)
            await session.commit()
            return result.rowcount

    async def __update(self, data_dict_list, whrere_dict, tablename):
        update_sql = get_update_sql(data_dict_list, whrere_dict, tablename)
        async with self.async_session() as session:
            result = await session.execute(update_sql)
            await session.commit()
            return result.rowcount

    def add_all(self, dictL, autorun=True):
        _coro = [self.__add_all(dictL)]
        if autorun: return self.run_in_loop(_coro)
        else: self.coro_list.extend(_coro)

    async def __add_all(self, dictL):
        itemL = [self.Base(**__d) for __d in dictL]
        async with self.async_session() as session:
            async with session.begin():
                session.add_all(itemL)
            await session.commit()


def create_asynorm(key, source_table_name, target_table_name=None):
    from xt_DAO.xt_chemyMeta import getModel
    from xt_DAO.xt_sqlalchemy import get_engine
    engine, _ = get_engine(key)
    _t = getModel(source_table_name, engine, target_table_name)  # #获取orm基类
    return AsynSqlOrm(Base=_t, key=key, tablename=_t.__tablename__)


if __name__ == '__main__':
    # aio = create_orm('TXbx', 'users2')
    # print(aio.query('select * from users2'))
    query_list = [
        "select * from users2 where id = 1",
        "select * from users2",
    ]

    item1 = {'username': '刘新军', 'password': '234567', '手机': '13910118122', '代理人编码': '10005393', '会员级别': 'SSS', '会员到期日': '9999-12-31 00:00:00'}
    executemany_sql = "update users2 set username=%s where ID = %s"
    executemany_data = [('刘澈', 1), ('刘新军', 2)]

    aio = create_asynorm('TXbx', 'users2')  #, 'user99')
    # res = aio.add_all([
    #     item1,
    # ])
    # print(res)
    # res = aio.insert([item1, ])
    # print(res)
    # res = aio.insert([item1, ], autorun=False)
    # res = aio.run_in_loop()
    # print(res)
    # res = aio.insert([item1, item1], 'users')
    # print(res)
    # res = aio.querymany(query_list)
    # print(res)
    res = aio.query(query_list[1])
    print(res)
    # update_sql = [
    #     "UPDATE users2 set username='刘澈' WHERE ID = '1'",
    #     "UPDATE users2 set username='刘新军' WHERE ID = '2'",
    # ]
    # res = aio.querymany(update_sql)
    # print(res)
    # res = aio.update(
    #     [{
    #         'username': '刘澈3'
    #     }, {
    #         'username': '刘新军4'
    #     }],
    #     [
    #         {
    #             'ID': '1',
    #         },
    #         {
    #             'ID': '2',
    #             # 'username': '刘新军',
    #         }
    #     ])
    # print(res)
