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

import aiomysql
import aiomysql.sa as aio_sa
from xt_Class import item_Mixin
from xt_DAO.cfg import DB_CONFIG


class AioMysql(item_Mixin):

    def __init__(self):
        self.engine = None

    async def initpool(self, key='default', autocommit=True):
        if key not in DB_CONFIG: raise ValueError(f'错误提示:检查数据库配置:{key}')
        conf = deepcopy(DB_CONFIG[key])
        conf.pop('type', None)
        try:
            self.engine = await aio_sa.create_engine(
                # minsize=1,
                # maxsize=10,
                # loop=None,
                # pool_recycle=-1,
                # compiled_cache=None,
                **conf, )
        except Exception as err:
            print('connect error:', err)

    async def query(self, sql, args=None):
        """
        :param   sql: sql语句
        :param args: 参数
        :return:
        """
        try:
            async with self.engine.acquire() as conn:
                result = await conn.execute(sql)
                return await result.fetchall()
        except Exception:
            print(traceback.format_exc())

    async def execute(self, sql, args=None):
        """
        :param   sql: sql语句
        :param args: 参数
        :return:
        """
        conn, cur = await self.getCurosr()
        try:
            await cur.execute(sql, args)
            affetced = cur.rowcount
        except Exception:
            print(traceback.format_exc())
        finally:
            # await conn.commit()
            if cur: await cur.close()
            # 释放掉conn,将连接放回到连接池中
            await self.pool.release(conn)
            return affetced

    async def executemany(self, sql, data):
        """
        增删改 操作
        :param  sql: sql语句框架
        :param data: sql语句内容
        :return:
        """
        conn, cur = await self.getCurosr()
        affetced = 0
        try:
            await cur.executemany(sql, data)
            affetced = cur.rowcount
        except Exception:
            print(traceback.format_exc())
        finally:
            # await conn.commit()
            if cur: await cur.close()
            # 释放掉conn,将连接放回到连接池中
            await self.pool.release(conn)
            return affetced


async def create_xt_aiomysql(db_name='default'):
    Aiomysql = AioMysql()
    await Aiomysql.initpool(db_name)
    return Aiomysql


async def query_aiomysql(db_name, sql_list):
    Aiomysql = await create_xt_aiomysql(db_name)
    return await asyncio.gather(*[Aiomysql.query(sql) for sql in sql_list])


async def execute_aiomysql(db_name, sql_list):
    Aiomysql = await create_xt_aiomysql(db_name)
    return await asyncio.gather(*[Aiomysql.execute(sql) for sql in sql_list])


async def executemany_aiomysql(db_name, sql_mode, data):
    Aiomysql = await create_xt_aiomysql(db_name)
    return await asyncio.gather(Aiomysql.executemany(sql_mode, data))


if __name__ == '__main__':

    query_list = [
        "select * from users2",
        "select * from users2 where id = 1",
    ]
    # execute_sql = "update users2 set username='刘新军1' where ID = 2",
    # executemany_sql = "update users2 set username=%s where ID = %s"
    # executemany_data = [('刘澈', 1), ('刘新军', 2)]
    loop = asyncio.get_event_loop()
    # execute_sql_res = loop.run_until_complete(execute_aiomysql('TXbx', execute_sql))
    # print(execute_sql_res)
    # executemany_sql_res = loop.run_until_complete(executemany_aiomysql('TXbx', executemany_sql, executemany_data))
    # print(executemany_sql_res)
    query_list_res = loop.run_until_complete(query_aiomysql('TXbx', query_list))
    print(query_list_res)
'''
python并发编程之asyncio协程(三) - 天宇之游 - 博客园
https://www.cnblogs.com/cwp-bg/p/9590700.html
https://cloud.tencent.com/developer/article/1625730?from=15425

asyncio.get_event_loop():创建一个事件循环，所有的异步函数都需要在事件循环中运行；
asyncio.ensure_future()：创建一个任务
asyncio.gather(*fs):添加并行任务
asyncio.wait(fs):添加并行任务，可以是列表
loop.run_until_complete(func):添加协程函数同时启动阻塞直到结束
loop.run_forever()：运行事件无限循环，直到stop被调用
loop.create_task()：创建一个任务并添加到循环
loop.close():关闭循环
loop.time():循环开始后到当下的时间
loop.stop():停止循环
loop.is_closed() # 判断循环是否关闭
loop.create_future():创建一个future对象，推荐使用这个函数而不要直接创建future实例
loop.call_soon() # 设置回调函数，不能接受返回的参数，需要用到future对象，立即回调
loop.call_soon_threadsafe() # 线程安全的对象
loop.call_later() # 异步返回后开始算起，延迟回调
loop.call_at() # 循环开始多少s回调
loop.call_exception_handler() # 错误处理
'''
