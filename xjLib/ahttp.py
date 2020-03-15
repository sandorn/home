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
@LastEditors: Even.Sand
@LastEditTime: 2020-03-15 17:53:08
'''
import asyncio
import ctypes
import json
from functools import partial

import aiohttp
from cchardet import detect
from fake_useragent import UserAgent
from lxml import etree
from retrying import retry

__all__ = ('map', 'Session', 'get', 'options', 'head', 'post', 'put', 'patch', 'delete')


myhead = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.6,en;q=0.4',
    'Accept-Charset': 'gb2312,utf-8;q=0.7,*;q=0.7',
    'Connection': 'close',
}


class Session:
    def __init__(self, *args, **kwargs):
        self.session = self
        self.headers = myhead
        self.cookies = {}
        self.request_pool = []

    def __getattr__(self, name):
        if name in ['get', 'options', 'head', 'post', 'put', 'patch', 'delete']:
            new_req = AsyncRequestTask(headers=self.headers, session=self.session)
            new_req.__getattr__(name)
            self.request_pool.append(new_req)
            return new_req.get_params

    def __repr__(self):
        return f"<Ahttp Session [id:{id(self.session)} client]>"


class AsyncRequestTask:
    def __init__(self, *args, session=None, headers=None, **kwargs):
        self.session = session
        self.headers = headers
        self.cookies = None
        self.kw = kwargs
        self.method = None

    def __getattr__(self, name):
        if name in ['get', 'options', 'head', 'post', 'put', 'patch', 'delete']:
            self.method = name
            return self.get_params

    def __repr__(self):
        return f"<AsyncRequestTask session:[{id(self.session)}] req:[{self.method.upper()}:{self.url}]>"

    def get_params(self, *args, **kw):
        self.url = args[0]
        self.args = args[1:]
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
        future = asyncio.ensure_future(single_task(self))
        loop = asyncio.get_event_loop()
        # asyncio.set_event_loop(loop)
        loop.run_until_complete(future)
        new_res = AhttpResponse(id(self.session), self.result, self.content, self)
        return [new_res, self.callback and self.callback(new_res)][0]


def wrap_headers(headers):
    ua = UserAgent()
    new_headers = {}
    for k, v in headers.items():
        new_headers[k] = str(v)

    new_headers['User-Agent'] = ua.random
    return new_headers


async def single_task(self):
    # #单个任务，从task.run()调用
    # 创建会话对象
    @retry(wait_random_min=20, wait_random_max=1000, stop_max_attempt_number=10)
    async def _run(self):
        async with aiohttp.ClientSession(cookies=self.cookies) as session:
            async with session.request(self.method, self.url, *self.args, verify_ssl=False, timeout=3000, headers=wrap_headers(self.headers or self.session.headers), **self.kw) as sessReq:
                content = await sessReq.read()
                self.result, self.content = sessReq, content

    try:
        await _run(self)
    except Exception as err:
        print(self.url, 'single_task Error:\t', repr(err))
        raise err


class AhttpResponse:
    # 结构化返回结果
    def __init__(self, index, sessReq, content, task):
        self.index = index
        self.content = content
        self.task = task
        self.raw = self.clientResponse = sessReq

    @property
    def text(self):
        code_type = detect(self.content)
        return self.content.decode(code_type['encoding'], 'ignore')

    @property
    def url(self):
        return self.clientResponse.url

    @property
    def cookies(self):
        return self.clientResponse.cookies

    @property
    def headers(self):
        return self.clientResponse.headers

    def json(self):
        return json.loads(self.text)

    @property
    def status(self):
        return self.clientResponse.status

    @property
    def method(self):
        return self.clientResponse.method

    @property
    def html(self):
        # @html.setter  #def html用于设置
        html = etree.HTML(self.text)
        return html

    def __repr__(self):
        return f"<AhttpResponse status[{self.status}] url=[{self.url}]>"


def run(tasks, pool=20, callback=None):
    if not isinstance(tasks, list):
        raise "the tasks of run must be a list object"

    conn = aiohttp.TCPConnector(use_dns_cache=True, loop=asyncio.get_event_loop(), ssl=False)
    # 并发量限制
    sem = asyncio.Semaphore(pool)
    result = []  # #存放返回结果集合
    loop = asyncio.get_event_loop()
    # asyncio.set_event_loop(loop)
    # 执行任务
    loop.run_until_complete(multi_req(tasks, conn, sem, callback, result))

    # #不排序直接返回结果
    return result


async def multi_req(tasks, conn, sem, callback, result):
    new_tasks = []
    # 创建会话对象,，使用单一session对象
    sessions_list = {}
    new_tasks = []
    for index in range(len(tasks)):
        task = tasks[index]
        if id(task.session) not in sessions_list:
            sessions_list[id(task.session)] = aiohttp.ClientSession(connector_owner=False, connector=conn, cookies=task.session.cookies)

        new_tasks.append(asyncio.ensure_future(control_sem(sem, index, task, callback, result, sessions_list[id(task.session)])))

    await asyncio.wait(new_tasks)
    await asyncio.wait([asyncio.ensure_future(v.close()) for k, v in sessions_list.items()])
    await conn.close()  # 关闭tcp连接器


async def control_sem(sem, index, task, callback, result, session):
    # 限制信号量
    async with sem:
        await fetch(index, task, callback, result, session)


async def fetch(index, task, callback, result, session):
    headers = wrap_headers(task.headers or ctypes.cast(task.session, ctypes.py_object).value.headers)

    def retry_if_error(exception):
        print('retry_if_error:\t', exception)
        return True

    def retry_if_result_none(result):
        # retry_on_result=retry_if_result_none
        print("retry_if_result_none")
        return result is None

    @retry(wait_random_min=20, wait_random_max=1000, stop_max_attempt_number=10, retry_on_exception=retry_if_error)
    async def _run(index, task, callback, result, session):
        async with session.request(task.method, task.url, *task.args, headers=headers, timeout=3000, **task.kw) as sessReq:

            assert sessReq.status == 200
            content = await sessReq.read()
            new_res = AhttpResponse(index, sessReq, content, task)
            result.append(new_res)

            if callback:
                callback(new_res)  # 有回调则调用

    try:
        await _run(index, task, callback, result, session)
    except Exception as err:
        print(task.url, 'fetch Error:\t', repr(err))
        raise err


async def fetch_0(index, task, callback, result, session):
    headers = wrap_headers(task.headers or ctypes.cast(task.session, ctypes.py_object).value.headers)
    Err = ''  # 错误标示
    max_try = 5
    while max_try > 0:
        try:
            async with session.request(task.method, task.url, *task.args, headers=headers, timeout=9, **task.kw) as sessReq:

                if sessReq.status != 200:
                    max_try = max_try - 1
                    Err = 'status!=200'
                    print(task.url, 'Error:', Err)
                    await asyncio.sleep(0.1)
                    continue

                content = await sessReq.read()
                new_res = AhttpResponse(index, sessReq, content, task)
                result.append(new_res)

                if Err:
                    print(task.url, 'result get OK')
                if callback:
                    callback(new_res)  # 有回调则调用
                break  # @status=200,完全退出循环
        except Exception as err:
            max_try = max_try - 1
            Err = repr(err)
            print(task.url, 'Error:', Err)
            await asyncio.sleep(0.1)
            continue  # 跳过此轮，继续下一轮循环


def create_session(method, *args, **kw):
    sess = Session()
    return {"get": sess.get, "post": sess.post, "options": sess.options, "head": sess.head, "put": sess.put, "patch": sess.patch, "delete": sess.delete}[method](*args, **kw)


# #使用偏函数 Partial，快速构建多个函数
get = partial(create_session, "get")
post = partial(create_session, "post")
options = partial(create_session, "options")
head = partial(create_session, "head")
put = partial(create_session, "put")
patch = partial(create_session, "patch")
delete = partial(create_session, "delete")


def ahttpGet(url, params=None, **kwargs):
    task = get(url, params=params, **kwargs)
    res = task.run()
    return res


def ahttpGetAll(urls, pool=20, callback=None, params=None, **kwargs):
    tasks = [get(url, params=params, **kwargs) for url in urls]
    resps = run(tasks, pool=pool, callback=callback)
    return resps
