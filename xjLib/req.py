# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-16 12:57:23
@LastEditors: Even.Sand
@LastEditTime: 2020-03-15 17:35:49
requests 简化调用
'''
from __future__ import absolute_import, unicode_literals

import json

import requests
from cchardet import detect
from lxml import etree
from retrying import retry

myhead = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 指定客户端浏览器可以支持的web服务器返回内容压缩编码类型
    'Accept-Encoding': 'gzip, deflate, sdch',
    # 指定HTTP客户端浏览器用来展示返回信息所优先选择的语言。
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.6,en;q=0.4',
    # 浏览器可以接受的字符编码集
    'Accept-Charset': 'gb2312,utf-8;q=0.7,*;q=0.7',
    # 表示是否需要持久连接  'keep-alive','close'
    'Connection': 'close',
    # 显示此HTTP连接的Keep-Alive时间    'Keep-Alive': '300',
    # 请求的web服务器域名地址    'Host': 'www.baidu.com',
}


class sResponse:
    # 结构化返回结果
    def __init__(self, sessReq):
        self.raw = self.clientResponse = sessReq

    @property
    def content(self):
        return self.clientResponse.content

    @property
    def text(self):
        code_type = detect(self.content)
        return self.content.decode(code_type['encoding'], 'ignore')

    @property
    def url(self):
        return self.clientResponse.url

    @property
    def cookies(self):
        return self.clientResponse.cookies

    @property
    def headers(self):
        return self.clientResponse.headers

    def json(self):
        return json.loads(self.text)

    @property
    def status(self):
        return self.clientResponse.status

    @property
    def html(self):
        # @html.setter  #def html用于设置
        html = etree.HTML(self.text)
        return html

    def __repr__(self):
        return f"<sResponse status[{self.status}] url=[{self.url}]>"


def parse_get(url, params=None, **kwargs):
    @retry(wait_random_min=20, wait_random_max=1000, stop_max_attempt_number=10)
    def _parse_url(url, params=params, **kwargs):
        response = requests.get(url, params=params, **kwargs)
        return response

    kwargs.setdefault('headers', myhead)
    kwargs.setdefault('allow_redirects', True)  # @启动重定向

    try:
        # 以下except捕获当requests请求异常
        response = _parse_url(url, params=params, **kwargs)
        # soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')
        # [s.extract() for s in soup(["script", "style"])]
    except Exception as err:
        print(url, 'parse_get Error:' + repr(err), flush=True)
        # raise err

    return sResponse(response)


def parse_post(url, data=None, json=None, **kwargs):
    @retry(wait_random_min=50, wait_random_max=1000, stop_max_attempt_number=100)
    def _parse_url(url, data=data, json=json, **kwargs):
        response = requests.post(url, data=data, json=json, **kwargs)
        if kwargs['allow_redirects']:
            assert response.status_code == 200
        else:
            assert (response.status_code == 200) or (response.status_code == 302)
        # # response.content.decode('utf-8')   # # response.text
        return response

    kwargs.setdefault('headers', myhead)
    kwargs.setdefault('allow_redirects', True)

    try:
        # 以下except捕获当requests请求异常
        response = _parse_url(url, data=data, json=json, **kwargs)
        # soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')
        # [s.extract() for s in soup(["script", "style"])]
    except Exception as e:
        print('xjLib.req.parse_get Exception:', e, url, flush=True)
        response = None
    return sResponse(response)


def set_cookies(cookies):
    # 将CookieJar转为字典：
    res_cookies_dic = requests.utils.dict_from_cookiejar(cookies)
    # 将新的cookies信息更新到手动cookies字典
    for i in res_cookies_dic.keys():
        cookies[i] = res_cookies_dic[i]
    return cookies


def session_url(url, params=None, **kwargs):
    '''
    session可以跨越很多页面,session的生命周期也是针对一个客户端
    在网站设置的会话周期内(一般是20-30分钟)，session里边的内容将一直存在
    即便关闭了这个客户端浏览器 session也不一定会马上释放掉的。
    可以理解是客户端同一个IE窗口发出的多个请求，之间可以传递参数，比如用户登录
    '''

    @retry(wait_random_min=50, wait_random_max=1000, stop_max_attempt_number=100)
    def _parse_url(url, params=params, **kwargs):
        # 开启一个session会话
        session = requests.session()
        session.keep_alive = False
        # 设置请求头信息
        session.headers = myhead
        # 将cookiesJar赋值给会话
        # session.cookies = self.read_cookies()
        # 向目标网站发起请求
        response = session.get(url, params=params, **kwargs)
        if kwargs['allow_redirects']:
            assert response.status_code == 200
            session.cookies = set_cookies(response.cookies)
        else:
            assert (response.status_code == 200) or (response.status_code == 302)
        # # response.content.decode('utf-8')   # # response.text
        return response

    try:
        # 以下except捕获当requests请求异常
        response = _parse_url(url, params=params, **kwargs)
    except Exception as e:
        print('xjLib.req.parse_get Exception:', e, url, flush=True)
        response = None
    return response
