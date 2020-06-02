# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-13 15:48:10
@LastEditors: Even.Sand
@LastEditTime: 2020-03-13 15:55:00
'''
import asyncio
import time

import redis


def now(): return time.time()


def get_redis():
    connection_pool = redis.ConnectionPool(host='127.0.0.1', db=4)
    return redis.Redis(connection_pool=connection_pool)


rcon = get_redis()


async def worker(x):
    print('Start worker:', x)

    while True:
        start = now()
        task = rcon.rpop("queue")
        if not task:
            await asyncio.sleep(0.1)
            continue
        print('Wait ', int(task))
        await asyncio.sleep(int(task))
        print('Done ', task, now() - start)


def main():
    asyncio.ensure_future(worker(1))
    asyncio.ensure_future(worker(3))

    loop = asyncio.get_event_loop()

    try:
        loop.run_forever()
    except KeyboardInterrupt as e:
        print(asyncio.gather(*asyncio.Task.all_tasks()).cancel())
        loop.stop()
        loop.run_forever()
    finally:
        loop.close()


if __name__ == '__main__':
    main()
