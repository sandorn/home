# !/usr/bin/env python
"""==============================================================
Descripttion : mysql 异步版本
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-08-17 11:53:01
FilePath     : /xjLib/xt_DAO/xt_Aiomysql.py
LastEditTime : 2021-04-14 16:15:59
Github       : https://github.com/sandorn/home
#==============================================================
https://www.yangyanxing.com/article/aiomysql_in_python.html
https://blog.csdn.net/ydyang1126/article/details/78226701/
"""

import asyncio
import traceback

import aiomysql.sa as aiosa
from xt_database.cfg import DB_CFG
from xt_database.untilsql import make_insert_sql, make_update_sql


class AioMysql:
    def __init__(self, key="default", tablename=None):
        self.coro_list = []
        if tablename:
            self.tablename = tablename
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.run_in_loop([self.create_engine(key)])

    async def create_engine(self, key, autocommit=True):
        if key not in DB_CFG:
            raise ValueError(f"错误提示:检查数据库配置:{key}")
        cfg = DB_CFG[key]
        cfg.pop("type", None)
        try:
            self.engine = await aiosa.create_engine(
                autocommit=autocommit,  # 自动提交模式
                echo=True if __name__ == "__main__" else False,
                **cfg,
            )
        except Exception as err:
            print("connect error:", err)

    def run_in_loop(self, coro_list=None):
        coro_list = coro_list or self.coro_list
        return self.loop.run_until_complete(asyncio.gather(*coro_list))

    def query(self, sql, autorun=True):
        _coro = [self.__query(sql)] if isinstance(sql, str) else [self.__query(_sql) for _sql in sql]

        return self.run_in_loop(_coro) if autorun else self.coro_list.extend(_coro)

    async def __query(self, sql, params: dict = None):
        try:
            async with self.engine.acquire() as conn:
                async with conn._connection.cursor() as cursor:  # @关键语句
                    result = await cursor.execute(sql, params)
                    return await cursor.fetchall() or result
        except Exception:
            print(traceback.format_exc())

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


if __name__ == "__main__":
    query_list = ["SELECT users2.ID FROM users2", "SELECT * FROM  users2"]

    item1 = {"username": "刘新军", "password": "234567", "手机": "13910118122", "代理人编码": "10005393", "会员级别": "SSS", "会员到期日": "9999-12-31 00:00:00"}

    aio = AioMysql("TXbx", "users2")
    # res = aio.insert([item1])
    # print(res)
    res = aio.insert([item1, item1], autorun=False)
    res = aio.run_in_loop()
    print(res)
    # res = aio.insert([item1, item1], 'users2')
    # print(res)
    res = aio.query(query_list)
    print(res)
    # res = aio.query(query_list[0])
    # print(res)
    update_sql = ["UPDATE users2 set username='刘澈' WHERE ID = '1'", "UPDATE users2 set username='刘新军' WHERE ID = '2'"]
    res = aio.query(update_sql)
    print(res)
    # res = aio.update(
    #     [{'username': '刘澈3'}, {'username': '刘新军4'}],
    #     [
    #         {
    #             'ID': '1',
    #         },
    #         {
    #             'ID': '2',
    #             # 'username': '刘新军',
    #         },
    #     ],
    # )
    # print(res)
