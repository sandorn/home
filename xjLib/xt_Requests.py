# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-06-07 10:35:33
FilePath     : /CODE/xjLib/xt_Requests.py
Github       : https://github.com/sandorn/home
==============================================================
requests 简化调用
"""

from functools import partial

import requests
from tenacity import retry, stop_after_attempt, wait_random
from xt_Head import MYHEAD, RETRY_TIME, TIMEOUT, Head
from xt_Log import log_decorator
from xt_Response import htmlResponse
from xt_Tools import try_except_wraps

Method_List = ['get', 'post', 'head', 'options', 'put', 'delete', 'trace', 'connect', 'patch']

TRETRY = retry(
    reraise=True,  # 保留最后一次错误
    stop=stop_after_attempt(RETRY_TIME),
    wait=wait_random(min=0, max=1),
)


def _setKw(kwargs):
    kwargs.setdefault('headers', Head().randua)
    kwargs.setdefault('timeout', TIMEOUT)  # @超时
    return kwargs


@log_decorator
def _request_parse(method, url, *args, **kwargs):
    """自实现重试"""
    attempts = RETRY_TIME
    response = None
    func_exc = ret_err = False
    kwargs = _setKw(kwargs)
    callback = kwargs.pop('callback', None)

    while attempts:
        try:
            func_exc = False
            response = requests.request(method, url, *args, **kwargs)
            assert response.status_code in [200, 201, 302]
        except Exception as err:
            attempts -= 1
            func_exc = True
            ret_err = err
            print(f'_request_parse_{method}:<{url}>; times:{RETRY_TIME - attempts}; Err:{ret_err!r}')
        else:
            # #返回正确结果
            result = htmlResponse(response)
            return callback(result) if callable(callback) else result

    # #错误返回None
    if func_exc:
        return ret_err


@log_decorator
def _request_wraps(method, url, *args, **kwargs):
    """利用自编重试装饰器,实现重试"""
    kwargs = _setKw(kwargs)
    callback = kwargs.pop('callback', None)

    @try_except_wraps()
    def __fetch_run():
        response = requests.request(method, url, *args, **kwargs)
        return response

    response = __fetch_run()
    result = htmlResponse(response)
    return callback(result) if callable(callback) else result


@log_decorator
def _request_tretry(method, url, *args, **kwargs):
    """利用TRETRY三方库实现重试"""
    kwargs = _setKw(kwargs)
    callback = kwargs.pop('callback', None)

    @TRETRY
    def __fetch_run():
        response = requests.request(method, url, *args, **kwargs)
        # response.raise_for_status()
        return response

    try:
        response = __fetch_run()
        result = htmlResponse(response)
        return callback(result) if callable(callback) else result
    except Exception as err:
        print(f'_request_tretry.{method}:<{url}>; Err:{err!r}')
        return err


get_parse = partial(_request_parse, 'get')
post_parse = partial(_request_parse, 'post')
get_wraps = partial(_request_wraps, 'get')
post_wraps = partial(_request_wraps, 'post')
get = partial(_request_tretry, 'get')
post = partial(_request_tretry, 'post')


class SessionClient:
    """封装session,保存cookies,利用TRETRY三方库实现重试"""

    __slots__ = ['sson', 'method', 'url', 'args', 'kwargs', 'response', 'callback']

    def __init__(self):
        self.sson = requests.session()
        self.response = None

    @log_decorator
    @TRETRY
    def _request(self):
        self.response = self.sson.request(self.method, self.url, *self.args, **self.kwargs)
        return self.response

    def start_fetch_run(self):
        try:
            self._request()
        except requests.exceptions.RequestException as err:
            print(f'SessionClient request:<{self.url}>; Err:{err!r}')
            return None
        else:
            self.update_cookies(self.response.cookies)
            result = htmlResponse(self.response)
            return self.callback(result) if callable(self.callback) else result

    def __create_params(self, *args, **kwargs):
        self.url = args[0]
        self.args = args[1:]

        self.update_headers(kwargs.pop('headers', MYHEAD))
        self.update_cookies(kwargs.pop('cookies', {}))
        self.callback = kwargs.pop('callback', None)
        kwargs.setdefault('timeout', TIMEOUT)
        self.kwargs = kwargs
        return self.start_fetch_run()

    def __getitem__(self, method):
        method = method.lower()
        if method in Method_List:
            self.method = method  # 保存请求方法
            return lambda *args, **kwargs: self.__create_params(*args, **kwargs)

    def __getattr__(self, method):
        method = method.lower()
        if method in Method_List:
            self.method = method  # 保存请求方法
            return self.__create_params  # @ 设置参数

    def update_cookies(self, cookie_dict):
        self.sson.cookies.update(cookie_dict)

    def update_headers(self, header_dict):
        self.sson.headers.update(header_dict)


if __name__ == '__main__':
    sion = SessionClient()
    print(sion.head('http://httpbin.org/headers').headers)
    # print(sion.put('http://httpbin.org/put', data=b'data'))
    # print(sion.delete('http://httpbin.org/delete'))
    # print(sion.options('http://httpbin.org/get').headers)
    # 'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
    # print(sion.options('https://cn.bing.com'))
    # print(sion.patch('http://httpbin.org/patch', data=b'data'))
    # urls = [
    # 'http://www.baidu.com',
    # 'http://www.163.com',
    # 'http://dangdang.com',
    # "https://httpbin.org",
    # 'https://www.google.com',
    # ]
    # for url in urls:
    # ...
    # print(get_wraps('http://www.baidu.com').cookies)
    # res = get('http://www.163.com')
    # print(res.xpath('//title/text()'))
    # print(res.xpath(['//title/text()', '//title/text()']))
    # print(res.xpath())
    # print(res.xpath(' '))
    # print(res.xpath(''))
    # print(res.dom.xpath('//title/text()'))
    # print(res.html.xpath('//title/text()'))
    # print(res.element.xpath('//title/text()'))
    # print(res.pyquery('title').text())
    """
    ###############################################################
    # allow_redirects=False #取消重定向
    res = get_wraps('https://www.biqukan8.cc/38_38163/')
    pr = res.pyquery('.listmain dl dd:gt(11)').children()
    bookname = res.pyquery('h2').text()
    temp_urls = [f'https://www.biqukan8.cc{i.attr("href")}' for i in pr.items()]
    titles = [i.text() for i in pr.items()]
    res2 = get_wraps(temp_urls[0])
    title = res2.pyquery('h1').text()
    content = res2.pyquery('#content').text()
    # print(bookname, title, '\n', content)
    # pr = res.pyquery('.listmain dl dt+dd~dd')
    div = res.pyquery('dt').eq(1).nextAll()
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
