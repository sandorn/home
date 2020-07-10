# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-12 16:18:13
#FilePath     : /xjLib/test/requests--test.py
#LastEditTime : 2020-07-10 14:18:04
#Github       : https://github.com/sandorn/home
#==============================================================
'''
from xt_Ahttp import ahttpGet, ahttpGetAll
from xt_Requests import SessionClient, get, parse_get
from xt_Asyncio import AioCrawl
import asyncio

s = SessionClient()
urls = [
    "https://nls-gateway.cn-shanghai.aliyuncs.com/rest/v1/tts/async",  # 0 status:[400]
    "https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/tts",
    "https://httpbin.org/get",  # 2 返回head及ip等信息
    "https://httpbin.org/post",  # 返回head及ip等信息
    "http://g.cn",  # 4 # status:[400]
    "http://www.google.com",  # 5 status:[400]
    "https://www.biqukan.com/38_38836/",
    "https://www.biqukan.com/38_38836/497577681.html",
]
args_dict = {}
# #s.session.auth = ('user', 'pass')
target = urls[5]
tout = 3.01
# res = parse_get(target, params=args_dict, json=args_dict, timeout=tout)
# print('parse_get:', res)  # , res.text)

# res = get(target, params=args_dict, json=args_dict, timeout=tout)
# print('get:', res)  # , res['text'])

res = s.get(target, params=args_dict, json=args_dict, timeout=tout)
print('session:', res)  # , res.text)
res = s.post(urls[3], params=args_dict, json=args_dict, timeout=tout)
print('session:', res, res.text)

# res = ahttpGet(target, params=args_dict, json=args_dict, timeout=tout)
# print('ahttpGet:', res)  # , res.text)
# print('ahttpGet:', res.text)

# res = ahttpGetAll([target, urls[5], urls[0]], timeout=tout)
# print('ahttpGetAll:', res)  # , res[0].text)

# aio = AioCrawl()
# res = asyncio.run(
#     aio.fetch(target, params=args_dict, json=args_dict, timeout=tout))
# print('AioCrawl:', res)  # , res[0].text)

# #xpath
# res = get(urls[6])
# element = res.element

# 全部章节节点 = element.xpath(
#     '//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a')

# for each in 全部章节节点:
#     print(each.xpath("@href")[0])  # 获取属性方法1
#     print(each.attrib['href'])  # 获取属性方法2
#     print(each.get('href'))  # 获取属性方法3

#     print(each.xpath("string(.)").strip())  # 获取文本方法1，全
#     print(each.text.strip())  # 获取文本方法2，可能不全
