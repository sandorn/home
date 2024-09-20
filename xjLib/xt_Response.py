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

from typing import Sequence

from chardet import detect
from html2text import HTML2Text
from pyquery import PyQuery

DEFAULT_ENCODING = "utf-8"


class htmlResponse:
    """封装网页结果,标准化"""

    __slots__ = ("raw", "content", "index", "encoding")

    def __init__(self, response=None, content=None, index=None):
        self.index: int = index or id(self)
        self.raw = response
        self.content: bytes = (
            content.encode(DEFAULT_ENCODING, "replace")
            if isinstance(content, str)
            else (
                content
                if isinstance(content, bytes)
                else (response.content if response else b"")
            )
        )
        self.encoding = detect(self.content).get("encoding") or getattr(
            response, "encoding", DEFAULT_ENCODING
        )

    def __repr__(self):
        if self.raw is None:
            return f"<htmlResponse [999] | {self.content} | ID:[{self.index}]>"
        return f"<htmlResponse [{self.status}] | ID:[{self.index}] | URL:[{self.url}]>"

    def __str__(self):
        return self.__repr__()

    def __bool__(self):
        return self.status == 200

    def __len__(self):
        return len(self.text) if self.text else 0

    @property
    def text(self):
        if isinstance(self.content, bytes):
            return self.content.decode(self.encoding, "ignore")
        elif isinstance(self.content, str):
            return self.content.encode(self.encoding).decode(self.encoding, "ignore")
        elif self.raw:
            return (
                self.raw.text.encode(self.encoding).decode(self.encoding, "ignore")
                if not callable(self.raw.text)
                else self.raw.text()
                .encode(self.encoding)
                .decode(self.encoding, "ignore")
            )
        else:
            return ""

    @property
    def elapsed(self):
        if self.raw and hasattr(self.raw, "elapsed"):
            return self.raw.elapsed
        else:
            return None

    @property
    def seconds(self):
        return (
            self.raw.elapsed.total_seconds()
            if self.raw and hasattr(self.raw, "elapsed")
            else 0
        )

    @property
    def url(self):
        return getattr(self.raw, "url", "")

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
        return getattr(self.raw, "status", getattr(self.raw, "status_code", 999))

    @property
    def html(self):
        """解析HTML，返回一个单一元素/文档。
        这个方法尝试最小化地解析文本块，而不知道它是片段还是文档。
        base_url将设置文档的base_url属性（以及树的docinfo.URL）
        html.base_url # 返回文档的基本URL
        """
        from lxml import html

        return html.fromstring(self.content.decode(self.encoding), base_url=self.url)

    @property
    def element(self):
        """
        解析字符串常量的HTML文档。返回根节点(或解析器目标返回的结果)。此函数可用于在Python代码中嵌入“HTML文字”。
        element.base # 返回文档的基本URL
        """
        from lxml import etree

        return etree.HTML(self.content.decode(self.encoding), base_url=self.url)

    @property
    def dom(self):
        """
        返回requests_html对象,支持html对象操作:find, xpath, render(先安装chromium浏览器)
        dom.url # 返回文档的基本URL
        """
        from requests_html import HTML

        html = HTML(html=self.content, url=self.url)
        return html

    @property
    def query(self):
        return PyQuery(self.html)

    def xpath(self, selectors: str | Sequence[str] = "") -> list:
        """
        在元素上执行XPath选择。
        参数selectors: XPath选择器,str | Sequence[str]。
        返回值: 选择的元素列表。
        """
        ele_list = [selectors] if isinstance(selectors, str) else list(selectors)

        return [
            self.element.xpath(ele_item)
            for ele_item in ele_list
            if isinstance(ele_item, str) and ele_item.strip()
        ]

    @property
    def ctext(self):
        "纯净字符串"
        h = HTML2Text()
        h.ignore_links = True
        if self.raw:
            return h.handle(self.raw.text)


class ACResponse(htmlResponse):
    """封装aiohttp网页抓取结果,标准化"""

    ...


if __name__ == "__main__":
    from xt_requests import get

    url = "https://www.baidu.com"
    url = "https://www.bigee.cc/book/6909/"
    rep = get(url)
    title_name = "title" if url == "https://www.baidu.com" else "h1"
    print(1111111, rep.dom.url, rep.dom)
    print(2222222, rep.xpath(f"//{title_name}/text()"))
    print(3333333, rep.dom.xpath(f"//{title_name}/text()"))
    print(4444444, rep.element.base, rep.element.xpath(f"//{title_name}/text()"))
    print(4545454, rep.html.base_url, rep.html.xpath(f"//{title_name}/text()"))
    print(5555555, rep.query(f"{title_name}").text())
    print(6666666, rep, rep.raw)
    print(7777777, rep.status)
    print(8888888, rep.text[1000:1300])
    # print(r := htmlResponse(None, "参数ele:666", 1), r, r.text, r.dom, end="\n\n")
