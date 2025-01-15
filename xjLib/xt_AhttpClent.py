# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-06-27 15:49:06
LastEditTime : 2024-06-28 13:30:00
FilePath     : /d:/CODE/xjLib/xt_ahttpclent.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import asyncio
import selectors

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from xt_head import TIMEOUT, TRETRY, Head
from xt_log import log_catch_decor
from xt_response import ACResponse


class MyPolicy(asyncio.DefaultEventLoopPolicy):
    def new_event_loop(self):
        selector = selectors.SelectSelector()
        return asyncio.SelectorEventLoop(selector)


asyncio.set_event_loop_policy(MyPolicy())


class AioHttpClient:
    def __init__(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._session = self._loop.run_until_complete(self.create_session())

    async def create_session(self):
        return ClientSession(connector=TCPConnector(ssl=False))

    async def close_session(self):
        if hasattr(self, "_session") and self._session is not None:
            await self._session.close()
            self._session = None

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        """关闭会话"""
        self._loop.run_until_complete(self.close_session())

    def __del__(self):
        """关闭会话"""
        self._loop.run_until_complete(self.close_session())

    def __getitem__(self, method):
        self.method = method.lower()  # 保存请求方法
        return self._make_parse  # 调用方法
        # return lambda *args, **kwargs: self._make_parse(*args, **kwargs)

    def __getattr__(self, method):
        return self.__getitem__(method)

    def _make_parse(self, url, **kwargs):
        index = kwargs.pop("index", id(url))
        return self._loop.run_until_complete(
            self._retry_request(url, index=index, **kwargs)
        )

    @log_catch_decor  # type:ignore
    async def _retry_request(self, url, index=None, **kwargs):
        kwargs.setdefault("headers", Head().randua)
        kwargs.setdefault("timeout", ClientTimeout(TIMEOUT))
        callback = kwargs.pop("callback", None)
        index = index or id(url)

        @TRETRY
        async def _single_fetch():
            async with self._session.request(  # type:ignore
                self.method, url, raise_for_status=True, **kwargs
            ) as response:
                content = await response.content.read()
                return response, content

        try:
            response, content = await _single_fetch()
            result = ACResponse(response, content, index)
            return callback(result) if callable(callback) else result
        except Exception as err:
            print(err_str := f"AioHttpClient:{self} | URL:{url} | RetryErr:{err!r}")
            return ACResponse(None, err_str.encode(), index)

    async def _multi_fetch(self, method, urls_list, **kwargs):
        self.method = method
        task_list = [
            self._retry_request(url, index=index, **kwargs)
            for index, url in enumerate(urls_list, start=1)
        ]
        return await asyncio.gather(*task_list, return_exceptions=True)

    def getall(self, urls_list, **kwargs):
        return self._loop.run_until_complete(
            self._multi_fetch("get", urls_list, **kwargs)
        )

    def postall(self, urls_list, **kwargs):
        return self._loop.run_until_complete(
            self._multi_fetch("post", urls_list, **kwargs)
        )


if __name__ == "__main__":
    url = "https://httpbin.org/get"
    AHC = AioHttpClient()
    res = AHC.get(url)
    print(111111, res)
    res = AHC.getall([url, "https://www.bigee.cc/book/6909"])
    print(222222, res)
