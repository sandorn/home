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
#LastEditTime : 2020-07-06 19:22:22
#Github       : https://github.com/sandorn/home
#==============================================================
requests 简化调用
'''

from functools import partial
import requests
from tenacity import retry as Tretry
from tenacity import stop_after_attempt, wait_random

from xt_Head import MYHEAD
from xt_Response import ReqResult

TIMEOUT = 20  # (30, 9, 9)
RETRY_TIME = 6  # 最大重试次数

TRETRY = Tretry(
    reraise=True,  # #保留最后一次错误
    stop=stop_after_attempt(RETRY_TIME),
    wait=wait_random(min=0, max=1),
)

# @不能用于协程,未能保留最后错误
# from retrying import retry as Retry
# RETRY = Retry(
#     wait_random_min=0,
#     wait_random_max=1000,
#     stop_max_attempt_number=RETRY_TIME,
#     wrap_exception=True,
#     retry_on_exception=lambda x: True,
#     retry_on_result=lambda ret: not ret,
# )


def _setKw(kwargs):
    kwargs.setdefault('headers', MYHEAD)
    # kwargs.setdefault('cookies', {})
    kwargs.setdefault('timeout', TIMEOUT)  # @超时
    kwargs.setdefault('allow_redirects', True)  # @重定向
    # kwargs.setdefault('cookies', requests.cookies.RequestsCookieJar())
    return kwargs


def request_parse(method, url, *args, **kwargs):
    attempts = 0
    response = None
    Timeout_exc = False
    Err_msg = None
    kwargs = _setKw(kwargs)

    while attempts < RETRY_TIME:
        try:
            Timeout_exc = False
            Err_msg = None
            response = requests.request(method, url, *args, **kwargs)
            response.raise_for_status()
            # $ assert response.status_code in [200, 201, 302]
        except requests.Timeout as err:
            attempts += 1
            Timeout_exc = True
            Err_msg = err
            print(f'parse_{method}:<{url}>; times:{attempts}; Err:{err!r}')
        except Exception as err:
            attempts += 1
            print(f'parse_{method}:<{url}>; times:{attempts}; Err:{err!r}')
        else:
            # #返回正确结果
            new_res = ReqResult(response)
            return new_res

    # #Timeout 错误，返回空
    if Timeout_exc:
        print(Err_msg)
        return None
    # #返回非正确结果
    new_res = ReqResult(response)
    return new_res


def request_retry(method, url, *args, **kwargs):
    response = None
    Timeout_exc = False
    kwargs = _setKw(kwargs)

    @TRETRY
    def _fetch_run():
        nonlocal response, Timeout_exc
        response = requests.request(method, url, *args, **kwargs)
        response.raise_for_status()

    try:
        _fetch_run()
    except requests.Timeout as err:
        # #Timeout 错误，返回空
        print(f'requests.{method}:<{url}>; Err:{err!r}')
        return None
    except Exception as err:
        print(f'requests.{method}:<{url}>; Err:{err!r}')

    # #返回结果,不管是否正确
    new_res = ReqResult(response)
    return new_res


parse_get = partial(request_parse, "get")
parse_post = partial(request_parse, "post")
get = partial(request_retry, "get")
post = partial(request_retry, "post")


class SessionClient:
    __slots__ = ('sn', 'headers', 'cookies', 'response', 'url', 'method',
                 'args', 'kwargs', 'callback')

    def __init__(self):
        self.sn = requests.session()
        self.cookies = {}

    @TRETRY
    def _request(self):
        self.response = self.sn.request(self.method, self.url, *self.args,
                                        **self.kwargs)
        self.response.raise_for_status()
        return self.response

    def _fetch_run(self):
        try:
            self.response = None
            self._request()
        except requests.Timeout as err:
            print(f'SessionClient request:<{self.url}>; Err:{err!r}')
            return None
        except Exception as err:
            print(f'SessionClient request:<{self.url}>; Err:{err!r}')

        # #返回结果,不管是否正确
        if hasattr(self.response, 'cookies'):
            self.update_cookies(self.response.cookies)

        new_res = ReqResult(self.response)
        if self.callback:
            new_res = self.callback(new_res)  # 有回调则调用
        return new_res

    def __create_params(self, *args, **kwargs):
        self.url = args[0]
        self.args = args[1:]

        kwargs = _setKw(kwargs)

        if "callback" in kwargs:
            self.callback = kwargs['callback']
            kwargs.pop("callback")
        else:
            self.callback = None

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
        self.headers.update(header_dict)


'''
    self.cookies = requests.cookies.RequestsCookieJar()
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
