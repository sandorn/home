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
#LastEditTime : 2020-07-01 10:20:56
#Github       : https://github.com/sandorn/home
#==============================================================
'''
from xt_Ahttp import ahttpGet, ahttpGetAll
from threading import Thread
from xt_Requests import SessionClient, get, parse_get
from xt_Head import MYHEAD
from xt_String import class_add_dict
from xt_Asyncio import AioCrawl
import asyncio
s = SessionClient()
s.update_headers({**MYHEAD})

url = "https://nls-gateway.cn-shanghai.aliyuncs.com/rest/v1/tts/async"  # 400
url_200 = "https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/tts"
url_get = "https://httpbin.org/get"  # 返回head及ip等信息
url_post = "https://httpbin.org/post"  # 返回head及ip等信息
args_dict = {}

# #s.session.auth = ('user', 'pass')
target = url
# res = parse_get(target, params=args_dict, json=args_dict, timeout=1.01)
# print('parse_get:', res)  # print(r['text'])  r.text
# res = get(target, params=args_dict, json=args_dict, timeout=1.01)
# print('get:', res)
# res = s.get(target, params=args_dict, json=args_dict, timeout=1.01)
# print('session:', res)

# res = ahttpGet(target, params=args_dict, json=args_dict, timeout=1.01)
# print('ahttpGet:', res)

# res = ahttpGetAll([
#     target,
# ], params=args_dict, json=args_dict, timeout=1.01)

# print('ahttpGetAll:', res)

# aio = AioCrawl()
# res = asyncio.run(aio.fetch(target))
# print(res)
