# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-06 11:23:14
#FilePath     : /xjLib/xt_Response.py
#LastEditTime : 2020-06-10 15:43:55
#Github       : https://github.com/sandorn/home
#==============================================================
'''


import json

# from html import unescape

from cchardet import detect
from lxml import etree


class ReqResult:
    # 结构化返回结果
    def __init__(self, response, content=None, index=None):
        self.raw = self.clientResponse = response
        self.content = content or self.clientResponse.content
        self.index = index or id(response)

    # @property装饰器把方法变成属性
    # #下标obj[key] 获取属性
    def __getitem__(self, attr):
        return getattr(self, attr)

    @property
    def text(self):
        code_type = detect(self.content)
        if code_type != 'utf-8':
            self.content = self.content.decode(code_type['encoding'], 'ignore').encode('utf-8')
        return self.content.decode('utf-8', 'ignore')

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
        def clean(html, filter):
            data = etree.HTML(html)
            trashs = data.xpath(filter)
            for item in trashs:
                item.getparent().remove(item)
            return data

        # html = clean(unescape(self.text), '//script') #解码html:unescape
        html = clean(self.text, '//script')
        return html

    @property
    def element(self):
        code_type = detect(self.content)
        if code_type != 'utf-8':
            self.content = self.content.decode(code_type['encoding'], 'ignore').encode('utf-8')
        element = etree.HTML(self.content.decode('utf-8', 'ignore'))
        return element

    def __repr__(self):
        return f"<sResponse status[{self.status }] url=[{self.url}]>"


'''
jxdm = response.xpath('//h3/a')
for each in jxdm:
    href = each.xpath("@href")[0] #获取属性方法1
    href = each.attrib['href']  #获取属性方法2
    href = each.get('href')  #获取属性方法3

    text = each.xpath("string(.)").strip()  #获取文本方法1，全
    text = each.text.strip()  #获取文本方法2，可能不全

    <Element>
    ['__bool__', '__class__', '__contains__', '__copy__', '__deepcopy__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '_init', 'addnext', 'addprevious', 'append', 'attrib', 'base', 'clear', 'cssselect', 'extend', 'find', 'findall', 'findtext', 'get', 'getchildren', 'getiterator', 'getnext', 'getparent', 'getprevious', 'getroottree', 'index', 'insert', 'items', 'iter', 'iterancestors', 'iterchildren', 'iterdescendants', 'iterfind', 'itersiblings', 'itertext', 'keys', 'makeelement', 'nsmap', 'prefix', 'remove', 'replace', 'set', 'sourceline', 'tag', 'tail', 'text', 'values', 'xpath']
'''
