# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-04 09:01:10
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-07-11 10:58:25
'''
import asyncio
from functools import partial

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from xt_Head import MYHEAD
from xt_Requests import TRETRY
from xt_Response import ReqResult

TIMEOUT = 20  # (30, 9, 9, 9)

__all__ = ('ahttpGet', 'ahttpGetAll', 'ahttpPost', 'ahttpPostAll')


def create_session(method, *args, **kw):
    session = SessionMeta()  # SessionMeta类
    _dict = {"get": session.get, "post": session.post}
    return _dict[method](*args, **kw)


# #使用偏函数 Partial，快速构建多个函数
get = partial(create_session, "get")
post = partial(create_session, "post")


class SessionMeta:

    def __init__(self, *args, **kwargs):
        pass

    def __getattr__(self, name):
        if name in ['get', 'post']:
            new_AsyncTask = AsyncTask()
            new_AsyncTask.__getattr__(name)
            return new_AsyncTask._make_params


class AsyncTask:

    def __init__(self, *args, **kwargs):
        self.id = id(self)
        self.index = id(self)
        self.pool = 1

    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value

    def __getattr__(self, name):
        if name in ['get', 'post']:
            self.method = name
            return self._make_params

    def __repr__(self):
        return f"<AsyncTask id:[{id(self.session)}]\tmethod:[{self.method}]\turl:[{self.url}]>"

    def _make_params(self, *args, **kwargs):
        self.url = args[0]
        self.args = args[1:]

        kwargs.setdefault('headers', MYHEAD)
        kwargs.setdefault('timeout', ClientTimeout(TIMEOUT))  # @超时
        kwargs.setdefault('verify_ssl', False)
        self.cookies = kwargs.pop("cookies", {})
        self.callback = kwargs.pop("callback", None)
        self.kwargs = kwargs

        return self

    def run(self):
        future = asyncio.ensure_future(Async_run(self))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
        return self.result


async def Async_run(self):
    # #单个任务,从  AsyncTask.run  调用
    @TRETRY
    async def _fetch_run():
        async with TCPConnector(ssl=False, limit=self.pool) as Tconn, ClientSession(cookies=self.cookies, connector=Tconn) as session, session.request(self.method, self.url, *self.args, raise_for_status=True, **self.kwargs) as self.response:
            self.content = await self.response.read()
            return self.response, self.content, self.index

    try:
        await _fetch_run()
    except Exception as err:
        print(f'Async_run:{self}; RetryErr:{err!r}')
        return None
    else:
        # #返回结果,不管是否正确
        self.result = ReqResult(self.response, self.content, index=self.index)
        if self.callback:  # 有回调则调用
            self.result = self.callback(self.result)
        return self.result


def run(tasks, pool):
    if not isinstance(tasks, (list, tuple)):
        raise "the tasks of run must be a list|tuple object"

    result_list = []  # #存放返回结果集合
    loop = asyncio.get_event_loop()
    loop.run_until_complete(multi_req(tasks, pool, result_list))
    # 返回结果集合
    return result_list


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


async def Async_Fetch(task, result_list, session):

    @TRETRY
    async def _fetch_run():
        async with session.request(task.method, task.url, *task.args, cookies=task.cookies, raise_for_status=True, **task.kwargs) as task.response:
            task.content = await task.response.read()
            return task.response, task.content, task.index

    try:
        await _fetch_run()
    except Exception as err:
        print(f'Async_Fetch:{task}; RetryErr:{err!r}')
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


def ahttp_parse(method, url, *args, **kwargs):
    task = eval(method)(url, *args, **kwargs)
    res = task.run()
    return res


def ahttp_parse_list(method, urls, pool=200, *args, **kwargs):
    tasks = [eval(method)(url, *args, **kwargs) for url in urls]
    if len(tasks) < pool: pool = len(tasks)
    resps = run(tasks, pool)
    return resps


ahttpGet = partial(ahttp_parse, "get")
ahttpPost = partial(ahttp_parse, "post")

ahttpGetAll = partial(ahttp_parse_list, "get")
ahttpPostAll = partial(ahttp_parse_list, "post")

if __name__ == "__main__":
    url = "https://nls-gateway.cn-shanghai.aliyuncs.com/rest/v1/tts/async"  # 400
    url_get = "https://httpbin.org/get"  # 返回head及ip等信息
    url_post = "https://httpbin.org/post"  # 返回head及ip等信息
    url_g = "http://g.cn"  # 返回head及ip等信息

    res = ahttpGet(url_g)
    print(res)
    res = ahttpPost(url_post)
    print(res)
    res = ahttpGetAll([url_g, url_get])
    print(res)
