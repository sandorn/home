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
#LastEditTime : 2020-05-11 15:24:14
requests 简化调用
'''
# from __future__ import absolute_import, unicode_literals

import json

import requests
from retrying import retry

from xjLib.head import myhead
from xjLib.Response import sResponse

RETRY_TIME = 10  # 最大重试次数
TIMEOUT = 0.5  # socket延时


def get_by_proxy(url, proxy):

    ip = proxy[0]
    port = proxy[1]
    proxies = {
        "http": "http://%s:%s" % (ip, port),
        "https": "http://%s:%s" % (ip, port)
    }

    try:
        response = parse_get(url, proxies=proxies, timeout=TIMEOUT)
        return response
    except Exception as err:
        print(url, f'_parse by [{proxies}] err:{err}', flush=True)
        raise err


class RequestsSession(object):
    '''参考 https://www.jb51.net/article/153917.htm'''

    def __init__(self):
        self.session = requests.session()
        self.header = myhead
        self.timeout = TIMEOUT
        self.cookies = requests.cookies.RequestsCookieJar()

    @retry(
        wait_random_min=20,
        wait_random_max=1000,
        stop_max_attempt_number=RETRY_TIME)
    def post(self, url, data=None,  **kwargs):
        try:
            response = self.session.post(
                url,
                data=data,
                allow_redirects=True,
                headers=self.header,
                timeout=self.timeout,
                cookies=self.cookies,  # 传递cookie
                **kwargs)
            self.cookies.update(response.cookies)  # 保存cookie
            self.session.cookies.update(response.cookies)  # 保存cookie
            # print(self.cookies, self.session.cookies)

            response.raise_for_status()
            return sResponse(response, response.content, id(response))
        except Exception as err:
            print("HTTP请求异常，异常信息：%s" % err)
            raise err

    @retry(
        wait_random_min=20,
        wait_random_max=1000,
        stop_max_attempt_number=RETRY_TIME)
    def get(self, url, params=None, **kwargs):
        try:
            response = self.session.get(
                url,
                params=params,
                allow_redirects=True,
                headers=self.header,
                timeout=self.timeout,
                cookies=self.cookies,  # 传递cookie
                **kwargs)
            self.cookies.update(response.cookies)  # 保存cookie
            self.session.cookies.update(response.cookies)  # 保存cookie

            response.raise_for_status()
            return sResponse(response, response.content, id(response))
        except Exception as err:
            print("HTTP请求异常，异常信息：%s" % err)
            raise err


def parse_get(url, params=None, **kwargs):

    @retry(
        wait_random_min=20,
        wait_random_max=1000,
        stop_max_attempt_number=RETRY_TIME,
        retry_on_exception=lambda x: True,
        retry_on_result=lambda ret: not ret)
    def _run():
        response = requests.get(url, params=params, **kwargs)
        # $assert response.status_code in [200, 201, 302]
        return response

    kwargs.setdefault('headers', myhead)
    kwargs.setdefault('allow_redirects', True)  # @启动重定向

    try:
        response = _run()
        response.raise_for_status()  #$与上一标识未试验
        return sResponse(response, response.content, id(response))
    except Exception as err:
        print(url, '_parse err:', repr(err), flush=True)
        raise err


def parse_post(url, data=None, json=None, **kwargs):

    @retry(
        wait_random_min=20,
        wait_random_max=1000,
        stop_max_attempt_number=RETRY_TIME,
        retry_on_exception=lambda x: True,
        retry_on_result=lambda ret: not ret)
    def _run():
        response = requests.post(url, data=data, json=json, **kwargs)
        # $assert response.status_code in [200, 201, 302]
        return response

    kwargs.setdefault('headers', myhead)
    kwargs.setdefault('allow_redirects', True)

    try:
        response = _run()
        response.raise_for_status()
        return sResponse(response, response.content, id(response))
    except Exception as err:
        print(url, '_parse post err:', repr(err), flush=True)
        raise err


def set_cookies(cookies):
    '''
    #将CookieJar转为字典：
    cookies = requests.utils.dict_from_cookiejar(r.cookies)
    session.cookies = set_cookies(response.cookies)

    #将字典转为CookieJar：
    cookies = requests.utils.cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True)
    可以把headers这个请求头直接转成cookiejar类型放入cookies里面
    cookies = requests.utils.cookiejar_from_dict(headers, cookiejar=None, overwrite=True)

    #https://blog.csdn.net/falseen/article/details/46962011
    用cookies属性的update方法更新cookie
    cookie_dict = {"a":1}
    session = requests.Session()
    session.cookies.update(cookie_dict)
    session.get(url)

    '''
    # 将CookieJar转为字典：
    res_cookies_dic = requests.utils.dict_from_cookiejar(cookies)
    # 将新的cookies信息更新到手动cookies字典
    for i in res_cookies_dic.keys():
        cookies[i] = res_cookies_dic[i]
    return cookies


class HttpClient(object):

    def __init__(self):
        pass

    def __post(self, url, data=None, json=None, **kargs):
        return requests.post(url=url, data=data, json=json, **kargs)

    def __get(self, url, params=None, **kargs):
        return requests.get(url=url, params=params, **kargs)

    def request(self,
                requestMethod,
                requestUrl,
                paramsType="params",
                requestData=None,
                headers=myhead,
                cookies=None):
        if requestMethod.lower() == "post":
            if paramsType == "form":
                response = self.__post(
                    url=requestUrl,
                    data=json.dumps(eval(requestData)),
                    headers=headers,
                    cookies=cookies)
                return sResponse(response, response.content, id(response))
            elif paramsType == 'json':
                response = self.__post(
                    url=requestUrl,
                    json=json.dumps(eval(requestData)),
                    headers=headers,
                    cookies=cookies)
                return sResponse(response, response.content, id(response))
        elif requestMethod == "get":
            if paramsType == "url":
                request_url = "%s%s" % (requestUrl, requestData)
                response = self.__get(
                    url=request_url, headers=headers, cookies=cookies)
                return sResponse(response, response.content, id(response))
            elif paramsType == "params":
                response = self.__get(
                    url=requestUrl,
                    params=requestData,
                    headers=headers,
                    cookies=cookies)
                return sResponse(response, response.content, id(response))


class FakeRequests(object):
    headers = myhead

    @classmethod
    def request(cls, method, url, **kwargs):
        kwargs.setdefault("headers", cls.headers)
        response = requests.request(method, url, **kwargs)
        response.encoding = response.apparent_encoding
        return sResponse(response, response.content, id(response))

    @classmethod
    def get(cls, url, params=None, **kwargs):
        kwargs.setdefault('allow_redirects', True)
        response = cls.request('get', url, params=params, **kwargs)
        return sResponse(response, response.content, id(response))

    @classmethod
    def post(cls, url, data=None, json=None, **kwargs):
        response = cls.request('post', url, data=data, json=json, **kwargs)
        return sResponse(response, response.content, id(response))


if __name__ == '__main__':
    r = FakeRequests.get(url="https://httpbin.org/get")
    print(r.text)
