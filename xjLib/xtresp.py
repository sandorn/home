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
- 统一的响应对象接口,同时支持同步和异步HTTP库
- 工厂模式创建适配不同类型的响应对象
- 适配器模式处理不同库的响应特性
- 完全兼容现有的BaseResponse、HtmlResponse和ACResponse功能
- 模块化设计,易于扩展

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
import re
from abc import ABC, abstractmethod
from collections.abc import Sequence
from contextlib import suppress
from typing import Any, ClassVar

from pyquery import PyQuery
from xtlog import mylog

# 初始化日志
DEFAULT_ENCODING = 'utf-8'

# 类型定义
RawResponseType = Any  # 原始响应对象类型
ContentDataType = str | bytes | None  # 响应内容类型
SelectorType = str | Sequence[str]  # 选择器类型


class RespFactory:
    """响应对象工厂,负责创建适当类型的响应对象"""

    @staticmethod
    def _select_adapter(response: RawResponseType) -> BaseRespAdapter:
        """根据响应对象类型选择合适的适配器"""
        # 检查是否为aiohttp响应
        response_module = getattr(response, '__module__', '')
        if 'aiohttp' in response_module:
            return AiohttpAdapter(response)

        # 对于其他所有情况(包括None),都使用RequestsAdapter作为默认适配器
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


class HttpError(Exception):
    """HTTP状态码错误异常"""

    def __init__(self, response, message=None):
        self.response = response
        self.status_code = response.status if response else 999
        self.message = message or f'HTTP Error {self.status_code}'
        super().__init__(self.message)


class BaseRespAdapter(ABC):
    """响应适配器接口,定义统一的响应处理方法"""

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


class RequestsAdapter(BaseRespAdapter):
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


class AiohttpAdapter(BaseRespAdapter):
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
    """统一响应类,提供同步和异步HTTP响应的统一接口"""

    # 类常量
    CHINESE_DOMAINS: ClassVar[list[str]] = ['baidu.com', 'sina.com', '163.com', 'qq.com', 'alibaba.com', 'taobao.com', 'jd.com', 'sohu.com']
    CHINESE_ENCODINGS: ClassVar[list[str]] = ['utf-8', 'gbk', 'gb18030', 'big5', 'gb2312']

    # 缓存属性
    _dom_cache: Any | None = None
    _query_cache: PyQuery | None = None
    _chinese_content_cache: dict | None = None

    def __init__(self, response: RawResponseType = None, content: ContentDataType = None, index: int | None = None, adapter: BaseRespAdapter | None = None, exception: Exception | None = None):
        """初始化统一响应对象"""
        self._raw = response
        self._index = index if index is not None else id(self)
        self._adapter = adapter or RespFactory._select_adapter(response)
        self._exception = exception
        self._error_type = type(exception).__name__ if exception else None

        # 处理内容
        self._content = self._process_content(content)

        # 初始化编码相关属性
        self._chinese_domains = self.CHINESE_DOMAINS
        self._chinese_encodings = self.CHINESE_ENCODINGS

        # 确定编码
        self._encoding = self._determine_encoding()

    def __repr__(self) -> str:
        base = f'{self.__class__.__name__} | STATUS:{self.status} | ID:{self._index}'
        return f'{base} | URL:{self.url}' if self._raw else base

    def __str__(self) -> str:
        return self.__repr__()

    def __bool__(self) -> bool:
        return self.status == 200

    def __len__(self) -> int:
        return len(self.text) if self.text else 0

    @property
    def ok(self):
        return RespFactory.is_success(self)

    @property
    def exception(self):
        return self._exception

    def raise_for_status(self):
        if not self.ok:
            raise HttpError(self)

    # ==================== 内容处理方法 ====================

    def _process_content(self, content: ContentDataType) -> bytes:
        """处理响应内容,转换为统一的字节格式"""
        if isinstance(content, str):
            return content.encode(DEFAULT_ENCODING, 'replace')
        if isinstance(content, bytes):
            return content
        if self._adapter:
            return self._adapter.get_content()
        return b''

    @property
    def text(self) -> str:
        """获取响应的文本内容,自动处理编码"""
        if isinstance(self._content, str):
            return self._content
        if isinstance(self._content, bytes):
            return self._decode_content(self._content, self._encoding)
        if self._raw:
            return self._get_raw_text()
        return ''

    def _decode_content(self, content: bytes, encoding: str) -> str:
        """解码字节内容,带有回退机制"""
        if not content:
            return ''

        # 首选编码解码
        try:
            return content.decode(encoding, errors='strict')
        except (UnicodeDecodeError, LookupError) as e:
            mylog.debug(f'首选编码[{encoding}]解码失败: {e}')

        # 回退解码策略
        return self._decode_with_fallback(content, encoding)

    def _decode_with_fallback(self, content: bytes, preferred_encoding: str) -> str:
        """使用回退策略解码内容"""
        # 构建编码尝试列表
        encodings_to_try = [preferred_encoding]

        # 如果有中文特征,添加中文编码
        if self._has_chinese_content():
            encodings_to_try.extend(self._chinese_encodings)
        else:
            encodings_to_try.extend(['utf-8', 'latin-1', 'iso-8859-1'])

        # 去重
        encodings_to_try = list(dict.fromkeys(encodings_to_try))

        # 尝试每种编码
        last_error = None
        for encoding in encodings_to_try:
            try:
                return content.decode(encoding, errors='strict')
            except (UnicodeDecodeError, LookupError) as e:
                last_error = e
                continue

        # 所有编码都失败,使用宽松方式
        mylog.warning(f'所有编码尝试失败,使用宽松解码: {last_error}')
        with suppress(Exception):
            return content.decode('utf-8', errors='replace')
        return content.decode('latin-1', errors='replace')

    def _get_raw_text(self) -> str:
        """从原始响应对象获取文本"""
        if not self._raw:
            return ''

        try:
            raw_text = None
            if callable(getattr(self._raw, 'text', None)):
                raw_text = self._raw.text()
            elif hasattr(self._raw, 'text'):
                raw_text = self._raw.text

            if raw_text is None:
                return ''

            if isinstance(raw_text, bytes):
                return self._decode_content(raw_text, self._encoding)
            if isinstance(raw_text, str):
                return raw_text
            return str(raw_text)

        except Exception as e:
            mylog.error(f'从原始响应获取文本失败: {e}')
            return ''

    # ==================== 编码检测方法 ====================

    def _has_chinese_content(self, sample_size: int = 1024) -> bool:
        """检查内容是否包含中文特征 - 带缓存版本"""
        if not self._content or len(self._content) == 0:
            return False

        # 使用缓存避免重复计算
        if self._chinese_content_cache is None:
            self._chinese_content_cache = {}

        cache_key = f'chinese_check_{hash(self._content[:100])}_{sample_size}'
        if cache_key in self._chinese_content_cache:
            return self._chinese_content_cache[cache_key]

        sample = self._content[:sample_size]
        result = self._check_chinese_content(sample)

        # 更新缓存（限制缓存大小）
        if len(self._chinese_content_cache) > 10:
            # 移除最早的一个缓存项
            self._chinese_content_cache.pop(next(iter(self._chinese_content_cache)))
        self._chinese_content_cache[cache_key] = result

        return result

    def _check_chinese_content(self, sample: bytes) -> bool:
        """检查字节样本是否包含中文内容"""
        # 1. 直接检查常见中文关键词的字节序列
        chinese_byte_patterns = [
            b'\xe4\xbd\xa0\xe5\xa5\xbd',  # 你好
            b'\xe4\xb8\xad\xe5\x9b\xbd',  # 中国
            b'\xe4\xb8\xad\xe6\x96\x87',  # 中文
            b'\xe7\xbd\x91\xe7\xab\x99',  # 网站
            b'\xe5\x86\x85\xe5\xae\xb9',  # 内容
            b'\xe6\xa0\x87\xe9\xa2\x98',  # 标题
            b'\xe6\x88\x91\xe6\x98\xaf',  # 我是
            b'\xe8\xbf\x99\xe6\x98\xaf',  # 这是
        ]

        if any(pattern in sample for pattern in chinese_byte_patterns):
            return True

        # 2. 检查UTF-8编码的中文字符模式
        utf8_chinese_patterns = [
            b'\xe4[\xb8-\xbf][\x80-\xbf]',  # 常用汉字区域1
            b'\xe5[\x80-\x9f][\x80-\xbf]',  # 常用汉字区域2
            b'\xe6[\x80-\xbf][\x80-\xbf]',  # 汉字扩展
            b'\xe7[\x80-\xbf][\x80-\xbf]',  # 汉字扩展
            b'\xe8[\x80-\xbf][\x80-\xbf]',  # 汉字扩展
            b'\xe9[\x80-\xbf][\x80-\xbf]',  # 汉字扩展
        ]

        for pattern in utf8_chinese_patterns:
            if re.search(pattern, sample):
                return True

        # 3. 检查GBK编码的中文字符特征
        with suppress(Exception):
            gbk_chinese_pattern = b'[\xb0-\xf7][\xa1-\xfe]'
            if re.search(gbk_chinese_pattern, sample):
                return True

        # 4. 尝试解码并检查关键词
        for encoding in ['utf-8', 'gbk']:
            with suppress(Exception):
                sample_text = sample.decode(encoding, errors='ignore')
                if any(ch in sample_text for ch in '你好中国中文网站内容标题我是这是'):
                    return True

        return False

    def _extract_encoding_from_content(self) -> str | None:
        """从内容中提取编码声明"""
        if not self._content:
            return None

        sample = self._content[:2048].lower()

        # 检查meta标签中的charset
        charset_patterns = [
            rb'charset\s*=\s*["\']?\s*([\w-]+)',
            rb'encoding\s*=\s*["\']?\s*([\w-]+)',
        ]

        for pattern in charset_patterns:
            match = re.search(pattern, sample)
            if match:
                encoding = match.group(1).decode('ascii', errors='ignore').lower()
                encoding = encoding.replace('_', '-')
                if encoding in ['utf8', 'utf8mb4']:
                    return 'utf-8'
                if encoding in ['gb2312']:
                    return 'gbk'
                if encoding in self._chinese_encodings:
                    return encoding

        return None

    def _is_chinese_domain(self, url: str) -> bool:
        """判断是否为中文网站域名"""
        url_lower = url.lower()
        return any(domain in url_lower for domain in self._chinese_domains)

    def _detect_encoding_with_chardet(self) -> str | None:
        """使用chardet检测编码"""
        if not self._content:
            return None

        try:
            import chardet

            result = chardet.detect(self._content)
            encoding = result.get('encoding')
            confidence = result.get('confidence', 0)

            if encoding and confidence > 0.6:
                encoding = encoding.lower()
                if encoding in ['utf8', 'utf8mb4']:
                    return 'utf-8'
                if encoding in ['gb2312']:
                    return 'gbk'
                return encoding

        except Exception as e:
            mylog.debug(f'chardet检测失败: {e}')

        return None

    def _determine_encoding(self) -> str:
        """确定响应内容的编码"""
        encoding_candidates = set()

        # 1. 从内容中提取声明的编码
        if content_encoding := self._extract_encoding_from_content():
            encoding_candidates.add(content_encoding)
            mylog.debug(f'从内容提取编码: {content_encoding}')

        # 2. 使用chardet检测
        if detected_encoding := self._detect_encoding_with_chardet():
            encoding_candidates.add(detected_encoding)
            mylog.debug(f'chardet检测编码: {detected_encoding}')

        # 3. 检查中文内容特征
        has_chinese = self._has_chinese_content()
        is_chinese_domain = self._is_chinese_domain(self.url)

        if has_chinese or is_chinese_domain:
            mylog.debug(f'检测到中文内容特征: 域名={is_chinese_domain}, 内容={has_chinese}')
            encoding_candidates.update(self._chinese_encodings)

        # 4. 适配器提供的编码
        if self._adapter and (adapter_encoding := self._adapter.get_encoding()):
            encoding_candidates.add(adapter_encoding)
            mylog.debug(f'适配器提供编码: {adapter_encoding}')

        # 5. 选择最佳编码
        final_encoding = self._select_best_encoding(list(encoding_candidates), has_chinese)
        mylog.debug(f'最终选择编码: {final_encoding}')

        return final_encoding

    def _select_best_encoding(self, candidates: list[str], has_chinese: bool) -> str:
        """从候选编码中选择最佳编码 - 简化修复版本"""
        if not candidates:
            return DEFAULT_ENCODING

        # 去重并保持顺序
        unique_candidates = []
        for enc in candidates:
            if enc and enc not in unique_candidates:
                unique_candidates.append(enc)

        # 优先选择 UTF-8（现代Web标准）
        if 'utf-8' in unique_candidates:
            return 'utf-8'

        # 如果有中文内容，选择其他中文编码
        if has_chinese:
            for encoding in ['gbk', 'gb18030', 'big5', 'gb2312']:
                if encoding in unique_candidates:
                    return encoding

        # 返回第一个候选编码
        return unique_candidates[0]

    # ==================== DOM解析方法 ====================

    def _get_lxml_dom(self) -> Any | None:
        """延迟初始化lxml的DOM对象"""
        if self._dom_cache is None and self.text:
            try:
                # 检查内容长度
                if len(self.text) > 10 * 1024 * 1024:
                    mylog.warning('HTML内容过大,可能影响解析性能')

                from lxml import html

                self._dom_cache = html.fromstring(self.text)

            except Exception as e:
                mylog.warning(f'DOM对象创建失败: {e}')
                self._dom_cache = self._parse_with_fallback()

        return self._dom_cache

    def _parse_with_fallback(self) -> Any | None:
        """使用后备解析器解析HTML"""
        # 方法1: 尝试使用soupparser
        try:
            from lxml.html import soupparser

            mylog.debug('尝试使用soupparser解析')
            return soupparser.fromstring(self.text)
        except ImportError:
            mylog.debug('未安装beautifulsoup4,无法使用soupparser')
        except Exception as e:
            mylog.debug(f'soupparser解析失败: {e}')

        # 方法2: 尝试使用html5lib
        try:
            import html5lib
            from lxml import html

            mylog.debug('尝试使用html5lib解析')
            document = html5lib.parse(self.text, treebuilder='lxml')
            return document.getroot()
        except ImportError:
            mylog.debug('未安装html5lib')
        except Exception as e:
            mylog.debug(f'html5lib解析失败: {e}')

        # 方法3: 尝试使用更宽松的HTMLParser
        try:
            from lxml import html

            mylog.debug('尝试使用宽松HTMLParser')
            parser = html.HTMLParser(
                encoding='utf-8',
                recover=True,
                remove_comments=True,
                remove_pis=True,
            )
            return html.fromstring(self.text.encode('utf-8'), parser=parser)
        except Exception as e:
            mylog.warning(f'所有HTML解析方法都失败: {e}')

        return None

    # ==================== PyQuery方法 ====================

    def _get_pyquery(self) -> PyQuery | None:
        """延迟初始化PyQuery对象"""
        if self._query_cache is None and self.text:
            try:
                self._query_cache = PyQuery(self.text, parser='html')
            except UnicodeDecodeError:
                if isinstance(self._content, bytes):
                    self._query_cache = PyQuery(self._content, parser='html', encoding=self._encoding)
                else:
                    self._query_cache = PyQuery(self.text.encode(self._encoding, 'ignore'), parser='html', encoding=self._encoding)
        return self._query_cache

    @property
    def query(self) -> PyQuery:
        """CSS选择器对象(PyQuery)"""
        result = self._get_pyquery()
        if result is None:
            return PyQuery('')
        return result

    # ==================== XPath方法 ====================

    def xpath(self, *args: str) -> list[list[Any]]:
        """执行XPath选择查询"""
        results = []
        if not args:
            return results

        dom = self.dom
        if dom is None:
            return [[] for _ in args]

        for arg in args:
            if not arg or not arg.strip():
                results.append([])
                continue

            try:
                if hasattr(dom, 'xpath'):
                    results.append(dom.xpath(arg))
                else:
                    results.append([])
            except Exception as e:
                mylog.warning(f'XPath查询失败: {arg}, 错误: {e}')
                results.append([])

        return results

    @property
    def dom(self) -> Any | None:
        """lxml的DOM对象,用于XPath解析"""
        return self._get_lxml_dom()

    # ==================== 基本属性 ====================

    @property
    def content(self) -> bytes:
        return self._content

    @property
    def encoding(self) -> str:
        return self._encoding

    @property
    def index(self) -> int:
        return self._index

    @property
    def raw(self) -> RawResponseType:
        return self._raw

    @property
    def elapsed(self) -> Any | None:
        if self._raw and hasattr(self._raw, 'elapsed'):
            return self._raw.elapsed
        return None

    @property
    def seconds(self) -> float:
        elapsed = self.elapsed
        return elapsed.total_seconds() if elapsed else 0.0

    @property
    def url(self) -> str:
        if self._adapter:
            return self._adapter.get_url()
        return getattr(self._raw, 'url', '')

    @property
    def cookies(self) -> dict[str, str]:
        if self._adapter:
            return self._adapter.get_cookies()
        if self._raw and hasattr(self._raw, 'cookies'):
            return dict(self._raw.cookies)
        return {}

    @property
    def headers(self) -> dict[str, str]:
        if self._adapter:
            return self._adapter.get_headers()
        if self._raw and hasattr(self._raw, 'headers'):
            return dict(self._raw.headers)
        return {}

    @property
    def status(self) -> int:
        if self._adapter:
            return self._adapter.get_status()
        if self._raw:
            return getattr(self._raw, 'status', getattr(self._raw, 'status_code', 999))
        return 999

    @property
    def status_code(self) -> int:
        return self.status

    @property
    def reason(self) -> str:
        if self._adapter:
            return self._adapter.get_reason()
        return getattr(self._raw, 'reason', '')

    @property
    def json(self) -> Any:
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

        return {}

    # ==================== 调试方法 ====================

    def debug_dom_info(self) -> dict:
        """调试DOM相关信息"""
        dom = self.dom
        has_dom = dom is not None
        dom_type = type(dom).__name__ if has_dom else None
        has_xpath_method = hasattr(dom, 'xpath') if has_dom else False
        root_tag = dom.tag if has_dom and hasattr(dom, 'tag') else None

        return {
            'has_dom': has_dom,
            'dom_type': dom_type,
            'has_xpath_method': has_xpath_method,
            'text_length': len(self.text) if self.text else 0,
            'content_type': type(self._content).__name__,
            'root_tag': root_tag,
        }


if __name__ == '__main__':

    def run_test(url: str):
        """运行测试"""
        mylog.info('=' * 70)
        mylog.info(f'正在测试网址: {url}')

        try:
            # 导入get函数
            from xt_requests import get

            # 获取原始响应
            raw_response = get(url)

            # 创建统一响应对象
            unified_resp = RespFactory.create_response(raw_response)

            mylog.info(f'响应状态: {unified_resp.status}|{unified_resp.index}')
            mylog.info(f'响应URL: {unified_resp.url}')
            mylog.info(f'响应编码: {unified_resp.encoding}')
            # 测试HTML解析功能
            title = unified_resp.xpath('//title/text()')
            mylog.info(f'页面标题: {title[0] if title and title[0] else "未找到"}')
            mylog.info(f'页面内容: {unified_resp.text[:100]}')

            # 增加更多的xpath测试内容
            xpath_result = unified_resp.xpath('//title/text()')
            mylog.info(f'xpath(//title/text()) : {xpath_result}')

            xpath_multi = unified_resp.xpath('//title/text()', '//title/text()')
            mylog.info(f'xpath([//title/text(), //title/text()]) : {xpath_multi}')

            query_result = unified_resp.query('title').text()
            mylog.info(f'query(title).text() : {query_result}')

            # 只有在DOM有效时才执行这个测试
            if unified_resp.dom is not None and hasattr(unified_resp.dom, 'xpath'):
                try:
                    dom_result = unified_resp.dom.xpath('//title/text()')
                    mylog.info(f'dom.xpath(//title/text()) : {dom_result}')
                except Exception as e:
                    mylog.warning(f'direct dom.xpath failed: {e}')
            else:
                mylog.info('dom.xpath: DOM对象不可用')

            mylog.info('测试完成!')
        except Exception as e:
            mylog.error(f'测试失败: {e}')
            import traceback

            mylog.error(f'详细堆栈: {traceback.format_exc()}')

    # 选择常用中文网址作为测试目标
    test_urls = [
        'https://www.baidu.com',
        'https://www.sina.com.cn',
        'https://cn.bing.com',
    ]

    # 运行测试
    for url in test_urls:
        run_test(url)

    mylog.info('\n\n所有测试完成!')
