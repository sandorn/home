# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-06 11:23:14
FilePath     : /xjLib/xt_Response.py
LastEditTime : 2020-08-14 11:08:33
#Github       : https://github.com/sandorn/home
#==============================================================
'''

import json

from cchardet import detect
from lxml import etree
from requests_html import HTML
from xt_Class import item_Mixin


class ReqResult(item_Mixin):
    '''封装网页抓取结果,使之标准化'''
    __slots__ = ('raw', 'clientResponse', '_content', 'index')

    # 结构化返回结果
    def __init__(self, response, content=None, index=None):
        if response is not None:
            self.raw = self.clientResponse = response
            self._content: bytes = content or response.content
            self.index: int = index or id(self)

    @property
    def content(self):
        if self._content is None: return None

        code_type = detect(self._content)

        if code_type != 'utf-8':
            self._content = self._content.decode(code_type['encoding'], 'ignore')
            self._content = self._content.encode('utf-8')
        return self._content

    @property
    def text(self):
        return self.content.decode('utf-8', 'ignore')

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

        def _clean(html_text, filter):
            data = etree.HTML(html_text)
            trashs = data.xpath(filter)
            for item in trashs:
                item.getparent().remove(item)
            return data

        return _clean(self.text, '//script')

    @property
    def element(self):
        return etree.HTML(self.text)

    @property
    def dom(self):
        """
        返回一个requests_html对象,支持所有requests_html的html对象的操作。例如find, xpath, render（先安装chromium浏览器）
        """
        html = HTML(html=self.text)
        html.url = self.raw.url
        return html

    def __repr__(self):
        return f"<ReqResult status:[{self.status}]; ID:[{self.index}]， url:[{self.url}] >"


'''
jxdm = response.xpath('//h3/a')
for each in jxdm:
    href = each.xpath("@href")[0] #获取属性方法1
    href = each.attrib['href']  #获取属性方法2
    href = each.get('href')  #获取属性方法3

    text = each.xpath("string(.)").strip()  #获取文本方法1，全
    text = each.text.strip()  #获取文本方法2，可能不全

'''
