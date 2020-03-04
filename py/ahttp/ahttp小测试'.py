# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-04 08:21:06
@LastEditors: Even.Sand
@LastEditTime: 2020-03-04 13:53:15
'''

from cchardet import detect
from xjLib.ahttp import ahttpGet


url = 'https://www.biqukan.com/2_2714/'
'''
res = session.get(url).run()
print(res.text)
res = ahttp.get(url).run()
print(res.html)
response = HTML(html=res.text)
print(response)
'''
a = ahttpGet(url)
html = a.html
print(a.encoding)
_bookname = html.xpath('//h2', first=True).text
print(_bookname)
