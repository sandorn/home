# !/usr/bin/env python
"""
==============================================================
Description  : HTTP请求工具模块 - 提供简化的requests调用和会话管理功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-09-06 11:00:00
FilePath     : /CODE/xjLib/xt_requests.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能:
- 简化的HTTP请求方法(get, post等)，自动添加请求头和超时设置
- 请求重试机制，提高网络请求稳定性
- 会话管理，支持Cookie持久化和请求头管理
- 与htmlResponse集成，方便后续解析处理

主要特性:
- 自动随机User-Agent设置，减少请求被拦截的风险
- 统一的异常处理和响应封装
- 支持同步函数的重试机制
- 会话复用，提高请求效率
==============================================================
"""

from __future__ import annotations

from functools import partial
from typing import Any

import requests
from xt_head import TIMEOUT, Head
from xt_response import htmlResponse
from xt_wraps import log_wraps, mylog, retry_wraps

# 支持的HTTP请求方法
supported_request_methods = ('get', 'post', 'head', 'options', 'put', 'delete', 'trace', 'connect', 'patch')


@retry_wraps
def _retry_request(method: str, url: str, *args: Any, **kwargs: Any) -> htmlResponse:
    """利用retry_wraps实现请求重试机制

    Args:
        method: HTTP请求方法
        url: 请求URL
        *args: 传递给requests.request的位置参数
        **kwargs: 传递给requests.request的关键字参数
            callback: 回调函数(会被忽略)
            index: 响应对象的索引标识，默认为url的id
            timeout: 请求超时时间，默认使用TIMEOUT常量

    Returns:
        htmlResponse: 包装后的响应对象

    Raises:
        requests.HTTPError: 当HTTP状态码不是2xx时抛出
    """
    # 移除不支持的参数
    _ = kwargs.pop('callback', None)
    index = kwargs.pop('index', id(url))
    timeout = kwargs.pop('timeout', TIMEOUT)

    try:
        response = requests.request(method, url, *args, timeout=timeout, **kwargs)
        response.raise_for_status()
        return htmlResponse(response, response.content, index)
    except Exception as e:
        mylog.error(f'Request failed: {method} {url}, error: {e!s}')
        raise


def single_parse(method: str, url: str, *args: Any, **kwargs: Any) -> htmlResponse:
    """执行单次HTTP请求，自动设置默认请求头和超时

    Args:
        method: HTTP请求方法
        url: 请求URL
        *args: 传递给_retry_request的位置参数
        **kwargs: 传递给_retry_request的关键字参数
            headers: 请求头，默认为随机User-Agent
            timeout: 请求超时时间，默认使用TIMEOUT常量
            cookies: Cookie字典，默认为空字典

    Returns:
        htmlResponse: 包装后的响应对象，如果方法不支持则返回错误信息
    """
    method_lower = method.lower()

    if method_lower not in supported_request_methods:
        error_msg = f'Method:{method} not in {supported_request_methods}'
        mylog.warning(error_msg)
        return htmlResponse(None, error_msg.encode(), id(url))

    # 设置默认参数
    kwargs.setdefault('headers', Head().randua)  # 自动设置随机User-Agent
    kwargs.setdefault('timeout', TIMEOUT)  # 自动设置超时时间
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

    __slots__ = ('args', 'kwargs', 'method', 'session', 'url')

    def __init__(self):
        """初始化会话客户端"""
        self.session = requests.session()
        self.session.default_timeout = TIMEOUT
        self.method: str = ''
        self.args: tuple = ()
        self.kwargs: dict[str, Any] = {}
        self.url: str = ''

    def __enter__(self):
        """支持上下文管理器协议，用于自动关闭会话"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文时关闭会话"""
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

    @log_wraps
    def create_task(self, *args, **kwargs) -> htmlResponse:
        """创建并执行请求任务

        Args:
            *args: 位置参数，第一个参数为URL
            **kwargs: 关键字参数
                headers: 请求头，默认为随机User-Agent
                cookies: Cookie字典，默认为空字典
                timeout: 请求超时时间，默认使用TIMEOUT常量
                callback: 回调函数(会被忽略)

        Returns:
            htmlResponse: 包装后的响应对象
        """
        self.url = args[0]

        if self.method not in supported_request_methods:
            error_msg = f'Method:{self.method} not in {supported_request_methods}'
            mylog.warning(error_msg)
            return htmlResponse(None, error_msg.encode(), id(self.url))

        self.args = args[1:]

        # 更新请求头和Cookie
        self.update_headers(kwargs.pop('headers', Head().randua))
        self.update_cookies(kwargs.pop('cookies', {}))

        # 移除不支持的参数并设置默认值
        _ = kwargs.pop('callback', None)
        kwargs.setdefault('timeout', TIMEOUT)
        self.kwargs = kwargs

        return self._fetch()

    @retry_wraps
    def _fetch(self) -> htmlResponse:
        """执行请求并处理响应

        Returns:
            htmlResponse: 包装后的响应对象
        """
        response = self.session.request(self.method, self.url, *self.args, **self.kwargs)
        # 自动更新Cookie
        self.update_cookies(response.cookies)
        return htmlResponse(response, response.content, id(self.url))

    def update_cookies(self, cookie_dict: dict[str, str]) -> None:
        """更新会话的Cookie

        Args:
            cookie_dict: 包含Cookie键值对的字典
        """
        self.session.cookies.update(cookie_dict)

    def update_headers(self, header_dict: dict[str, str]) -> None:
        """更新会话的请求头

        Args:
            header_dict: 包含请求头键值对的字典
        """
        self.session.headers.update(header_dict)


if __name__ == '__main__':
    """模块使用示例和测试"""

    def basic_request_example():
        """基础请求示例"""
        # 简单GET请求
        mylog.info('执行简单GET请求')
        response = get('http://www.163.com')
        if isinstance(response, htmlResponse):
            mylog.success(f'请求成功，状态码: {response.status}')
            # 解析响应内容
            content = response.text
            mylog.debug(f'响应内容长度: {len(content)} 字符')
            print('xpath(//title/text()) ：', response.xpath('//title/text()'))
            print('xpath([//title/text(), //title/text()]) ：', response.xpath(['//title/text()', '//title/text()']))
            print('//title/text() ：', response.xpath(['//title/text()', '', ' ']))
            print('xpath( ) ：', response.xpath(' '))
            print('xpath() ：', response.xpath(''))
            print('dom.xpath(//title/text()) ：', response.dom.xpath('//title/text()'))
            print('html.xpath(//title/text()) ：', response.html.xpath('//title/text()'))
            print('element.xpath(//title/text()) ：', response.element.xpath('//title/text()'))
            print('query(title).text() ：', response.query('title').text())
            print('soup.select(title)[0].text ：', response.soup.select('title')[0].text)
            print('soup.find(title).text ：', response.soup.find('title').text)

    def session_example():
        """会话请求示例"""
        mylog.info('执行会话请求')
        # 使用上下文管理器创建会话
        with SessionClient() as client:
            # 第一次请求，设置Cookie
            client.get('https://httpbin.org/cookies/set?name=value')
            # 第二次请求，会自动携带Cookie
            response = client.get('https://httpbin.org/cookies')
            if isinstance(response, htmlResponse):
                try:
                    # 使用标准json模块解析JSON数据
                    import json

                    cookies = json.loads(response.text).get('cookies', {})
                    mylog.success(f'会话Cookie: {cookies}')
                except Exception as e:
                    mylog.error(f'解析Cookie失败: {e!s}')
                    mylog.debug(f'响应内容: {response.text[:100]}...')

    def post_request_example():
        """POST请求示例"""
        mylog.info('执行POST请求')
        data = {'key1': 'value1', 'key2': 'value2'}
        response = post('https://httpbin.org/post', data=data)
        if isinstance(response, htmlResponse):
            try:
                # 使用标准json模块解析JSON数据
                import json

                json_data = json.loads(response.text)
                form_data = json_data.get('form', {})
                mylog.success(f'POST数据接收: {form_data}')
            except Exception as e:
                mylog.error(f'解析POST响应失败: {e!s}')
                mylog.debug(f'响应内容: {response.text[:100]}...')

    # 执行示例
    mylog.info('=== HTTP请求工具模块测试开始 ===')
    try:
        # basic_request_example()
        # session_example()
        # post_request_example()
        print(get('https://httpbin.org/post'))
        mylog.success('=== HTTP请求工具模块测试完成 ===')
    except Exception as e:
        mylog.error(f'测试过程中发生错误: {e!s}')
