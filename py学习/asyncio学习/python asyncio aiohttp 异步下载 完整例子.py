# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-03 21:50:30
@LastEditors: Even.Sand
@LastEditTime: 2020-03-09 16:44:02
'''
import asyncio
import os
import sys
import time

import aiohttp
import tqdm

FLAGS = ('CN IN US ID BR PK NG BD RU JP '
         'MX PH VN ET EG DE IR TR CD FR').split()
BASE_URL = 'http://flupy.org/data/flags'  # 下载url
DEST_DIR = 'downloads/'  # 保存目录
# 获取链接,下载文件


async def fetch(session: aiohttp.ClientSession, url: str, path: str, flag: str):
    print(flag, ' 开始下载')
    async with session.get(url) as resp:
        with open(path, 'wb') as fd:
            while True:
                chunk = await resp.content.read(1024)  # 每次获取1024字节
                if not chunk:
                    break
                fd.write(chunk)
    return flag


async def begin_download(sem, session: aiohttp.ClientSession, url: str, path: str, flag: str):
    # 控制协程并发数量
    with (await sem):
        return await fetch(session, url, path, flag)


async def download(sem: asyncio.Semaphore):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for flag in FLAGS:
            # 创建路径以及url
            path = os.path.join(DEST_DIR, flag.lower() + '.gif')
            url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=flag.lower())
            # 构造一个协程列表
            tasks.append(asyncio.ensure_future(begin_download(sem, session, url, path, flag)))
        # 等待返回结果
        tasks_iter = asyncio.as_completed(tasks)
        # 创建一个进度条
        fk_task_iter = tqdm.tqdm(tasks_iter, total=len(FLAGS))
        for coroutine in fk_task_iter:
            # 获取结果
            res = await coroutine
            print(res, '下载完成')

# 创建目录
os.makedirs(DEST_DIR, exist_ok=True)
# 获取事件循环
lp = asyncio.get_event_loop()
start = time.time()
# 创建一个信号量以防止DDos
sem = asyncio.Semaphore(20)
lp.run_until_complete(download(sem))
end = time.time()
lp.close()
print('耗时:', end - start)
