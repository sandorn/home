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
#LastEditTime : 2020-06-24 19:09:24
#Github       : https://github.com/sandorn/home
#==============================================================
'''
from threading import Thread
from xt_Requests import SessionClient, get, parse_get
from xt_Head import myhead
from xt_String import class_add_dict
from xt_Alispeech.conf import SpeechArgs
s = SessionClient()
s.update_headers({
    # 'Content-Type': 'application/json',
    # 'charset': 'UTF-8',
    **myhead
})

url = "https://nls-gateway.cn-shanghai.aliyuncs.com/rest/v1/tts/async"  # 400
url_200 = "https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/tts"
url_get = "https://httpbin.org/get"  # 返回head及ip等信息
url_post = "https://httpbin.org/post"  # 返回head及ip等信息
args_dict = class_add_dict(SpeechArgs())
args_dict['text'] = '规范化的请求字符串,URL编码后的签名'  # 添加

# #s.session.auth = ('user', 'pass')
# res = s.get(
res = parse_get(url, params=args_dict, json=args_dict, timeout=1.01)

print(res)  # print(r['text'])  r.text
print(res.elapsed.total_seconds())

# t = Thread(None,
#            parse_get,
#            args=(url, ),
#            kwargs={
#                'params': args_dict,
#                'json': args_dict
#            })
# t.start()
# t.join()
