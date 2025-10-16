# !/usr/bin/env python
"""
==============================================================
Descripttion : HTTP Headers工具模块
Develop      : VSCode
Author       : sandorn sandorn@live.cn
LastEditTime : 2025-10-14 22:00:00
Github       : https://github.com/sandorn/xthttp
==============================================================
"""

from __future__ import annotations

import random
from typing import Any

from aiohttp import ClientTimeout
from fake_useragent import UserAgent

# 异步HTTP请求超时配置
TIMEOUT_AIOH = ClientTimeout(
    total=30,  # 总超时30秒
    connect=8,  # 连接超时8秒
    sock_read=20,  # 读取超时20秒
    sock_connect=8,  # socket连接8秒
)

# 同步请求超时配置
TIMEOUT_REQU = (8, 30)

# 精简USER_AGENTS列表，保留主流浏览器最新版本
USER_AGENTS = [
    # Chrome最新版本
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    # Firefox最新版本
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
    # Safari最新版本
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.1 Safari/605.1.15',
    # Edge最新版本
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Edg/120.0.0.0',
]

# 默认HTTP请求头配置
MYHEAD = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'Accept': '*/*,application/*,application/json,text/*,text/html',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Encoding': 'gzip,deflate,compress',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.6,en;q=0.4',
    'Accept-Charset': 'UTF-8,GB2312,GBK,GB18030,ISO-8859-1,ISO-8859-5;q=0.7,*;q=0.7',
    'Content-Type': 'text/html,application/x-www-form-unlencoded; charset=UTF-8',
    'Upgrade': 'HTTP/1.1',  # 强制降级到'HTTP/1.1'
    'Connection': 'Upgrade',
}


class Head:
    """HTTP Headers管理类，提供User-Agent随机化和headers更新功能"""

    def __init__(self) -> None:
        """初始化Headers管理器"""
        self.headers: dict[str, str] = MYHEAD.copy() or {}
        self._user_agent: UserAgent | None = None
        self._cached_ua: str | None = None

    def __setattr__(self, name: str, value: Any) -> None:
        """保护headers属性不被意外修改

        Args:
            name: 属性名
            value: 属性值

        Raises:
            TypeError: 当headers属性被设置为非字典类型时
        """
        if name == 'headers' and not isinstance(value, dict):
            raise TypeError('headers must be a dictionary')
        super().__setattr__(name, value)

    @property
    def _ua_instance(self) -> UserAgent:
        """延迟加载UserAgent实例

        Returns:
            UserAgent: fake_useragent库的UserAgent实例
        """
        if self._user_agent is None:
            self._user_agent = UserAgent()
        return self._user_agent

    @property
    def randua(self) -> dict[str, str]:
        """获取随机User-Agent（使用fake_useragent库）

        Returns:
            dict[str, str]: 包含随机User-Agent的headers字典
        """
        self.headers['User-Agent'] = self._ua_instance.random
        return self.headers

    @property
    def ua(self) -> dict[str, str]:
        """获取预定义随机User-Agent的headers

        Returns:
            dict[str, str]: 包含预定义随机User-Agent的headers字典
        """
        if self._cached_ua is None:
            self._cached_ua = random.choice(USER_AGENTS)  # noqa: S311
        self.headers['User-Agent'] = self._cached_ua
        return self.headers

    def update_headers(self, headers: dict[str, str] | None = None) -> None:
        """安全更新headers，支持空值和类型验证

        Args:
            headers: 要更新的headers字典，可为None

        Raises:
            TypeError: 当headers不是字典类型时
            ValueError: 当headers格式无效时
        """
        if headers is None:
            return

        if not isinstance(headers, dict):
            raise TypeError(f'headers must be dict or None, got {type(headers).__name__}')

        try:
            # 过滤非字符串键值对和空值
            valid_headers = {str(key): str(value) for key, value in headers.items() if key is not None and value is not None}
            self.headers.update(valid_headers)
        except (AttributeError, ValueError) as e:
            raise ValueError(f'Invalid headers format: {e}') from e

    def reset_headers(self) -> None:
        """重置headers为默认配置"""
        self.headers = MYHEAD.copy()

    def get_header(self, key: str, default: str | None = None) -> str | None:
        """安全获取指定header值

        Args:
            key: header键名
            default: 默认值

        Returns:
            str | None: header值或默认值
        """
        return self.headers.get(str(key), default)

    def set_header(self, key: str, value: str) -> None:
        """安全设置单个header值

        Args:
            key: header键名
            value: header值

        Raises:
            TypeError: 当key或value不是字符串时
        """
        if not isinstance(key, str) or not isinstance(value, str):
            raise TypeError('Header key and value must be strings')
        self.headers[key] = value

    def remove_header(self, key: str) -> bool:
        """移除指定header

        Args:
            key: 要移除的header键名

        Returns:
            bool: 是否成功移除
        """
        if key in self.headers:
            del self.headers[key]
            return True
        return False

    def copy_headers(self) -> dict[str, str]:
        """返回headers的深拷贝

        Returns:
            dict[str, str]: headers字典的深拷贝
        """
        return self.headers.copy()


__all__ = ('TIMEOUT_AIOH', 'TIMEOUT_REQU', 'Head')
