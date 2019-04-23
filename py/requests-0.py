# ！/usr/bin/env python
# -*-coding:utf-8-*-
'''
@Software:   VSCode
@File    :   requests-0.py
@Time    :   2019/04/20 12:45:29
@Author  :   Even Sand
@Version :   1.0
@Contact :   sandorn@163.com
@License :   (C)Copyright 2019-2019, NewSea
@Desc    :   None
'''

import json

import requests

r = requests.get(url='http://www.baidu.com')  # 最基本的GET请求
print(r.status_code)  # 获取返回状态
print(r)
r = requests.get(
    url='http://dict.baidu.com/s', params={'wd': 'python'})  #带参数的GET请求
print(r.status_code)  # 获取返回状态
print(r.url)
print(r.text)  #打印解码后的返回数据

data = {'some': 'data'}
headers = {
    'content-type':
        'application/json',
    'User-Agent':
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}

r = requests.post(
    'https://api.github.com/some/endpoint', data=data, headers=headers)
print(r.text)
