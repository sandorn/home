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
import sys
from functools import partial
from threading import Thread

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from xt_head import TIMEOUT, TRETRY, Head
from xt_log import log_catch_decor
from xt_response import ACResponse

__all__ = ("ahttpGet", "ahttpGetAll", "ahttpPost", "ahttpPostAll")

Method_List = (
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
    """aiohttp异步任务"""

    cfg_flag = False

    def __init__(self, index=None):
        self.index = index or id(self)
        self.result = None
        self.set_config()

    def __getitem__(self, method):
        if method.lower() in Method_List:
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

    @log_catch_decor
    async def start(self):
        """执行核心操作,单任务和多任务均调用"""

        @TRETRY
        async def _fetch_run():
            async with ClientSession(
                cookies=self.cookies, connector=TCPConnector()
            ) as session, session.request(
                self.method, self.url, raise_for_status=True, *self.args, **self.kwargs
            ) as response:
                content = await response.content.read()
                return response, content

        try:
            response, content = await _fetch_run()
            _result = ACResponse(response, content, self.index)
            return self.callback(_result) if callable(self.callback) else _result

        except Exception as err:
            print(err_str := f"Async_fetch:{self} | RetryErr:{err!r}")
            return ACResponse(None, err_str.encode(), self.index)

    @staticmethod
    def set_config():
        if sys.platform == "win32" and not AsyncTask.cfg_flag:
            print("asyncio - on windows aiodns needs SelectorEventLoop")
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            AsyncTask.cfg_flag = True


def create_task(method, url, index=None, *args, **kwargs):
    """构建任务"""
    if method.lower() not in Method_List:
        return ACResponse(
            None, f"Method:{method} not in {Method_List}".encode(), id(url)
        )

    return getattr(AsyncTask(index), method)(url, *args, **kwargs)


def __parse(method, url, *args, **kwargs):
    """发起单任务"""
    task = partial(create_task, method)(url, *args, **kwargs)
    coro = task.start()
    return asyncio.run(coro)


ahttpGet = partial(__parse, "get")
ahttpPost = partial(__parse, "post")


async def __run_many_parse(tasks_list, channel=None):
    coro_list = []
    for index, task in enumerate(tasks_list, start=1):
        task.index = index
        coro_list.append(task.start())

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


def _many_parse(method, urls, *args, **kwargs):
    """发起多任务"""
    tasks_list = [partial(create_task, method)(url, *args, **kwargs) for url in urls]
    return asyncio.run(__run_many_parse(tasks_list))


ahttpGetAll = partial(_many_parse, "get")
ahttpPostAll = partial(_many_parse, "post")

if __name__ == "__main__":
    url1 = "https://www.163.com"
    url_get = "https://httpbin.org/get"
    url_post = "https://httpbin.org/post"
    url_headers = "https://httpbin.org/headers"

    # print(1111111111111111,  ahttpGet(url_get))

    # print(2222222222222222,  ahttpPost(url_post, data=b"data"))

    def handle_back_ait(resp):
        """help"""
        if isinstance(resp, ACResponse):
            return resp

    print(
        3333333333333333,
        ahttpGetAll([url_headers, url_get, url1], callback=handle_back_ait),
    )

    def main():
        urls = [
            "http://www.baidu.com",
            "http://www.163.com",
            "http://dangdang.com",
            "https://httpbin.org",
            # "https://www.google.com",
        ]
        print(111111111111111111111, ahttpGetAll(urls))
        print(222222222222222222222, ahttpPost(url_post, data=b"data"))
        print(333333333333333333333, res := ahttpGet(urls[1]))
        print("xpath-1".ljust(10), ":", res.xpath("//title/text()"))
        print("xpath-2".ljust(10), ":", res.xpath(["//title/text()", "//title/text()"]))
        print(
            "blank".ljust(10),
            ":",
            res.xpath(["", " ", " \t", " \n", " \r", " \r\n", " \n\r", " \r\n\t"]),
        )
        print("dom".ljust(10), ":", res.dom.xpath("//title/text()"))
        print("element".ljust(10), ":", res.element.xpath("//title/text()"))
        print("html".ljust(10), ":", res.html.xpath("//title/text()"))
        print("query".ljust(10), ":", res.query("title").text())
        print("text".ljust(10), ":", res.text[1000:1300])

    # main()
