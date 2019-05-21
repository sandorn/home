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
@LastEditTime: 2019-05-20 16:09:39
'''
import time
from retrying import retry
import requests
from bs4 import BeautifulSoup

myhead = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    # 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip,deflate,sdch, br',
    'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'close',
    'Proxy-Connection': 'no-cache',
}
# Cache-Control':'no-cache','keep-alive'
# Connection':'close','keep-alive'
# 'Host': 'www.baidu.com'


def parse_url(url, params=None, headers=myhead, proxies=None, timeout=6, ecode='utf-8',
              wait_random_min=200, wait_random_max=3000, stop_max_attempt_number=100):

    @retry(wait_random_min=wait_random_min, wait_random_max=wait_random_max, stop_max_attempt_number=stop_max_attempt_number)
    def _parse_url(url):
        response = requests.get(url, params=params, headers=headers, proxies=proxies, timeout=timeout)
        assert response.status_code == 200
        # return response.text
        return response.content.decode(ecode)

    try:
        # 以下except捕获当requests请求异常
        response = _parse_url(url)
        soup = BeautifulSoup(response.text, 'lxml')
        [s.extract() for s in soup(["script", "style"])]
    except requests.exceptions.ConnectionError as e:
        print('ConnectionError:', e, url, flush=True)
        soup = None
    except requests.exceptions.ChunkedEncodingError as e:
        print('ChunkedEncodingError:', e, url, flush=True)
        soup = None
    except Exception as e:
        print('Unfortunitely Unknow Error:', e, url, flush=True)
        soup = None
    return soup


def set_cookies(cookies):
    # 将CookieJar转为字典：
    res_cookies_dic = requests.utils.dict_from_cookiejar(cookies)
    # 将新的cookies信息更新到手动cookies字典
    for i in res_cookies_dic.keys():
        cookies[i] = res_cookies_dic[i]
    return cookies


def session_url(url, params=None, headers=myhead, proxies=None, timeout=6, ecode='utf-8',
                wait_random_min=200, wait_random_max=3000, stop_max_attempt_number=100):

    @retry(wait_random_min=wait_random_min, wait_random_max=wait_random_max, stop_max_attempt_number=stop_max_attempt_number)
    def _parse_url(url):
        # 开启一个session会话
        session = requests.session()
        session.keep_alive = False
        # 设置请求头信息
        session.headers = headers
        # 将cookiesJar赋值给会话
        # session.cookies = self.read_cookies()
        # 向目标网站发起请求
        response = session.get(url, params=params, headers=headers, proxies=proxies, timeout=timeout)
        assert response.status_code == 200
        session.cookies = set_cookies(response.cookies)
        # return response.text
        return response.content.decode(ecode)  # .content.decode('gbk')  # 'utf-8'

    try:
        # 以下except捕获当requests请求异常
        response = _parse_url(url)
        soup = BeautifulSoup(response, 'lxml')
        [s.extract() for s in soup(["script", "style"])]
    except requests.exceptions.ConnectionError as e:
        print('ConnectionError:', e, url, flush=True)
        soup = None
    except requests.exceptions.ChunkedEncodingError as e:
        print('ChunkedEncodingError:', e, url, flush=True)
        soup = None
    except Exception as e:
        print('Unfortunitely Unknow Error:', e, url, flush=True)
        soup = None
    return soup


def savefile(_filename, 内容):
    # 函数说明:将爬取的文章内容写入文件
    print('[' + _filename + ']开始保存......', end='', flush=True)
    内容.sort()
    with open(_filename, 'a', encoding='utf-8') as f:
        for i in 内容:
            f.write(i[1] + '\n' + i[2] + '\n')
    print('[' + _filename + ']保存完成。', flush=True)


def get_stime(bool=True):
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    stamp = ("".join(time_stamp.split()[0].split("-")) + "".join(time_stamp.split()[1].split(":"))).replace('.', '')

    if bool:
        return stamp
    else:
        return time_stamp

    if __name__ == "__main__":
        pass
