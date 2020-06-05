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
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-06-05 23:29:30
requests 简化调用
'''
# from __future__ import absolute_import, unicode_literals

import requests

from retrying import retry

from xt_Head import myhead
from xt_Response import ReqResult

from pysnooper import snoop
from xt_Log import log
log = log()
snooper = snoop(log.filename)
print = log.debug

RETRY_TIME = 6  # 最大重试次数
Retry = retry(wait_random_min=20, wait_random_max=1000, stop_max_attempt_number=RETRY_TIME, retry_on_exception=lambda x: True, retry_on_result=lambda ret: not ret)


def parse_get(url, params=None, **kwargs):
    attempts = 0
    response = None
    kwargs.setdefault('headers', myhead)
    kwargs.setdefault('allow_redirects', True)  # @重定向

    while attempts < RETRY_TIME:
        try:
            response = requests.get(url, params=params, **kwargs)
            response.raise_for_status()
            # $ assert response.status_code in [200, 201, 302]
        except Exception as err:
            attempts += 1
            print(f'requests.get {attempts} times ; {repr(err)}')
        else:
            return ReqResult(response, response.content, id(response))

    return response


def parse_post(url, data=None, json=None, **kwargs):
    attempts = 0
    response = None
    kwargs.setdefault('headers', myhead)
    kwargs.setdefault('allow_redirects', True)  # @重定向

    while attempts < RETRY_TIME:
        try:
            response = requests.post(url, data=data, json=json, **kwargs)
            response.raise_for_status()
            # $ assert response.status_code in [200, 201, 302]
        except Exception as err:
            attempts += 1
            print(f'requests.get {attempts} times ; {repr(err)}')
        else:
            return ReqResult(response, response.content, id(response))

    return response


def get(url, params=None, **kwargs):
    response = None
    kwargs.setdefault('headers', myhead)
    kwargs.setdefault('allow_redirects', True)  # @启动重定向

    @Retry
    def _run():
        nonlocal response
        response = requests.get(url, params=params, **kwargs)
        return response

    try:
        response = _run()
    except Exception as err:
        print(repr(err))
    else:
        # #返回正确结果
        return ReqResult(response, response.content, id(response))

    # #返回错误结果
    return response


def post(url, data=None, json=None, **kwargs):
    response = None
    kwargs.setdefault('headers', myhead)
    kwargs.setdefault('allow_redirects', True)

    @Retry
    def _run():
        nonlocal response
        response = requests.post(url, data=data, json=json, **kwargs)
        return response

    try:
        response = _run()
    except Exception as err:
        print(repr(err))
    else:
        # #返回正确结果
        return ReqResult(response, response.content, id(response))

    # #返回错误结果
    return response


class SessionClient(object):
    def __init__(self):
        self.session = requests.session()
        self.cookies = requests.cookies.RequestsCookieJar()

    def _get(self, url, params=None, **kwargs):  # #原版
        return self.session.get(url, params=params, cookies=self.cookies, **kwargs)

    def _post(self, url, data=None, json=None, **kwargs):  # #原版
        return self.session.post(url, data=data, json=json, cookies=self.cookies, **kwargs)

    def parse_get(self, url, params=None, **kwargs):
        attempts = 0
        response = None
        while attempts < RETRY_TIME:
            try:
                response = self._get(url, params=params, **kwargs)
                response.raise_for_status()
                # $ assert response.status_code in [200, 201, 302]
            except Exception as err:
                attempts += 1
                print(f'session.get {attempts} times ; {repr(err)}')
            else:
                self.update_cookies(response.cookies)
                return ReqResult(response, response.content, id(response))

        return response

    def parse_post(self, url, data=None, json=None, **kwargs):
        attempts = 0
        response = None
        while attempts < RETRY_TIME:
            try:
                response = self._post(url, data=data, json=json, **kwargs)
                response.raise_for_status()
                # $ assert response.status_code in [200, 201, 302]
            except Exception as err:
                attempts += 1
                print(f'session.post {attempts} times ; {repr(err)}')
            else:
                self.update_cookies(response.cookies)
                return ReqResult(response, response.content, id(response))

        return response

    def get(self, url, params=None, **kwargs):
        response = None
        kwargs.setdefault('headers', myhead)
        kwargs.setdefault('allow_redirects', True)  # @启动重定向

        @Retry
        def _run():
            nonlocal response
            response = self._get(url, params=params, **kwargs)
            return response

        try:
            response = _run()
        except Exception as err:
            print(repr(err))
        else:
            self.update_cookies(response.cookies)
            # #返回正确结果
            return ReqResult(response, response.content, id(response))

        # #返回错误结果
        return response

    def post(self, url, data=None, json=None, **kwargs):
        response = None
        kwargs.setdefault('headers', myhead)
        kwargs.setdefault('allow_redirects', True)  # @启动重定向

        @Retry
        def _run():
            nonlocal response
            response = self._post(url, data=data, json=json, **kwargs)
            return response

        try:
            response = _run()
        except Exception as err:
            print(repr(err))
        else:
            self.update_cookies(response.cookies)
            # #返回正确结果
            return ReqResult(response, response.content, id(response))

        # #返回错误结果
        return response

    def update_cookies(self, cookie_dict):
        self.session.cookies.update(cookie_dict)
        self.cookies.update(cookie_dict)

    def update_headers(self, header_dict):
        self.session.headers.update(header_dict)


if __name__ == '__main__':
    s = SessionClient()
    s.update_headers({'Content-Type': 'application/json', 'charset': 'UTF-8', **myhead})

    url = "https://nls-gateway.cn-shanghai.aliyuncs.com/rest/v1/tts/async"  # 400
    url_get = "https://httpbin.org/get"  # 返回head及ip等信息
    url_post = "https://httpbin.org/post"  # 返回head及ip等信息

    r = s.post(url_post)
    print(type(r))
    print(r.text)  # print(r['text'])  r.text


'''
    set_cookies(cookies)

    #将CookieJar转为字典：
    cookies = requests.utils.dict_from_cookiejar(r.cookies)

    #将字典转为CookieJar：
    cookies = requests.utils.cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True)
    可以把headers这个请求头直接转成cookiejar类型放入cookies里面
    cookies = requests.utils.cookiejar_from_dict(headers, cookiejar=None, overwrite=True)

    #https://blog.csdn.net/falseen/article/details/46962011
    用cookies属性的update方法更新cookie

    cookie_dict = {"a":1}
    session = requests.Session()
    session.cookies.update(cookie_dict)

    # 将新的cookies信息更新到手动cookies字典
    for i in res_cookies_dic.keys():
        cookies[i] = res_cookies_dic[i]
    return cookies
'''
