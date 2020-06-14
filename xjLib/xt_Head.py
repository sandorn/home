# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-06 11:05:52
#LastEditTime : 2020-06-14 19:29:10
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''

from fake_useragent import UserAgent

myhead = {
    'User-Agent': UserAgent().random,
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Content-Encoding': 'gzip,deflate,compress',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.6,en;q=0.4',
    'Accept-Charset': 'gb2312,utf-8;q=0.7,*;q=0.7',
    'Connection': 'close',
    # 'Content-Type':'application/json'  #!影响post json
    # 'Connection': 'keep-alive',
    # 显示此HTTP连接的Keep-Alive时间    'Keep-Alive': '300',
    # 请求的web服务器域名地址    'Host': 'www.baidu.com',
}

if __name__ == '__main__':
    headers = myhead
    print(headers)
