# !/usr/bin/env python
"""
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-07 15:02:23
FilePath     : /xjLib/xt_Response.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from chardet import detect
from html2text import HTML2Text
from lxml import etree
from pyquery import PyQuery
from requests_html import HTML


class htmlResponse:
    """封装网页抓取结果,使之标准化"""

    __slots__ = ("raw", "_content", "index", "encoding", "code_type")

    def __init__(self, response, content=None, index=None):
        self.index: int = index or id(self)

        if response is not None:
            self.raw = response
            self._content: bytes = content if content else response.content
            self.encoding = response.encoding if hasattr(response, "encoding") else "utf-8"
            self.code_type = detect(self._content)["encoding"] if isinstance(self._content, bytes) else self.encoding
        else:
            self.raw = None
            self._content = b""
            self.encoding = "utf-8"
            self.code_type = "utf-8"

    def __repr__(self):
        if self.raw is None:
            return f"<htmlResponse [None] | ID:[{self.index}]>"
        return f"<htmlResponse [{self.status}] | ID:[{self.index}] | URL:[{self.url}]>"

    def __str__(self):
        return self.__repr__()

    def __bool__(self):
        return self.status == 200

    def __len__(self):
        if self.text:
            return len(self.text)
        else:
            return 0

    @property
    def content(self):
        if isinstance(self.code_type, str):
            return self._content.decode(self.code_type, "ignore")

    @property
    def text(self):
        if self.raw:
            return self.raw.text.encode(self.encoding).decode(self.code_type, "ignore")
        else:
            return self.content

    @property
    def elapsed(self):
        if self.raw and hasattr(self.raw, "elapsed"):
            return self.raw.elapsed
        else:
            return None

    @property
    def seconds(self):
        if self.raw and hasattr(self.raw, "elapsed"):
            return self.raw.elapsed.total_seconds()
        else:
            return 0

    @property
    def url(self):
        if self.raw and hasattr(self.raw, "url"):
            return self.raw.url

    @property
    def cookies(self):
        if self.raw and hasattr(self.raw, "cookies"):
            return self.raw.cookies

    @property
    def headers(self):
        if self.raw and hasattr(self.raw, "headers"):
            return self.raw.headers

    @property
    def status(self):
        if self.raw:
            return self.raw.status if hasattr(self.raw, "status") else self.raw.status_code

    @property
    def html(self, filter="//script"):
        element = self.element
        trashs = element.xpath(filter)
        for item in trashs:
            item.getparent().remove(item)
        return element

    @property
    def element(self):
        return etree.HTML(self.content, parser=None)

    @property
    def dom(self):
        """
        返回requests_html对象,支持html对象操作:find, xpath, render(先安装chromium浏览器)
        """
        html = HTML(html=self._content)
        setattr(html, "url", self.url)
        return html

    @property
    def query(self):
        return PyQuery(self.html)  # , parser='xml')

    def xpath(self, selectors: str | list | tuple = "") -> list:
        """
        在元素上执行XPath选择。
        参数selectors: XPath选择器,可以是字符串或字符串的列表/元组。
        返回值: 选择的元素列表。
        """
        if isinstance(selectors, str):
            selectors = [selectors] if selectors.strip() else []
        elif isinstance(selectors, list | tuple):
            selectors = [selector for selector in selectors if isinstance(selector, str) and selector.strip()]

        return [self.element.xpath(selector) for selector in selectors]

    @property
    def ctext(self):
        h = HTML2Text()
        h.ignore_links = True
        if self.raw:
            return h.handle(self.raw.text)


if __name__ == "__main__":
    print(htmlResponse(None))
