# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-06-07 10:35:33
FilePath     : /CODE/xjLib/xt_requests.py
Github       : https://github.com/sandorn/home
==============================================================
requests 简化调用
"""

from functools import partial

import requests
from xt_head import TIMEOUT, TRETRY, Head
from xt_log import log_decor
from xt_response import htmlResponse
from xt_retry import RetryLogWrapper  # retry_log_by_tenacity

request_methods = (
    "get",
    "post",
    "head",
    "options",
    "put",
    "delete",
    "trace",
    "connect",
    "patch",
)


@TRETRY  # from xt_catch import try_except_wraps
def _retry_request_0(method, url, **kwargs):
    """无用暂存，利用 TRETRY 库实现重试"""
    callback = kwargs.pop("callback", None)
    index = kwargs.pop("index", None)
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()  # 如果响应状态码不是200，则抛出HTTPError
        result = htmlResponse(response=response, index=index)
        return callback(result) if callable(callback) else result
    except Exception as err:
        print(err_str := f"Request_tretry:{method} | URL:{url} | Err:{err!r}")
        raise ValueError(err_str)
        return htmlResponse(None, err_str.encode(), id(url))


@RetryLogWrapper  # retry_log_by_tenacity()
def _retry_request(method, url, *args, **kwargs):
    """利用 RetryLogWrapper 实现重试"""
    callback = kwargs.pop("callback", None)
    index = kwargs.pop("index", None)
    response = requests.request(method, url, *args, **kwargs)
    response.raise_for_status()
    result = htmlResponse(response=response, index=index)

    return callback(result) if callable(callback) else result


def single_parse(method, url, *args, **kwargs):
    if method.lower() not in request_methods:
        return htmlResponse(
            None, f"Method:{method} not in {request_methods}".encode(), id(url)
        )
    kwargs.setdefault("headers", Head().randua)  # @headers
    kwargs.setdefault("timeout", TIMEOUT)  # @timeout
    kwargs.setdefault("cookies", {})  # @cookies

    return _retry_request(method.lower(), url, *args, **kwargs)


get = partial(single_parse, "get")
post = partial(single_parse, "post")


class SessionClient:
    """封装session,保存cookies,利用TRETRY三方库实现重试"""

    __slots__ = [
        "session",
        "method",
        "url",
        "args",
        "kwargs",
        "callback",
    ]

    def __init__(self):
        self.session = requests.session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def __getitem__(self, method):
        self.method = method.lower()  # 保存请求方法
        return self.create_task  # 调用方法
        # return lambda *args, **kwargs: self.create_task(*args, **kwargs)

    def __getattr__(self, method):
        return self.__getitem__(method)

    @log_decor
    def create_task(self, *args, **kwargs):
        self.url = args[0]
        if self.method not in request_methods:
            return htmlResponse(
                None,
                f"Method:{self.method} not in {request_methods}".encode(),
                id(self.url),
            )
        self.args = args[1:]

        self.update_headers(kwargs.pop("headers", Head().randua))
        self.update_cookies(kwargs.pop("cookies", {}))
        self.callback = kwargs.pop("callback", None)
        kwargs.setdefault("timeout", TIMEOUT)
        self.kwargs = kwargs
        return self._retry_request()

    @TRETRY
    def _retry_request(self):
        """利用 TRETRY 库实现重试"""
        try:
            response = self.session.request(
                self.method, self.url, *self.args, **self.kwargs
            )
            self.update_cookies(response.cookies)
            result = htmlResponse(response, None, id(self.url))
            return self.callback(result) if callable(self.callback) else result
        except requests.exceptions.RequestException as err:
            print(err_str := f"SessionClient:{self} | URL:{self.url} | Err:{err!r}")
            return htmlResponse(None, err_str.encode(), id(self.url))

    def update_cookies(self, cookie_dict):
        self.session.cookies.update(cookie_dict)

    def update_headers(self, header_dict):
        self.session.headers.update(header_dict)


if __name__ == "__main__":
    urls = [
        "https://www.163.com",
        "https://httpbin.org/get",
        "https://httpbin.org/post",
        "https://httpbin.org/headers",
        "https://www.google.com",
    ]
    elestr = "//title/text()"

    def main():
        # print(111111111111111111111, SessionClient().get(urls[3]))

        # print(222222222222222222222, partial(single_parse, "HEAD")(urls[3]))
        # print(3333333333333333333, get(urls[4]))
        print(4444444444444444444, res := get(urls[0], index=66))
        print("xpath-1".ljust(10), ":", res.xpath(elestr))
        print("xpath-2".ljust(10), ":", res.xpath([elestr, elestr]))
        print(
            "blank".ljust(10),
            ":",
            res.xpath(["", " ", " \t", " \n", " \r", " \r\n", " \n\r", " \r\n\t"]),
        )
        print("dom".ljust(10), ":", res.dom.xpath(elestr), res.dom.url)
        print("query".ljust(10), ":", res.query("title").text())
        print("element".ljust(10), ":", res.element.xpath(elestr), res.element.base)
        print("html".ljust(10), ":", res.html.xpath(elestr), res.html.base_url)

    main()

    @TRETRY
    def my_func():
        return get("https://www.google.com")

    # print(my_func())

    """
    ###############################################################
    # allow_redirects=False #取消重定向
    res = get_wraps('https://www.biqukan8.cc/38_38163/')
    pr = res.query('.listmain dl dd:gt(11)').children()
    bookname = res.query('h2').text()
    temp_urls = [f'https://www.biqukan8.cc{i.attr("href")}' for i in pr.items()]
    titles = [i.text() for i in pr.items()]
    res2 = get_wraps(temp_urls[0])
    title = res2.query('h1').text()
    content = res2.query('#content').text()
    # print(bookname, title, '\n', content)
    # pr = res.query('.listmain dl dt+dd~dd')
    div = res.query('dt').eq(1).nextAll()
    urls = [f'https://www.biqukan8.cc{i.attr("href")}' for i in pr.items()]
    titles = [i.text() for i in pr.items()]
    print(len(urls), len(titles))
    ###############################################################
    # #s.session.auth = ('user', 'pass')

    self.cookies = requests.cookies.RequestsCookieJar()
    set_cookies(cookies)

    # 将CookieJar转为字典：
    cookies = requests.utils.dict_from_cookiejar(r.cookies)

    # 将字典转为CookieJar：
    cookies = requests.utils.cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True)
    #其中cookie_dict是要转换字典转换完之后就可以把它赋给cookies 并传入到session中了：
    s=requests.Session()
    s.cookies=cookies

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

        print(each.xpath("string(.)").strip())  # 获取文本方法1,全
        print(each.text.strip())  # 获取文本方法2,可能不全
"""
