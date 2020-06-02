# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-06-27 13:43:34
@LastEditors: Even.Sand
@LastEditTime: 2020-04-03 19:05:14
'''
import base64

import urllib.parse
chinese_str = bytes('中mbaoir=3-p.0927820985文', 'utf8')
# 先进行gb2312编码
# chinese_str = chinese_str.encode('gb2312')
# print(chinese_str)
# 输出 b'\xd6\xd0mbaoir=3-p.0927820985\xce\xc4'
# 再进行urlencode编码
# chinese_str_url = urllib.parse.quote(chinese_str)
# print(chinese_str_url)
# 输出 %D6%D0%CE%C4
# print(bytes('你 好 ', 'utf-8'))  # b'\xe4\xbd\xa0 \xe5\xa5\xbd '

base64_data = base64.b64encode(chinese_str)
print(base64_data.decode())

ori_data = str(base64.b64decode(base64_data), 'utf8')
print(ori_data)

html = u"%5B%7B%22pageSize%22%3A%2220%22%2C%22pageNo%22%3A1%2C%22spaceType%22%3A%22%22%2C%22spaceId%22%3A%22%22%2C%22typeId%22%3A%221%22%2C%22condition%22%3A%22%22%2C%22textfield1%22%3A%22%22%2C%22textfield2%22%3A%22%22%2C%22myBul%22%3A%22%22%7D%5D"

print(urllib.parse.unquote(html))


'''
#解码
from urllib import parse
encoded_url = '%7B%22ShoppingToken%22%3A%22NewAirChina%257CCA4173%252C1%252C%252C12-CA989%252C1%252C%252C12%257CY%252CV%252C-Y%252CV%252C%257C0%257C3430%252C1564%252CCAGJ-CA%257CNOR%257C%22%2C%22Eligibility%22%3A%22NOR%22%7D'
print(parse.unquote(encoded_url)

复制代码
#编码
from urllib import parse
url = '{"ShoppingToken":"NewAirChina%7CCA4173%2C1%2C%2C12-CA989%2C1%2C%2C12%7CY%2CV%2C-Y%2CV%2C%7C0%7C3430%2C1564%2CCAGJ-CA%7CNOR%7C","Eligibility":"NOR"}'
print(parse.quote(url))

Python3编码解码url - 一杯闪光喵 - 博客园
https://www.cnblogs.com/lyxdw/p/9935137.html
'''
