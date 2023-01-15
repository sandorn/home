# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-15 14:38:58
FilePath     : /CODE/py学习/asyncio学习/Python-aiohttp百万并发_server.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import asyncio
import random
from datetime import datetime

from aiohttp import web


# set seed to ensure async and sync client get same distribution of delay values
# and tests are fair random.seed(1)
async def hello(request):
    name = request.match_info.get("name", "foo")
    n = datetime.now().isoformat()
    delay = random.randint(0, 3)
    await asyncio.sleep(delay)
    headers = {"content_type": "text/html", "delay": str(delay)}
    # opening file is not async here, so it may block, to improve
    # efficiency of this you can consider using asyncio Executors
    # that will delegate file operation to separate thread or process
    # and improve performance
    # https://docs.python.org/3/library/asyncio-eventloop.html#executor
    # https://pymotw.com/3/asyncio/executors.html
    with open("frank.html", "rb") as html_body:
        print(f"{n}: {request.path} delay: {delay}")
        return web.Response(body=html_body.read(), headers=headers)


app = web.Application()
app.router.add_route("GET", "/{name}", hello)
web.run_app(app)
