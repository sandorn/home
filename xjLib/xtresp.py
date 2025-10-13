# !/usr/bin/env python3
"""
==============================================================
模块名称     : xt_response_unified.py
功能描述     : 统一响应处理模块 - 提供同步和异步HTTP响应的统一接口
开发工具     : VSCode
作者         : Even.Sand
联系方式     : sandorn@163.com
最后修改时间 : 2025-10-13 17:00:00
Github       : https://github.com/sandorn/home

【核心功能】
- 统一的响应对象接口，同时支持同步和异步HTTP库
- 工厂模式创建适配不同类型的响应对象
- 适配器模式处理不同库的响应特性
- 完全兼容现有的BaseResponse、HtmlResponse和ACResponse功能
- 模块化设计，易于扩展

【使用示例】
    >>> from xt_requests import get
    >>> from xt_response_unified import RespFactory
    >>> response = get('https://example.com')
    >>> unified_resp = RespFactory.create_response(response)
    >>> print(unified_resp.status)  # 获取状态码
    200
    >>> title = unified_resp.xpath('//title/text()')[0][0]  # 使用XPath提取标题

【注意事项】
    - 保持了与原有响应类的向后兼容性
    - 自动识别响应类型并创建适当的处理对象
==============================================================
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

from chardet import detect
from pyquery import PyQuery
from xtlog import mylog

# 初始化日志
DEFAULT_ENCODING = 'utf-8'

# 类型定义
RawResponseType = Any  # 原始响应对象类型
ContentDataType = str | bytes | None  # 响应内容类型
SelectorType = str | Sequence[str]  # 选择器类型


class HttpError(Exception):
    """HTTP状态码错误异常"""

    def __init__(self, response, message=None):
        self.response = response
        self.status_code = response.status if response else 999
        self.message = message or f'HTTP Error {self.status_code}'
        super().__init__(self.message)


class IResponseAdapter(ABC):
    """响应适配器接口，定义统一的响应处理方法"""

    @abstractmethod
    def get_content(self) -> bytes:
        """获取原始响应内容（字节形式）"""
        pass

    @abstractmethod
    def get_status(self) -> int:
        """获取响应状态码"""
        pass

    @abstractmethod
    def get_url(self) -> str:
        """获取请求URL"""
        pass

    @abstractmethod
    def get_headers(self) -> dict[str, str]:
        """获取响应头部"""
        pass

    @abstractmethod
    def get_cookies(self) -> dict[str, str]:
        """获取响应Cookie"""
        pass

    @abstractmethod
    def get_encoding(self) -> str:
        """获取响应编码"""
        pass

    @abstractmethod
    def get_reason(self) -> str:
        """获取响应原因短语"""
        pass


class RequestsAdapter(IResponseAdapter):
    """requests库响应适配器"""

    def __init__(self, raw_response: Any):
        self.raw_response = raw_response

    def get_content(self) -> bytes:
        return getattr(self.raw_response, 'content', b'')

    def get_status(self) -> int:
        return getattr(self.raw_response, 'status_code', 999)

    def get_url(self) -> str:
        return getattr(self.raw_response, 'url', '')

    def get_headers(self) -> dict[str, str]:
        headers = getattr(self.raw_response, 'headers', {})
        return dict(headers) if headers else {}

    def get_cookies(self) -> dict[str, str]:
        cookies = getattr(self.raw_response, 'cookies', {})
        return dict(cookies) if cookies else {}

    def get_encoding(self) -> str:
        return getattr(self.raw_response, 'encoding', DEFAULT_ENCODING)

    def get_reason(self) -> str:
        return getattr(self.raw_response, 'reason', '')


class AiohttpAdapter(IResponseAdapter):
    """aiohttp库响应适配器"""

    def __init__(self, raw_response: Any):
        self.raw_response = raw_response

    def get_content(self) -> bytes:
        content = getattr(self.raw_response, 'content', b'')
        # aiohttp的content可能已经是bytes类型
        return content if isinstance(content, bytes) else b''

    def get_status(self) -> int:
        return getattr(self.raw_response, 'status', 999)

    def get_url(self) -> str:
        request_info = getattr(self.raw_response, 'request_info', None)
        if request_info and hasattr(request_info, 'url'):
            return str(request_info.url)
        return ''

    def get_headers(self) -> dict[str, str]:
        headers = getattr(self.raw_response, 'headers', {})
        return dict(headers) if headers else {}

    def get_cookies(self) -> dict[str, str]:
        cookies = getattr(self.raw_response, 'cookies', {})
        return dict(cookies) if cookies else {}

    def get_encoding(self) -> str:
        return getattr(self.raw_response, 'charset', DEFAULT_ENCODING)

    def get_reason(self) -> str:
        return getattr(self.raw_response, 'reason', '')


class UnifiedResp:
    """统一响应类，提供同步和异步HTTP响应的统一接口"""

    # 缓存属性，避免重复解析
    _dom_cache: Any | None = None
    _query_cache: PyQuery | None = None

    def __init__(self, response: RawResponseType = None, content: ContentDataType = None, index: int | None = None, adapter: IResponseAdapter | None = None, exception: Exception | None = None):
        """初始化统一响应对象

        Args:
            response: 原始HTTP响应对象(如requests.Response, aiohttp.ClientResponse)
            content: 响应内容(字符串或字节流),可选
            index: 响应对象的唯一标识符,可选
            adapter: 响应适配器,可选
        """
        self._raw = response
        self._index: int = index if index is not None else id(self)

        # 如果没有提供适配器，自动选择合适的适配器
        self._adapter = adapter or RespFactory._select_adapter(response)

        # 处理内容
        self._content: bytes = self._process_content(content)

        # 确定编码
        self._encoding: str = self._determine_encoding()

        # 异常信息
        self._exception: Exception | None = exception  # 保存原始异常对象类型
        self._error_type = type(exception).__name__ if exception else None

    @property
    def ok(self):
        """检查响应是否成功"""
        return RespFactory.is_success(self)

    @property
    def exception(self):
        """获取原始异常对象"""
        return self._exception

    def raise_for_status(self):
        """如果状态码不是200-299，抛出异常"""
        if not self.ok:
            raise HttpError(self)

    def _process_content(self, content: ContentDataType) -> bytes:
        """处理响应内容，转换为统一的字节格式"""
        if isinstance(content, str):
            # 字符串内容转换为字节流
            return content.encode(DEFAULT_ENCODING, 'replace')
        if isinstance(content, bytes):
            # 已经是字节流，直接返回
            return content

        # 尝试从原始响应或适配器获取内容
        if self._adapter:
            return self._adapter.get_content()

        # 无法处理的情况，返回空字节流
        return b''

    def _has_chinese_content(self) -> bool:
        """检查内容是否包含中文特征"""
        if not self._content:
            return False

        # 常见中文特征字节序列
        common_chinese_bytes = [
            b'\xe4\xbd\xa0\xe5\xa5\xbd',  # "你好"
            b'\xe4\xb8\xad\xe6\x96\x87',  # "中文"
            b'\xe7\xbd\x91\xe7\xab\x99',  # "网站"
        ]

        # 检查内容前1KB中是否包含中文特征
        content_sample = self._content[:1024]
        return any(chinese_bytes in content_sample for chinese_bytes in common_chinese_bytes)

    def _get_chinese_encoding(self) -> str:
        """获取适合中文内容的编码"""
        url = self.url.lower()

        # 检查内容中的charset声明
        if self._content:
            content_sample = self._content[:1024].lower()
            if b'charset=utf-8' in content_sample or b'utf-8' in url.encode():
                return 'utf-8'
            if b'charset=gb' in content_sample:
                return 'gbk'

        return 'utf-8'  # 默认返回UTF-8

    def _determine_encoding(self) -> str:
        """确定响应内容的编码"""
        # 预定义常见的中文编码优先级列表
        chinese_encodings = ['utf-8', 'gbk', 'gb2312', 'big5', 'utf-16']

        try:
            # 1. 检查URL是否包含中文域名特征
            url = self.url.lower()
            if any(chinese_domain in url for chinese_domain in ['baidu.com', 'sina.com', '163.com', 'qq.com', 'alibaba.com']):
                mylog.debug(f'中文域名识别: {url}')
                return self._get_chinese_encoding() if self._has_chinese_content() else 'utf-8'

            # 2. 优先使用chardet自动检测编码
            if self._content:
                detected_encoding = detect(self._content).get('encoding')
                if detected_encoding:
                    # 规范化编码名称（转换为小写）
                    detected_encoding = detected_encoding.lower()

                    # 避免使用不适合中文的编码
                    problematic_encodings = ['windows-1254', 'iso-8859-1', 'iso-8859-9']
                    if detected_encoding in problematic_encodings and self._has_chinese_content():
                        return 'utf-8'

                    # 确保中文编码优先级
                    if detected_encoding in chinese_encodings or self._has_chinese_content():
                        return detected_encoding if detected_encoding in chinese_encodings else 'utf-8'

                    return detected_encoding
        except Exception as e:
            mylog.warning(f'编码检测失败: {e}')

        # 3. 如果chardet检测失败，尝试使用适配器提供的编码
        if self._adapter:
            adapter_encoding = self._adapter.get_encoding()
            if adapter_encoding:
                return adapter_encoding

        # 4. 最后返回默认编码
        return DEFAULT_ENCODING

    def __repr__(self) -> str:
        """返回对象的字符串表示"""
        base = f'{self.__class__.__name__} | STATUS:{self.status} | ID:{self._index}'
        return f'{base} | URL:{self.url}' if self._raw else base

    def __str__(self) -> str:
        """返回对象的字符串表示"""
        return self.__repr__()

    def __bool__(self) -> bool:
        """布尔值转换，当状态码为200时返回True"""
        return self.status == 200

    def __len__(self) -> int:
        """返回文本内容的长度"""
        return len(self.text) if self.text else 0

    @property
    def text(self) -> str:
        """获取响应的文本内容，自动处理编码"""
        if isinstance(self._content, str):
            return self._content

        try:
            if isinstance(self._content, bytes):
                return self._content.decode(self._encoding, 'ignore')

            # 处理原始响应对象的text属性
            if self._raw:
                if callable(getattr(self._raw, 'text', None)):
                    # 处理可调用的text方法(例如aiohttp响应)
                    raw_text = self._raw.text()
                    if isinstance(raw_text, bytes):
                        return raw_text.decode(self._encoding, 'ignore')
                    return raw_text

                # 处理直接可访问的text属性
                raw_text = getattr(self._raw, 'text', '')
                if isinstance(raw_text, bytes):
                    return raw_text.decode(self._encoding, 'ignore')
                return raw_text
        except Exception as e:
            mylog.error(f'文本解码失败: {e}')

        # 所有尝试都失败，返回空字符串
        return ''

    @property
    def content(self) -> bytes:
        """获取原始响应内容（字节形式）"""
        return self._content

    @property
    def encoding(self) -> str:
        """获取响应内容的编码"""
        return self._encoding

    @property
    def index(self) -> int:
        """获取响应对象的唯一标识符"""
        return self._index

    @property
    def raw(self) -> RawResponseType:
        """获取原始HTTP响应对象"""
        return self._raw

    @property
    def elapsed(self) -> Any:
        """获取请求的响应时间"""
        if self._raw and hasattr(self._raw, 'elapsed'):
            return self._raw.elapsed
        return None

    @property
    def seconds(self) -> float:
        """获取请求的响应时间(秒)"""
        elapsed = self.elapsed
        return elapsed.total_seconds() if elapsed else 0.0

    @property
    def url(self) -> str:
        """获取请求的URL"""
        if self._adapter:
            return self._adapter.get_url()
        return getattr(self._raw, 'url', '')

    @property
    def cookies(self) -> dict[str, str]:
        """获取响应的Cookie"""
        if self._adapter:
            return self._adapter.get_cookies()
        if self._raw and hasattr(self._raw, 'cookies'):
            return dict(self._raw.cookies)
        return {}

    @property
    def headers(self) -> dict[str, str]:
        """获取响应的HTTP头部"""
        if self._adapter:
            return self._adapter.get_headers()
        if self._raw and hasattr(self._raw, 'headers'):
            return dict(self._raw.headers)
        return {}

    @property
    def status(self) -> int:
        """获取响应的状态码"""
        if self._adapter:
            return self._adapter.get_status()
        if self._raw:
            return getattr(self._raw, 'status', getattr(self._raw, 'status_code', 999))
        return 999

    @property
    def status_code(self) -> int:
        """获取响应的状态码(status的别名)"""
        return self.status

    @property
    def reason(self) -> str:
        """获取响应的原因短语"""
        if self._adapter:
            return self._adapter.get_reason()
        return getattr(self._raw, 'reason', '')

    @property
    def json(self) -> Any:
        """解析JSON响应内容"""
        # 首先尝试使用raw对象的json方法
        if self._raw and hasattr(self._raw, 'json'):
            try:
                return self._raw.json()
            except (ValueError, TypeError, AttributeError) as e:
                mylog.debug(f'使用raw.json()解析失败: {e}')

        # 尝试使用标准json模块解析text属性
        try:
            if self.text:
                return json.loads(self.text)
        except (ValueError, TypeError) as e:
            mylog.debug(f'使用json.loads()解析失败: {e}')

        # 解析失败时返回空字典
        return {}

    def _get_lxml_dom(self) -> Any:
        """延迟初始化lxml的DOM对象"""
        if self._dom_cache is None and self.text:
            try:
                from lxml.html import fromstring

                # 使用文本内容直接初始化，让lxml自动处理编码
                if isinstance(self.text, str):
                    # 对于已解码的字符串，lxml可以直接处理
                    self._dom_cache = fromstring(self.text)
                else:
                    # 对于字节流，使用指定编码解码
                    self._dom_cache = fromstring(self.text.encode(self._encoding, 'ignore'))
            except Exception as e:
                mylog.warning(f'解析HTML失败(LXML): {e}')
                self._dom_cache = None
        return self._dom_cache

    def _get_pyquery(self) -> PyQuery | None:
        """延迟初始化PyQuery对象"""
        if self._query_cache is None and self.text:
            from pyquery import PyQuery

            # 对于已经解码的字符串，PyQuery可以直接处理
            # 如果遇到编码问题，可以尝试使用字节流初始化并指定编码
            try:
                self._query_cache = PyQuery(self.text, parser='html')
                print(99999999, self._query_cache.size())
            except UnicodeDecodeError:
                # 如果字符串解码有问题，尝试使用原始内容并指定编码
                if isinstance(self._content, bytes):
                    self._query_cache = PyQuery(self._content, parser='html', encoding=self._encoding)
                else:
                    # 转换为字节流再尝试
                    self._query_cache = PyQuery(self.text.encode(self._encoding, 'ignore'), parser='html', encoding=self._encoding)

        return self._query_cache

    @property
    def query(self) -> PyQuery:
        """CSS选择器对象(PyQuery)
        
        Returns:
            PyQuery: 始终返回一个可用的PyQuery对象，不会返回None
        """
        result = self._get_pyquery()
        if result is None:
            # 当无法创建PyQuery对象时，返回空的PyQuery对象
            from pyquery import PyQuery
            return PyQuery('')
        return result

    def xpath(self, selectors: SelectorType = '') -> list[list[Any]]:
        """执行XPath选择查询

        Args:
            selectors: XPath选择器，可以是单个字符串或字符串列表

        Returns:
            list[list[Any]]: 查询结果列表，外层列表对应每个选择器，内层列表是查询结果
        """
        # 处理空选择器的情况
        if not selectors or (isinstance(selectors, str) and not selectors.strip()):
            return [[]]

        # 统一处理为列表形式
        selector_list = [selectors] if isinstance(selectors, str) else selectors
        results = []

        for selector in selector_list:
            # 检查选择器是否为字符串并且非空
            if not isinstance(selector, str) or not selector.strip():
                results.append([])
                continue

            try:
                # 优先使用lxml的xpath方法
                if self.dom is not None and hasattr(self.dom, 'xpath'):
                    selector_results = self.dom.xpath(selector)
                    results.append(selector_results)
                else:
                    results.append([])
            except Exception as e:
                mylog.warning(f'XPath查询失败: {selector}, 错误: {e}')
                results.append([])

        return results

    @property
    def dom(self) -> Any:
        """lxml的DOM对象，用于XPath解析"""
        return self._get_lxml_dom()


class RespFactory:
    """响应对象工厂，负责创建适当类型的响应对象"""

    @staticmethod
    def _select_adapter(response: RawResponseType) -> IResponseAdapter:
        """根据响应对象类型选择合适的适配器"""
        # 检查是否为aiohttp响应
        response_module = getattr(response, '__module__', '')
        if 'aiohttp' in response_module:
            return AiohttpAdapter(response)

        # 对于其他所有情况(包括None)，都使用RequestsAdapter作为默认适配器
        return RequestsAdapter(response)

    @staticmethod
    def create_response(response: RawResponseType = None, content: ContentDataType = None, index: int | None = None) -> UnifiedResp:
        """创建统一响应对象

        Args:
            response: 原始HTTP响应对象(如requests.Response, aiohttp.ClientResponse)
            content: 响应内容(字符串或字节流),可选
            index: 响应对象的唯一标识符,可选

        Returns:
            UnifiedResp: 统一响应对象
        """
        return UnifiedResp(response=response, content=content, index=index)

    @staticmethod
    def is_success(response: UnifiedResp | RawResponseType) -> bool:
        """检查响应是否成功(状态码在200-299之间)"""
        if isinstance(response, UnifiedResp):
            return 200 <= response.status < 300

        # 处理原始响应对象
        status = getattr(response, 'status', getattr(response, 'status_code', 999))
        return 200 <= status < 300


if __name__ == '__main__':
    """测试统一响应模块"""
    from xt_requests import get

    # 选择常用中文网址作为测试目标
    test_urls = [
        'https://www.baidu.com',  # 百度 - 中文搜索引擎
        'https://www.sina.com.cn',  # 新浪 - 综合门户网站
    ]

    def run_test(url: str):
        """运行测试"""
        mylog.info('=' * 70)
        mylog.info(f'正在测试网址: {url}')

        try:
            # 获取原始响应
            raw_response = get(url)

            # 创建统一响应对象
            unified_resp = RespFactory.create_response(raw_response)

            mylog.info(f'响应状态: {unified_resp.status}|{unified_resp.index}')
            mylog.info(f'响应URL: {unified_resp.url}')
            mylog.info(f'响应编码: {unified_resp.encoding}')

            # 测试HTML解析功能
            title = unified_resp.xpath('//title/text()')
            mylog.info(f'页面标题: {title[0][0] if title and title[0] else "N/A"}')
            mylog.info(f'页面内容: {unified_resp.text[:100]}')  # 显示前100个字符
            # 增加更多的xpath测试内容
            xpath_result = unified_resp.xpath('//title/text()')
            mylog.info(f'xpath(//title/text()) : {xpath_result}')

            xpath_multi = unified_resp.xpath(['//title/text()', '//title/text()'])
            mylog.info(f'xpath([//title/text(), //title/text()]) : {xpath_multi}')

            xpath_mixed = unified_resp.xpath(['//title/text()', '', ' '])
            mylog.info(f'//title/text() : {xpath_mixed}')

            xpath_space = unified_resp.xpath(' ')
            mylog.info(f'xpath( ) : {xpath_space}')

            xpath_empty = unified_resp.xpath('')
            mylog.info(f'xpath() : {xpath_empty}')

            try:
                if unified_resp.query:
                    query_result = unified_resp.query('title').text()
                    mylog.info(f'query(title).text() : {query_result}')
            except Exception as e:
                mylog.warning(f'query测试失败: {e}')

            try:
                if unified_resp.dom is not None:
                    dom_result = unified_resp.dom.xpath('//title/text()')
                    mylog.info(f'dom.xpath(//title/text()) : {dom_result}')
            except Exception as e:
                mylog.warning(f'dom.xpath测试失败: {e}')

            mylog.info('测试完成!')
        except Exception as e:
            mylog.error(f'测试失败: {e}')

    # 运行测试
    for url in test_urls:
        run_test(url)

    mylog.info('\n\n所有测试完成!')
