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
#LastEditTime : 2020-06-16 13:17:35
#Github       : https://github.com/sandorn/home
#==============================================================
'''

from xt_Requests import SessionClient
from xt_Head import myhead
from xt_String import class_to_dict
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
args_dict = class_to_dict(SpeechArgs())
args_dict['text'] = '规范化的请求字符串,URL编码后的签名'  # 添加

# #s.session.auth = ('user', 'pass')
res = s.get(
    url_200,
    params=args_dict,
    json=args_dict,
    #  headers={'Content-Type': 'application/json'}
)
print(res)  # print(r['text'])  r.text
# print(res.text)
with open('1.wav', mode='wb') as f:
    f.write(res.content)
