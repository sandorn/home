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
#LastEditTime : 2020-06-14 00:50:07
#Github       : https://github.com/sandorn/home
#==============================================================
'''

import json
from cchardet import detect
from lxml import etree


class ReqResult:
    __slots__ = ('raw', 'clientResponse', 'content', 'index')

    # 结构化返回结果
    def __init__(self, response, content=None, index=None):
        self.raw = self.clientResponse = response
        self.content = content or self.clientResponse.content
        self.index = index or id(response)

    # #下标obj[key] 获取属性
    def __getitem__(self, attr):
        return getattr(self, attr)

    # @property装饰器把方法变成属性,只读
    @property
    def text(self):
        code_type = detect(self.content)
        if code_type != 'utf-8':
            self.content = self.content.decode(code_type['encoding'],
                                               'ignore').encode('utf-8')
        return self.content.decode('utf-8', 'ignore')

    @property
    def url(self):
        return self.raw.url

    @property
    def cookies(self):
        return self.raw.cookies

    @property
    def headers(self):
        return self.raw.headers

    @property
    def json(self):
        try:
            json_temp = json.loads(self.text)
        except ValueError:
            json_temp = None
        return json_temp

    @property
    def status(self):
        if hasattr(self.raw, 'status'):
            return self.raw.status
        else:
            return self.raw.status_code

    @property
    def html(self):
        def clean(html, filter):
            data = etree.HTML(html)
            trashs = data.xpath(filter)
            for item in trashs:
                item.getparent().remove(item)
            return data

        html = clean(self.text, '//script')
        return html

    @property
    def element(self):
        code_type = detect(self.content)
        if code_type != 'utf-8':
            self.content = self.content.decode(code_type['encoding'],
                                               'ignore').encode('utf-8')
        element = etree.HTML(self.content.decode('utf-8', 'ignore'))
        return element

    def __repr__(self):
        return "< ReqResult status:[{}]， ID:[{}]， url:[{}] >".format(
            self.status, self.index, self.url)


'''
jxdm = response.xpath('//h3/a')
for each in jxdm:
    href = each.xpath("@href")[0] #获取属性方法1
    href = each.attrib['href']  #获取属性方法2
    href = each.get('href')  #获取属性方法3

    text = each.xpath("string(.)").strip()  #获取文本方法1，全
    text = each.text.strip()  #获取文本方法2，可能不全

'''
