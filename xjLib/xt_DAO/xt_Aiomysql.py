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
from xt_Class import item_Mixin
from xt_DAO.dbconf import db_conf


class xt_aiomysql(item_Mixin):

    def __init__(self):
        self.coon = None
        self.pool = None

    async def initpool(self, key='default'):
        try:
            if key not in db_conf:
                raise ('错误提示：检查数据库配置：' + self.db_name)
            else:
                conf = deepcopy(db_conf[key])
            if 'type' in conf: conf.pop('type')

            self.pool = await aiomysql.create_pool(
                minsize=5,  # 连接池最小值
                maxsize=10,  # 连接池最大值
                autocommit=False,  # 自动提交模式
                **conf,
            )
            return self.pool
        except Exception:
            print('connect error:', Exception)

    async def getCurosr(self):
        conn = await self.pool.acquire()
        cur = await conn.cursor()
        return conn, cur

    async def query(self, sql, args=None):
        """
        :param   sql: sql语句
        :param args: 参数
        :return:
        """
        conn, cur = await self.getCurosr()
        try:
            await cur.execute(sql, args)
            return await cur.fetchall()
        except Exception:
            print(traceback.format_exc())
        finally:
            await conn.commit()
            if cur: await cur.close()
            # 释放掉conn,将连接放回到连接池中
            await self.pool.release(conn)

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
            await conn.commit()
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
        try:
            await cur.executemany(sql, data)
            affetced = cur.rowcount
        except Exception:
            print(traceback.format_exc())
        finally:
            await conn.commit()
            if cur: await cur.close()
            # 释放掉conn,将连接放回到连接池中
            await self.pool.release(conn)
            return affetced


async def Create_xt_aiomysql(db_name='default'):
    Aiomysql_obj = xt_aiomysql()
    await Aiomysql_obj.initpool(db_name)
    return Aiomysql_obj


async def query_aiomysql(db_name, sql_list):
    Aiomysql_obj = await Create_xt_aiomysql(db_name)
    results = await asyncio.gather(*[Aiomysql_obj.query(sql) for sql in sql_list])
    return results


async def execute_aiomysql(db_name, sql_list):
    Aiomysql_obj = await Create_xt_aiomysql(db_name)
    results = await asyncio.gather(*[Aiomysql_obj.execute(sql) for sql in sql_list])
    return results


async def executemany_aiomysql(db_name, sql_mode, data):
    Aiomysql_obj = await Create_xt_aiomysql(db_name)
    results = await asyncio.gather(Aiomysql_obj.executemany(sql_mode, data))
    return results


if __name__ == '__main__':

    query_list = [
        "select * from users2",
        "select * from users2 where id = 1",
    ]
    execute_sql = "update users2 set username='刘新军' where ID = 2",
    executemany_sql = "update users2 set username=%s where ID = %s"
    executemany_data = [('刘澈', 1), ('刘新军', 2)]
    loop = asyncio.get_event_loop()
    execute_sql_res = loop.run_until_complete(execute_aiomysql('TXbx', execute_sql))
    print(execute_sql_res)
    executemany_sql_res = loop.run_until_complete(executemany_aiomysql('TXbx', executemany_sql, executemany_data))
    print(executemany_sql_res)
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
