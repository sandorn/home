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
#LastEditTime : 2020-06-15 03:14:10
#Github       : https://github.com/sandorn/home
#==============================================================
'''

from xt_Requests import SessionClient
from xt_Head import myhead

s = SessionClient()
s.update_headers({
    'Content-Type': 'application/json',
    'charset': 'UTF-8',
    # **myhead
})

url = "https://nls-gateway.cn-shanghai.aliyuncs.com/rest/v1/tts/async"  # 400
url_get = "https://httpbin.org/get"  # 返回head及ip等信息
url_post = "https://httpbin.org/post"  # 返回head及ip等信息

# #s.session.auth = ('user', 'pass')
res = s.get(url_get)  #, auth=('sandorn', '123456'))
print(res.text)  # print(r['text'])  r.text
# print(res.text)
