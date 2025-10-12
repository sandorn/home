# !/usr/bin/env python
"""
==============================================================
Description  : 异步HTTP请求模块 - 提供基于aiohttp的高性能异步HTTP客户端功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2025-09-07 10:00:00
FilePath     : /CODE/xjlib/xt_ahttp.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能:
- 基于aiohttp的异步HTTP请求客户端实现
- 支持单任务和批量任务的执行
- 并发控制与限制机制
- 统一的响应处理和错误管理
- 自动重试和日志记录功能

主要组件:
- AsyncHttpClient: 支持并发控制的异步HTTP客户端
- AsyncTask: 封装HTTP请求参数和执行逻辑的任务原型
- 快捷函数: ahttp_get/ahttp_post/ahttp_get_all/ahttp_post_all

使用场景:
- 高并发Web请求场景
- 批量数据采集和API调用
- 需要性能优化的爬虫系统
==============================================================
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from functools import partial

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from nswrapslite.exception import _handle_exception as handle_exception
from nswrapslite.log import logging_wraps as log_wraps
from nswrapslite.retry import retry_wraps
from xt_head import TIMEOUT, Head
from xt_response import ACResponse

# 定义模块公开接口
__all__ = ('AsyncHttpClient', 'ahttp_get', 'ahttp_get_all', 'ahttp_post', 'ahttp_post_all')

# 定义支持的HTTP请求方法
REQUEST_METHODS = ('get', 'post', 'head', 'options', 'put', 'delete', 'trace', 'connect', 'patch')


class AsyncHttpClient:
    """异步HTTP客户端 - 提供并发控制的HTTP请求管理

    该类实现了并发请求控制、会话共享和批量请求处理,
    适合需要高效执行大量HTTP请求的场景。
    """

    def __init__(self, max_concurrent: int = 10):
        """初始化异步HTTP客户端

        Args:
            max_concurrent: 最大并发请求数,默认为10,控制同时发起的请求数量
        """
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def request(self, method: str, url: str, *args, **kwargs) -> ACResponse:
        """执行单个HTTP请求

        Args:
            method: HTTP方法,如'get'、'post'等
            url: 请求的目标URL
            *args: 传递给aiohttp.ClientSession.request的额外位置参数
            **kwargs: 传递给aiohttp.ClientSession.request的额外关键字参数
                - headers: 请求头信息,默认为自动生成的随机User-Agent
                - timeout: 请求超时时间,默认为TIMEOUT常量
                - cookies: Cookie信息
                - callback: 响应处理的回调函数
                - data/json: 请求体数据
                - params: URL查询参数

        Returns:
            ACResponse: 包含响应状态、头部和内容的统一响应对象
        """
        task = getattr(AsyncTask(), method)(url, *args, **kwargs)
        async with self.semaphore:
            return await task.start()

    async def request_multi(self, method: str, urls: list[str], *args, **kwargs) -> list[ACResponse | Exception]:
        """批量执行HTTP请求(共享会话方式)

        特点:使用共享的TCP连接器和ClientSession,大幅减少连接建立的开销

        Args:
            method: HTTP方法,如'get'、'post'等
            urls: 要请求的URL列表
            *args: 传递给每个请求的额外位置参数
            **kwargs: 传递给每个请求的额外关键字参数

        Returns:
            list[Union[ACResponse, Exception]]: 响应对象或异常的列表
        """
        tasks = [AsyncTask(index)[method](url, *args, **kwargs) for index, url in enumerate(urls)]

        async with ClientSession(
            connector=TCPConnector(ssl=False, limit=self.max_concurrent),
            timeout=ClientTimeout(total=TIMEOUT),
        ) as client:
            return await asyncio.gather(*[task.multi_start(client) for task in tasks], return_exceptions=True)

    async def request_batch(self, method: str, urls: list[str], *args, **kwargs) -> list[ACResponse | Exception]:
        """批量执行HTTP请求(分批处理方式)

        特点:将请求分成多个批次执行,每批次不超过max_concurrent个请求

        Args:
            method: HTTP方法
            urls: 要请求的URL列表
            *args: 传递给每个请求的额外位置参数
            **kwargs: 传递给每个请求的额外关键字参数

        Returns:
            list[Union[ACResponse, Exception]]: 响应对象或异常的列表
        """
        tasks = [AsyncTask(index)[method](url, *args, **kwargs) for index, url in enumerate(urls)]

        results = []
        # 分批处理,避免同时发起过多请求
        for i in range(0, len(tasks), self.max_concurrent):
            batch = tasks[i : i + self.max_concurrent]
            batch_results = await asyncio.gather(*[task.start() for task in batch], return_exceptions=True)
            results.extend(batch_results)

        return results


class AsyncTask:
    """aiohttp异步任务原型 - 封装HTTP请求的参数和执行逻辑

    该类提供了灵活的请求配置接口,支持不同的HTTP方法、请求参数设置
    以及回调函数处理。
    """

    def __init__(self, index: int | None = None):
        """初始化异步任务

        Args:
            index: 任务索引,用于标识不同的任务,默认使用对象ID
        """
        self.index = index if index is not None else id(self)
        self.url: str = ''
        self.args: tuple = ()
        self.cookies: dict = {}
        self.callback: Callable | None = None
        self.kwargs: dict = {}
        self.method: str = ''

    def __getitem__(self, method: str):
        """通过索引方式获取请求方法处理器

        用法示例: task['get'](url) 或 task['post'](url, data=payload)

        Args:
            method: HTTP请求方法

        Returns:
            Callable: 配置请求参数的方法

        Raises:
            ValueError: 当请求方法不在支持列表中时
        """
        if method.lower() in REQUEST_METHODS:
            self.method = method.lower()
            return self.create
        raise ValueError(f'未知的请求方法: {method},支持的方法: {REQUEST_METHODS}')

    def __getattr__(self, method: str):
        """通过属性访问方式获取请求方法处理器

        用法示例: task.get(url) 或 task.post(url, data=payload)

        Args:
            method: HTTP请求方法

        Returns:
            Callable: 配置请求参数的方法
        """
        return self.__getitem__(method)

    def __repr__(self):
        """返回任务的字符串表示形式,方便调试和日志记录"""
        return f'AsyncTask | Method:{self.method} | Index:{self.index} | URL:{self.url}'

    def create(self, url: str, *args, **kwargs) -> AsyncTask:
        """创建并配置异步请求任务

        Args:
            url: 请求的目标URL
            *args: 传递给aiohttp请求的额外位置参数
            **kwargs: 传递给aiohttp请求的额外关键字参数
                - headers: 请求头信息,默认自动生成随机User-Agent
                - timeout: 请求超时时间,默认使用TIMEOUT常量
                - cookies: Cookie信息
                - callback: 响应处理的回调函数

        Returns:
            AsyncTask: 配置完成的任务对象,支持链式调用
        """
        self.url: str = url
        self.args: tuple = args
        kwargs.setdefault('headers', Head().randua)
        kwargs.setdefault('timeout', ClientTimeout(TIMEOUT))
        self.cookies: dict = kwargs.pop('cookies', {})
        self.callback: Callable | None = kwargs.pop('callback', None)
        self.kwargs: dict = kwargs
        return self

    @retry_wraps(default_return=(None, '重试失败'))
    async def _fetch(self) -> ACResponse:
        """执行HTTP请求,内部方法

        使用独立的ClientSession执行请求,自动重试失败的请求

        Returns:
            ACResponse: 统一的响应对象,包含状态码、头部和内容

        Raises:
            可能抛出的异常包括网络错误、超时、HTTP错误等
        """
        async with (
            ClientSession(cookies=self.cookies, connector=TCPConnector(ssl=False), timeout=ClientTimeout(total=TIMEOUT)) as session,
            session.request(
                self.method,
                self.url,
                *self.args,
                raise_for_status=True,
                **self.kwargs,
            ) as response,
        ):
            content = await response.content.read()
            return response, content

    @log_wraps
    async def start(self) -> ACResponse:
        """启动单任务执行

        执行请求并处理响应,支持回调函数处理结果

        Returns:
            ACResponse: 统一的响应对象,包含状态码、头部和内容
        """

        response, content = await self._fetch()
        return ACResponse(response, content, self.index)
 
    @retry_wraps
    async def multi_start(self, client: ClientSession) -> ACResponse:
        """在共享会话中执行任务

        用于批量请求场景,使用共享的ClientSession减少资源消耗

        Args:
            client: 共享的ClientSession对象

        Returns:
            ACResponse: 统一的响应对象
        """
        try:
            async with client.request(self.method, self.url, *self.args, raise_for_status=True, **self.kwargs) as response:
                content = await response.content.read()
                result = ACResponse(response, content, self.index)
        except Exception as err:
            handle_exception(err, callfrom=self.multi_start)
            result = ACResponse(None, f'{type(err).__name__} | {err!s}'.encode(), self.index)
        return self.callback(result) if callable(self.callback) else result


# 全局默认客户端实例
_default_client = AsyncHttpClient(max_concurrent=10)


def single_parse(method: str, url: str, *args, **kwargs) -> ACResponse:
    """构建并运行单个HTTP请求任务

    Args:
        method: HTTP方法
        url: 请求URL
        *args: 额外位置参数
        **kwargs: 额外关键字参数

    Returns:
        ACResponse: 响应对象
    """
    if method.lower() not in REQUEST_METHODS:
        return ACResponse(None, f'不支持的请求方法:{method},支持的方法:{REQUEST_METHODS}'.encode(), id(url))
    # 使用全局默认客户端处理请求
    return asyncio.run(_default_client.request(method, url, *args, **kwargs))


def multi_parse(method: str, urls: list[str], *args, **kwargs) -> list[ACResponse | Exception]:
    """构建并运行多个HTTP请求任务

    Args:
        method: HTTP方法
        urls: URL列表
        *args: 额外位置参数
        **kwargs: 额外关键字参数

    Returns:
        list[Union[ACResponse, Exception]]: 响应对象或异常的列表
    """
    if method.lower() not in REQUEST_METHODS:
        return [ACResponse(None, f'不支持的请求方法:{method},支持的方法:{REQUEST_METHODS}'.encode(), 0)]

    force_sequential = kwargs.pop('force_sequential', False)

    if force_sequential:
        return asyncio.run(_default_client.request_multi(method, urls, *args, **kwargs))

    return asyncio.run(_default_client.request_batch(method, urls, *args, **kwargs))


# 快捷函数 - 提供更简单的API接口
ahttp_get = partial(single_parse, 'get')
ahttp_post = partial(single_parse, 'post')
ahttp_get_all = partial(multi_parse, 'get')
ahttp_post_all = partial(multi_parse, 'post')
ahttp_get_all_sequential = partial(multi_parse, 'get', max_concurrency=24, force_sequential=True)

# 为保持与xt_ahttp.py的兼容性
ahttpGet = ahttp_get  # 兼容驼峰命名  # noqa: N816
ahttpPost = ahttp_post  # 兼容驼峰命名  # noqa: N816
ahttpGetAll = ahttp_get_all  # 兼容驼峰命名  # noqa: N816
ahttpPostAll = ahttp_post_all  # 兼容驼峰命名  # noqa: N816


class AHttpLoop:
    """异步HTTP客户端 - 使用loop实现"""
    
    def __init__(self, max_concurrent: int = 10):
        self.method: str = ''  # 保存请求方法
        self.max_concurrent: int = max_concurrent  # 最大并发请求数
        # 获取或创建事件循环
        try:
            self._loop = asyncio.get_running_loop()
        except RuntimeError:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
        self._session: ClientSession | None = None

        try:
            self._session = self._loop.run_until_complete(self.create_session())
        except Exception as err:
            self._session = None
            return handle_exception(err, re_raise=True, callfrom=self.__init__)

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
            connector=TCPConnector(ssl=False, limit=self.max_concurrent),
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
            except RuntimeError as err:
                # 如果事件循环已关闭，创建新的循环执行关闭
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self._session.close())
                loop.close()
                handle_exception(err, re_raise=True, callfrom=self.close)
                return f'AHttpLoop.close失败 | Exception:{err!r}'
            finally:
                self._session = None
        return None

    def __del__(self):
        """析构函数，确保资源释放"""
        self.close()

    def __getitem__(self, method: str) -> Callable:
        self.method = method.lower()  # 保存请求方法
        return self._make_parse

    def __getattr__(self, method: str) -> Callable:
        return self.__getitem__(method)

    def _make_parse(self, url: str, **kwargs) -> ACResponse:
        index = kwargs.pop('index', id(url))
        return self._loop.run_until_complete(self._retry_request(url, index=index, **kwargs))

    @log_wraps
    async def _retry_request(self, url: str, index: int | None = None, **kwargs) -> ACResponse:
        kwargs.setdefault('headers', Head().randua)
        kwargs.setdefault('timeout', ClientTimeout(TIMEOUT))
        index = index or id(url)
        _ = kwargs.pop('callback', None)

        @retry_wraps
        async def _single_fetch() -> tuple:
            if self._session is None:
                self._session = await self.create_session()
            async with self._session.request(self.method, url, raise_for_status=True, **kwargs) as response:
                response.raise_for_status()
                content = await response.content.read()
                return response, content

        try:
            response, content = await _single_fetch()
            return ACResponse(response, content, index)
        except Exception as err:
            handle_exception(err, callfrom=self._retry_request)
            return ACResponse(None, f'{type(err).__name__} | {err!s}'.encode(), index)

    async def _multi_fetch(self, method: str, urls_list: list[str], **kwargs):
        self.method = method
        task_list = [self._retry_request(url, index=index, **kwargs) for index, url in enumerate(urls_list)]
        return await asyncio.gather(*task_list, return_exceptions=True)

    def getall(self, urls_list: list[str], **kwargs):
        return self._loop.run_until_complete(self._multi_fetch('get', urls_list, **kwargs))

    def postall(self, urls_list: list[str], **kwargs):
        return self._loop.run_until_complete(self._multi_fetch('post', urls_list, **kwargs))


if __name__ == '__main__':
    """示例用法和测试代码"""
    from xt_thread.wraps import thread_print

    # 测试URL列表
    urls = ('https://www.163.com', 'https://www.qq.com', 'https://www.126.com', 'https://httpbin.org/post')

    def main():
        """主测试函数"""
        # 使用便捷函数发送单个GET请求
        thread_print('发送单个GET请求...', ahttp_get(urls[0]))

        # 使用便捷函数发送多个GET请求
        thread_print('ahttp_get_all 发送多个GET请求...', ahttp_get_all(urls, force_sequential=False))

        # 发送POST请求
        thread_print('发送POST请求...', ahttp_post(urls[3], data=b'test_data'))

    def test_ahttploop():
        ahc = AHttpLoop()
        thread_print(111111, ahc.get('https://www.163.com'))
        thread_print(222222, ahc.getall(['https://www.163.com', 'https://httpbin.org/ip']))

    async def demo_async_client():
        """演示AsyncHttpClient的异步用法"""
        client = _default_client

        # 单个请求
        thread_print('\nclient.request:', await client.request('get', urls[3]))

        # 批量请求(共享会话方式)
        thread_print('\nclient.request_multi(共享会话):', await client.request_multi('get', urls[2:4]))

        # 批量请求(分批处理方式)
        thread_print('\nclient.request_batch(分批处理):', await client.request_batch('get', urls[2:4]))

    # main()
    # test_ahttploop()
    asyncio.run(demo_async_client())
