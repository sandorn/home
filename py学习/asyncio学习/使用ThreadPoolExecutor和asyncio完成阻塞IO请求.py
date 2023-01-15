# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-15 08:38:37
FilePath     : /CODE/py学习/asyncio学习/使用ThreadPoolExecutor和asyncio完成阻塞IO请求.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import asyncio
import socket
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse


def get_url_socket(url):
    # 通过socket请求html
    url = urlparse(url)
    host = url.netloc
    path = url.path
    if path == "":
        path = "/"

    # 建立socket连接
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client.setblocking(False)
    client.connect((host, 80))  # 阻塞不会消耗cpu

    # 不停的询问连接是否建立好， 需要while循环不停的去检查状态
    # 做计算任务或者再次发起其他的连接请求

    client.send("GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n".format(path, host).encode("utf8"))

    data = b""
    while True:
        d = client.recv(1024)
        if d:
            data += d
        else:
            break

    data = data.decode("utf8")
    # html_data = data.split("\r\n\r\n")[1]
    print(data)
    client.close()


# 如果在协程中要用到阻塞IO，就把他放到线程池里面去运行，在运行的时候，本质还是线程池，同步的
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    pool = ThreadPoolExecutor(3)
    tasks = []
    url = "https://www.lingdianksw.com/0/405"
    for _ in range(2):
        task = loop.run_in_executor(pool, get_url_socket, url)
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))
