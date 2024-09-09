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
from lxml import html
from pyquery import PyQuery


class htmlResponse:
    """封装网页结果,标准化"""

    __slots__ = ("raw", "_content", "index", "encoding", "code_type")

    def __init__(self, response, content=None, index=None):
        self.index: int = index or id(self)

        if response:
            self.raw = response
            self._content: bytes = (
                content if isinstance(content, bytes) else response.content
            )
            self.encoding = (
                response.encoding if hasattr(response, "encoding") else "utf-8"
            )
            self.code_type = (
                detect(self._content)["encoding"]
                if isinstance(self._content, bytes)
                else "utf-8"
            )
        else:
            self.raw = None
            self._content = (
                content.encode("utf-8", "replace")
                if isinstance(content, str)
                else (content or b"")
            )
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
        return len(self.text) if self.text else 0

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
        return (
            self.raw.elapsed.total_seconds()
            if self.raw and hasattr(self.raw, "elapsed")
            else 0
        )

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
            return (
                self.raw.status if hasattr(self.raw, "status") else self.raw.status_code
            )

    @property
    def html(self, filter="//script"):
        element = self.element
        [item.getparent().remove(item) for item in element.xpath(filter)]
        return element

    @property
    def element(self):
        # self.content 有decode问题,self._content 有乱码问题
        # from lxml import etree
        # return etree.HTML(self.content, parser=None)
        return html.fromstring(self.text, parser=None)

    @property
    def dom(self):
        """
        返回requests_html对象,支持html对象操作:find, xpath, render(先安装chromium浏览器)
        """
        from requests_html import HTML

        html = HTML(html=self._content)
        setattr(html, "url", self.url)
        return html

    @property
    def query(self):
        return PyQuery(self.html)  # , parser='xml')

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
    print(res := htmlResponse(rep))
    print(res.url, res.dom)
    print(res.xpath(f"//{title_name}/text()"))
    print(res.dom.xpath(f"//{title_name}/text()"))
    print(res.query(f"{title_name}").text())
