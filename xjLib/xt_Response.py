# !/usr/bin/env python
"""
==============================================================
模块名称     : xt_response.py
功能描述     : 网页响应封装模块 - 提供统一的HTTP响应处理、解析和数据提取功能
开发工具     : VSCode
作者         : Even.Sand
联系方式     : sandorn@163.com
创建时间     : 2022-12-22 17:35:56
最后修改时间 : 2025-09-19 16:30:00
文件路径     : /xjLib/xt_response.py
Github       : https://github.com/sandorn/home

【核心功能】
- BaseResponse: 基础响应类，提供通用的响应处理功能
- HtmlResponse: 扩展响应类，提供HTML解析和数据提取功能
- ACResponse: 异步响应类，专门处理aiohttp库的异步响应
- 支持多种解析方式: XPath、DOM、PyQuery、lxml等
- JSON数据解析与提取
- Unicode文本规范化和清理
- 自动编码检测与处理

【主要特性】
- 统一的响应对象接口，兼容requests和aiohttp等库
- 模块化设计，分离基础功能和扩展功能
- 健壮的错误处理和数据转换机制
- 丰富的文本处理功能，支持Unicode规范化
- 完善的类型注解，提升代码可读性和IDE支持
- 多级缓存机制，提高解析性能

【使用示例】
    >>> from xt_requests import get
    >>> response = get('https://example.com')
    >>> print(response.status)  # 获取状态码
    200
    >>> print(response.text[:100])  # 获取前100个字符的文本内容
    >>> title = response.xpath('//title/text()')[0][0]  # 使用XPath提取标题

【参数说明】
    - response: 原始HTTP响应对象(如requests.Response, aiohttp.ClientResponse)
    - content: 响应内容(字符串或字节流)，可选
    - index: 响应对象的唯一标识符，可选

【注意事项】
    - 需要安装可选依赖: lxml, pyquery, requests_html, beautifulsoup4, chardet
    - 对于aiohttp响应，推荐使用ACResponse类
    - 编码检测依赖于chardet库，对于特殊编码内容可能需要手动指定编码
    - 部分功能需要安装相应依赖库才能使用
==============================================================
"""

from __future__ import annotations

import json
import re
from collections.abc import Sequence
from typing import Any

import lxml
import requests_html
from bs4 import BeautifulSoup
from chardet import detect
from pyquery import PyQuery
from xt_unicode import text_cleaner
from xt_wraps import LogCls

# 初始化日志
logger = LogCls()

DEFAULT_ENCODING = 'utf-8'


class BaseResponse:
    """基础响应类，提供通用的HTTP响应处理功能。

    封装HTTP响应的通用属性和方法，作为特定响应类型的基类。
    支持访问响应内容、状态码、URL等基本属性。
    兼容requests和aiohttp等HTTP库的响应对象。
    """

    __slots__ = ('_content', '_encoding', '_index', '_raw')

    def __init__(
        self,
        response: Any | None = None,
        content: Any | None = None,
        index: int | None = None,
    ):
        """初始化基础响应对象。

        Args:
            response: 原始HTTP响应对象(如requests.Response)
            content: 响应内容(字符串或字节流)
            index: 响应对象的唯一标识符
        """
        self._index: int = index if index is not None else id(self)
        self._raw = response
        self._content: bytes = self._process_content(content, response)
        self._encoding: str = self._determine_encoding()

    def _process_content(self, content: Any, response: Any) -> bytes:
        """处理响应内容，转换为统一的字节格式

        Args:
            content: 响应内容，可以是字符串、字节流或其他类型
            response: 原始响应对象，用于获取content属性

        Returns:
            bytes: 统一格式的字节内容
        """
        if isinstance(content, str):
            # 字符串内容转换为字节流
            return content.encode(DEFAULT_ENCODING, 'replace')
        if isinstance(content, bytes):
            # 已经是字节流，直接返回
            return content
        if response and hasattr(response, 'content'):
            # 从原始响应对象获取内容
            return response.content
        # 无法处理的情况，返回空字节流
        return b''

    def _determine_encoding(self) -> str:
        """确定响应内容的编码

        处理流程:
        1. 尝试使用chardet库自动检测编码
        2. 如果检测失败或无结果，使用原始响应对象的编码
        3. 如果以上都失败，使用默认编码(utf-8)

        Returns:
            str: 确定的编码名称
        """
        try:
            # 优先使用chardet自动检测编码
            detected_encoding = detect(self._content).get('encoding')
            if detected_encoding:
                return detected_encoding
        except Exception as e:
            logger.warning(f'编码检测失败: {e}')

        # 如果chardet检测失败，尝试使用原始响应对象的编码
        if self._raw and hasattr(self._raw, 'encoding'):
            return self._raw.encoding

        # 最后返回默认编码
        return DEFAULT_ENCODING

    def __repr__(self) -> str:
        """返回对象的字符串表示"""
        if self._raw is None:
            return f'{self.__class__.__name__} | STATUS:{self.status} | ID:{self._index}'
        return f'{self.__class__.__name__} | STATUS:{self.status} | ID:{self._index} | URL:{self.url}'

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
        """获取响应的文本内容，自动处理编码

        处理流程:
        1. 如果内容已经是字符串，直接返回
        2. 如果内容是字节流，使用确定的编码解码
        3. 如果存在原始响应对象，尝试获取其text属性
        4. 处理过程中捕获异常并记录错误日志

        Returns:
            str: 解码后的文本内容，解码失败返回空字符串
        """
        if isinstance(self._content, str):
            # 内容已经是字符串，直接返回
            return self._content

        try:
            if isinstance(self._content, bytes):
                # 内容是字节流，使用确定的编码解码
                return self._content.decode(self._encoding, 'ignore')

            if self._raw:
                # 处理原始响应对象的text属性
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
            logger.error(f'文本解码失败: {e}')

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
    def raw(self) -> Any:
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
        return getattr(self._raw, 'url', '')

    @property
    def cookies(self) -> dict[str, str]:
        """获取响应的Cookie"""
        if self._raw and hasattr(self._raw, 'cookies'):
            return dict(self._raw.cookies)
        return {}

    @property
    def headers(self) -> dict[str, str]:
        """获取响应的HTTP头部"""
        if self._raw and hasattr(self._raw, 'headers'):
            return dict(self._raw.headers)
        return {}

    @property
    def status(self) -> int:
        """获取响应的状态码"""
        if self._raw:
            return getattr(self._raw, 'status', getattr(self._raw, 'status_code', 999))
        return 999

    @property
    def status_code(self) -> int:
        """获取响应的状态码(status的别名)"""
        return self.status

    @property
    def json(self) -> Any:
        """解析JSON响应内容

        尝试将响应内容解析为JSON对象，支持常见的JSON格式解析。
        如解析失败会抛出异常，使用时建议进行异常处理。

        Returns:
            Any: 解析后的JSON对象（通常为字典或列表）

        Raises:
            ValueError: 当响应内容不是有效的JSON格式时
        """
        # 首先尝试使用raw对象的json方法
        if self._raw and hasattr(self._raw, 'json'):
            try:
                return self._raw.json()
            except (ValueError, TypeError, AttributeError) as e:
                logger.debug(f'使用raw.json()解析失败: {e}')

        # 尝试使用标准json模块解析text属性
        try:
            if self.text:
                return json.loads(self.text)
        except (ValueError, TypeError) as e:
            logger.debug(f'使用json.loads()解析失败: {e}')

        # 解析失败时返回空字典
        return {}


class HtmlResponse(BaseResponse):
    """HTML响应类，提供HTML解析和数据提取功能。
    继承自BaseResponse，增加了针对HTML内容的解析和数据提取方法。
    支持多种解析引擎：lxml、PyQuery、requests_html等。
    """

    # 缓存属性，避免重复解析
    _html_cache: Any | None = None
    _element_cache: Any | None = None
    _dom_cache: Any | None = None
    _query_cache: PyQuery | None = None
    _soup_cache: BeautifulSoup | None = None

    @property
    def html(self) -> Any:
        """解析HTML，返回lxml.html.HtmlElement对象

        使用lxml.html模块解析HTML内容，提供更丰富的HTML处理功能。
        自动缓存结果，避免重复解析，提升性能。

        Returns:
            lxml.html.HtmlElement: 解析后的HTML元素对象，解析失败返回None

        Example:
            >>> response = HtmlResponse('<div class="content"><h1>Title</h1><p>Paragraph</p></div>')
            >>> title = response.html.xpath('//h1/text()')[0]  # 获取标题文本
            >>> links = response.html.xpath('//a/@href')  # 获取所有链接
            >>> response.html.make_links_absolute('https://example.com')  # 转换相对链接为绝对链接
        """
        if self._html_cache is None:
            try:
                # 优先尝试使用content直接解析
                html_content = self._content if isinstance(self._content, bytes) else str(self._content).encode(self._encoding, 'ignore')
                # 配置parser，确保正确处理编码
                parser = lxml.html.HTMLParser(encoding=self._encoding)
                self._html_cache = lxml.html.fromstring(html_content, base_url=str(self.url), parser=parser)
            except ImportError:
                logger.error('lxml库未安装，无法使用html属性')
                self._html_cache = None
            except Exception as e:
                logger.warning(f'HTML解析失败: {e}')
                # 备用方案：使用etree并指定编码
                self._html_cache = self.element
        return self._html_cache

    @property
    def element(self) -> Any:
        """解析HTML文档，返回lxml.etree._Element对象

        使用lxml.etree模块解析HTML内容，提供基础的XML解析功能。
        与html属性相比，更专注于XML解析能力。

        Returns:
            lxml.etree._Element: 解析后的根节点元素，解析失败返回None

        Example:
            >>> response = HtmlResponse('<div class="content"><h1>Title</h1><p>Paragraph</p></div>')
            >>> root = response.element
            >>> title = root.find('.//h1').text  # 查找h1元素并获取文本
            >>> paragraphs = root.findall('.//p')  # 查找所有p元素
            >>> for p in paragraphs:
            ...     print(p.text)
        """
        if self._element_cache is None:
            try:
                # 优先尝试使用content直接解析
                html_content = self._content if isinstance(self._content, bytes) else str(self._content).encode(self._encoding, 'ignore')
                # 配置parser，确保正确处理编码
                parser = lxml.etree.HTMLParser(encoding=self._encoding)
                self._element_cache = lxml.etree.HTML(html_content, base_url=str(self.url), parser=parser)
            except ImportError:
                logger.error('lxml库未安装，无法使用element属性')
                self._element_cache = None
            except Exception as e:
                logger.warning(f'Element解析失败: {e}')
                # 备用方案：直接使用text并指定编码
                try:
                    parser = lxml.etree.HTMLParser(encoding=self._encoding)
                    self._element_cache = lxml.etree.HTML(
                        self.text.encode(self._encoding, 'ignore'),
                        base_url=str(self.url),
                        parser=parser,
                    )
                except Exception:
                    self._element_cache = None
        return self._element_cache

    @property
    def soup(self) -> BeautifulSoup:
        """返回BeautifulSoup对象，提供灵活的HTML解析功能

        优先使用lxml作为解析器，如不可用则回退到Python标准库的html.parser。
        BeautifulSoup提供了简单灵活的API来导航、搜索和修改HTML树结构。

        Returns:
            BeautifulSoup: BeautifulSoup对象实例，解析失败返回None

        Example:
            >>> response = HtmlResponse('<div class="content"><h1>Title</h1><p>Paragraph</p></div>')
            >>> soup = response.soup
            >>> title = soup.find('h1').text  # 查找h1元素并获取文本
            >>> paragraphs = soup.find_all('p', class_='content')  # 按类名查找p元素
            >>> soup.title.string = 'New Title'  # 修改标题内容
            >>> modified_html = soup.prettify()  # 获取格式化的HTML
            >>> soup.select('h1')  # 使用CSS选择器查找h1元素
            >>> soup.select('h1')[0].text
        """
        try:
            try:
                parser = 'lxml'
            except ImportError:
                parser = 'html.parser'
                logger.debug('lxml不可用，使用html.parser')

            self._soup_cache = BeautifulSoup(self._content, parser)
            return self._soup_cache
        except ImportError:
            logger.error('bs4库未安装，无法使用soup属性')
            self._soup_cache = None
        except Exception as e:
            logger.warning(f'Soup解析失败: {e}')
            self._soup_cache = None
        return self._soup_cache

    @property
    def dom(self) -> Any:
        """返回requests_html.HTML对象，提供增强的HTML解析功能

        requests_html库提供了额外的功能，如JavaScript渲染(需安装chromium)、
        更简洁的选择器API等。适合需要处理动态网页内容的场景。

        Returns:
            requests_html.HTML: HTML解析对象，解析失败返回None

        Example:
            >>> response = HtmlResponse('<div class="content"><h1>Title</h1><p>Paragraph</p></div>')
            >>> dom = response.dom
            >>> title = dom.xpath('//h1/text()')[0]  # 使用XPath选择器
            >>> paragraphs = dom.find('p')  # 使用CSS选择器
            >>> # 对于动态网页，可使用render()方法执行JavaScript(需安装chromium)
            >>> # dom.render()  # 渲染JavaScript
            >>> links = [link.attrs['href'] for link in dom.find('a')]  # 提取所有链接
        """
        if self._dom_cache is None:
            try:
                self._dom_cache = requests_html.HTML(html=self._content, url=str(self.url))
            except ImportError:
                logger.error('requests_html库未安装，无法使用dom属性')
                self._dom_cache = None
            except Exception as e:
                logger.warning(f'DOM解析失败: {e}')
                self._dom_cache = None
        return self._dom_cache

    @property
    def query(self) -> PyQuery:
        """返回PyQuery对象，支持jQuery风格的CSS选择器

        PyQuery提供了类似jQuery的API，使用CSS选择器来选取和操作HTML元素，
        语法简洁直观，适合熟悉jQuery的用户。

        Returns:
            PyQuery: PyQuery对象实例，解析失败返回空的PyQuery对象

        Example:
            >>> response = HtmlResponse('<div class="content"><h1>Title</h1><p>Paragraph</p></div>')
            >>> q = response.query
            >>> title = q('h1').text()  # 获取h1元素的文本
            >>> content = q('.content').html()  # 获取class为content的元素的HTML内容
            >>> links = q('a').map(lambda i, e: PyQuery(e).attr('href')).items()  # 提取所有链接
            >>> q('p').each(lambda i, e: print(PyQuery(e).text()))  # 遍历所有p元素
        """
        if self._query_cache is None:
            try:
                html_str = self._content.decode(self._encoding, 'ignore') if isinstance(self._content, bytes) else str(self._content)
                self._query_cache = PyQuery(html_str, parser='html')
            except Exception as e:
                logger.warning(f'PyQuery解析失败: {e}')
                try:
                    self._query_cache = PyQuery(self.text, parser='html')
                except Exception:
                    self._query_cache = PyQuery('')
        return self._query_cache

    def xpath(self, selectors: str | Sequence[str] = '') -> list[list[Any]]:
        """执行XPath选择查询

        提供统一的XPath查询接口，支持单个或多个XPath选择器。
        优先使用lxml的xpath方法，如不可用则尝试使用BeautifulSoup的CSS选择器。

        Args:
            selectors: XPath选择器，可以是单个字符串或字符串列表

        Returns:
            list[list[Any]]: 选择的元素列表，每个选择器对应一个结果列表

        Example:
            >>> response = HtmlResponse('<div class="content"><h1>Title</h1><p>Paragraph</p><a href="https://example.com">Link</a></div>')
            >>> # 单个XPath选择器 - 获取标题文本
            >>> titles = response.xpath('//h1/text()')
            >>> # titles = [['Title']]
            >>> # 多个XPath选择器 - 同时获取标题和段落
            >>> results = response.xpath(['//h1/text()', '//p/text()'])
            >>> # results = [['Title'], ['Paragraph']]
            >>> # 获取属性值 - 提取所有链接的href属性
            >>> links = response.xpath('//a/@href')
            >>> # 使用条件选择器 - 按类名查找元素
            >>> content_divs = response.xpath('//div[@class="content"]')
            >>> # 获取嵌套元素 - 查找content类下的所有p元素
            >>> content_paragraphs = response.xpath('//div[@class="content"]//p/text()')
        """

        # 处理空选择器的情况 - 统一检查逻辑
        if not selectors or (isinstance(selectors, str) and not selectors.strip()):
            return [[]]

        # 统一处理为列表形式
        selector_list = [selectors] if isinstance(selectors, str) else selectors
        results = []

        for selector in selector_list:
            # 检查选择器是否为字符串并且非空（去除空白后）
            if not isinstance(selector, str) or not selector.strip():
                results.append([])
                continue

            try:
                # 优先使用lxml的xpath方法
                if hasattr(self.html, 'xpath') and self.html is not None:
                    selector_results = self.html.xpath(selector)
                    results.append(selector_results)
                elif self.soup is not None:
                    # 备用方案：尝试使用BeautifulSoup的CSS选择器
                    # ! 将XPath转换为CSS选择器，可能不完美
                    selector_results = self.soup.select(selector)
                    results.append(selector_results)
                else:
                    results.append([])
            except Exception as e:
                logger.warning(f'XPath查询失败: {selector}, 错误: {e}')
                results.append([])

        return results

    @property
    def ctext(self) -> str:
        """获取纯净文本内容，去除HTML标签、脚本、样式和链接

        对原始文本进行多步骤清理：移除标题、脚本、样式、注释等非内容元素，
        保留段落结构和有意义的文本内容，适合文本分析和内容提取场景。

        Returns:
            str: 清理后的纯净文本内容
        """

        try:
            soup = self.soup
            if not soup:
                return self.text

            # 移除不需要的标签（扩展列表以提高清理效果）
            for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'form', 'iframe', 'noscript', 'meta', 'link', 'button', 'input']):
                tag.decompose()

            # 提取文本并保留段落结构
            text = soup.get_text()

            # 优化文本清理流程，保留段落结构
            lines = []
            for line in text.splitlines():
                line = line.strip()
                if line:  # 只保留非空行
                    # 压缩行内多余空格
                    line = re.sub(r'[ \t]+', ' ', line)
                    lines.append(line)

            # 保留段落分隔（空行）
            text = '\n'.join(lines)
            return re.sub(r'\n{3,}', '\n\n', text)  # 多个空行压缩为两个
        except Exception as e:
            logger.error(f'纯净文本提取失败: {e}')
            return self.text

    @property
    def clean_text(self) -> str:
        """对文本进行深度清理和规范化处理

        在ctext的基础上进一步优化文本质量：执行Unicode规范化、
        移除不可见字符、合并多余空白等，适合对文本质量要求较高的场景。

        Returns:
            str: 完全规范化和清理后的文本内容
        """
        try:
            raw_text = self.text
            return text_cleaner.clean_and_normalize(raw_text)
        except Exception as e:
            logger.error(f'文本清理失败: {e}')
            return self.text


class ACResponse(HtmlResponse):
    """异步响应处理类，专门用于处理aiohttp异步响应

    继承自HtmlResponse，针对aiohttp的响应对象进行封装，提供与同步响应
    相同的丰富属性和方法，支持异步环境下的HTML解析、文本提取等操作。

    Args:
        response: aiohttp.ClientResponse对象
        url: 请求的URL
        encoding: 响应内容的编码方式
    """

    def __init__(
        self,
        response: Any | None = None,
        content: Any | None = None,
        index: int | None = None,
    ):
        """初始化异步响应对象。

        Args:
            response: 原始aiohttp响应对象
            content: 响应内容(字符串或字节流)
            index: 响应对象的唯一标识符
        """
        super().__init__(response=response, content=content, index=index)

    @property
    def text(self) -> str:
        """获取响应的文本内容，针对aiohttp响应对象进行优化"""
        # 对aiohttp的响应对象进行特殊处理
        if self._raw and hasattr(self._raw, 'content') and isinstance(self._raw.content, bytes):
            return self._raw.content.decode(self._encoding, 'ignore')
        return super().text

    @property
    def status(self) -> int:
        """获取响应的状态码，针对aiohttp响应对象进行优化"""
        if self._raw:
            return getattr(self._raw, 'status', 999)
        return 999

    @property
    def reason(self) -> str:
        """获取aiohttp响应的原因短语"""
        if self._raw and hasattr(self._raw, 'reason'):
            return self._raw.reason
        return ''

    @property
    def request_info(self) -> Any:
        """获取aiohttp请求信息"""
        if self._raw and hasattr(self._raw, 'request_info'):
            return self._raw.request_info
        return None

    @property
    def history(self) -> list[Any]:
        """获取aiohttp响应的重定向历史"""
        if self._raw and hasattr(self._raw, 'history'):
            return self._raw.history
        return []


# 为保持向后兼容性，保留原来的htmlResponse名称
htmlResponse = HtmlResponse  # noqa

if __name__ == '__main__':
    from xt_requests import get

    # 选择常用中文网址作为测试目标
    chinese_urls = [
        'https://www.baidu.com',  # 百度 - 中文搜索引擎
        'https://www.sina.com.cn',  # 新浪 - 综合门户网站
        'https://www.163.com',  # 网易 - 综合门户网站
        'https://www.zhihu.com',  # 知乎 - 问答社区
        'https://news.qq.com',  # 腾讯新闻 - 新闻网站
        'https://www.ctrip.com',  # 携程 - 旅游网站
        'https://www.jd.com',  # 京东 - 电商网站
    ]

    def test_base_attributes(response):
        """测试基础响应属性"""
        logger.info('=' * 60)
        logger.info(f'测试URL: {response.url} | 状态码: {response.status} | 编码: {response.encoding} | 响应对象类型: {type(response).__name__} | __repr__: {response!r}')
        logger.info('请求头示例(前5个):')
        for _, (key, value) in enumerate(list(response.headers.items())[:1]):
            logger.info(f'  {key}: {value}')
        logger.info(f'Cookie数量: {len(response.cookies)}')
        if response.cookies:
            logger.info(f'Cookie示例: {response.cookies.items()}')

    def test_html_parsing(response):
        """测试HTML解析功能"""
        logger.info('-' * 50)
        # 测试标题解析
        title_xpath = '//title/text()'
        title_css = 'title'

        # 使用不同的解析方式获取标题
        logger.info('页面标题解析:')
        try:
            dom_title = response.dom.xpath(title_xpath)[0] if response.dom.xpath(title_xpath) else 'N/A'
            logger.info(f'  dom.xpath: {dom_title}')
        except Exception as e:
            logger.error(f'  dom.xpath 解析失败: {e!s}')

        try:
            query_title = response.query(title_css).text() if response.query(title_css) else 'N/A'
            logger.info(f'  query: {query_title}')
        except Exception as e:
            logger.error(f'  query 解析失败: {e!s}')

        try:
            element_title = response.element.xpath(title_xpath)[0] if response.element.xpath(title_xpath) else 'N/A'
            logger.info(f'  element.xpath: {element_title}')
        except Exception as e:
            logger.error(f'  element.xpath 解析失败: {e!s}')

        try:
            html_title = response.html.xpath(title_xpath)[0] if response.html.xpath(title_xpath) else 'N/A'
            logger.info(f'  html.xpath: {html_title}')
        except Exception as e:
            logger.error(f'  html.xpath 解析失败: {e!s}')

        try:
            html_title = response.soup.select(title_css)[0].text if response.soup.select(title_css) else 'N/A'
            logger.info(f'  soup.select: {html_title}')
        except Exception as e:
            logger.error(f'  soup.select 解析失败: {e!s}')
        # 测试自定义xpath方法
        try:
            custom_xpath_title = response.xpath(title_xpath)[0][0] if response.xpath(title_xpath) else 'N/A'
            logger.info(f'  自定义xpath方法: {custom_xpath_title}')
        except Exception as e:
            logger.error(f'  自定义xpath方法 解析失败: {e!s}')

    def test_text_processing(response):
        """测试文本处理功能"""
        logger.info('-' * 50)
        logger.info('文本处理测试:')

        # 获取页面文本样本
        sample_text = response.text[:200] + '...' if len(response.text) > 200 else response.text
        logger.info(f'原始文本样本: {sample_text}')

        # 测试clean_text
        clean_sample = response.clean_text[:200] + '...' if len(response.clean_text) > 200 else response.clean_text
        logger.info(f'清理后文本样本: {clean_sample}')
        logger.info(f'清理后文本样本2: {response.ctext[:200]}')

    def test_json_parsing(response):
        """测试JSON解析功能"""
        logger.info('\n' + '-' * 50)
        logger.info('\nJSON解析测试:')
        try:
            json_data = response.json
            if isinstance(json_data, dict) and json_data:
                logger.info(f'JSON数据类型: {type(json_data)}')
                logger.info(f'JSON键数量: {len(json_data)}')
                # 显示前5个键值对
                json_preview = dict(list(json_data.items())[:5])
                logger.info(f'JSON数据预览: {json_preview}')
            else:
                logger.info('响应内容不包含有效JSON数据')
        except Exception as e:
            logger.error(f'JSON解析失败: {e!s}')

    def run_comprehensive_test(urls_to_test=None, max_urls=3):
        """运行全面测试，测试常用中文网站的响应处理"""
        if urls_to_test is None:
            urls_to_test = chinese_urls  # 默认测试前3个网址

        logger.info('=' * 70)
        logger.info('响应类综合测试 - 常用中文网站')

        for url in urls_to_test:
            try:
                logger.info('=' * 70)
                logger.info(f'正在测试网站: {url}')

                # 获取响应
                response = get(url)

                # 测试基础属性
                # test_base_attributes(response)

                # 测试HTML解析
                test_html_parsing(response)

                # 测试文本处理
                # test_text_processing(response)

                # 测试JSON解析 (如果适用)
                # test_json_parsing(response)

            except Exception as e:
                logger.error(f'\n测试网址 {url} 时出错: {e!s}')
                import traceback

                traceback.print_exc()

        # 运行兼容性测试

        logger.info('=' * 70)
        logger.info('测试完成')
        logger.info('=' * 70)

    # 运行全面测试，默认测试前3个常用中文网址
    run_comprehensive_test()
