# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-06 11:23:14
#LastEditTime : 2020-05-06 15:09:01
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''

import json
from html import unescape

from cchardet import detect
from lxml import etree


class sResponse:
    # 结构化返回结果
    def __init__(self, sessReq, content=None, index=None):
        self.raw = self.clientResponse = sessReq
        self.content = content or self.clientResponse.content
        self.index = index or 1

    @property
    def text(self):
        code_type = detect(self.content)
        return self.content.decode(code_type['encoding'], 'ignore')

    @property
    def url(self):
        return self.clientResponse.url

    @property
    def cookies(self):
        return self.clientResponse.cookies

    @property
    def headers(self):
        return self.clientResponse.headers

    def json(self):
        return json.loads(self.text)

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

        # #去除节点clean # #解码html:unescape
        html = clean(unescape(self.text), '//script')
        # html = etree.HTML(self.text)
        return html

    def __repr__(self):
        return f"<sResponse status[{self.status }] url=[{self.url}]>"
