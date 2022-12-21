# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-20 23:21:47
LastEditTime : 2022-12-20 23:21:48
FilePath     : /py学习/test/网页编码.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import cchardet
import requests

url = 'http://zgdysj.com/html/news/20190222/30452.shtml'

html = requests.get(url)
result = cchardet.detect(html.content)
res = html.content.decode(result['encoding'])
html.encoding = result['encoding']
# print(html.content)
print(html.content)
# print(res)

str1 = "我爱祖国"
str2 = "I love my country"
print("utf8编码：", str1.encode(encoding="utf8", errors="strict"))  #等价于print("utf8编码：",str1.encode("utf8"))
print("utf8编码：", str2.encode(encoding="utf8", errors="strict"))
print("gb2312编码：", str1.encode(encoding="gb2312", errors="strict"))  #以gb2312编码格式对str1进行编码，获得bytes类型对象的str
print("gb2312编码：", str2.encode(encoding="gb2312", errors="strict"))
print("cp936编码：", str1.encode(encoding="cp936", errors="strict"))
print("cp936编码：", str2.encode(encoding="cp936", errors="strict"))
print("gbk编码：", str1.encode(encoding="gbk", errors="strict"))
print("gbk编码：", str2.encode(encoding="gbk", errors="strict"))
