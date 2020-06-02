# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@LastEditors: Even.Sand
@Date: 2019-05-12 08:11:10
@LastEditTime: 2019-05-12 08:11:19
'''
from fake_useragent import UserAgent
ua = UserAgent()


#禁用服务器缓存：
#ua = UserAgent(use_cache_server=False)
#不缓存数据：
#ua = UserAgent(cache=False)
#忽略ssl验证：
#ua = UserAgent(verify_ssl=False)
#解决办法：
#下载： https://fake-useragent.herokuapp.com/browsers/0.1.11 并另存为：fake_useragent.json
def get_header():
    location = os.getcwd() + '/fake_useragent.json'
    ua = fake_useragent.UserAgent(path=location)
    return ua.random


self.myhead = {'User-Agent': ua.random}
