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
@LastEditors  : Even.Sand
@LastEditTime : 2020-02-13 19:07:55
requests 简化调用
'''
from __future__ import absolute_import, unicode_literals
from retrying import retry
import requests
import re

myhead = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 指定客户端浏览器可以支持的web服务器返回内容压缩编码类型
    'Accept-Encoding': 'gzip, deflate, br',
    # 指定HTTP客户端浏览器用来展示返回信息所优先选择的语言。
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.6,en;q=0.4',
    # 浏览器可以接受的字符编码集
    'Accept-Charset': 'gb2312,utf-8;q=0.7,*;q=0.7',
    # 表示是否需要持久连接  'keep-alive','close'
    'Connection': 'close',
    # 显示此HTTP连接的Keep-Alive时间    'Keep-Alive': '300',
    # 请求的web服务器域名地址    'Host': 'www.baidu.com',
}


def parse_get(url, params=None, **kwargs):

    @retry(wait_random_min=200, wait_random_max=3000, stop_max_attempt_number=100,)
    def _parse_url(url, params=params, **kwargs):
        response = requests.get(url, params=params, **kwargs)
        if kwargs['allow_redirects']:
            assert response.status_code == 200
        else:
            assert response.status_code == 200 or 302
        # # response.content.decode('utf-8')   # # response.text
        return response

    kwargs.setdefault('headers', myhead)
    kwargs.setdefault('allow_redirects', True)

    try:
        # 以下except捕获当requests请求异常
        response = _parse_url(url, params=params, **kwargs)
        # soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')
        # [s.extract() for s in soup(["script", "style"])]
    except requests.exceptions.ConnectionError as e:
        print('ConnectionError:', e, url, flush=True)
        response = None
    except requests.exceptions.ChunkedEncodingError as e:
        print('ChunkedEncodingError:', e, url, flush=True)
        response = None
    except Exception as e:
        print('Unfortunitely Unknow Error:', e, url, flush=True)
        response = None
    return response


def parse_post(url, data=None, json=None, **kwargs):

    @retry(wait_random_min=200, wait_random_max=3000, stop_max_attempt_number=100,)
    def _parse_url(url, data=data, json=json, **kwargs):
        response = requests.post(url, data=data, json=json, **kwargs)
        if kwargs['allow_redirects']:
            assert response.status_code == 200
        else:
            assert response.status_code == 200 or 302
        # # response.content.decode('utf-8')   # # response.text
        return response

    kwargs.setdefault('headers', myhead)
    kwargs.setdefault('allow_redirects', True)

    try:
        # 以下except捕获当requests请求异常
        response = _parse_url(url, data=data, json=json, **kwargs)
        # soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')
        # [s.extract() for s in soup(["script", "style"])]
    except requests.exceptions.ConnectionError as e:
        print('ConnectionError:', e, url, flush=True)
        response = None
    except requests.exceptions.ChunkedEncodingError as e:
        print('ChunkedEncodingError:', e, url, flush=True)
        response = None
    except Exception as e:
        print('Unfortunitely Unknow Error:', e, url, flush=True)
        response = None
    return response


def set_cookies(cookies):
    # 将CookieJar转为字典：
    res_cookies_dic = requests.utils.dict_from_cookiejar(cookies)
    # 将新的cookies信息更新到手动cookies字典
    for i in res_cookies_dic.keys():
        cookies[i] = res_cookies_dic[i]
    return cookies


def session_url(url,
                params=None,
                headers=myhead,
                proxies=None,
                allow_redirects=True,
                timeout=6,
                wait_random_min=200,
                wait_random_max=3000,
                stop_max_attempt_number=100):
    '''
    session可以跨越很多页面,session的生命周期也是针对一个客户端
    在网站设置的会话周期内(一般是20-30分钟)，session里边的内容将一直存在
    即便关闭了这个客户端浏览器 session也不一定会马上释放掉的。
    可以理解是客户端同一个IE窗口发出的多个请求，之间可以传递参数，比如用户登录
    '''

    @retry(
        wait_random_min=wait_random_min,
        wait_random_max=wait_random_max,
        stop_max_attempt_number=stop_max_attempt_number)
    def _parse_url(url):
        # 开启一个session会话
        session = requests.session()
        session.keep_alive = False
        # 设置请求头信息
        session.headers = headers
        # 将cookiesJar赋值给会话
        # session.cookies = self.read_cookies()
        # 向目标网站发起请求
        response = session.get(
            url,
            params=params,
            headers=headers,
            proxies=proxies,
            timeout=timeout,
            allow_redirects=allow_redirects)
        if allow_redirects:
            assert response.status_code == 200
            session.cookies = set_cookies(response.cookies)
        else:
            assert response.status_code == 200 or 302
        return response

    try:
        # 以下except捕获当requests请求异常
        response = _parse_url(url)
    except requests.exceptions.ConnectionError as e:
        print('ConnectionError:', e, url, flush=True)
        response = None
    except requests.exceptions.ChunkedEncodingError as e:
        print('ChunkedEncodingError:', e, url, flush=True)
        response = None
    except Exception as e:
        print('Unfortunitely Unknow Error:', e, url, flush=True)
        response = None
    return response


def list2file(_filename, _list_texts, br='\t'):
    # 函数说明:将爬取的文章内容写入文件,只能1层
    print('[' + _filename + ']开始保存......', end='', flush=True)
    _list_texts.sort()
    with open(_filename, 'w', encoding='utf-8') as f:
        f.write('   key   \tpage\tindex\ttitle\turl\t\n')
        for key in _list_texts:  # 区分关键字
            for index in key:  # 区分记录index
                [f.write(str(v) + br) for v in index]
                f.write('\n')

    print('[' + _filename + ']保存完成。', flush=True)
    # # 下面换行问题
    # #[f.write(str(v) + '\t') for key in lists for index in key for v in index]


def savefile(_filename, _list_texts, br='\t'):
    # 函数说明:将爬取的文章内容写入文件,迭代多层
    # #多层次的list 或 tuple写入文件
    print('[' + _filename + ']开始保存......', end='', flush=True)
    with open(_filename, 'w', encoding='utf-8') as f:

        def each(data):
            for index, value in enumerate(data):
                if isinstance(value, list) or isinstance(value, tuple):
                    each(value)
                else:
                    f.write(str(value) + br)
                    if index == len(data) - 1:
                        f.write('\n')

        each(_list_texts)

    print('[' + _filename + ']保存完成。', flush=True)


def flatten(nested):
    try:
        # 不要迭代类似字符串的对象：
        # if isinstance(variate,list) or isinstance(variate,tuple):
        try:
            nested + ''
        except TypeError:
            pass
        else:
            raise TypeError

        for sublist in nested:
            for element in flatten(sublist):
                yield element
    except TypeError:
        yield nested


def get_stime():
    import datetime

    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return time_now


def get_litetime():
    import datetime

    time_now = datetime.datetime.now().strftime('%H:%M:%S.%f')
    return time_now


if __name__ == "__main__":
    res = ([1, 2, 3, 4, 5], [11, 46,
                             87], [125232], [5667, 2356, 26, 6215, 9741, 23525])
    res2 = [
        'and', 'B', ['not', 'A'], [1, 2, 1, [2, 1], [1, 1, [2, 2, 1]]],
        ['not', 'A', 'A'], ['or', 'A', 'B', 'A'], 'B'
    ]
    savefile('d:/1.txt', res2)
    # for i in flatten(12141.98792):
    #   print(i)
