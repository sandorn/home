# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
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
'''

import json

from chardet import detect
from lxml import etree
from multipledispatch import dispatch
from pyquery import PyQuery
from requests_html import HTML
from xt_Class import item_Mixin


class htmlResponse(item_Mixin):
    '''封装网页抓取结果,使之标准化'''
    __slots__ = ('raw', 'clientResponse', '_content', 'index', 'encoding', 'code_type')

    def __init__(self, response, content=None, index=None):
        if response is not None:
            self.raw = self.clientResponse = response
            self._content: bytes = content or response.content
            self.index: int = index or id(self)
            self.encoding = response.encoding if hasattr(response, 'encoding') else 'utf-8'
            if isinstance(self._content, bytes): self.code_type = detect(self._content)['encoding'] or 'utf-8'
            # response.apparent_encoding

    @property
    def content(self):
        return self._content.decode(self.code_type, 'ignore')

    @property
    def text(self):
        try:
            _text = self.clientResponse.text.encode(self.encoding).decode(self.code_type, 'ignore')
        except AttributeError:
            _text = self.content
        return _text

    @property
    def elapsed(self):
        if hasattr(self.clientResponse, 'elapsed'):
            return self.clientResponse.elapsed
        else:
            return None

    @property
    def seconds(self):
        if hasattr(self.clientResponse, 'elapsed'):
            return self.clientResponse.elapsed.total_seconds()
        else:
            return 0

    @property
    def url(self):
        return self.clientResponse.url

    @property
    def cookies(self):
        return self.clientResponse.cookies

    @property
    def headers(self):
        return self.clientResponse.headers

    @property
    def json(self):
        try:
            json_temp = json.loads(self.text)
        except ValueError:
            json_temp = None
        return json_temp

    @property
    def status(self):
        if hasattr(self.clientResponse, 'status'):
            return self.clientResponse.status
        else:
            return self.clientResponse.status_code

    @property
    def html(self):

        def _clean(filter):
            element = self.element
            trashs = element.xpath(filter)
            for item in trashs:
                item.getparent().remove(item)
            return element

        return _clean('//script')

    @property
    def element(self):
        return etree.HTML(self.content, parser=None)

    @property
    def dom(self):
        """
        返回requests_html对象,支持html对象操作:find, xpath, render(先安装chromium浏览器)
        """
        html = HTML(html=self._content)
        html.url = self.clientResponse.url
        return html

    @property
    def pyquery(self):
        return PyQuery(self.html)  # , parser='xml')

    @dispatch()
    def xpath(self, selectors=None):
        return [self.element]

    @dispatch()
    def xpath(self, selectors: str):
        element = self.element
        return [*element.xpath(selectors)] if selectors.strip() != "" else [element]

    @dispatch()
    def xpath(self, selectors: (list, tuple)):
        element = self.element
        return [element.xpath(selector) for selector in selectors]

    @dispatch()
    def xpath(self, selectors: (dict, int, float, bool)):
        return [self.element]

    def __repr__(self):
        return f"<htmlResponse | ID:[{self.index}] | STATUS:[{self.status}] | URL:[{self.url}]>"

    def __str__(self):
        return self.__repr__()

    def __bool__(self):
        return self.status == 200

    def __eq__(self, other):
        return self.index == other.index


'''
jxdm = response.xpath('//h3/a')
for each in jxdm:
    href = each.xpath("@href")[0] #获取属性方法1
    href = each.attrib['href']  #获取属性方法2
    href = each.get('href')  #获取属性方法3

    text = each.xpath("string(.)").strip()  #获取文本方法1,全
    text = each.text.strip()  #获取文本方法2,可能不全

'''
