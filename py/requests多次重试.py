# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@LastEditors: Even.Sand
@Date: 2019-05-12 07:53:07
@LastEditTime: 2019-05-12 08:01:58
'''
import requests
from requests.adapters import HTTPAdapter

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))

s.get('http://example.com', timeout=1)


import requests
from retrying import retry

headers = {}

def parse_url(url):
    @retry(stop_max_attempt_number=3) #最大重试3次，3次全部报错，才会报错
    def _parse_url(url):
        response = requests.get(url, headers=headers, timeout=3) #超时的时候回报错并重试
        assert response.status_code == 200 #状态码不是200，也会报错并充实
        return response

    try:   # 进行异常捕获
        response = _parse_url(url)
    except Exception as e:
        print(e)
        response = None
    return response

'''
---------------------
作者：huwei_1993
来源：CSDN
原文：https://blog.csdn.net/huwei_1993/article/details/81674743
版权声明：本文为博主原创文章，转载请附上博文链接！

在爬虫代码的编写中，requests请求网页的时候常常请求失败或错误，
一般的操作是各种判断状态和超时，需要多次重试请求，这种情况下，
如果想优雅的实现功能，可以学习下retrying包下的retry装饰器的使用

安装：pip install retrying
在@retry()装饰器中，比较重要的几个参数如下：
stop_max_attempt_number：在停止之前尝试的最大次数，最后一次如果还是有异常则会抛出异常，停止运行，默认为5次
stop_max_delay：比如设置成10000，那么从被装饰的函数开始执行的时间点开始，到函数成功运行结束或者失败报错中止的时间点，只要这段时间超过10秒，则停止重试（单位是毫秒）
retry_on_result：指定一个函数，如果指定的函数返回True，则重试，否则抛出异常退出
retry_on_exception: 指定一个函数，如果此函数返回指定异常，则会重试，如果不是指定的异常则会退出
wait_fixed：设置在两次retrying之间的停留时间，单位毫秒
wait_random_min：在两次调用方法停留时长，停留最短时间，默认为0,单位毫秒
wait_random_max：在两次调用方法停留时长，停留最长时间，默认为1000毫秒
wait_exponential_multiplier
wait_exponential_max：以指数的形式产生两次retrying之间的停留时间，
产生的值为2^previous_attempt_number * wait_exponential_multiplier， 
 previous_attempt_number是前面已经retry的次数，如果产生的这个值超过了wait_exponential_max的大小，那么之后两个retrying之间的停留值都为wait_exponential_max
'''

import traceback
from retrying import retry
import requests
from user_agent import agert as ag
import random
def _result(result):
    return result is None


def header(header):
    try:
        if header != None:
            header['User-Agent'] = random.choice(ag)
        else:
            header = {'User-Agent': random.choice(ag)}
        return header
    except Exception as e:
        traceback.print_exc(e)
@retry(stop_max_attempt_number=5, wait_random_min=1000, wait_random_max=2000, retry_on_result=_result)
def My_Request_Get(url, headers=None):
        headers = header(headers)
        # with open('./proxy_txt', 'r') as f:
        #     proxy = f.readline()
        #     proxy = json.loads(proxy)
        # print proxy, type(proxy), '/*-'*10
        response = requests.get(url, headers=headers, timeout=6)
        if response.status_code != 200:
            raise requests.RequestException('my_request_get error!!!!')
        return response


'''
错误重试
错误重试用到的方法之一是：@retry()装饰器
'''
from retrying import retry
# @retry((指定重试的错误类型), 参数设置)，例如
@retry((ValueError, TypeError), stop_max_attempt_number=5)
def func_name():
    XXX

func_name()

def retry_if_result_none(result):
    return result is None

@retry(retry_on_result=retry_if_result_none)
def get_result():
    print 'Retry forever ignoring Exceptions with no wait if return value is None'
    return None

'''
超时处理
爬虫可能会因为网络问题导致请求失败，或一直等待响应，这样会影响程序效率。为避免该问题，我们可以给requests的请求加上timeout参数，限制爬虫在一定的时间内需返回结果，否则就会报超时错误。

requests.get或requests.post——timeout参数的单位为秒，可以设置请求的超时时间，如果超出时间，则返回异常
'''
response = requests.get(url, headers=headers, timeout=0.4)


'''
超时处理与retry装饰器的结合应用
爬虫请求中的timeout参数可以与retry装饰器结合使用。这样爬虫就可以避免偶然的网络波动导致的请求错误，会在设置的重试次数内重复发起请求。
'''
import requests
from retrying import retry


# 全部报错才会报错，如果其中一次正常，则继续执行
# 两次retry之间等待2秒，重试5次
@retry(stop_max_attempt_number=5, wait_fixed=2000)
def get_request(url):
    response = requests.get(url, headers=headers, timeout=1)
    return response.content.decode()


headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
url = "https://www.baidu.com/"
print(get_request(url))
 '''
上面的例子，每次请求的超时限制是1秒，如果超过1秒未返回响应，则会报错。报错之后，会间隔2秒后再重新发起请求。只要其中一次正常，就会继续执行；否则，如果5次全部报错，才会报错。

捕捉异常
'''
import requests
from retrying import retry


# 全部报错才会报错，如果其中一次正常，则继续执行
# 两次retry之间等待2秒，重试5次
@retry(stop_max_attempt_number=5, wait_fixed=1000)
def _get_request(url):
    response = requests.get(url, headers=headers, timeout=1)
    return response.content.decode()


def get_request(url):
    try:
        html_str = _get_request(url)
    except TimeoutError:  # 1
        html_str = 'TimeoutError'
    except:  # 2
        html_str = 'OtherError'
    return html_str


headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
url = "https://www.baidu.com/"
print(get_request(url))
 '''
上面# 2处的except下面会出现“too broad exception clauses”
（This inspection highlights too broad exception
clauses such as no exception class specified,
or specified as 'Exception'.）
这是由于# 2处的except没有指定具体的报错类型，
所以会出现exception过于宽泛的提示。
---------------------
作者：linzhjbtx
来源：CSDN
原文：https://blog.csdn.net/linzhjbtx/article/details/86581972
版权声明：本文为博主原创文章，转载请附上博文链接！
'''
