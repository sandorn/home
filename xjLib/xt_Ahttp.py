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

## 异步请求，多任务数量过大可能导致大量请求失败，建议分批次请求
import asyncio
import selectors
from functools import partial

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from xt_head import TIMEOUT, TRETRY, Head
from xt_log import log_decor
from xt_response import ACResponse
from xt_retry import retry_log_wrapper


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
        """执行单任务"""

        @TRETRY
        async def _fetch():
            async with ClientSession(
                cookies=self.cookies, connector=TCPConnector()
            ) as session, session.request(
                self.method, self.url, raise_for_status=True, *self.args, **self.kwargs
            ) as response:
                content = await response.content.read()
                return response, content

        try:
            response, content = await _fetch()
            _result = ACResponse(response, content, self.index)
            return self.callback(_result) if callable(self.callback) else _result
        except Exception as err:
            print(err_str := f"Async_fetch:{self} | RetryErr:{err!r}")
            return ACResponse(None, err_str.encode(), self.index)

    @retry_log_wrapper()
    async def run(self, clent):
        """执行多任务,使用同一session"""
        async with clent.request(
            self.method, self.url, raise_for_status=True, *self.args, **self.kwargs
        ) as response:
            content = await response.content.read()
            _result = ACResponse(response, content, self.index)
            return self.callback(_result) if callable(self.callback) else _result


def single_parse(method, url, *args, **kwargs):
    """构建并运行单任务"""
    if method.lower() not in request_methods:
        return ACResponse(
            None, f"Method:{method} not in {request_methods}".encode(), id(url)
        )

    task = getattr(AsyncTask(), method)(url, *args, **kwargs)
    return asyncio.run(task.start())


ahttpGet = partial(single_parse, "get")
ahttpPost = partial(single_parse, "post")


async def _multi_fetch(method, urls, *args, **kwargs):
    """构建并运行多任务"""
    tasks_list = [
        getattr(AsyncTask(index), method)(url, *args, **kwargs)
        for index, url in enumerate(urls, start=1)
    ]

    """异步,相同session"""
    async with ClientSession(connector=TCPConnector()) as clent:
        return await asyncio.gather(
            *[task.run(clent) for task in tasks_list], return_exceptions=True
        )


def multi_parse(method, urls, *args, **kwargs):
    """发起多任务"""
    return asyncio.run(_multi_fetch(method, urls, *args, **kwargs))  # , debug=True)


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

    def main():
        print(111111111111111111111, ahttpGetAll([urls[0], urls[1]] * 3))
        # print(222222222222222222222, ahttpPost(urls[2], data=b"data"))
        # print(333333333333333333333, res := ahttpGet(urls[0]))
        # print("xpath-1".ljust(10), ":", res.xpath(elestr))
        # print("xpath-2".ljust(10), ":", res.xpath([elestr, elestr]))
        # print(
        #     "blank".ljust(10),
        #     ":",
        #     res.xpath(["", " ", " \t", " \n", " \r", " \r\n", " \n\r", " \r\n\t"]),
        # )
        # print("dom".ljust(10), ":", res.dom.xpath(elestr), res.dom.url)
        # print("query".ljust(10), ":", res.query("title").text())
        # print("element".ljust(10), ":", res.element.xpath(elestr), res.element.base)
        # print("html".ljust(10), ":", res.html.xpath(elestr), res.html.base_url)

    main()
