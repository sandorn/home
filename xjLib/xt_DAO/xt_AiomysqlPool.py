# !/usr/bin/env python
"""
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
"""

import asyncio
import traceback
from copy import deepcopy
from functools import partial

import aiomysql
from xt_Class import item_Mixin
from xt_DAO.cfg import DB_CONFIG


class AioMysql(item_Mixin):
    def __init__(self):
        self.pool = None

    async def create_pool(self, key='default', autocommit=True):
        if key not in DB_CONFIG:
            raise ValueError(f'错误提示:检查数据库配置:{key}')
        conf = deepcopy(DB_CONFIG[key])
        conf.pop('type', None)
        self.autocommit = autocommit
        try:
            self.pool = await aiomysql.create_pool(
                # minsize=5,  # 连接池最小值
                # maxsize=10,  # 连接池最大值
                # echo: bool = False,
                # pool_recycle: int = -1,
                # loop: Unknown | None = None,
                autocommit=self.autocommit,  # 自动提交模式
                **conf,
            )
            return self.pool
        except Exception:
            print('connect error:', Exception)

    async def getCurosr(self):
        conn = await self.pool.acquire()
        cur = await conn.cursor()
        return conn, cur

    async def closeCurosr(self, conn, cur):
        if not self.autocommit:
            await conn.commit()
        await cur.close()
        # 释放掉conn,将连接放回到连接池中
        await self.pool.release(conn)

    async def query(self, sql, args=None):
        """
        :param   sql: sql语句
        :param args: 参数
        :return:
        """
        conn, cur = await self.getCurosr()
        res = ''
        try:
            await cur.execute(sql, args)
            res = await cur.fetchall()
        except Exception:
            print(traceback.format_exc())
        finally:
            await self.closeCurosr(conn, cur)
            return res

    async def execute(self, sql, args=None):
        conn, cur = await self.getCurosr()
        affetced = 0
        try:
            affetced = await cur.execute(sql, args)
            # affetced = cur.rowcount
        except Exception:
            print(traceback.format_exc())
        finally:
            await self.closeCurosr(conn, cur)
            return affetced

    async def executemany(self, sql, data):
        conn, cur = await self.getCurosr()
        affetced = 0
        try:
            affetced = await cur.executemany(sql, data)
        except Exception:
            print(traceback.format_exc())
        finally:
            await self.closeCurosr(conn, cur)
            return affetced


async def create_xt_aiomysql(key='default'):
    Aiomysql = AioMysql()
    await Aiomysql.create_pool(key)
    return Aiomysql


async def _query_aiomysql(key, sql_list):
    Aiomysql = await create_xt_aiomysql(key)
    return await asyncio.gather(*[Aiomysql.query(sql) for sql in sql_list])


async def _execute_aiomysql(key, sql_list):
    Aiomysql = await create_xt_aiomysql(key)
    return await asyncio.gather(*[Aiomysql.execute(sql) for sql in sql_list])


async def _executemany_aiomysql(key, sql, data):
    Aiomysql = await create_xt_aiomysql(key)
    return await asyncio.gather(Aiomysql.executemany(sql, data))


def _run_aiomysql(func, *args, **kwargs):
    # loop = asyncio.new_event_loop()
    return asyncio.run(func(*args, **kwargs))


query_aiomysql = partial(_run_aiomysql, _query_aiomysql)
execute_aiomysql = partial(_run_aiomysql, _execute_aiomysql)
executemany_aiomysql = partial(_run_aiomysql, _executemany_aiomysql)

if __name__ == '__main__':
    query_list = [
        'select * from users2',
        'select * from users2 where ID = 1',
        "update users2 set username='刘新军1' where ID = 2",
        'select * from users2 where ID = 2',
    ]
    up_sql = ("update users2 set username='刘新新' where ID = 2",)
    ups_sql = 'update users2 set username=%s where ID = %s'
    ups_data = [('刘澈', 1), ('刘新军', 2)]
    # res = execute_aiomysql('TXbx', up_sql)
    # print(res)
    # res = executemany_aiomysql('TXbx', ups_sql, ups_data)
    # print(res)
    res = query_aiomysql('TXbx', query_list)
    print(res)
"""
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
"""
