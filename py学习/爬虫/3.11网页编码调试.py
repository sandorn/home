# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2021-04-14 16:26:25
LastEditTime : 2022-12-21 11:22:37
FilePath     : /py学习/爬虫/3.11网页编码调试.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import requests
from chardet import detect
from xt_Ahttp import ahttpGet
from xt_Head import MYHEAD
from xt_Response import ReqResult

kwargs = {}
kwargs.setdefault('headers', MYHEAD)
kwargs.setdefault('cookies', {})
kwargs.setdefault('timeout', 20)

url = 'https://www.biqukan8.cc/38_38163/'
res = ahttpGet(url, **kwargs)
# res = ReqResult(res)

# print(1111111111111, cont)
print(2222222222222, res.content)
# print(3333333333333, res.apparent_encoding)
response = res.element
bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
temp_urls = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')
titles = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/text()')
print(bookname, temp_urls, titles)
