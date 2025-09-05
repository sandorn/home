# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-09-05 09:52:42
FilePath     : /CODE/xjLib/xt_database/amysqlpool.py
Github       : https://github.com/sandorn/home
==============================================================
https://www.yangyanxing.com/article/aiomysql_in_python.html
https://blog.csdn.net/ydyang1126/article/details/78226701/
"""

import asyncio
import traceback
from typing import Optional

import aiomysql
from xt_database.cfg import DB_CFG
from xt_wraps.singleon import SingletonMixin


class AioSqlPool(SingletonMixin):
    def __init__(self, key="default", autocommit=True):
        self.autocommit = autocommit
        self.db_key = key
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)  # @解决循环的关键点
        self.run_in_loop([self.create_pool()])

    def run_in_loop(self, coro_list: list):
        return self.loop.run_until_complete(asyncio.gather(*coro_list))

    async def create_pool(self):
        db_key = self.db_key
        if not hasattr(DB_CFG, db_key):
            raise ValueError(f"错误提示:检查数据库配置:{db_key}")
        cfg = DB_CFG[db_key].value.copy()
        cfg.pop("type", None)

        try:
            self.pool = await aiomysql.create_pool(
                # minsize=5,  # 连接池最小值
                # maxsize=10,  # 连接池最大值
                echo=True if __name__ == "__main__" else False,
                # pool_recycle: int = -1,
                # loop: Unknown | None = None,
                autocommit=self.autocommit,  # 自动提交模式
                **cfg,
            )
            return self.pool
        except Exception:
            print("connect error:", Exception)

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

    async def _query(self, sql, args=None):
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
            await self.closeCurosr(conn, cur)

    async def _execute(self, sql, args=None):
        conn, cur = await self.getCurosr()
        try:
            affetced = await cur.execute(sql, args)
            return affetced if affetced else cur.lastrowid
        except Exception:
            print(traceback.format_exc())
        finally:
            await self.closeCurosr(conn, cur)

    async def _executeall(self, sql, args=None):
        conn, cur = await self.getCurosr()
        try:
            affetced = await cur.executemany(sql, args)
            return affetced if affetced else cur.lastrowid
        except Exception:
            print(traceback.format_exc())
        finally:
            await self.closeCurosr(conn, cur)

    def query(self, sql_list, params: Optional[dict] = None):
        sql_list = [sql_list] if isinstance(sql_list, str) else sql_list
        _coro = [self._query(_sql, params) for _sql in sql_list]
        return self.run_in_loop(_coro)

    def execute(self, sql_list, args=None):
        sql_list = [sql_list] if isinstance(sql_list, str) else sql_list
        args = [args] * len(sql_list) if not isinstance(args, (tuple, list)) else args
        _coro = [self._execute(sql, data) for sql, data in zip(sql_list, args)]
        return self.run_in_loop(_coro)

    def executeall(self, sql, args=None):
        _coro = [self._executeall(sql, args)]
        return self.run_in_loop(_coro)


if __name__ == "__main__":
    query_list = [
        "select * from users2",
        "select * from users2 where ID = 1",
        "update users2 set username='刘新军1' where ID = 2",
        "select * from users2 where ID = 2",
    ]
    up_sql = "update users2 set username='刘新新' where ID = 2"
    ups_sql = "update users2 set username=%s where ID = %s"
    ups_data = [("刘澈", 2), ("刘新军", 1)]
    self = AioSqlPool("TXbx")
    print(111111111111111111, self.execute(up_sql))
    print(222222222222222222, self.executeall(ups_sql, ups_data))
    print(333333333333333333, res := self.query(query_list[0]))
    print(444444444444444444, self.query(query_list[1]))

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
