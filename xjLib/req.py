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
@LastEditTime: 2020-04-03 10:44:07
requests 简化调用
'''
from __future__ import absolute_import, unicode_literals

import json
from functools import partial
from html import unescape

import requests
from cchardet import detect
from fake_useragent import UserAgent
from lxml import etree
from retrying import retry

myhead = {
    'User-Agent': UserAgent().random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Content-Encoding': 'gzip,deflate,compress',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.6,en;q=0.4',
    'Accept-Charset': 'gb2312,utf-8;q=0.7,*;q=0.7',
    'Connection': 'close',
    # 'Connection': 'keep-alive',
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
        def clean(html, filter):
            data = etree.HTML(html)
            trashs = data.xpath(filter)
            for item in trashs:
                item.getparent().remove(item)
            return data
        # #去除节点clean # #解码html:unescape
        html = clean(unescape(self.text), '//script')
        #html = etree.HTML(self.text)
        return html

    def __repr__(self):
        return f"<sResponse status[{self.status}] url=[{self.url}]>"


def parse_get(url, params=None, **kwargs):
    @retry(
        wait_random_min=20,
        wait_random_max=1000,
        stop_max_attempt_number=10,
        retry_on_exception=lambda x: True,
        retry_on_result=lambda ret: not ret
    )
    def _run(url, params=params, **kwargs):
        response = requests.get(url, timeout=10, params=params, **kwargs)
        assert (response.status_code == 200) or (response.status_code == 302)
        return response

    kwargs.setdefault('headers', myhead)
    kwargs.setdefault('allow_redirects', True)  # @启动重定向

    try:
        response = _run(url, params=params, **kwargs)
    except Exception as err:
        print(url, '_parse err:', repr(err), flush=True)
        raise err

    return sResponse(response)


@retry(wait_random_min=20, wait_random_max=1000, stop_max_attempt_number=10)
def parse_get_0(url, params=None, **kwargs):
    kwargs.setdefault('headers', myhead)
    kwargs.setdefault('allow_redirects', True)  # @启动重定向
    response = requests.get(url, params=params, **kwargs)
    assert (response.status_code == 200) or (response.status_code == 302)
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


class HttpClient(object):
    def __init__(self):
        pass

    def __post(self, url, data=None, json=None, **kargs):
        return requests.post(url=url, data=data, json=json, **kargs)

    def __get(self, url, params=None, **kargs):
        return requests.get(url=url, params=params, **kargs)

    def request(self, requestMethod, requestUrl, paramsType="params", requestData=None, headers=None, cookies=None):
        if requestMethod.lower() == "post":
            if paramsType == "form":
                response = self.__post(url=requestUrl, data=json.dumps(eval(requestData)), headers=headers, cookies=cookies)
                return response
            elif paramsType == 'json':
                response = self.__post(url=requestUrl, json=json.dumps(eval(requestData)), headers=headers, cookies=cookies)
                return response
        elif requestMethod == "get":
            if paramsType == "url":
                request_url = "%s%s" % (requestUrl, requestData)
                response = self.__get(url=request_url, headers=headers, cookies=cookies)
                return response
            elif paramsType == "params":
                response = self.__get(url=requestUrl, params=requestData, headers=headers, cookies=cookies)
                return response


class FakeRequests(object):
    """
    经常到处找请求头用户代理，这下一次解决完
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0"
    }

    @classmethod
    def request(cls, method, url, **kwargs):
        kwargs.setdefault("headers", cls.headers)
        response = requests.request(method, url, **kwargs)
        response.encoding = response.apparent_encoding
        return response

    @classmethod
    def get(cls, url, params=None, **kwargs):
        kwargs.setdefault('allow_redirects', True)
        return cls.request('get', url, params=params, **kwargs)

    @classmethod
    def post(cls, url, data=None, json=None, **kwargs):
        return cls.request('post', url, data=data, json=json, **kwargs)


if __name__ == '__main__':
    r = FakeRequests.get(url="https://httpbin.org/get")
    print(r.text)

    hc = HttpClient()
    response = hc.request("get", "https://www.163.com")
    print(response)

    # response=hc.request("post","http://39.106.41.11:8080/register/","form",'{"username":"xufengchai6","password":"xufengchai121","email":"xufengchai@qq.com"}')
