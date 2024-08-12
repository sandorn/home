# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-08-08 12:13:33
FilePath     : /CODE/xjLib/xt_ahttp.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import asyncio
from functools import partial
from threading import Thread

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from tenacity import retry, stop_after_attempt, wait_random
from xt_head import RETRY_TIME, TIMEOUT, Head
from xt_log import log_decorator
from xt_response import ACResponse

TRETRY = retry(
    reraise=True,  # 保留最后一次错误
    stop=stop_after_attempt(RETRY_TIME),
    wait=wait_random(min=0, max=1),
)

__all__ = ("ahttpGet", "ahttpGetAll", "ahttpPost", "ahttpPostAll")

Method_List = [
    "get",
    "post",
    "head",
    "options",
    "put",
    "delete",
    "trace",
    "connect",
    "patch",
]


class AsyncTask:
    """aiohttp异步任务"""

    def __init__(self, index=None):
        self.index = index or id(self)

    def __getitem__(self, method):
        if method.lower() in Method_List:
            self.method = method.lower()  # 保存请求方法
            return self._make_method  # 调用方法
            # return lambda *args, **kwargs: self._make_method(*args, **kwargs)

    def __getattr__(self, method):
        return self.__getitem__(method)

    def __repr__(self):
        return f"AsyncTask | Method:[{self.method}] | Index:[{self.index}] | URL:[{self.url}]"

    def _make_method(self, *args, **kwargs):
        self.url = args[0]
        self.args = args[1:]
        kwargs.setdefault("headers", Head().randua)
        kwargs.setdefault("timeout", ClientTimeout(TIMEOUT))  # @超时
        self.cookies = kwargs.pop("cookies", {})
        self.callback = kwargs.pop("callback", None)
        self.kwargs = kwargs
        return self

    async def start(self):
        """
        执行核心操作
        """
        return await _async_fetch(self)


@log_decorator
async def _async_fetch(self):
    """
    核心操作,单任务和多任务均调用
    """

    @TRETRY
    async def _retryable_request():
        async with TCPConnector(ssl=False) as Tconn, ClientSession(
            cookies=self.cookies, connector=Tconn
        ) as self.session, self.session.request(
            self.method, self.url, raise_for_status=True, *self.args, **self.kwargs
        ) as self.response:
            self.content = await self.response.read()
            self.response.text = await self.response.text()
            return self.response, self.content, self.index

    try:
        await _retryable_request()
        _result = ACResponse(self.response, self.content, self.index)
        self.result = self.callback(_result) if callable(self.callback) else _result
        return self.result
    except Exception as err:
        print(f"Async_fetch:{self} | RetryErr:{err!r}")
        self.result = ACResponse("", str(err), index=self.index)
        return self.result


def __session_method(method, *args, **kwargs):
    """构建任务"""
    return getattr(AsyncTask(), method)(*args, **kwargs)


def __parse(method, url, *args, **kwargs):
    """发起单任务"""
    task = partial(__session_method, method)(url, *args, **kwargs)
    return asyncio.run(task.start())
    # _coroutine = task.start()
    # loop = asyncio.new_event_loop()
    # return loop.run_until_complete(_coroutine)


ahttpGet = partial(__parse, "get")
ahttpPost = partial(__parse, "post")


async def __create_thread_task(tasks):
    """不推荐，异步，子线程,用不同session"""
    thread_loop = asyncio.new_event_loop()
    Thread(target=thread_loop.run_forever, name="ThreadSafe", daemon=True).start()

    future_list = []
    for index, task in enumerate(tasks, start=1):
        task.index = index
        future_list.append(asyncio.run_coroutine_threadsafe(task.start(), thread_loop))

    return [future.result() for future in future_list]


async def __create_gather_task(tasks):
    """异步,使用不同session"""
    future_list = []
    for index, task in enumerate(tasks, 1):
        task.index = index
        future_list.append(task.start())
    return await asyncio.gather(*future_list, return_exceptions=True)


def __gather_parse(method, urls, *args, **kwargs):
    """发起多任务"""
    coroes = [partial(__session_method, method)(url, *args, **kwargs) for url in urls]
    task_method = (
        __create_thread_task if kwargs.pop("thread", False) else __create_gather_task
    )
    return asyncio.run(task_method(coroes))


ahttpGetAll = partial(__gather_parse, "get")
ahttpPostAll = partial(__gather_parse, "post")

if __name__ == "__main__":
    url1 = "http://www.163.com"
    url_get = "https://httpbin.org/get"
    url_post = "https://httpbin.org/post"
    url_headers = "https://httpbin.org/headers"

    res = ahttpGet(url_get)
    print(res)
    # res = ahttpPost(url_post, data=b"data")
    # print(res)

    def handle_back_ait(resp):
        if isinstance(resp, ACResponse):
            return resp

    res = ahttpGetAll([url_headers, url_get], callback=handle_back_ait)
    print(res)
