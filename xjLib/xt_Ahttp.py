# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:49
LastEditTime : 2022-12-10 21:23:42
FilePath     : /xjLib/xt_Ahttp.py
Github       : https://github.com/sandorn/home
==============================================================
https://github.com/web-trump/ahttp/blob/master/ahttp.py
'''
import asyncio
import threading  # #
from functools import partial

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from xt_Head import Headers
from xt_Requests import TRETRY
from xt_Response import htmlResponse

TIMEOUT = 20  # (30, 9, 9, 9)

__all__ = ('get', 'post', 'head', 'put', 'delete', 'options', 'trace', 'connect', 'patch', 'ahttpGet', 'ahttpGetAll', 'ahttpPost', 'ahttpPostAll')


def _unil_session_method(method, *args, **kwargs):
    session = SessionMeta()
    method_dict = {
        "get": session.get,
        "post": session.post,
        'head': session.head,
        'options': session.options,
        'put': session.put,
        'delete': session.delete,
        'trace': session.trace,
        'connect': session.connect,
        'patch': session.patch,
    }
    return method_dict[method](*args, **kwargs)


# #使用偏函数 Partial,快速构建多个函数
get = partial(_unil_session_method, "get")
post = partial(_unil_session_method, "post")
head = partial(_unil_session_method, "head")  # 结果正常，无法使用ReqResult
options = partial(_unil_session_method, "options")  # 'NoneType' object is not callable??
put = partial(_unil_session_method, "put")
delete = partial(_unil_session_method, "delete")
trace = partial(_unil_session_method, "trace")  # 有命令，服务器未响应
connect = partial(_unil_session_method, "connect")  # 有命令，服务器未响应
patch = partial(_unil_session_method, "patch")


class SessionMeta:

    def __init__(self, *args, **kwargs):
        ...

    def __getattr__(self, name):
        if name in ['get', 'post', 'head', 'options', 'put', 'delete', 'trace', 'connect', 'patch']:
            new_AsyncTask = AsyncTask()
            return new_AsyncTask.__getattr__(name)  # @ 设置方法


class AsyncTask:

    def __init__(self, *args, **kwargs):
        self.id = id(self)
        self.index = id(self)
        self.pool = 60  # @连接池

    def __iter__(self):
        yield from self.__dict__.iteritems()

    def __getattr__(self, name):
        if name in ['get', 'post', 'head', 'options', 'put', 'delete', 'trace', 'connect', 'patch']:
            self.method = name  # @ 设置方法
            return self._make_params  # @ 设置参数

    def __repr__(self):
        return f"<AsyncTask | ID:[{id(self.session)}] | METHOD:[{self.method}] | URL:[{self.url}]>"

    def _make_params(self, *args, **kwargs):
        self.url = args[0]
        self.args = args[1:]

        kwargs.setdefault('headers', Headers().randomheaders)
        kwargs.setdefault('timeout', ClientTimeout(TIMEOUT))  # @超时
        self.cookies = kwargs.pop("cookies", {})
        self.callback = kwargs.pop("callback", None)
        self.kwargs = kwargs
        return self


async def asynctask_run(self):
    '''单个任务,从 AsyncTask 调用'''

    @TRETRY
    async def _fetch_run():
        async with TCPConnector(ssl=False, limit=self.pool) as Tconn, ClientSession(cookies=self.cookies, connector=Tconn) as session, session.request(self.method, self.url, *self.args, raise_for_status=True, **self.kwargs) as self.response:
            self.content = await self.response.read()
            return self.response, self.content, self.index

    try:
        # print('asynctask_run', threading.current_thread(), ' | ', self)
        await _fetch_run()
    except Exception as err:
        print(f'Async_run:{self} | RetryErr:{err!r}')
        return None
    else:
        # #返回结果,不管是否正确
        self.result = htmlResponse(self.response, self.content, index=self.index)
        if self.callback: self.result = self.callback(self.result)
        return self.result


async def _async_fetch(task, session):
    '''多个任务,从 ahttpGetAll 初始调用'''

    @TRETRY
    async def _fetch_run():
        async with session.request(task.method, task.url, *task.args, cookies=task.cookies, raise_for_status=True, **task.kwargs) as task.response:
            task.content = await task.response.read()
            return task.response, task.content, task.index

    try:
        # print('_async_fetch', threading.current_thread(), ' | ', task)
        await _fetch_run()
    except Exception as err:
        print(f'Async_Fetch:{task} | RetryErr:{err!r}')
        task.response = task.content = task.result = None
        return None
    else:
        # #返回正确结果
        new_res = htmlResponse(task.response, task.content, task.index)
        if task.callback:
            new_res = task.callback(new_res)  # 有回调则调用
        task.result = new_res
        return new_res


async def gather_async_fetch(tasks, pool):
    '''异步单线程,调用 _async_fetch'''
    async with TCPConnector(ssl=False, limit=pool) as Tconn, ClientSession(connector=Tconn) as session:
        new_tasks = []
        for index, task in enumerate(tasks):
            task.index = index + 1
            task.pool = pool
            new_tasks.append(_async_fetch(task, session))
        # #等待纤程结束
        return await asyncio.gather(*new_tasks)


async def threads_asynctask_run(tasks, pool):
    '''异步多线程,调用 asynctask_run'''
    advocate_loop = asyncio.new_event_loop()
    threading.Thread(target=advocate_loop.run_forever, daemon=True).start()

    new_tasks = []
    for index, task in enumerate(tasks):
        task.index = index + 1
        task.pool = pool
        new_tasks.append(asyncio.run_coroutine_threadsafe(asynctask_run(task), advocate_loop))

    return [task.result() for task in new_tasks]


def ahttp_parse(method, url, *args, **kwargs):
    task = eval(method)(url, *args, **kwargs)
    ## 原有方式
    # loop = asyncio.get_event_loop()
    # return loop.run_until_complete(asynctask_run(task))
    # # 3.7+方式
    return asyncio.run(asynctask_run(task))


def ahttp_parse_list(method, urls, pool=60, threadsafe=True, *args, **kwargs):
    tasks = [eval(method)(url, *args, **kwargs) for url in urls]
    if len(tasks) < pool: pool = len(tasks)
    # #原有方式,单线程,不用明示返回值
    # advocate_loop = asyncio.get_event_loop()
    # return advocate_loop.run_until_complete(multi_req(tasks, pool))
    # # 3.7+ 方式 , threadsafe:单线程或者多线程
    _coroutine = threads_asynctask_run(tasks, pool) if threadsafe else gather_async_fetch(tasks, pool)
    return asyncio.run(_coroutine)


ahttpGet = partial(ahttp_parse, "get")
ahttpPost = partial(ahttp_parse, "post")
ahttpGetAll = partial(ahttp_parse_list, "get")
ahttpPostAll = partial(ahttp_parse_list, "post")

if __name__ == "__main__":

    url_get = "https://httpbin.org/get"
    url_post = "https://httpbin.org/post"
    url_headers = "https://httpbin.org/headers"
    res = ahttpGet(url_get)
    print(res)
    # res = ahttpPost(url_post, data=b'data')
    # print(res)
    res = ahttpGetAll([url_headers, url_get] * 2)
    print(res)
    #######################################################################################################
    # print(head(url_headers).start().headers)
    # print(put('http://httpbin.org/put', data=b'data').start())
    # print(delete('http://httpbin.org/delete').start())
    # print(options('http://httpbin.org/get').start().headers)
    # #'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
    # print(trace('http://www.baidu.com').start().headers)
    # print(connect('http://www.baidu.com').start())
    # print(patch('http://httpbin.org/patch', data=b'data').start())
