# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-10-26 17:05:52
FilePath     : /CODE/xjLib/xt_Ahttp.py
Github       : https://github.com/sandorn/home
==============================================================
https://github.com/web-trump/ahttp/blob/master/ahttp.py
"""

import asyncio
from functools import partial
from threading import Thread

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from tenacity import retry, stop_after_attempt, wait_random
from xt_Head import RETRY_TIME, TIMEOUT, Head
from xt_Log import log_decorator
from xt_Response import htmlResponse

TRETRY = retry(
    reraise=True,  # 保留最后一次错误
    stop=stop_after_attempt(RETRY_TIME),
    wait=wait_random(min=0, max=1),
)

__all__ = (
    'get',
    'post',
    'head',
    'options',
    'put',
    'delete',
    'trace',
    'connect',
    'patch',
    'ahttpGet',
    'ahttpGetAll',
    'ahttpPost',
    'ahttpPostAll',
)


Method_List = ['get', 'post', 'head', 'options', 'put', 'delete', 'trace', 'connect', 'patch']


class AsyncTask:
    def __init__(self, *args, **kwargs):
        self.index = id(self)

    def __getitem__(self, method):
        method = method.lower()
        if method in Method_List:
            self.method = method  # 保存请求方法
            return lambda *args, **kwargs: self.__create_params(*args, **kwargs)

    def __getattr__(self, method):
        if method in Method_List:
            self.method = method  # 保存请求方法
            return self.__create_params  # @ 设置参数

    def __repr__(self):
        return f'<AsyncTask | Method:[{self.method}] | Index:[{self.index}] | Session:[{id(self.session)}] | URL:[{self.url}]>'

    def __create_params(self, *args, **kwargs):
        self.url = args[0]
        self.args = args[1:]
        kwargs.setdefault('headers', Head().randua)
        kwargs.setdefault('timeout', ClientTimeout(TIMEOUT))  # @超时
        self.cookies = kwargs.pop('cookies', {})
        self.callback = kwargs.pop('callback', None)
        self.kwargs = kwargs
        return self

    def run(self):
        return asyncio.run(_async_fetch(self))

    async def start(self):
        """主线程"""
        return await _async_fetch(self)


@log_decorator
async def _async_fetch(self):
    """单任务和多任务均调用此方法"""

    @TRETRY
    async def _fetch_run():
        async with TCPConnector(ssl=False) as Tconn, ClientSession(cookies=self.cookies, connector=Tconn) as self.session, self.session.request(self.method, self.url, raise_for_status=True, *self.args, **self.kwargs) as self.response:
            self.content = await self.response.read()
            return self.response, self.content, self.index

    try:
        await _fetch_run()
        self.result = htmlResponse(self.response, self.content, index=self.index)
        if self.callback:
            self.result = self.callback(self.result)
        return self.result
    except Exception as err:
        print(f'Async_fetch:{self} | RetryErr:{err!r}')
        self.response = self.content = None
        self.result = [self.index, err, '']
        return self


def __session_method(method, *args, **kwargs):
    session = AsyncTask()
    method = method.lower()
    if method in Method_List:
        # return session[method](*args, **kwargs) #__getitem__
        return getattr(session, method)(*args, **kwargs)  # getattr


get = partial(__session_method, 'get')
post = partial(__session_method, 'post')
head = partial(__session_method, 'head')  # 结果正常，无ReqResult
options = partial(__session_method, 'options')
put = partial(__session_method, 'put')
delete = partial(__session_method, 'delete')
trace = partial(__session_method, 'trace')  # 有命令，服务器未响应
connect = partial(__session_method, 'connect')  # 有命令，服务器未响应
patch = partial(__session_method, 'patch')


async def create_gather_task(tasks):
    """异步单线程,使用同一个session"""
    tasks_list = []
    for index, task in enumerate(tasks, 1):
        task.index = index
        _coroutine = task.start()
        tasks_list.append(_coroutine)
    return await asyncio.gather(*tasks_list, return_exceptions=True)


async def create_threads_task(coroes):
    """异步多线程,使用不同session"""
    threadsafe_loop = asyncio.new_event_loop()
    Thread(target=threadsafe_loop.run_forever, name='ThreadSafe', daemon=True).start()

    tasks_list = []
    for index, coro in enumerate(coroes, 1):
        coro.index = index
        _coroutine = coro.start()
        tasks_list.append(asyncio.run_coroutine_threadsafe(_coroutine, threadsafe_loop))

    return [task.result() for task in tasks_list]


def aiohttp_parse(method, url, *args, **kwargs):
    method = method.lower()
    task = eval(method)(url, *args, **kwargs)
    _coroutine = task.start()
    loop = asyncio.new_event_loop()
    return loop.run_until_complete(_coroutine)


def aiohttp__issue(method, urls, *args, **kwargs):
    method = method.lower()
    coroes = [eval(method)(url, *args, **kwargs) for url in urls]
    _coroutine = create_threads_task(coroes) if kwargs.pop('threadsafe', True) else create_gather_task(coroes)
    return asyncio.run(_coroutine)


ahttpGet = partial(aiohttp_parse, 'get')
ahttpPost = partial(aiohttp_parse, 'post')
ahttpGetAll = partial(aiohttp__issue, 'get')
ahttpPostAll = partial(aiohttp__issue, 'post')

if __name__ == '__main__':
    url_get = 'https://httpbin.org/get'
    url_post = 'https://httpbin.org/post'
    url_headers = 'https://httpbin.org/headers'

    res = ahttpGet(url_get)
    print(res)
    res = ahttpPost(url_post, data=b'data')
    print(res)
    res = ahttpGetAll([url_headers, url_get])
    print(res)
    #######################################################################################################
    # print(get('http://httpbin.org/headers').run().headers)
    # print(put('http://httpbin.org/put', data=b'data').start())
    # print(delete('http://httpbin.org/delete').start())
    # print(options('http://httpbin.org/get').start().headers)
    # #'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
    # print(trace('http://www.baidu.com').start().headers)
    # print(connect('http://www.baidu.com').start())
    # print(patch('http://httpbin.org/patch', data=b'data').start())
