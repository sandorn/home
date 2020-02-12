# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-09 08:53:18
@LastEditors: Even.Sand
@LastEditTime: 2019-05-21 16:25:35
'''
from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<div><div><div><p class="story">Once upon a time there were three little sisters; and their names were
<div>
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,</div><div>
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a></div> and<div>
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;</div></div></div></div>
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
# 获取所有a标签节点内容
c_showurl_bf = BeautifulSoup(html_doc)
c_showurl = c_showurl_bf.find_all('a')

# 查找已经获取a标签节点中所有连接
for link in c_showurl:
    print(link.name, link['href'], link.get_text())
