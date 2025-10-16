# !/usr/bin/env python
"""
==============================================================
Description  : HTTP请求工具模块 - 提供简化的requests调用和会话管理功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
LastEditTime : 2025-10-14 22:00:00
Github       : https://github.com/sandorn/xthttp

本模块提供以下核心功能:
- 简化的HTTP请求方法(get, post等),自动添加请求头和超时设置
- 请求重试机制,提高网络请求稳定性
- 会话管理,支持Cookie持久化和请求头管理
- 与UnifiedResp集成,方便后续解析处理

主要特性:
- 自动随机User-Agent设置,减少请求被拦截的风险
- 统一的异常处理和响应封装
- 支持同步函数的重试机制
- 会话复用,提高请求效率
==============================================================
"""

from __future__ import annotations

from functools import partial
from typing import Any

import requests
from nswrapslite.retry import spider_retry

from .headers import TIMEOUT_REQU, Head
from .resp import UnifiedResp

# 支持的HTTP请求方法（使用集合提高查找效率）
REQUEST_METHODS: set[str] = {'get', 'post', 'head', 'options', 'put', 'delete', 'trace', 'connect', 'patch'}

# Head实例缓存（避免重复创建）
_HEAD_INSTANCE: Head | None = None


def _get_head_instance() -> Head:
    """获取Head单例实例

    Returns:
        Head: Head类的单例实例
    """
    global _HEAD_INSTANCE
    if _HEAD_INSTANCE is None:
        _HEAD_INSTANCE = Head()
    return _HEAD_INSTANCE


@spider_retry
def _retry_request(method: str, url: str, *args: Any, **kwargs: Any) -> UnifiedResp:
    """利用spider_retry实现请求重试机制

    Args:
        method: HTTP请求方法（已转换为小写）
        url: 请求URL
        *args: 传递给requests.request的位置参数
        **kwargs: 传递给requests.request的关键字参数
            callback: 回调函数（会被忽略）
            index: 响应对象的索引标识，默认为url的id
            timeout: 请求超时时间，默认使用timeout常量

    Returns:
        UnifiedResp: 包装后的响应对象

    Raises:
        requests.HTTPError: 当HTTP状态码不是2xx时抛出
    """
    # 使用字典视图减少复制操作
    filtered_kwargs = {k: v for k, v in kwargs.items() if k not in {'callback', 'index', 'timeout'}}

    index = kwargs.get('index', id(url))
    timeout = kwargs.get('timeout', TIMEOUT_REQU)

    response = requests.request(method, url, *args, timeout=timeout, **filtered_kwargs)
    response.raise_for_status()
    return UnifiedResp(response, response.content, index, url)


def single_parse(method: str, url: str, *args: Any, **kwargs: Any) -> UnifiedResp:
    """执行单次HTTP请求，自动设置默认请求头和超时

    Args:
        method: HTTP请求方法
        url: 请求URL
        *args: 传递给_retry_request的位置参数
        **kwargs: 传递给_retry_request的关键字参数
            headers: 请求头，默认为随机User-Agent
            timeout: 请求超时时间，默认使用timeout常量
            cookies: Cookie字典，默认为空字典

    Returns:
        UnifiedResp: 包装后的响应对象，如果方法不支持则返回错误信息

    Raises:
        ValueError: 当请求方法不在支持列表中时
    """
    method_lower = method.lower()

    if method_lower not in REQUEST_METHODS:
        raise ValueError(f'未知的HTTP请求方法: {method}')

    # 使用单例Head实例，避免重复创建
    head_instance = _get_head_instance()

    # 设置默认参数（使用字典的setdefault方法）
    kwargs.setdefault('headers', head_instance.randua)  # 自动设置随机User-Agent
    kwargs.setdefault('timeout', TIMEOUT_REQU)  # 自动设置超时时间
    kwargs.setdefault('cookies', {})  # 自动设置空Cookie字典

    return _retry_request(method_lower, url, *args, **kwargs)


# 创建常用请求方法的快捷方式
get = partial(single_parse, 'get')
post = partial(single_parse, 'post')
head = partial(single_parse, 'head')
options = partial(single_parse, 'options')
put = partial(single_parse, 'put')
delete = partial(single_parse, 'delete')
patch = partial(single_parse, 'patch')


class SessionClient:
    """会话客户端 - 封装requests.Session，管理Cookie持久化和请求重试

    提供会话级别的HTTP请求管理，支持Cookie保存和请求头持久化，
    适用于需要维持会话状态的场景。

    Example:
        >>> with SessionClient() as client:
        >>> # 登录获取Cookie
        >>>     client.post('https://example.com/login', data={'username': 'user', 'password': 'pass'})
        >>> # 使用同一会话访问需要登录的页面
        >>>     response = client.get('https://example.com/user/profile')
    """

    __slots__ = ('_head_instance', 'args', 'kwargs', 'method', 'session', 'timeout', 'url')

    def __init__(self) -> None:
        """初始化会话客户端"""
        self.session = requests.session()
        self.timeout: tuple = TIMEOUT_REQU
        self.method: str = ''
        self.args: tuple = ()
        self.kwargs: dict[str, Any] = {}
        self.url: str = ''
        self._head_instance: Head = _get_head_instance()

    def __enter__(self) -> SessionClient:
        """支持上下文管理器协议，用于自动关闭会话

        Returns:
            SessionClient: 当前会话实例
        """
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any) -> None:
        """退出上下文时关闭会话

        Args:
            exc_type: 异常类型
            exc_val: 异常值
            exc_tb: 异常回溯
        """
        self.session.close()

    def __getitem__(self, method: str):
        """支持通过索引方式设置请求方法

        Args:
            method: HTTP请求方法

        Returns:
            指向create_task方法的引用，用于链式调用
        """
        self.method = method.lower()  # 保存请求方法
        return self.create_task  # 返回创建任务的方法

    def __getattr__(self, method: str):
        """支持通过属性访问设置请求方法

        Args:
            method: HTTP请求方法名称

        Returns:
            指向create_task方法的引用，用于链式调用
        """
        return self.__getitem__(method)

    def create_task(self, *args: Any, **kwargs: Any) -> UnifiedResp:
        """创建并执行请求任务

        Args:
            *args: 位置参数，第一个参数为URL
            **kwargs: 关键字参数
                headers: 请求头，默认为随机User-Agent
                cookies: Cookie字典，默认为空字典
                timeout: 请求超时时间，默认使用timeout常量
                callback: 回调函数（会被忽略）

        Returns:
            UnifiedResp: 包装后的响应对象

        Raises:
            ValueError: 当请求方法不在支持列表中时
        """
        if not args:
            raise ValueError('URL参数不能为空')

        self.url = args[0]

        if self.method not in REQUEST_METHODS:
            raise ValueError(f'未知的HTTP请求方法: {self.method}')

        self.args = args[1:]

        # 更新请求头和Cookie（使用单例Head实例）
        headers = kwargs.pop('headers', self._head_instance.randua)
        cookies = kwargs.pop('cookies', {})

        self.update_headers(headers)
        self.update_cookies(cookies)

        # 移除不支持的参数并设置默认值
        kwargs.pop('callback', None)
        kwargs.setdefault('timeout', TIMEOUT_REQU)

        self.kwargs = kwargs

        return self.start()

    @spider_retry
    def start(self) -> UnifiedResp:
        """执行请求并处理响应

        Returns:
            UnifiedResp: 包装后的响应对象

        Raises:
            requests.RequestException: 当请求失败时
        """
        response = self.session.request(self.method, self.url, *self.args, **self.kwargs)
        response.raise_for_status()
        self.update_cookies(dict(response.cookies))
        return UnifiedResp(response, response.content, id(self.url), self.url)

    def update_cookies(self, cookie_dict: dict[str, str]) -> None:
        """更新会话的Cookie

        Args:
            cookie_dict: 包含Cookie键值对的字典

        Raises:
            TypeError: 当cookie_dict不是字典类型时
        """
        if not isinstance(cookie_dict, dict):
            raise TypeError('cookie_dict必须是字典类型')
        self.session.cookies.update(cookie_dict)

    def update_headers(self, header_dict: dict[str, str]) -> None:
        """更新会话的请求头

        Args:
            header_dict: 包含请求头键值对的字典

        Raises:
            TypeError: 当header_dict不是字典类型时
        """
        if not isinstance(header_dict, dict):
            raise TypeError('header_dict必须是字典类型')
        self.session.headers.update(header_dict)

    def get_current_headers(self) -> dict[str, str | bytes]:
        """获取当前会话的请求头

        Returns:
            dict[str, str | bytes]: 当前请求头的副本
        """
        return dict(self.session.headers)

    def get_current_cookies(self) -> dict[str, str]:
        """获取当前会话的Cookie

        Returns:
            dict[str, str]: 当前Cookie的副本
        """
        return dict(self.session.cookies)


__all__ = (
    'SessionClient',
    'delete',
    'get',
    'head',
    'options',
    'patch',
    'post',
    'put',
)
