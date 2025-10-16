# !/usr/bin/env python
"""
==============================================================
Description  : 异步HTTP请求模块 - 提供基于aiohttp的高性能异步HTTP客户端功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
LastEditTime : 2025-10-14 22:00:00
Github       : https://github.com/sandorn/xthttp

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
from collections.abc import Callable, Sequence
from functools import partial

from aiohttp import ClientSession, TCPConnector
from nswrapslite import spider_retry
from yarl import URL

from .headers import TIMEOUT_AIOH, Head
from .resp import UnifiedResp

# 定义模块公开接口
__all__ = ('AsyncHttpClient', 'ahttp_get', 'ahttp_get_all', 'ahttp_post', 'ahttp_post_all')

# 定义支持的HTTP请求方法
REQUEST_METHODS = ('get', 'post', 'head', 'options', 'put', 'delete', 'trace', 'connect', 'patch')


class AsyncHttpClient:
    """异步HTTP客户端 - 提供并发控制的HTTP请求管理

    该类实现了并发请求控制和批量请求处理,
    适合需要高效执行大量HTTP请求的场景。

    核心特性：
    - 并发控制与限制
    - 超时控制与错误处理
    - 支持批量请求处理
    """

    def __init__(self, max_concurrent: int = 10):
        """初始化异步HTTP客户端

        Args:
            max_concurrent: 最大并发请求数,默认为10,控制同时发起的请求数量
        """
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def request(self, method: str, url: str, *args, **kwargs) -> UnifiedResp:
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
            UnifiedResp: 包含响应状态、头部和内容的统一响应对象
        """
        task = getattr(AsyncTask(), method)(url, *args, **kwargs)
        async with self.semaphore:
            return await task.start()

    async def multi_request(self, method: str, urls: Sequence[str], *args, **kwargs) -> Sequence[UnifiedResp | BaseException | None]:
        """批量执行HTTP请求(共享会话方式)

        特点:使用共享的TCP连接器和ClientSession,大幅减少连接建立的开销
        注意：该方法假设传入的URL已经过验证，由multi_parse函数调用

        Args:
            method: HTTP方法,如'get'、'post'等
            urls: 要请求的URL列表(已验证)
            *args: 传递给每个请求的额外位置参数
            **kwargs: 传递给每个请求的额外关键字参数

        Returns:
            Sequence[UnifiedResp | BaseException]: 响应对象或异常的序列
        """
        # 预先分配结果列表，保持原始顺序
        n = len(urls)
        results: list[UnifiedResp | BaseException | None] = [None] * n  # 预先分配固定大小的列表

        # 分离有效URL和无效URL
        valid_tasks = []  # 存储 (task, original_index)
        invalid_indices = []  # 存储 (original_index, error)

        # 第一遍遍历：分类URL并记录索引
        for index, url in enumerate(urls):
            if isinstance(url, ValueError):
                # 记录无效URL的位置和错误
                invalid_indices.append((index, url))
            else:
                # 创建有效URL的任务
                task = AsyncTask(index)[method](url, *args, **kwargs)
                valid_tasks.append((task, index))

        # 预先设置无效URL的结果
        for index, error in invalid_indices:
            results[index] = error

        # 如果有有效URL，创建共享会话并执行
        if valid_tasks:
            async with ClientSession(
                connector=TCPConnector(ssl=False, limit=self.max_concurrent),
                timeout=TIMEOUT_AIOH,
            ) as client:
                # 并发执行所有有效任务
                batch_results = await asyncio.gather(*[self._request_with_semaphore(task.multi_start, client) for task, _ in valid_tasks], return_exceptions=True)

                # 将有效任务结果放入正确位置
                for (_, original_index), result in zip(valid_tasks, batch_results, strict=False):
                    results[original_index] = result

        return results

    async def _request_with_semaphore(self, func, *args, **kwargs):
        """使用信号量控制并发执行指定函数"""
        async with self.semaphore:
            return await func(*args, **kwargs)

    async def batch_request(self, method: str, urls: Sequence[str], *args, **kwargs) -> Sequence[UnifiedResp | BaseException | None]:
        """批量执行HTTP请求(分批处理方式)

        特点:将请求分成多个批次执行,每批次不超过max_concurrent个请求
        适合处理大量URL的场景，可以有效避免连接数过多导致的资源耗尽问题。
        注意：该方法假设传入的URL已经过验证，由multi_parse函数调用

        Args:
            method: HTTP方法
            urls: 要请求的URL列表(已验证)
            *args: 传递给每个请求的额外位置参数
            **kwargs: 传递给每个请求的额外关键字参数

        Returns:
            Sequence[UnifiedResp | BaseException]: 响应对象或异常的序列
        """
        # 预先分配结果列表，保持原始顺序
        n = len(urls)
        results: list[UnifiedResp | BaseException | None] = [None] * n  # 预先分配固定大小的列表

        # 分离有效URL和无效URL
        valid_tasks = []  # 存储 (task, original_index)
        invalid_indices = []  # 存储 (original_index, error)

        # 第一遍遍历：分类URL并记录索引
        for index, url in enumerate(urls):
            if isinstance(url, ValueError):
                # 记录无效URL的位置和错误
                invalid_indices.append((index, url))
            else:
                # 为有效URL创建任务
                task = AsyncTask(index)[method](url, *args, **kwargs)
                valid_tasks.append((task, index))

        # 预先设置无效URL的结果
        for index, error in invalid_indices:
            results[index] = error

        # 分批处理，每批次不超过max_concurrent个请求
        for i in range(0, len(valid_tasks), self.max_concurrent):
            batch = valid_tasks[i : i + self.max_concurrent]

            # 并发执行当前批次
            batch_results = await asyncio.gather(*[self._request_with_semaphore(task.start) for task, _ in batch], return_exceptions=True)

            # 将当前批次的结果放入正确位置
            for (_, original_index), result in zip(batch, batch_results, strict=False):
                results[original_index] = result

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
        if method.lower() not in REQUEST_METHODS:
            raise ValueError(f'未知的HTTP请求方法: {method}')

        self.method = method.lower()
        return self._create_parse

    def __getattr__(self, method: str):
        """通过属性访问方式获取请求方法处理器"""
        return self.__getitem__(method)

    def __repr__(self):
        """返回任务的字符串表示形式,方便调试和日志记录"""
        return f'AsyncTask | Method:{self.method} | Id:{self.index} | Url:{self.url}'

    def _create_parse(self, url: str, *args, **kwargs) -> AsyncTask:
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
        self.url = url
        self.args = args
        kwargs.setdefault('headers', Head().randua)
        kwargs.setdefault('timeout', TIMEOUT_AIOH)
        self.cookies = kwargs.pop('cookies', {})
        self.callback = kwargs.pop('callback', None)
        self.kwargs = kwargs
        return self

    @spider_retry
    async def start(self) -> UnifiedResp:
        """启动单任务执行

        执行请求并处理响应,支持回调函数处理结果。
        每个请求使用独立的ClientSession，避免会话管理问题。

        Returns:
            UnifiedResp: 统一的响应对象,包含状态码、头部和内容
        """
        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            # 添加cookies到会话
            if self.cookies and session:
                for key, value in self.cookies.items():
                    session.cookie_jar.update_cookies({key: value}, response_url=URL(self.url))

            # 发起请求
            response = await session.request(
                self.method,
                self.url,
                *self.args,
                raise_for_status=True,
                **self.kwargs,
            )

            # 读取内容
            content = await response.read()
            result = UnifiedResp(response, content, self.index, self.url)

        return self.callback(result) if callable(self.callback) else result

    @spider_retry
    async def multi_start(self, client: ClientSession) -> UnifiedResp:
        """在共享会话中执行任务

        用于批量请求场景,使用共享的ClientSession减少资源消耗

        Args:
            client: 共享的ClientSession对象

        Returns:
            UnifiedResp: 统一的响应对象
        """
        async with client.request(
            self.method,
            self.url,
            *self.args,
            raise_for_status=True,
            **self.kwargs,
        ) as response:
            content = await response.read()
            result = UnifiedResp(response, content, self.index, self.url)
        return self.callback(result) if callable(self.callback) else result


# 全局默认客户端实例
_default_client = AsyncHttpClient(max_concurrent=10)


def single_parse(method: str, url: str, *args, **kwargs) -> UnifiedResp:
    """构建并运行单个HTTP请求任务

    Args:
        method: HTTP方法
        url: 请求URL
        *args: 额外位置参数
        **kwargs: 额外关键字参数

    Returns:
        UnifiedResp: 响应对象

    Raises:
        ValueError: 当请求方法不在支持列表中时
    """
    # 边界条件检查
    if not url or not url.strip():
        raise ValueError(f'无效的URL: {url}')

    if method.lower() not in REQUEST_METHODS:
        raise ValueError(f'未知的HTTP请求方法: {method}')

    # 使用全局默认客户端处理请求
    return asyncio.run(_default_client.request(method, url, *args, **kwargs))


def multi_parse(method: str, urls: Sequence[str], *args, **kwargs) -> Sequence[UnifiedResp | BaseException | None]:
    """构建并运行多个HTTP请求任务

    Args:
        method: HTTP方法
        urls: URL列表
        *args: 额外位置参数
        **kwargs: 额外关键字参数
        - force_sequential: 是否共享会话方式,默认False,
            当为True时,使用共享会话方式执行请求,
            否则使用分批处理方式执行请求,
            建议在批量请求场景下使用分批处理方式,
            以避免会话超时问题。

    Returns:
        Sequence[UnifiedResp | BaseException]: 响应对象或异常的序列

    Raises:
        ValueError: 当请求方法不在支持列表中时
    """
    # 边界条件检查
    if not urls:
        return []

    # 验证URL格式并将无效URL标记为ValueError对象
    # 这是唯一的URL验证点，批处理方法不再重复验证
    valid_urls = []
    for url in urls:
        if not isinstance(url, str) or not url.strip():
            valid_urls.append(ValueError(f'无效的URL: {url}'))  # 保持长度一致
        else:
            valid_urls.append(url)

    # 验证请求方法
    if method.lower() not in REQUEST_METHODS:
        raise ValueError(f'未知的HTTP请求方法: {method}')

    # 选择请求执行方式
    force_sequential = kwargs.pop('force_sequential', False)

    if force_sequential:
        return asyncio.run(_default_client.multi_request(method, valid_urls, *args, **kwargs))

    return asyncio.run(_default_client.batch_request(method, valid_urls, *args, **kwargs))


# 快捷函数 - 提供更简单的API接口
ahttp_get = partial(single_parse, 'get')
ahttp_post = partial(single_parse, 'post')
ahttp_get_all = partial(multi_parse, 'get')
ahttp_post_all = partial(multi_parse, 'post')
ahttp_get_all_sequential = partial(multi_parse, 'get', force_sequential=True)
