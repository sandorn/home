# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-10-26 17:05:52
FilePath     : /CODE/xjLib/xt_Ahttp.py
Github       : https://github.com/sandorn/home
==============================================================
https://github.com/web-trump/ahttp/blob/master/ahttp.py
"""

import asyncio
from functools import partial
from threading import Thread

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from xt_Head import TIMEOUT, Head
from xt_Requests import TRETRY
from xt_Response import htmlResponse

__all__ = (
    "get",
    "post",
    "head",
    "put",
    "delete",
    "options",
    "trace",
    "connect",
    "patch",
    "ahttpGet",
    "ahttpGetAll",
    "ahttpPost",
    "ahttpPostAll",
)


def _unil_session_method(method, *args, **kwargs):
    session = SessionMeta()
    method_dict: dict = {
        "get": session.get,
        "post": session.post,
        "head": session.head,
        "options": session.options,
        "put": session.put,
        "delete": session.delete,
        "trace": session.trace,
        "connect": session.connect,
        "patch": session.patch,
    }

    if method in [
        "get",
        "post",
        "head",
        "options",
        "put",
        "delete",
        "trace",
        "connect",
        "patch",
    ]:
        return method_dict.get(method)(*args, **kwargs)


# #使用偏函数 Partial,快速构建多个函数
get = partial(_unil_session_method, "get")
post = partial(_unil_session_method, "post")
head = partial(_unil_session_method, "head")  # 结果正常，无ReqResult
options = partial(_unil_session_method, "options")
put = partial(_unil_session_method, "put")
delete = partial(_unil_session_method, "delete")
trace = partial(_unil_session_method, "trace")  # 有命令，服务器未响应
connect = partial(_unil_session_method, "connect")  # 有命令，服务器未响应
patch = partial(_unil_session_method, "patch")


class SessionMeta:
    def __getattr__(self, name):
        if name in [
            "get",
            "post",
            "head",
            "options",
            "put",
            "delete",
            "trace",
            "connect",
            "patch",
        ]:
            new_AsyncTask = AsyncTask()
            return new_AsyncTask.__getattr__(name)  # @ 设置方法


class AsyncTask:
    def __init__(self, *args, **kwargs):
        self.index = id(self)

    def __getattr__(self, name):
        if name in [
            "get",
            "post",
            "head",
            "options",
            "put",
            "delete",
            "trace",
            "connect",
            "patch",
        ]:
            self.method = name  # @ 设置方法
            return self._make_params  # @ 设置参数

    def __repr__(self):
        return f"<AsyncTask | Method:[{self.method}] | Index:[{self.index}] | Session:{id(self.session)}] | Url:[{self.url}]>"

    def _make_params(self, *args, **kwargs):
        self.url = args[0]
        self.args = args[1:]

        kwargs.setdefault("headers", Head().randua)
        kwargs.setdefault("timeout", ClientTimeout(TIMEOUT))  # @超时
        self.cookies = kwargs.pop("cookies", {})
        self.callback = kwargs.pop("callback", None)
        self.kwargs = kwargs
        return self

    def run(self):
        return asyncio.run(_async_fetch(self))

    async def start(self):
        """主线程"""
        return await _async_fetch(self)


async def _async_fetch(self):
    """单任务和多任务均调用此方法"""

    @TRETRY
    async def _fetch_run():
        async with TCPConnector(ssl=False) as Tconn, ClientSession(
            cookies=self.cookies, connector=Tconn
        ) as self.session, self.session.request(
            self.method, self.url, raise_for_status=True, *self.args, **self.kwargs
        ) as self.response:
            self.content = await self.response.read()
            return self.response, self.content, self.index

    try:
        await _fetch_run()
    except Exception as err:
        print(f"Async_fetch:{self} | RetryErr:{err!r}")
        self.response = self.content = None
        self.result = err
        return self
    else:
        # #返回结果,不管是否正确
        self.result = htmlResponse(self.response, self.content, index=self.index)
        if self.callback:
            self.result = self.callback(self.result)
        return self.result


async def create_gather_task(tasks):
    """异步单线程,使用同一个session"""
    new_tasks = []
    for index, task in enumerate(tasks, 1):
        task.index = index
        _coroutine = task.start()
        new_tasks.append(_coroutine)
    return await asyncio.gather(*new_tasks, return_exceptions=True)


async def create_threads_task(coroes):
    """异步多线程,使用不同session"""
    threadsafe_loop = asyncio.new_event_loop()
    Thread(target=threadsafe_loop.run_forever, name="ThreadSafe", daemon=True).start()

    new_tasks = []
    for index, coro in enumerate(coroes, 1):
        coro.index = index
        _coroutine = coro.start()
        new_tasks.append(asyncio.run_coroutine_threadsafe(_coroutine, threadsafe_loop))

    return [task.result() for task in new_tasks]


def aiohttp_parse(method, url, *args, **kwargs):
    task = eval(method)(url, *args, **kwargs)
    _coroutine = task.start()
    loop = asyncio.new_event_loop()  # asyncio.get_event_loop()
    return loop.run_until_complete(_coroutine)


def aiohttp__issue(method, urls, *args, **kwargs):
    coroes = [eval(method)(url, *args, **kwargs) for url in urls]
    _coroutine = (
        create_threads_task(coroes)
        if kwargs.pop("threadsafe", True)
        else create_gather_task(coroes)
    )
    # return asyncio.run(_coroutine)  # 3.7+ 方式 , threadsafe:单线程或者多线程
    loop = asyncio.new_event_loop()  # asyncio.get_event_loop()
    return loop.run_until_complete(_coroutine)


ahttpGet = partial(aiohttp_parse, "get")
ahttpPost = partial(aiohttp_parse, "post")
ahttpGetAll = partial(aiohttp__issue, "get")
ahttpPostAll = partial(aiohttp__issue, "post")

if __name__ == "__main__":
    url_get = "https://httpbin.org/get"
    url_post = "https://httpbin.org/post"
    url_headers = "https://httpbin.org/headers"

    # res = ahttpPost(url_post, data=b'data')

    res = ahttpGet(url_get)
    print(res)
    res = ahttpGetAll([url_headers, url_get])
    print(res)
    #######################################################################################################
    print(get("http://httpbin.org/headers").run().headers)
    # print(put('http://httpbin.org/put', data=b'data').start())
    # print(delete('http://httpbin.org/delete').start())
    # print(options('http://httpbin.org/get').start().headers)
    # #'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
    # print(trace('http://www.baidu.com').start().headers)
    # print(connect('http://www.baidu.com').start())
    # print(patch('http://httpbin.org/patch', data=b'data').start())
