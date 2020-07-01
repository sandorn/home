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
#LastEditTime : 2020-06-30 14:58:29
'''
import asyncio
import ctypes
from functools import partial
from random import random

import aiohttp

from xt_Head import MYHEAD
from xt_Response import ReqResult

# from xt_Log import mylog
# print = mylog.warn

TIMEOUT = 30  # (30, 9, 9, 9)
RETRY_TIME = 6  # 最大重试次数

__all__ = ('ahttpGet', 'ahttpGetAll', 'ahttpPost', 'ahttpPostAll')


class SessionMeta:
    def __init__(self, *args, **kwargs):
        self.session = self
        self.headers = MYHEAD
        self.cookies = {}

    def __getattr__(self, name):
        if name in ['get', 'post']:
            new_AyReqTask = AyReqTaskMeta(headers=self.headers,
                                          session=self.session,
                                          cookies=self.cookies)
            new_AyReqTask.__getattr__(name)
            return new_AyReqTask.get_params

    def __repr__(self):
        return f"<SessionMeta id:[{id(self.session)}] client>"


class AyReqTaskMeta:
    def __init__(self,
                 *args,
                 session=None,
                 headers=None,
                 cookies=None,
                 **kwargs):
        self.session = session
        self.headers = headers
        self.cookies = cookies
        self.kw = kwargs
        self.method = None

    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value

    def __getattr__(self, name):
        if name in [
                'get', 'options', 'head', 'post', 'put', 'patch', 'delete'
        ]:
            self.method = name
            return self.get_params

    def __repr__(self):
        return f"<AyReqTaskMeta id:[{id(self.session)}]\tmethod:[{self.method.upper()}]\turl:[{self.url}]>"

    def get_params(self, *args, **kw):
        self.url = args[0]
        self.args = args[1:]
        kw.setdefault('timeout', aiohttp.ClientTimeout(TIMEOUT))  # @超时
        kw.setdefault('verify_ssl', False)  # @超时

        if "callback" in kw:
            self.callback = kw['callback']
            kw.pop("callback")
        else:
            self.callback = None

        if "headers" in kw:
            self.headers = kw['headers']
            kw.pop("headers")
        self.kw = kw
        return self

    def run(self):
        future = asyncio.ensure_future(AyReqTask_run(self))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
        new_res = ReqResult(self.result, self.content, id(self))
        return [new_res, self.callback and self.callback(new_res)][0]


def create_session(method, *args, **kw):
    session = SessionMeta()  # SessionMeta类
    _dict = {
        "get": session.get,
        "post": session.post,
        "options": session.options,
        "head": session.head,
        "put": session.put,
        "patch": session.patch,
        "delete": session.delete
    }
    return _dict[method](*args, **kw)


# #使用偏函数 Partial，快速构建多个函数
get = partial(create_session, "get")
post = partial(create_session, "post")
options = partial(create_session, "options")
head = partial(create_session, "head")
put = partial(create_session, "put")
patch = partial(create_session, "patch")
delete = partial(create_session, "delete")


async def AyReqTask_run(self):
    # #单个任务，从task.run()调用
    async def _fetch_run():
        async with aiohttp.ClientSession(cookies=self.cookies) as session:
            async with session.request(self.method,
                                       self.url,
                                       *self.args,
                                       headers=self.headers,
                                       **self.kw) as response:
                self.content = await response.read()
                self.result = response
                assert response.status in [200, 201, 302]
                return self.result, self.content, id(self)

    attempts = 0
    while attempts < RETRY_TIME:
        try:
            await _fetch_run()
            if attempts != 0:
                print(f'{self}; times:{attempts}; AyReqTask_run Done.')
        except Exception as err:
            print(f'{self}; times:{attempts}; AyReqTask_run Err:{repr(err)}')
            attempts += 1
            continue  # 继续下一轮循环
        else:
            # #返回正确结果
            new_res = ReqResult(self.result, self.content, id(self))
            return new_res

    # #返回错误结果
    new_res = ReqResult(self.result, self.content, id(self))
    return new_res


def run(tasks, pool=0, single_session=True):
    if not isinstance(tasks, list):
        raise "the tasks of run must be a list object"

    result_list = []  # #存放返回结果集合
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        multi_req(tasks, pool, result_list, single_session=single_session))
    # 返回结果集合
    return result_list


async def multi_req(tasks, pool, result_list, single_session=False):
    # 不能传递cookies
    myconn = aiohttp.TCPConnector(use_dns_cache=True,
                                  loop=asyncio.get_event_loop(),
                                  ssl=False,
                                  limit=pool)

    if single_session:
        # #默认使用单一session
        async with aiohttp.ClientSession(connector_owner=False,
                                         connector=myconn) as mysession:
            new_tasks = []
            for index, task in enumerate(tasks):
                task.id = index + 1
                new_tasks.append(
                    asyncio.ensure_future(
                        fetch_async(task, result_list, mysession)))
            await asyncio.wait(new_tasks)

    else:
        # #选择使用多个session
        sessions_list = {}
        new_tasks = []
        for index, task in enumerate(tasks):
            if id(task.session) not in sessions_list:
                async with aiohttp.ClientSession(
                        connector_owner=False,
                        connector=myconn,
                        cookies=task.session.cookies) as mysession:
                    sessions_list[id(task.session)] = mysession
                new_tasks.append(
                    asyncio.ensure_future(
                        fetch_async(
                            task,
                            result_list,
                            sessions_list[id(task.session)],
                        )))

        await asyncio.wait(new_tasks)
        await asyncio.wait([
            asyncio.ensure_future(v.close()) for k, v in sessions_list.items()
        ])

    await myconn.close()  # 关闭tcp连接器


async def fetch_async(task, result_list, session):
    async def _fetch_run():
        headers = task.headers or ctypes.cast(
            task.session, ctypes.py_object).value.headers or MYHEAD
        async with session.request(task.method,
                                   task.url,
                                   *task.args,
                                   headers=headers,
                                   **task.kw) as response:
            task.content = await response.read()
            task.result = response
            assert response.status in [200, 201, 302]
            return task.result, task.content, task.id

    attempts = 0
    while attempts < RETRY_TIME:
        try:
            await _fetch_run()
            if attempts != 0:
                print(f'{task}; times:{attempts}; async_Fetch Done.')
        except Exception as err:
            print(f'{task}; times:{attempts}; async_Fetch Err:{repr(err)}')
            attempts += 1
            await asyncio.sleep(0.1)
            continue  # 继续下一轮循环
        else:
            # #返回正确结果
            new_res = ReqResult(task.result, task.content, task.id)
            if task.callback:
                new_res = task.callback(new_res)  # 有回调则调用
            result_list.append(new_res)
            return new_res

    # #返回错误结果
    new_res = ReqResult(task.result, task.content, task.id)
    if task.callback:
        new_res = task.callback(new_res)  # 有回调则调用
    result_list.append(new_res)
    return new_res


def ahttpGet(url, *args, **kwargs):
    task = get(url, *args, **kwargs)
    res = task.run()
    return res


def ahttpPost(url, *args, **kwargs):
    task = post(url, *args, **kwargs)
    res = task.run()
    return res


def ahttpGetAll(urls, pool=100, single_session=True, *args, **kwargs):
    tasks = [get(url, *args, **kwargs) for url in urls]
    resps = run(tasks, pool=pool, single_session=single_session)
    return resps


def ahttpPostAll(urls, pool=100, single_session=True, *args, **kwargs):
    tasks = [post(url, *args, **kwargs) for url in urls]
    resps = run(tasks, pool=pool, single_session=single_session)
    return resps


if __name__ == "__main__":
    url = "https://nls-gateway.cn-shanghai.aliyuncs.com/rest/v1/tts/async"  # 400
    url_get = "https://httpbin.org/get"  # 返回head及ip等信息
    url_post = "https://httpbin.org/post"  # 返回head及ip等信息
    res = ahttpGet(url_get)
    print(res.text)
    res = ahttpPost(url_post)
    print(res.text)
    res = ahttpGetAll([url, url_get])
    print(res)
    # t = aiohttp.ClientTimeout(TIMEOUT)
    # print(t)
