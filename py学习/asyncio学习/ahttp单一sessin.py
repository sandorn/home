# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-11 12:34:56
@LastEditors: Even.Sand
@LastEditTime: 2020-03-11 12:35:02
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
        future = asyncio.ensure_future(single_req(self))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
        new_res = AhttpResponse(self.result, self.content, self)
        return [new_res, self.callback and self.callback(new_res)][0]


async def single_req(self):
    # #单个任务，从task.run()调用
    # 创建会话对象
    async with aiohttp.ClientSession(cookies=self.cookies) as session:
        # 发送请求
        async with session.request(
                self.method,
                self.url,
                *self.args,
                verify_ssl=False,
                timeout=20,
                headers=wrap_headers(self.headers or self.session.headers),
                **self.kw) as resp:
            # 读取响应
            res = await resp.read()
            # 将相应结果保存
            self.result, self.content = resp, res


class AhttpResponse:
    # 结构化返回结果
    def __init__(self, res, content, req, *args, **kwargs):
        self.content = content
        self.req = req
        self.raw = self.clientResponse = res

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


def run(tasks, pool=20, max_try=3, callback=None, order=False):
    # #改为无回调则排序
    order = True if callback is None else False
    if not isinstance(tasks, list):
        raise "the tasks of run must be a list object"

    # 并发量限制
    sem = asyncio.Semaphore(pool)
    result = []  # #存放返回结果集合
    loop = asyncio.get_event_loop()
    # 执行任务
    loop.run_until_complete(multi_req(tasks, sem, callback, max_try, result))

    # #不排序则直接返回结果
    if not order:
        return result

    # #排序
    rid = [*map(lambda x: id(x), tasks)]
    new_res = [*rid]
    for res in result:
        index = rid.index(id(res.req))
        rid[index] = 0
        new_res[index] = res
    return new_res


def wrap_headers(headers):
    ua = UserAgent()
    new_headers = {}
    for k, v in headers.items():
        new_headers[k] = str(v)

    new_headers['User-Agent'] = ua.random
    return new_headers


async def multi_req(tasks, sem, callback, max_try, result):
    new_tasks = []
    # 创建会话对象,，使用单一session对象
    conn = aiohttp.TCPConnector(
        # limit=100, limit_per_host=100,
        loop=asyncio.get_event_loop(),
        verify_ssl=False
    )
    session = aiohttp.ClientSession(connector_owner=False, connector=conn)

    for task in tasks:
        new_task = asyncio.ensure_future(
            control_sem(sem, task, callback, max_try, result, session)
        )

        # if callback: # 如果有回调则在这里绑定
        #    new_task.add_done_callback(callback)
        new_tasks.append(new_task)

    await asyncio.wait(new_tasks)
    await session.close()  # 关闭session连接器
    await conn.close()  # 关闭tcp连接器


async def control_sem(sem, task, callback, max_try, result, session):
    # 限制信号量
    async with sem:
        return await fetch(task, callback, max_try, result, session)


async def fetch(task, callback, max_try, result, session):
    headers = wrap_headers(task.headers or ctypes.cast(task.session, ctypes.py_object).value.headers)
    while max_try > 0:
        try:
            async with session.request(task.method, task.url, *task.args, headers=headers, **task.kw) as resp:
                res = await resp.read()
                rResp = AhttpResponse(resp, res, task)
                if rResp.status == 200:
                    result.append(rResp)
                    print(task.url, 'result.append')
                    if callback:
                        print(task.url, 'callback')
                        callback(rResp)
                    break  # 完全退出循环
        except (
            asyncio.TimeoutError,
            aiohttp.ClientOSError,
            aiohttp.ClientResponseError,
            aiohttp.ClientPayloadError,
            aiohttp.ServerDisconnectedError,
        ) as err:
            print(task.url, 'Err:', err)
            max_try = max_try - 1
            await asyncio.sleep(0.2)
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


get = partial(create_session, "get")
post = partial(create_session, "post")
options = partial(create_session, "options")
head = partial(create_session, "head")
put = partial(create_session, "put")
patch = partial(create_session, "patch")
delete = partial(create_session, "delete")
# #使用偏函数 Partial，快速构建多个函数


def ahttpGet(url, params=None, **kwargs):
    task = get(url, params=params, **kwargs)
    res = task.run()
    return res


def ahttpGetAll(urls, pool=20, callback=None, params=None, **kwargs):
    tasks = [get(url, params=params, **kwargs) for url in urls]
    resps = run(tasks, pool=pool, callback=callback)
    return resps
