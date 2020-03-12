# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-02 18:40:44
@LastEditors: Even.Sand
@LastEditTime: 2020-03-04 19:14:33
'''

import asyncio
import aiohttp

default_headers = {
    'User-Agent': ('Mozilla/5.0 (compatible; MSIE 9.0; '
                   'Windows NT 6.1; Win64; x64; Trident/5.0)'),
}


async def fetch(url, session, semaNum=100, headers=default_headers, timeout=3000):
    async with asyncio.Semaphore(semaNum):
        async with session.get(url=url, headers=headers, timeout=timeout) as resp:
            status = resp.status
            html = await resp.read()
            encoding = resp.get_encoding()
            if encoding == 'gb2312':
                encoding = 'gbk'
            html = html.decode(encoding, errors='ignore')
            redirected_url = str(resp.url)
    return status, html, redirected_url


async def fetchs(url, semaNum=100, headers=default_headers, timeout=3000):
    async with asyncio.Semaphore(semaNum):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers, timeout=timeout) as resp:
                status = resp.status
                html = await resp.read()
                encoding = resp.get_encoding()
                if encoding == 'gb2312':
                    encoding = 'gbk'
                html = html.decode(encoding, errors='ignore')
                redirected_url = str(resp.url)
    return status, html, redirected_url
