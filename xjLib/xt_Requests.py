# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2019-05-16 12:57:23
FilePath     : /xjLib/xt_Requests.py
LastEditTime : 2021-04-14 18:09:32
#Github       : https://github.com/sandorn/home
#==============================================================
requests 简化调用
'''

from functools import partial

import requests
from tenacity import retry as Tretry
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_random
from xt_Head import MYHEAD
from xt_Response import ReqResult
from xt_Tools import try_except_wraps

TIMEOUT = 20  # (30, 9, 9)
RETRY_TIME = 6  # 最大重试次数

TRETRY = Tretry(
    reraise=True,  # #保留最后一次错误
    stop=stop_after_attempt(RETRY_TIME),
    wait=wait_random(min=0, max=1),
)


def _setKw(kwargs):
    kwargs.setdefault('headers', MYHEAD)
    kwargs.setdefault('cookies', {})
    kwargs.setdefault('timeout', TIMEOUT)  # @超时
    return kwargs


def _request_parse(method, url, *args, **kwargs):
    '''自实现重试'''
    attempts = RETRY_TIME
    response = None
    func_exc = False
    kwargs = _setKw(kwargs)

    while attempts:
        try:
            func_exc = False
            response = requests.request(method, url, *args, **kwargs)
            response.raise_for_status()
            # assert response.status_code in [200, 201, 302]
        except requests.Timeout as err:
            attempts -= 1
            func_exc = True
            print(f'parse_{method}:<{url}>; times:{RETRY_TIME-attempts}; Timeout:{err!r}')
        except Exception as err:
            attempts -= 1
            func_exc = True
            print(f'parse_{method}:<{url}>; times:{RETRY_TIME-attempts}; Err:{err!r}')
        else:
            # #返回正确结果
            return ReqResult(response)

    # #错误返回None
    if func_exc: return None


def _request_try_wraps(method, url, *args, **kwargs):
    '''利用自编重试装饰器，实现重试'''
    kwargs = _setKw(kwargs)

    @try_except_wraps
    def _fetch_run():
        response = requests.request(method, url, *args, **kwargs)
        response.raise_for_status()
        return response

    response = _fetch_run()
    # #错误返回None
    if response is None: return None
    # #返回正确结果
    return ReqResult(response)


def _request_tretry(method, url, *args, **kwargs):
    '''利用TRETRY三方库实现重试'''
    response = None
    kwargs = _setKw(kwargs)

    @TRETRY
    def _fetch_run():
        nonlocal response
        response = requests.request(method, url, *args, **kwargs)
        response.raise_for_status()

    try:
        _fetch_run()
    except Exception as err:
        print(f'requests.{method}:<{url}>; Err:{err!r}')
        return None
    else:
        # #返回正确结果
        return ReqResult(response)


get_parse = partial(_request_parse, "get")
post_parse = partial(_request_parse, "post")
get_wraps = partial(_request_try_wraps, "get")
post_wraps = partial(_request_try_wraps, "post")
get = partial(_request_tretry, "get")
post = partial(_request_tretry, "post")


class SessionClient:
    '''封装session，保存cookies，利用TRETRY三方库实现重试'''
    __slots__ = ('sson', 'headers', 'cookies', 'response', 'url', 'method', 'args', 'kwargs', 'callback')

    def __init__(self):
        self.sson = requests.session()

    @TRETRY
    def _request(self):
        self.response = self.sson.request(self.method, self.url, *self.args, **self.kwargs)
        self.response.raise_for_status()
        return self.response

    def _fetch_run(self):
        try:
            self.response = None
            self._request()
        except Exception as err:
            print(f'SessionClient request:<{self.url}>; Err:{err!r}')
            return None
        else:
            # #返回正确结果
            self.update_cookies(self.response.cookies)

            new_res = ReqResult(self.response)
            if self.callback:  # 有回调则调用
                new_res = self.callback(new_res)
            return new_res

    def __create_params(self, *args, **kwargs):
        self.url = args[0]
        self.args = args[1:]

        kwargs = _setKw(kwargs)
        self.cookies = kwargs.pop("cookies")
        self.callback = kwargs.pop("callback", None)
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
        self.sson.cookies.update(cookie_dict)
        self.cookies.update(cookie_dict)

    def update_headers(self, header_dict):
        self.sson.headers.update(header_dict)
        self.headers.update(header_dict)


if __name__ == '__main__':
    res = get("https://www.biqukan8.cc/38_38163/")  # 'https://www.baidu.com'
    print(res)
    print(res.dom.xpath('//title/text()'))
    print(res.html.xpath('//title/text()'))
    print(res.element.xpath('//title/text()'))
'''
    # @不能用于协程,且不保留最后错误
    # from retrying import retry as Retry
    # RETRY = Retry(
    #     wait_random_min=0,
    #     wait_random_max=1000,
    #     stop_max_attempt_number=RETRY_TIME,
    #     wrap_exception=True,
    #     retry_on_exception=lambda x: True,
    #     retry_on_result=lambda ret: not ret,
    # )
    # #s.session.auth = ('user', 'pass')

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


    res = get("https://www.biqukan.com/38_38836/")
    element = res.element

    全部章节节点 = element.xpath(
        '//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a')

    for each in 全部章节节点:
        print(each.xpath("@href")[0])  # 获取属性方法1
        print(each.attrib['href'])  # 获取属性方法2
        print(each.get('href'))  # 获取属性方法3

        print(each.xpath("string(.)").strip())  # 获取文本方法1，全
        print(each.text.strip())  # 获取文本方法2，可能不全
'''
