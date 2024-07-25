# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-23 00:23:58
LastEditTime : 2023-02-04 20:42:41
FilePath     : /CODE/xjLib/xt_DAO/xt_asynOrm.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import asyncio

from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from xt_database.cfg import connect_str
from xt_database.untilsql import make_insert_sql, make_update_sql
from xt_database.xt_sqlorm_meta import ErrorMetaClass, get_db_model
from xt_singleon import SingletonMetaCls


class AsynSqlOrm(ErrorMetaClass, metaclass=SingletonMetaCls):
    def __init__(self, key="default", new_table_name=None, old_table_name=None):
        self.engine = create_engine(connect_str(key))
        self.Base = get_db_model(self.engine, new_table_name, old_table_name)
        # 创建引擎
        self.async_engine = create_async_engine(
            connect_str(key=key, odbc="aiomysql"),
            max_overflow=0,  # 超过连接池大小外最多创建的连接
            pool_size=5,  # 连接池大小
            pool_timeout=30,  # 池中没有线程最多等待的时间,否则报错
            pool_recycle=-1,  # 多久之后对线程池中的线程进行一次连接的回收（重置）
            echo=True if __name__ == "__main__" else False,  # echo参数为True时,会显示每条执行的SQL语句
            future=True,  # 使用异步模式
            # poolclass=NullPool, # 禁用池
        )
        self.async_session = async_sessionmaker(
            bind=self.async_engine
            # expire_on_commit=True, # 默认为True,提交后自动过期
            # class_=AsyncSession,
        )
        self.coro_list = []
        self.tablename = new_table_name
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)  # @解决循环的关键点

    def run_in_loop(self, coro_list=None):
        coro_list = coro_list or self.coro_list
        return self.loop.run_until_complete(asyncio.gather(*coro_list))

    def query(self, sql_list, params: dict = None, autorun=True):
        sql_list = [sql_list] if isinstance(sql_list, str) else sql_list
        _coro = [self.__query(_sql, params) for _sql in sql_list]
        return self.run_in_loop(_coro) if autorun else self.coro_list.extend(_coro)

    async def __query(self, sql, params: dict = None):
        async with self.async_session() as session:
            result = await session.execute(text(sql), params)
            try:
                await session.commit()
                return result.all() if result.returns_rows else result.rowcount
            except BaseException:
                await session.rollback()
                return 0

    def insert(self, dict_in_list, tablename=None, autorun=True):
        tablename = tablename or self.tablename
        if isinstance(dict_in_list, dict):
            dict_in_list = [dict_in_list]
        insert_sql_list = [make_insert_sql(data_dict, tablename) for data_dict in dict_in_list]

        _coro = [self.__query(insert_sql) for insert_sql in insert_sql_list]
        return self.run_in_loop(_coro) if autorun else self.coro_list.extend(_coro)

    def update(self, dict_in_list, whrere_dict_list, tablename=None, autorun=True):
        tablename = tablename or self.tablename
        if isinstance(dict_in_list, dict):
            dict_in_list = [dict_in_list]

        update_sql_list = [make_update_sql(data_dict, whrere_dict, tablename) for data_dict, whrere_dict in zip(dict_in_list, whrere_dict_list)]

        _coro = [self.__query(update_sql) for update_sql in update_sql_list]
        return self.run_in_loop(_coro) if autorun else self.coro_list.extend(_coro)

    def add_all(self, dict_in_list, autorun=True):
        _coro = [self.__add_all(dict_in_list)]
        return self.run_in_loop(_coro) if autorun else self.coro_list.extend(_coro)

    async def __add_all(self, dict_in_list):
        items_list = [self.Base(**__d) for __d in dict_in_list]
        async with self.async_session() as session:
            session.add_all(items_list)
            try:
                await session.commit()
                return len(items_list)
            except BaseException:
                await session.rollback()
                return 0


if __name__ == "__main__":
    query_list = ["select * from users2 where id = 1", "select * from users2"]
    item1 = {"username": "刘新", "password": "234567", "手机": "13910118122", "代理人编码": "10005393", "会员级别": "SSS", "会员到期日": "9999-12-31 00:00:00"}

    aio = AsynSqlOrm("TXbx", "users2", "users")
    # res = aio.add_all([item1])
    # print(1111, res)
    # res = aio.insert([item1])
    # print(2222, res)
    # res = aio.insert([item1, item1], "users2")
    # print(4444, res)
    res = aio.query(query_list[1])
    print(5555, res)
    # res = aio.update([{"username": "刘澈111"}, {"username": "刘新军111"}], [{"ID": "1"}, {"ID": "2", "username": "刘新军"}])
    # print(6666, res)
