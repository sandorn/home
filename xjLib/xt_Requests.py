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
#LastEditTime : 2020-06-03 11:47:50
requests 简化调用
'''
# from __future__ import absolute_import, unicode_literals

import requests

from retrying import retry

from xt_Head import myhead
from xt_Response import ReqResult

RETRY_TIME = 10  # 最大重试次数
TIMEOUT = 0.5  # socket延时
Retry = retry(wait_random_min=20, wait_random_max=1000, stop_max_attempt_number=RETRY_TIME, retry_on_exception=lambda x: True, retry_on_result=lambda ret: not ret)


def parse_get(url, params=None, **kwargs):
    attempts = 0
    response = None
    while attempts < RETRY_TIME:
        try:
            kwargs.setdefault('headers', myhead)
            kwargs.setdefault('allow_redirects', True)  # @启动重定向

            response = requests.get(url, params=params, **kwargs)
            response.raise_for_status()
            # $ assert response.status_code in [200, 201, 302]
            return ReqResult(response, response.content, id(response))
        except Exception as err:
            print(f'requests.get:<{attempts}>times;url:<{url}>;err:<{repr(err)}>。', flush=True)
            attempts += 1
    return response


def parse_post(url, data=None, json=None, **kwargs):
    attempts = 0
    response = None

    while attempts < RETRY_TIME:
        try:
            kwargs.setdefault('headers', myhead)
            kwargs.setdefault('allow_redirects', True)  # @启动重定向

            response = requests.post(url, data=data, json=json, **kwargs)
            response.raise_for_status()
            # $ assert response.status_code in [200, 201, 302]
            return ReqResult(response, response.content, id(response))
        except Exception as err:
            print(f'requests.post:<{attempts}>times;url:<{url}>;err:<{repr(err)}>。', flush=True)
            attempts += 1

    return response


def get_retry(url, params=None, **kwargs):
    @Retry
    def _run():
        return requests.get(url, params=params, **kwargs)

    kwargs.setdefault('headers', myhead)
    kwargs.setdefault('allow_redirects', True)  # @启动重定向

    # $ assert  response.raise_for_status()
    # $ if response.status_code not in [200, 201, 302]:
    # $ assert response.status_code in [200, 201, 302]

    try:
        response = _run()
        return ReqResult(response, response.content, id(response))
    except Exception as err:
        print(f'requests.get:{url} retryerr:{repr(err)}', flush=True)


def post_retry(url, data=None, json=None, **kwargs):
    @Retry
    def _run():
        return requests.post(url, data=data, json=json, **kwargs)

    kwargs.setdefault('headers', myhead)
    kwargs.setdefault('allow_redirects', True)

    try:
        response = _run()
        return ReqResult(response, response.content, id(response))
    except Exception as err:
        print(f'requests.post:{url} retryerr:{repr(err)}', flush=True)


class SessionClient(object):
    def __init__(self):
        self.session = requests.session()
        self.cookies = requests.cookies.RequestsCookieJar()

    def _get(self, url, params=None, **kwargs):  # #原版
        return self.session.get(url, params=params, cookies=self.cookies, **kwargs)

    def _post(self, url, data=None, json=None, **kwargs):  # #原版
        return self.session.post(url, data=data, json=json, cookies=self.cookies, **kwargs)

    def get(self, url, params=None, **kwargs):
        attempts = 0
        response = None
        while attempts < RETRY_TIME:
            try:
                response = self._get(url, params=params, **kwargs)
                response.raise_for_status()
                self.update_cookies(response.cookies)
                return ReqResult(response, response.content, id(response))
            except Exception as err:
                print(f'requests.get:<{attempts}>times;url:<{url}>;err:<{repr(err)}>。', flush=True)
                attempts += 1
        return response

    def post(self, url, data=None, json=None, **kwargs):
        attempts = 0
        response = None
        while attempts < RETRY_TIME:
            try:
                response = self._post(url, data=data, json=json, **kwargs)
                response.raise_for_status()
                self.update_cookies(response.cookies)
                return ReqResult(response, response.content, id(response))
            except Exception as err:
                print(f'requests.post:<{attempts}>times;url:<{url}>;err:<{repr(err)}>。', flush=True)
                attempts += 1

        return response

    def get_retry(self, url, params=None, **kwargs):
        @Retry
        def _run():
            return self._get(url, params=params, **kwargs)

        try:
            response = _run()
            self.update_cookies(response.cookies)
            return ReqResult(response, response.content, id(response))
        except Exception as err:
            print(f'requests.get:{url} retryerr:{repr(err)}', flush=True)

    def post_retry(self, url, data=None, json=None, **kwargs):
        @Retry
        def _run():
            return self._post(url, data=data, json=json, **kwargs)

        try:
            response = _run()
            self.update_cookies(response.cookies)
            return ReqResult(response, response.content, id(response))
        except Exception as err:
            print(f'requests.post:{url} retryerr:{repr(err)}', flush=True)

    def update_cookies(self, cookie_dict):
        self.session.cookies.update(cookie_dict)
        self.cookies.update(cookie_dict)

    def update_headers(self, header_dict):
        self.session.headers.update(header_dict)


if __name__ == '__main__':
    s = SessionClient()
    s.update_headers({'Content-Type': 'application/json', 'charset': 'UTF-8', **myhead})

    r = parse_post(url="https://httpbin.org/post")
    print(r.text)


'''
{
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
}
'''
