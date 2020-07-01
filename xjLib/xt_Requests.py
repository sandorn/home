# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2019-05-16 12:57:23
#FilePath     : /xjLib/xt_Requests.py
#LastEditTime : 2020-06-30 19:18:46
#Github       : https://github.com/sandorn/home
#==============================================================
requests 简化调用
'''

import requests
from xt_Head import MYHEAD
from xt_Response import ReqResult
from retrying import retry
from tenacity import retry as tretry
from tenacity import stop_after_attempt, wait_random
# from xt_Log import mylog
# print = mylog.warn

TIMEOUT = 20  # (20, 9, 9)
RETRY_TIME = 6  # 最大重试次数

TRETRY = tretry(stop=stop_after_attempt(RETRY_TIME),
                wait=wait_random(min=0, max=1))

RETRY = retry(wait_random_min=20,
              wait_random_max=1000,
              stop_max_attempt_number=RETRY_TIME,
              retry_on_exception=lambda x: True,
              retry_on_result=lambda ret: not ret)


def _setdict(kwargs):
    kwargs.setdefault('headers', MYHEAD)
    kwargs.setdefault('allow_redirects', True)  # @重定向
    kwargs.setdefault('timeout', TIMEOUT)  # @超时
    return kwargs


def parse_get(url, *args, **kwargs):
    attempts = 0
    response = None
    elapsed = 0
    kwargs = _setdict(kwargs)

    while attempts < RETRY_TIME:
        try:
            response = requests.get(url, *args, **kwargs)
            response.raise_for_status()
            # $ assert response.status_code in [200, 201, 302]
        except Exception as err:
            attempts += 1
            print(
                f'parse_get:<{url}>; {attempts} times; Err:{repr(err)}; total_seconds:{response.elapsed.total_seconds()}'
            )
        else:
            # #返回正确结果
            new_res = ReqResult(response, response.content, id(response))
            return new_res

    # #返回非正确结果
    new_res = ReqResult(response, response.content, id(response))
    return new_res


def parse_post(url, *args, **kwargs):
    attempts = 0
    response = None
    elapsed = 0
    kwargs = _setdict(kwargs)

    while attempts < RETRY_TIME:
        try:
            response = requests.post(url, *args, **kwargs)
            response.raise_for_status()
            # $ assert response.status_code in [200, 201, 302]
        except Exception as err:
            attempts += 1
            print(
                f'parse_post:<{url}>; {attempts} times; Err:{repr(err)}; total_seconds:{response.elapsed.total_seconds() }'
            )
        else:
            # #返回正确结果
            new_res = ReqResult(response, response.content, id(response))
            return new_res

    # #返回非正确结果
    new_res = ReqResult(response, response.content, id(response))
    return new_res


def get(url, *args, **kwargs):
    response = None
    kwargs = _setdict(kwargs)

    @RETRY
    def _fetch_run():
        nonlocal response
        response = requests.get(url, *args, **kwargs)
        # response.raise_for_status()
        # assert response.status_code in [200, 201, 302]
        return response

    try:
        _fetch_run()
    except Exception as err:
        print(
            f'requests.get:<{url}>; Err:{repr(err)}; total_seconds:{response.elapsed.total_seconds()}'
        )
    finally:
        # #返回结果,不管是否正确
        new_res = ReqResult(response, response.content, id(response))
        return new_res


def post(url, *args, **kwargs):
    response = None
    kwargs = _setdict(kwargs)

    @RETRY
    def _fetch_run():
        nonlocal response
        response = requests.post(url, *args, **kwargs)
        return response

    try:
        _fetch_run()
    except Exception as err:
        print(
            f'requests.post:<{url}>; Err:{repr(err)}; total_seconds:{response.elapsed.total_seconds()}'
        )
    finally:
        # #返回结果,不管是否正确
        new_res = ReqResult(response, response.content, id(response))
        return new_res


class SessionClient:
    __slots__ = ('sn', 'headers', 'cookies', 'result', 'url', 'method', 'args',
                 'kwargs', 'callback')

    def __init__(self):
        self.sn = requests.session()
        self.cookies = requests.cookies.RequestsCookieJar()

    @RETRY
    def _request(self):
        res = self.sn.request(self.method, self.url, *self.args, **self.kwargs)
        self.result = res
        return self.result

    def _fetch_run(self):
        try:
            self._request()
        except Exception as err:
            print(
                f'SessionClient request:<{self.url}>; Err:{repr(err)}; total_seconds:{self.result.elapsed.total_seconds()}'
            )
        finally:
            # #返回结果,不管是否正确
            self.update_cookies(self.result.cookies)
            new_res = ReqResult(self.result, self.result.content,
                                id(self.result))
            self.result = None
            return new_res

    def __create_params(self, *args, **kwargs):
        kwargs = _setdict(kwargs)
        self.url = args[0]
        self.args = args[1:]
        if "callback" in kwargs:
            self.callback = kwargs['callback']
            kwargs.pop("callback")
        else:
            self.callback = None

        if "headers" in kwargs:
            self.headers = kwargs['headers']
            kwargs.pop("headers")
        self.kwargs = kwargs

        return self._fetch_run()

    def __getattr__(self, method):
        if method in ['get', 'post']:
            self.method = method
            # @不带括号,传递*args, **kwargs参数
            return self.__create_params

    # #下标obj[key]
    def __getitem__(self, method):
        if method in ['get', 'post']:
            self.method = method
            # @不带括号,传递*args, **kwargs参数
            return self.__create_params

    def update_cookies(self, cookie_dict):
        self.sn.cookies.update(cookie_dict)
        self.cookies.update(cookie_dict)

    def update_headers(self, header_dict):
        self.sn.headers.update(header_dict)


'''
    set_cookies(cookies)

    # 将CookieJar转为字典：
    cookies = requests.utils.dict_from_cookiejar(r.cookies)

    # 将字典转为CookieJar：
    cookies = requests.utils.cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True)
    可以把headers这个请求头直接转成cookiejar类型放入cookies里面
    cookies = requests.utils.cookiejar_from_dict(headers, cookiejar=None, overwrite=True)

    # https://blog.csdn.net/falseen/article/details/46962011
    用cookies属性的update方法更新cookie

    cookie_dict = {"a":1}
    session = requests.Session()
    session.cookies.update(cookie_dict)

    # 将新的cookies信息更新到手动cookies字典
    for i in res_cookies_dic.keys():
        cookies[i] = res_cookies_dic[i]
    return cookies
'''
