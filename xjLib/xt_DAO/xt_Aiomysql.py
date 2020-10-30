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
LastEditTime : 2020-09-08 12:00:32
Github       : https://github.com/sandorn/home
#==============================================================
https://www.yangyanxing.com/article/aiomysql_in_python.html
https://blog.csdn.net/ydyang1126/article/details/78226701/
'''
import traceback
import aiomysql
import asyncio
from xt_DAO.dbconf import db_conf
from copy import deepcopy


class Pmysql:
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

            self.pool = await aiomysql.create_pool(minsize=5, maxsize=10, autocommit=False, **conf)
            return self.pool
        except Exception:
            print('connect error:', Exception)

    async def getCurosr(self):
        conn = await self.pool.acquire()
        cur = await conn.cursor()
        return conn, cur

    async def query(self, query, param=None):
        conn, cur = await self.getCurosr()
        try:
            await cur.execute(query, param)
            return await cur.fetchall()
        except Exception:
            print(traceback.format_exc())
        finally:
            if cur: await cur.close()
            # 释放掉conn,将连接放回到连接池中
            await self.pool.release(conn)


async def AiomysqlCls(key='default'):
    mysqlobj = Pmysql()
    await mysqlobj.initpool(key)
    return mysqlobj


if __name__ == '__main__':

    async def test(mysqlobj):
        r = await mysqlobj.query("select * from users2")
        return r

    async def test2(mysqlobj):
        r = await mysqlobj.query("select * from users2 where id = (%s)", (1, ))
        return r

    async def querysum():
        mysqlobj = await AiomysqlCls('TXbx')
        result = await asyncio.gather(test(mysqlobj), test2(mysqlobj))
        for i in result:
            print(i)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(querysum())
'''
python并发编程之asyncio协程(三) - 天宇之游 - 博客园
https://www.cnblogs.com/cwp-bg/p/9590700.html

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
