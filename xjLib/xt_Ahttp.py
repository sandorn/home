# !/usr/bin/env python
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
from tenacity import retry, stop_after_attempt, wait_random
from xt_Head import RETRY_TIME, TIMEOUT, Head
from xt_Log import log_decorator
from xt_Response import htmlResponse

TRETRY = retry(
    reraise=True,  # 保留最后一次错误
    stop=stop_after_attempt(RETRY_TIME),
    wait=wait_random(min=0, max=1),
)

__all__ = ("ahttpGet", "ahttpGetAll", "ahttpPost", "ahttpPostAll")

Method_List = ["get", "post", "head", "options", "put", "delete", "trace", "connect", "patch"]


class AsyncTask:
    def __init__(self):
        self.index = id(self)

    def __getitem__(self, method):
        if method.lower() in Method_List:
            self.method = method.lower()  # 保存请求方法
            return lambda *args, **kwargs: self.__create_params(*args, **kwargs)

    def __getattr__(self, method):
        if method.lower() in Method_List:
            self.method = method.lower()  # 保存请求方法
            return self.__create_params  # @ 设置参数

    def __repr__(self):
        return f"《 AsyncTask | Method:[{self.method}] | Index:[{self.index}] | URL:[{self.url}] 》"

    def __create_params(self, *args, **kwargs):
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


@log_decorator
async def _async_fetch(self):
    """单任务和多任务均调用此方法"""

    @TRETRY
    async def _fetch_run():
        async with TCPConnector(ssl=False) as Tconn, ClientSession(cookies=self.cookies, connector=Tconn) as self.session, self.session.request(self.method, self.url, raise_for_status=True, *self.args, **self.kwargs) as self.response:
            self.content = await self.response.read()
            return self.response, self.content, self.index

    try:
        await _fetch_run()
        _result = htmlResponse(self.response, self.content, index=self.index)
        self.result = self.callback(self.result) if callable(self.callback) else _result
        return self.result
    except Exception as err:
        print(f"Async_fetch:{self} | RetryErr:{err!r}")
        self.response = self.content = None
        self.result = htmlResponse("", err, index=self.index)
        return self.result


def __session_method(method, *args, **kwargs):
    return getattr(AsyncTask(), method)(*args, **kwargs)


def __parse(method, url, *args, **kwargs):
    """单任务"""
    task = partial(__session_method, method)(url, *args, **kwargs)
    _coroutine = task.start()
    loop = asyncio.new_event_loop()
    return loop.run_until_complete(_coroutine)


ahttpGet = partial(__parse, "get")
ahttpPost = partial(__parse, "post")


async def create_gather_task(tasks):
    """异步,使用不同session"""
    tasks_list = []
    for index, task in enumerate(tasks, 1):
        task.index = index
        _coroutine = task.start()
        tasks_list.append(_coroutine)
    return await asyncio.gather(*tasks_list, return_exceptions=True)


async def create_threads_task(tasks):
    """异步线程安全,使用不同session"""
    threadsafe_loop = asyncio.new_event_loop()
    Thread(target=threadsafe_loop.run_forever, name="ThreadSafe", daemon=True).start()

    tasks_list = []
    for index, task in enumerate(tasks, start=1):
        task.index = index
        _coroutine = task.start()
        tasks_list.append(asyncio.run_coroutine_threadsafe(_coroutine, threadsafe_loop))

    return [task.result() for task in tasks_list]


def __gather_parse(method, urls, *args, **kwargs):
    """多任务"""
    # coroes = [AsyncTask()[method](url, *args, **kwargs) for url in urls]
    coroes = [partial(__session_method, method)(url, *args, **kwargs) for url in urls]
    _coroutine = create_threads_task(coroes) if kwargs.pop("threadsafe", True) else create_gather_task(coroes)
    return asyncio.run(_coroutine)


ahttpGetAll = partial(__gather_parse, "get")
ahttpPostAll = partial(__gather_parse, "post")

if __name__ == "__main__":
    url1 = "http://www.163.com"
    url_get = "https://httpbin.org/get"
    url_post = "https://httpbin.org/post"
    url_headers = "https://httpbin.org/headers"

    # res = ahttpGet(url_get)
    # print(res)
    # res = ahttpPost(url_post, data=b'data')
    # print(res)
    res = ahttpGetAll([url_headers, url_get])
    print(res)
