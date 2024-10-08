# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-10-07 10:40:07
FilePath     : /CODE/xjLib/xt_ahttp.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import asyncio
import selectors
import sys
from functools import partial
from threading import Thread

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from xt_head import TIMEOUT, TRETRY, Head
from xt_log import log_decor
from xt_response import ACResponse


class MyPolicy(asyncio.DefaultEventLoopPolicy):
    def new_event_loop(self):
        selector = selectors.SelectSelector()
        return asyncio.SelectorEventLoop(selector)


asyncio.set_event_loop_policy(MyPolicy())

__all__ = ("ahttpGet", "ahttpGetAll", "ahttpPost", "ahttpPostAll")

request_methods = (
    "get",
    "post",
    "head",
    "options",
    "put",
    "delete",
    "trace",
    "connect",
    "patch",
)


class AsyncTask:
    """aiohttp异步任务原型"""

    def __init__(self, index=None):
        self.index = index or id(self)

    def __getitem__(self, method):
        if method.lower() in request_methods:
            self.method = method.lower()  # 保存请求方法
            return self._make_parse  # 调用方法
            # return lambda *args, **kwargs: self._make_parse(*args, **kwargs)

    def __getattr__(self, method):
        return self.__getitem__(method)

    def __repr__(self):
        return f"AsyncTask | Method:[{self.method}] | Index:[{self.index}] | URL:[{self.url}]"

    def _make_parse(self, url, *args, **kwargs):
        self.url = url
        self.args = args
        kwargs.setdefault("headers", Head().randua)
        kwargs.setdefault("timeout", ClientTimeout(TIMEOUT))
        self.cookies = kwargs.pop("cookies", {})
        self.callback = kwargs.pop("callback", None)
        self.kwargs = kwargs
        return self

    @log_decor
    async def start(self):
        """执行核心操作,单任务和多任务均调用"""

        @TRETRY
        async def _single_fetch():
            async with ClientSession(
                cookies=self.cookies, connector=TCPConnector()
            ) as session, session.request(
                self.method, self.url, raise_for_status=True, *self.args, **self.kwargs
            ) as response:
                content = await response.content.read()
                return response, content

        try:
            response, content = await _single_fetch()
            _result = ACResponse(response, content, self.index)
            return self.callback(_result) if callable(self.callback) else _result
        except Exception as err:
            print(err_str := f"Async_fetch:{self} | RetryErr:{err!r}")
            return ACResponse(None, err_str.encode(), self.index)

    @staticmethod
    def set_config() -> None:
        if sys.platform == "win32":
            print("asyncio - on windows aiodns needs SelectorEventLoop")
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def single_parse(method, url, *args, **kwargs):
    """构建并运行单任务"""
    if method.lower() not in request_methods:
        return ACResponse(
            None, f"Method:{method} not in {request_methods}".encode(), id(url)
        )

    task = getattr(AsyncTask(), method)(url, *args, **kwargs)
    coro = task.start()
    return asyncio.run(coro)


ahttpGet = partial(single_parse, "get")
ahttpPost = partial(single_parse, "post")


async def _multi_fetch(method, urls, *args, channel=None, **kwargs):
    """构建并运行多任务"""
    tasks_list = [
        getattr(AsyncTask(index), method)(url, *args, **kwargs)
        for index, url in enumerate(urls, start=1)
    ]
    coro_list = [task.start() for task in tasks_list]

    if channel == "thread":
        """异步，子线程,不同session,不推荐"""
        _child_thread_loop = asyncio.new_event_loop()
        Thread(
            target=_child_thread_loop.run_forever, name="ThreadSafe", daemon=True
        ).start()
        future_list = [
            asyncio.run_coroutine_threadsafe(coro, _child_thread_loop)
            for coro in coro_list
        ]
        return [future.result() for future in future_list]
    else:
        """异步,不同session"""
        return await asyncio.gather(*coro_list, return_exceptions=True)


def multi_parse(method, urls, *args, **kwargs):
    """发起多任务"""
    return asyncio.run(_multi_fetch(method, urls, *args, **kwargs))


ahttpGetAll = partial(multi_parse, "get")
ahttpPostAll = partial(multi_parse, "post")

if __name__ == "__main__":
    urls = [
        "https://www.163.com",
        "https://httpbin.org/get",
        "https://httpbin.org/post",
        "https://httpbin.org/headers",
        "https://www.google.com",
    ]
    elestr = "//title/text()"

    def handle_back_ait(resp):
        if isinstance(resp, ACResponse):
            return resp

    def main():
        print(
            111111111111111111111,
            ahttpGetAll([urls[0], urls[1], urls[3]], callback=handle_back_ait),
        )
        print(222222222222222222222, ahttpPost(urls[2], data=b"data"))
        print(333333333333333333333, res := ahttpGet(urls[0]))
        print("xpath-1".ljust(10), ":", res.xpath(elestr))
        print("xpath-2".ljust(10), ":", res.xpath([elestr, elestr]))
        print(
            "blank".ljust(10),
            ":",
            res.xpath(["", " ", " \t", " \n", " \r", " \r\n", " \n\r", " \r\n\t"]),
        )
        print("dom".ljust(10), ":", res.dom.xpath(elestr), res.dom.url)
        print("query".ljust(10), ":", res.query("title").text())
        print("element".ljust(10), ":", res.element.xpath(elestr), res.element.base)
        print("html".ljust(10), ":", res.html.xpath(elestr), res.html.base_url)

    main()
