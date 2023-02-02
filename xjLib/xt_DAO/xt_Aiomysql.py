# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
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
'''
import asyncio
import traceback
from copy import deepcopy

import aiomysql.sa as aio_sa
# from sqlalchemy import text  # , MetaData, Table, create_engine
from xt_Class import item_Mixin
from xt_DAO.cfg import DB_CONFIG  # , connect_str


class AioMysql(item_Mixin):

    def __init__(self, key='default', table_name=None):
        self.coro_list = []
        self.key = key
        if table_name: self.init_orm(table_name)
        self.loop = asyncio.get_event_loop()
        self.run_in_loop([self.create_engine(key=self.key, autocommit=True)])

    def __del__(self):
        # self.loop.close()
        ...

    async def create_engine(self, key='default', autocommit=True):
        if key not in DB_CONFIG: raise ValueError(f'错误提示:检查数据库配置:{key}')
        conf = deepcopy(DB_CONFIG[key])
        conf.pop('type', None)
        try:
            self.engine = await aio_sa.create_engine(
                autocommit=autocommit,
                **conf,
            )
        except Exception as err:
            print('connect error:', err)

    def run_in_loop(self, coro_list=None):
        coro_list = coro_list or self.coro_list
        return self.loop.run_until_complete(asyncio.gather(*coro_list))

    def init_orm(self, table_name):
        # self.s_engine = create_engine(connect_str(self.key))
        # self.tbl = Table(self.table_name, MetaData(bind=self.s_engine), autoload=True)
        # insert_sql = tbl.insert().values({'name': 'test', 'age': 18})
        # update_sql = tbl.update().where(tbl.c.id == 1).values({'name': 'test', 'age': 18})
        self.table_name = table_name

    def querymany(self, sql_list, autorun=True):
        _coro = [self.__query(sql) for sql in sql_list]
        if autorun: return self.run_in_loop(_coro)
        else: self.coro_list.extend(_coro)

    def query(self, sql, autorun=True):
        _coro = [self.__query(sql)]
        if autorun: return self.run_in_loop(_coro)
        else: self.coro_list.extend(_coro)

    async def __query(self, sql):

        try:
            async with self.engine.acquire() as conn:
                result = await conn.execute(sql)
                return await result.fetchall() if result._metadata != None else 1
        except Exception:
            print(traceback.format_exc())

    @staticmethod
    def get_insert_sql(item, table_name):
        cols = ", ".join(f"`{k}`" for k in item.keys())
        vals = ", ".join(f"'{v}'" for v in item.values())
        sql = f"INSERT INTO `{table_name}`({cols}) VALUES({vals})"
        return sql.replace('%', '%%')  # text() 用于防止sql注入

    @staticmethod
    def get_update_sql(item, condition, table_name):
        item_kv = ", ".join([f"`{k}`='{item[k]}'" for k in item])
        cond_k = ", ".join([f"`{k}`" for k in condition.keys()])
        cond_v = ", ".join([f"'{v}'" for v in condition.values()])
        sql = f"UPDATE `{table_name}` SET {item_kv} WHERE ({cond_k})=({cond_v})"
        return sql.replace('%', '%%')  # text() 用于防止sql注入

    def insert(self, data_dict_list, table_name=None, autorun=True):
        table_name = table_name or self.table_name
        if isinstance(data_dict_list, dict): data_dict_list = [data_dict_list]
        _coro = [self.__insert(data_dict, table_name) for data_dict in data_dict_list]
        if autorun: return self.run_in_loop(_coro)
        else: self.coro_list.extend(_coro)

    async def __insert(self, data_dict_list, table_name):
        insert_sql = self.get_insert_sql(data_dict_list, table_name)
        async with self.engine.acquire() as conn:
            # 注意: 执行的执行必须开启一个事务, 否则数据是不会进入到数据库中的
            async with conn.begin():
                try:
                    result = await conn.execute(insert_sql)
                    return result.rowcount  # 影响的行数
                except Exception:
                    print(traceback.format_exc())

    def update(self, data_dict_list, whrere_dict_list, table_name=None, autorun=True):
        table_name = table_name or self.table_name
        if isinstance(data_dict_list, dict): data_dict_list = [data_dict_list]
        _coro = [self.__update(data_dict, whrere_dict, table_name) for data_dict, whrere_dict in zip(data_dict_list, whrere_dict_list)]
        if autorun: return self.run_in_loop(_coro)
        else: self.coro_list.extend(_coro)

    async def __update(self, data_dict_list, whrere_dict, table_name):
        update_sql = self.get_update_sql(data_dict_list, whrere_dict, table_name)
        async with self.engine.acquire() as conn:
            async with conn.begin():
                try:
                    result = await conn.execute(update_sql)
                    return result.rowcount  # 影响的行数
                except Exception:
                    print(traceback.format_exc())


if __name__ == '__main__':

    query_list = [
        "select * from users2 where id = 1",
        "select * from users2",
    ]

    item1 = {'username': '刘新军', 'password': '234567', '手机': '13910118122', '代理人编码': '10005393', '会员级别': 'SSS', '会员到期日': '9999-12-31 00:00:00'}
    executemany_sql = "update users2 set username=%s where ID = %s"
    executemany_data = [('刘澈', 1), ('刘新军', 2)]

    aio = AioMysql('TXbx', table_name='users2')
    # res = aio.insert([item1, item1])
    # print(res)
    # res = aio.insert([item1, item1], autorun=False)
    # res = aio.run_in_loop()
    # print(res)
    # res = aio.insert([item1, item1], 'users')
    # print(res)
    # res = aio.querymany(query_list)
    # print(res)
    # res = aio.query(query_list[0])
    # print(res)
    # update_sql = [
    #     "UPDATE users2 set username='刘新军1' WHERE ID = '1'",
    #     "UPDATE users2 set username='刘新军2' WHERE ID = '2'",
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
