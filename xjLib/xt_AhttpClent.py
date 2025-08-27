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
from typing import Callable, List, Optional

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
    """异步HTTP客户端，基于aiohttp实现，支持重试、超时和并发请求"""

    def __init__(self):
        self.method: str = ""  # 保存请求方法
        # 获取或创建事件循环
        try:
            self._loop = asyncio.get_running_loop()
        except RuntimeError:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
        self._session: Optional[ClientSession] = None
        try:
            self._session = self._loop.run_until_complete(self.create_session())
        except Exception as e:
            print(f"Failed to create session: {e}")
            self._session = None

    async def __aenter__(self):
        """异步上下文管理器入口"""
        self._session = await self.create_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出，确保会话关闭"""
        if self._session:
            await self._session.close()
            self._session = None

    async def create_session(self) -> ClientSession:
        """创建并返回一个配置好的ClientSession"""
        return ClientSession(
            connector=TCPConnector(ssl=False),
            timeout=ClientTimeout(total=TIMEOUT),
        )

    async def close_session(self) -> None:
        """异步关闭会话"""
        if self._session is not None:
            await self._session.close()
            self._session = None

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        """关闭会话"""
        self._loop.run_until_complete(self.close_session())

    def close(self) -> None:
        """同步关闭方法"""
        if self._session and not self._session.closed:
            try:
                self._loop.run_until_complete(self._session.close())
            except RuntimeError:
                # 如果事件循环已关闭，创建新的循环执行关闭
                _loop = asyncio.new_event_loop()
                asyncio.set_event_loop(_loop)
                _loop.run_until_complete(self._session.close())
                _loop.close()
            finally:
                self._session = None

    def __del__(self):
        """析构函数，确保资源释放"""
        self.close()

    def __getitem__(self, method: str) -> Callable:
        self.method = method.lower()  # 保存请求方法
        return self._make_parse

    def __getattr__(self, method: str) -> Callable:
        return self.__getitem__(method)

    def _make_parse(self, url: str, **kwargs) -> ACResponse:
        index = kwargs.pop("index", id(url))
        try:
            return self._loop.run_until_complete(
                self._retry_request(url, index=index, **kwargs)
            )
        except Exception as e:
            print(f"Request failed: {e}")
            return ACResponse(None, str(e).encode(), index)

    @log_catch_decor  # type:ignore
    async def _retry_request(
        self, url: str, index: Optional[int] = None, **kwargs
    ) -> ACResponse:
        kwargs.setdefault("headers", Head().randua)
        kwargs.setdefault("timeout", ClientTimeout(TIMEOUT))
        index = index or id(url)
        _ = kwargs.pop("callback", None)

        @TRETRY
        async def _single_fetch() -> tuple:
            if self._session is None:
                self._session = await self.create_session()
            async with self._session.request(
                self.method, url, raise_for_status=True, **kwargs
            ) as response:
                content = await response.content.read()
                return response, content

        try:
            response, content = await _single_fetch()
            result = ACResponse(response, content, index)
            return result
        except Exception as err:
            err_str = f"AioHttpClient:{self} | URL:{url} | RetryErr:{err!r}"
            print(err_str)
            return ACResponse(None, err_str.encode(), index)

    async def _multi_fetch(self, method: str, urls_list: List[str], **kwargs):
        self.method = method
        task_list = [
            self._retry_request(url, index=index, **kwargs)
            for index, url in enumerate(urls_list, start=1)
        ]
        return await asyncio.gather(*task_list, return_exceptions=True)

    def getall(self, urls_list: List[str], **kwargs):
        return self._loop.run_until_complete(
            self._multi_fetch("get", urls_list, **kwargs)
        )

    def postall(self, urls_list: List[str], **kwargs):
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
