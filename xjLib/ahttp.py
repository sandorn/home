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
@LastEditTime: 2020-03-12 15:29:27
'''
import asyncio
import ctypes
import json
from functools import partial

import aiohttp
from cchardet import detect
from fake_useragent import UserAgent
from requests_html import HTML, HTMLSession

__all__ = ('map', 'Session', 'get', 'options', 'head', 'post', 'put', 'patch', 'delete')


class Session:
    def __init__(self, *args, **kwargs):
        self.session = self
        self.headers = HTMLSession().headers
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
    async with aiohttp.ClientSession(cookies=self.cookies) as session:
        # 发送请求
        async with session.request(
                self.method,
                self.url,
                *self.args,
                verify_ssl=False,
                timeout=9,
                headers=wrap_headers(self.headers or self.session.headers),
                **self.kw) as resp:
            # 读取响应
            content = await resp.read()
            # 将相应结果保存
            self.result, self.content = resp, content


class AhttpResponse:
    # 结构化返回结果
    def __init__(self, index, sessReq, content, task, *args, **kwargs):
        self.index = index
        self.content = content
        self.task = task
        self.raw = self.clientResponse = sessReq

    @property
    def text(self):
        code_type = detect(self.content)
        return self.content.decode(code_type['encoding'])

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
        # @重写，原库GB18030编码的网页可能导致乱码，这里使用content，而不是text，避免二次转码
        html = HTML(html=self.content, url=self.raw.url)
        return html

    @property
    def dom(self):
        """
        返回一个requests_html对象，
        支持所有requests_html的html对象的操作。例如find, xpath, render（先安装chromium浏览器）
        """
        html = HTML(html=self.text)
        html.url = self.raw.url
        return html

    def __repr__(self):
        return f"<AhttpResponse status[{self.status}] url=[{self.url}]>"


def run(tasks, pool=20, max_try=5, callback=None, log=True):
    if not isinstance(tasks, list):
        raise "the tasks of run must be a list object"

    conn = aiohttp.TCPConnector(use_dns_cache=True, loop=asyncio.get_event_loop(), ssl=False)
    # 并发量限制
    sem = asyncio.Semaphore(pool)
    result = []  # #存放返回结果集合
    loop = asyncio.get_event_loop()
    # 执行任务
    loop.run_until_complete(multi_req(tasks, conn, sem, callback, log, max_try, result))

    # #不排序直接返回结果
    return result


@asyncio.coroutine
async def multi_req(tasks, conn, sem, callback, log, max_try, result):
    new_tasks = []
    # 创建会话对象,，使用单一session对象
    sessions_list = {}
    new_tasks = []
    for index in range(len(tasks)):
        task = tasks[index]
        if id(task.session) not in sessions_list:
            sessions_list[id(task.session)] = aiohttp.ClientSession(
                connector_owner=False,
                connector=conn,
                cookies=task.session.cookies
            )

        new_tasks.append(
            asyncio.ensure_future(
                control_sem(
                    sem, index, task, callback, log, max_try, result, sessions_list[id(task.session)])
            )
        )

    await asyncio.wait(new_tasks)
    await asyncio.wait([asyncio.ensure_future(v.close()) for k, v in sessions_list.items()])
    await conn.close()  # 关闭tcp连接器


@asyncio.coroutine
async def control_sem(sem, index, task, callback, log, max_try, result, session):
    # 限制信号量
    async with sem:
        await fetch(index, task, callback, log, max_try, result, session)


@asyncio.coroutine
async def fetch(index, task, callback, log, max_try, result, session):
    headers = wrap_headers(task.headers or ctypes.cast(task.session, ctypes.py_object).value.headers)
    Err = ''  # 错误标示
    while max_try > 0:
        try:
            async with session.request(task.method, task.url, *task.args, headers=headers, timeout=9, **task.kw) as sessReq:

                if sessReq.status != 200:
                    max_try = max_try - 1
                    Err = 'status!=200'
                    if log: print(task.url, 'Error:', Err)
                    await asyncio.sleep(0.1)
                    continue

                content = await sessReq.read()
                new_res = AhttpResponse(index, sessReq, content, task)
                result.append(new_res)

                if log and Err: print(task.url, 'result get OK')
                if callback: callback(new_res)  # 有回调则调用
                break  # @status=200,完全退出循环
        except Exception as err:
            max_try = max_try - 1
            Err = repr(err)
            if log: print(task.url, 'Error:', Err)
            await asyncio.sleep(0.1)
            continue  # 跳过此轮，继续下一轮循环


def create_session(method, *args, **kw):
    sess = Session()
    return {"get": sess.get,
            "post": sess.post,
            "options": sess.options,
            "head": sess.head,
            "put": sess.put,
            "patch": sess.patch,
            "delete": sess.delete}[method](*args, **kw)


# #使用偏函数 Partial，快速构建多个函数
get = partial(create_session, "get")
post = partial(create_session, "post")
options = partial(create_session, "options")
head = partial(create_session, "head")
put = partial(create_session, "put")
patch = partial(create_session, "patch")
delete = partial(create_session, "delete")


def ahttpGet(url, callback=None, params=None, **kwargs):
    task = get(url, params=params, **kwargs)
    res = task.run()
    return res


def ahttpGetAll(urls, pool=20, callback=None, max_try=5, log=True, params=None, **kwargs):
    tasks = [get(url, params=params, **kwargs) for url in urls]
    resps = run(tasks, pool=pool, callback=callback, log=log)
    return resps
