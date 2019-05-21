# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-16 01:04:34
@LastEditors: Even.Sand
@LastEditTime: 2019-05-18 04:47:34
'''
import asyncio


async def wget(host):
    print('wget %s...' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = await connect
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    await writer.drain()
    rede, rit = await connect
    while True:
        line = await reader.readline()
        if line == b'\r\n':
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    writer.close()


loop = asyncio.get_event_loop()
tasks = [
    wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']
]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
'''---------------------
作者：三贝
来源：CSDN
原文：https://blog.csdn.net/lecorn/article/details/82814142
版权声明：本文为博主原创文章，转载请附上博文链接！'''
