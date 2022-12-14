# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:36:04
LastEditTime : 2022-12-14 23:20:56
FilePath     : /py学习/asyncio学习/协程停止.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import asyncio


async def test1(num):
    print(num)
    await asyncio.sleep(1 / num)
    print(num * 10)
    return num * num * 100


tasks = [
    asyncio.ensure_future(test1(1)),
    asyncio.ensure_future(test1(2)),
    asyncio.ensure_future(test1(3)),
]


def func():

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.wait(tasks))
    except KeyboardInterrupt as e:
        print(e)
        for task in asyncio.Task.all_tasks():
            task.cancel()
        loop.stop()
        loop.run_forever()
    finally:
        loop.close()


def func2():
    a = test1(5)
    b = test1(8)

    try:
        a.send(None)  # 可以通过调用 send 方法，执行协程函数
    except StopIteration as e:
        print(e.value)
        # 协程函数执行结束时会抛出一个StopIteration 异常，标志着协程函数执行结束，返回值在value中
        pass
    try:
        b.send(None)  # 可以通过调用 send 方法，执行协程函数
    except StopIteration as e:
        print(e.value)
        # 协程函数执行结束时会抛出一个StopIteration 异常，标志着协程函数执行结束，返回值在value中
        pass


def func3():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))  # 注意asyncio.wait方法
    for task in tasks:
        print("task result is ", task.result())


if __name__ == "__main__":
    # func()
    func3()
