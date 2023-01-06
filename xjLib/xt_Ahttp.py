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
'''
import asyncio
from functools import partial

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from xt_Head import Headers
from xt_Requests import TRETRY
from xt_Response import ReqResult

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
        if name in ['get', 'post', 'head', 'optins', 'put', 'delete', 'trace', 'connect', 'patch']:
            new_AsyncTask = AsyncTask()
            return new_AsyncTask.__getattr__(name)  # @ 设置方法


class AsyncTask:

    def __init__(self, *args, **kwargs):
        self.id = id(self)
        self.index = id(self)
        self.pool = 1

    def __iter__(self):
        yield from self.__dict__.iteritems()

    def __getattr__(self, name):
        if name in ['get', 'post', 'head', 'optins', 'put', 'delete', 'trace', 'connect', 'patch']:
            self.method = name  # @ 设置方法
            return self._make_params  # @ 设置参数

    def __repr__(self):
        return f"<AsyncTask id:[{id(self.session)}] | Method:[{self.method}] | Url:[{self.url}]>"

    def _make_params(self, *args, **kwargs):
        self.url = args[0]
        self.args = args[1:]

        kwargs.setdefault('headers', Headers().random())
        kwargs.setdefault('timeout', ClientTimeout(TIMEOUT))  # @超时
        kwargs.setdefault('verify_ssl', False)
        self.cookies = kwargs.pop("cookies", {})
        self.callback = kwargs.pop("callback", None)
        self.kwargs = kwargs
        return self

    def start(self):
        future = asyncio.ensure_future(asynctask_run(self))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
        # return future.result()
        return self.result


async def asynctask_run(self):
    # 单个任务,从  AsyncTask.start  调用
    @TRETRY
    async def _fetch_run():
        async with TCPConnector(ssl=False, limit=self.pool) as Tconn, ClientSession(cookies=self.cookies, connector=Tconn) as session, session.request(self.method, self.url, *self.args, raise_for_status=True, **self.kwargs) as self.response:
            self.content = await self.response.read()
            return self.response, self.content, self.index

    try:
        await _fetch_run()
    except Exception as err:
        print(f'Async_run:{self} | RetryErr:{err!r}')
        return None
    else:
        # #返回结果,不管是否正确
        self.result = ReqResult(self.response, self.content, index=self.index)
        if self.callback: self.result = self.callback(self.result)
        return self.result


async def Async_Fetch(task, result_list, session):

    @TRETRY
    async def _fetch_run():
        async with session.request(task.method, task.url, *task.args, cookies=task.cookies, raise_for_status=True, **task.kwargs) as task.response:
            task.content = await task.response.read()
            return task.response, task.content, task.index

    try:
        await _fetch_run()
    except Exception as err:
        print(f'Async_Fetch:{task} | RetryErr:{err!r}')
        task.response = task.content = task.result = None
        result_list.append(None)
        return None
    else:
        # #返回正确结果
        new_res = ReqResult(task.response, task.content, task.index)
        if task.callback:
            new_res = task.callback(new_res)  # 有回调则调用
        task.result = new_res
        result_list.append(new_res)
        return new_res


async def multi_req(tasks, pool, result_list):
    '''多个task使用同一sessionn model == 0'''
    async with TCPConnector(ssl=False, limit=pool) as Tconn, ClientSession(connector=Tconn) as session:
        new_tasks = []
        for index, task in enumerate(tasks):
            task.index = index + 1
            new_tasks.append(asyncio.ensure_future(Async_Fetch(task, result_list, session)))

        # #等待纤程结束
        await asyncio.wait(new_tasks)

    return result_list


def util_tasks(tasks, pool):
    assert isinstance(tasks, (list, tuple)), "tasks must be list or tuple"
    result_list = []  # #存放返回结果集合
    future = asyncio.ensure_future(multi_req(tasks, pool, result_list))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(future)
    # 返回结果集合
    return result_list


def ahttp_parse(method, url, *args, **kwargs):
    task = eval(method)(url, *args, **kwargs)
    return task.start()


def ahttp_parse_list(method, urls, pool=200, *args, **kwargs):
    tasks = [eval(method)(url, *args, **kwargs) for url in urls]
    if len(tasks) < pool: pool = len(tasks)
    return util_tasks(tasks, pool)


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
    # res = ahttpPost(url_post)
    # print(res)
    # res = ahttpGetAll([url_headers, url_get])
    # print(res)
    #######################################################################################################
    print(head(url_headers).start().headers)
    # print(put('http://httpbin.org/put', data=b'data').run())
    # print(delete('http://httpbin.org/delete').run())
    # print(options('http://httpbin.org/get').run())  # 'NoneType' object is not callable??
    # print(trace('http://httpbin.org').run())  #有命令，服务器未响应
    #ypeError: Expected object of type bytes or bytearray, got: <class 'aiohttp.streams.EmptyStreamReader'>
    # print(connect('http://httpbin.org/connect').run())  #有命令，服务器未响应
    #ypeError: Expected object of type bytes or bytearray, got: <class 'aiohttp.streams.EmptyStreamReader'>
    # print(patch('http://httpbin.org/patch', data=b'data').run())
