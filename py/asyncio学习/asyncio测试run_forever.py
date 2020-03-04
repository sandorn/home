# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-03 13:32:44
@LastEditors: Even.Sand
@LastEditTime: 2020-03-03 13:33:14
'''
# coding=utf-8
import asyncio
import functools
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [*] %(processName)s  %(threadName)s  %(message)s"
)


def done_callback(loop, futu):
    loop.stop()


# async def work01 (x):
#     logging.info(f'Waiting :{str(x)}')
#     await asyncio.sleep(x)
#     logging.info(f'Done :{str(x)}')


async def work02(
        loop,  # 第二种运行方式
        x
):
    logging.info(f'Waiting :{str(x)}')
    await asyncio.sleep(x)
    logging.info(f'Done :{str(x)}')
    # loop.stop()  # 第二种运行方式


if __name__ == '__main__':
    start = time.time()

    loop = asyncio.get_event_loop()
    # 第一种运行方式
    # loop.run_until_complete(work01(1))
    # loop.run_until_complete(work01(3))
    # 第二种运行方式( 第二个协程没结束，loop 就停止了——被先结束的那个协程给停掉的。)
    # asyncio.ensure_future(work02(loop, 1))
    # asyncio.ensure_future(work02(loop, 3))
    # 解决第二种运行方式的最佳方法
    futus = asyncio.gather(work02(loop, 1), work02(loop, 3))
    futus.add_done_callback(functools.partial(done_callback, loop))

    loop.run_forever()
    loop.close()
    logging.info(f"<程序退出> 总用时：{time.time() - start}")
