# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-06-27 15:49:06
LastEditTime : 2024-06-28 12:59:21
FilePath     : /CODE/xjLib/xt_AhttpClent.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import asyncio

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from tenacity import retry, stop_after_attempt, wait_random
from xt_head import MYHEAD, RETRY_TIME, TIMEOUT
from xt_log import log_decorator
from xt_response import ACResponse

TRETRY = retry(
    reraise=True,  # 保留最后一次错误
    stop=stop_after_attempt(RETRY_TIME),
    wait=wait_random(min=0, max=1),
)
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


class AioHttpClient:
    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop_policy().new_event_loop()
        asyncio.set_event_loop(self.loop)
        self._session = self.loop.run_until_complete(self.create_session())
        self.cookies = {}

    async def create_session(self):
        if self._session is None:
            self._session = ClientSession(
                cookies=self.cookies, connector=TCPConnector(ssl=False)
            )
        return self._session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """关闭会话"""
        self.close()

    def __del__(self):
        self.close()
        self.loop.close()

    async def close_session(self):
        if self._session is not None:
            await self._session.close()
            self._session = None

    def close(self):
        self.loop.run_until_complete(self.close_session())

    def __getitem__(self, method):
        if method.lower() in Method_List:
            self.method = method.lower()  # 保存请求方法
            return lambda *args, **kwargs: self._make_method(*args, **kwargs)

    def __getattr__(self, method):
        if method.lower() in Method_List:
            self.method = method.lower()  # 保存请求方法
            return self._make_method  # 调用方法

    def _make_method(self, *args, **kwargs):
        return self.loop.run_until_complete(self.request(*args, **kwargs))

    @log_decorator
    async def request(self, url, index=None, *args, **kwargs):
        kwargs.setdefault("headers", MYHEAD)
        kwargs.setdefault("timeout", ClientTimeout(TIMEOUT))
        callback = kwargs.pop("callback", None)
        index = index or id(url)

        @TRETRY
        async def __fetch():
            Session = await self.create_session()
            async with Session.request(
                self.method, url, raise_for_status=True, *args, **kwargs
            ) as response:
                content = await response.content.read()
                return response, content, index

        try:
            response, content, index = await __fetch()
            result = ACResponse(response, content, index)
            return callback(result) if callable(callback) else result
        except Exception as err:
            print(f"AioHttpClient:{self} | RetryErr:{err!r}")
            return ACResponse("", err, index)

    def getall(self, *args, **kwargs):
        self.method = "get"  # 保存请求方法
        task_list = [
            self.request(*arg, index=index, **kwargs)
            for index, arg in enumerate(list(zip(*args)), start=1)
        ]
        return self.loop.run_until_complete(
            asyncio.gather(*task_list, return_exceptions=True)
        )

    def postall(self, *args, **kwargs):
        self.method = "post"  # 保存请求方法
        task_list = [
            self.request(*arg, index=index, **kwargs)
            for index, arg in enumerate(list(zip(*args)), start=1)
        ]
        return self.loop.run_until_complete(
            asyncio.gather(*task_list, return_exceptions=True)
        )


if __name__ == "__main__":
    url = "https://httpbin.org/get"
    with AioHttpClient() as AHC:
        # res = AHC.get(url)
        # print(111111, res.headers)
        res = AHC.getall([url, url, "https://www.bigee.cc/book/6909/2.html"])
        print(222222, res)
    # AHC = AioHttpClient()
    # res = AHC.GET(url)
    # print(333333, res.headers)
    # res = AHC.GET(url)
    # print(444444, res.status)
