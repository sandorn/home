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
@LastEditTime: 2020-03-24 09:15:03
'''
import asyncio
import ctypes
import json
from functools import partial
from html import unescape

import aiohttp
from cchardet import detect
from fake_useragent import UserAgent
from lxml import etree
from opnieuw import RetryException, retry
# from retrying import retry

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

    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value

    def __getattr__(self, name):
        if name in ['get', 'options', 'head', 'post', 'put', 'patch', 'delete']:
            self.method = name
            return self.get_params

    def __repr__(self):
        return f"<AsyncTask session:[{id(self.session)}]\t{self.method.upper()}:{self.url}>"

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
        future = asyncio.ensure_future(ArTask_run(self))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
        new_res = AhttpResponse(self.result, self.content, self)
        return [new_res, self.callback and self.callback(new_res)][0]


def wrap_headers(headers):
    ua = UserAgent()
    new_headers = {}
    for k, v in headers.items():
        new_headers[k] = str(v)

    new_headers['User-Agent'] = ua.random
    return new_headers


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


async def ArTask_run(self):
    # #单个任务，从task.run()调用
    async def _run():
        async with aiohttp.ClientSession(cookies=self.cookies) as session:
            async with session.request(self.method, self.url, *self.args, verify_ssl=False, headers=wrap_headers(self.headers or self.session.headers), **self.kw) as sessReq:
                content = await sessReq.read()
                self.result, self.content, self.index = sessReq, content, id(self.result)

    max_try = 10
    index = 0
    while max_try > 0:
        try:
            await _run()
            print(self, index, 'ArTask_run done')
            break
        except Exception as err:
            print(self, index, 'ArTask_run err:', repr(err))
            max_try -= 1
            index += 1
            await asyncio.sleep(0.1)
            continue  # 继续下一轮循环


class AhttpResponse:
    # 结构化返回结果
    def __init__(self, sessReq, content, task):
        self.index = task.index
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
        def clean(html, filter):
            data = etree.HTML(html)
            trashs = data.xpath(filter)
            for item in trashs:
                item.getparent().remove(item)
            return data
        # #去除节点clean # #解码html:unescape
        html = clean(unescape(self.text), '//script')
        # html = etree.HTML(self.text)
        return html

    def __repr__(self):
        return f"<AhttpResponse status[{self.status}] url=[{self.url}]>"


def run(tasks, pool=100):
    if not isinstance(tasks, list):
        raise "the tasks of run must be a list object"

    conn = aiohttp.TCPConnector(
        use_dns_cache=True,
        loop=asyncio.get_event_loop(),
        ssl=False,
        # limit=100,  # 限制并行连接的总量,0无限制
    )
    result = []  # #存放返回结果集合
    loop = asyncio.get_event_loop()
    loop.run_until_complete(multi_req(tasks, conn, pool, result))

    # 返回结果集合
    return result


async def multi_req(tasks, conn, pool, result):
    new_tasks = []
    sion_list = {}
    for index in range(len(tasks)):
        task = tasks[index]
        task.index = index  # #将任务序号分配给每个任务
        task.pool = pool  # #将并发限制赋值给每个任务
        if id(task.session) not in sion_list:
            sion_list[id(task.session)] = aiohttp.ClientSession(
                connector_owner=False,
                connector=conn,
                cookies=task.session.cookies)

        new_tasks.append(
            asyncio.ensure_future(
                control_sem(task, result, sion_list[id(task.session)])
            )
        )

    await asyncio.wait(new_tasks)
    await asyncio.wait(
        [asyncio.ensure_future(v.close()) for k, v in sion_list.items()]
    )
    await conn.close()  # 关闭tcp连接器


async def control_sem(task, result, session):
    # !适用信号量限制并发数
    maxsem = asyncio.Semaphore(task.pool)
    async with maxsem:
        await fetch(task, result, session)


async def fetch_Opnieuw(task, result, session):
    # # fetch_Opnieuw  #最终解决：增加timeout为300
    @retry(
        retry_on_exceptions=(asyncio.exceptions.TimeoutError, asyncio.exceptions.CancelledError, asyncio.TimeoutError, RetryException),
        max_calls_total=10,
        retry_window_after_first_call_in_seconds=5,)
    async def _run():
        print(task, 'fetch start...')
        headers = wrap_headers(task.headers or ctypes.cast(task.session, ctypes.py_object).value.headers)
        async with session.request(task.method, task.url, *task.args, headers=headers, timeout=20, **task.kw) as sessReq:
            assert (sessReq.status == 200) or (sessReq.status == 302)
            content = await sessReq.read()
            new_res = AhttpResponse(sessReq, content, task)
            result.append(new_res)

            if task.callback:
                task.callback(new_res)  # 有回调则调用
            return new_res

    try:
        await _run()
        print(task, 'fetch done。')
    except Exception as err:
        print(task, 'fetch err:', repr(err), flush=True)
        #raise err


async def fetch(task, result, session):
    async def _run(index):
        print(task, index, 'fetch start...')
        headers = wrap_headers(task.headers or ctypes.cast(task.session, ctypes.py_object).value.headers)
        async with session.request(task.method, task.url, headers=headers, *task.args, **task.kw) as sessReq:
            assert sessReq.status in [200, 201, 302]
            content = await sessReq.read()
            new_res = AhttpResponse(sessReq, content, task)
            result.append(new_res)

            if task.callback:
                task.callback(new_res)  # 有回调则调用
            return new_res

    max_try = 10
    index = 0
    while max_try > 0:
        try:
            await _run(index)
            print(task, index, 'fetch done。')
            break
        except Exception as err:
            print(task, index, 'fetch err:', repr(err))
            index += 1
            max_try -= 1
            await asyncio.sleep(0.1)
            continue  # 继续下一轮循环


def ahttpGet(url, params=None, **kwargs):
    task = get(url, params=params, **kwargs)
    res = task.run()
    return res


def ahttpGetAll(urls, pool=100, params=None, **kwargs):
    tasks = [get(url, params=params, **kwargs) for url in urls]
    resps = run(tasks, pool=pool)
    return resps
