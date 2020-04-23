# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-04-16 13:57:50
@LastEditors: Even.Sand
@LastEditTime: 2020-04-23 18:41:08
'''

import os
import asyncio
import ctypes
import json
import random
from functools import partial
from html import unescape

import aiohttp
from cchardet import detect
from fake_useragent import UserAgent
from lxml import etree

from xjLib.mystr import Ex_Re_Sub, Ex_Replace, savefile

# from retrying import retry

__all__ = ('map', 'Session', 'get', 'options', 'head', 'post', 'put', 'patch',
           'delete')

myhead = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':
        'gzip, deflate, sdch',
    'Accept-Language':
        'zh-CN,zh;q=0.9,en-US;q=0.6,en;q=0.4',
    'Accept-Charset':
        'gb2312,utf-8;q=0.7,*;q=0.7',
    'Connection':
        'close',
}


class Session:

    def __init__(self, *args, **kwargs):
        self.session = self
        self.headers = myhead
        self.cookies = {}
        self.request_pool = []

    def __getattr__(self, name):
        if name in ['get', 'options', 'head', 'post', 'put', 'patch', 'delete']:
            new_req = AsyncRequestTask(
                headers=self.headers, session=self.session)
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
        future = asyncio.ensure_future(AyTask_run(self))
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
    session = Session()
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


async def AyTask_run(self):
    # #单个任务，从task.run()调用
    async def _run():
        async with aiohttp.ClientSession(cookies=self.cookies) as session:
            async with session.request(
                    self.method,
                    self.url,
                    *self.args,
                    verify_ssl=False,
                    headers=wrap_headers(self.headers or self.session.headers),
                    **self.kw) as sessReq:
                content = await sessReq.read()
                self.result, self.content, self.index = sessReq, content, id(
                    self.result)

    max_try = 10
    index = 0
    while max_try > 0:
        try:
            await _run()
            print(f'{self}\ttimes:{index}\tAyTask Done.')
            break
        except Exception as err:
            warn(f'{self}\ttimes:{index}\tAyTask Err:{ repr(err)}')
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
    def session(self):
        return self.task.session

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
                control_sem(task, result, sion_list[id(task.session)])))

    await asyncio.wait(new_tasks)
    await asyncio.wait(
        [asyncio.ensure_future(v.close()) for k, v in sion_list.items()])
    await conn.close()  # 关闭tcp连接器


async def control_sem(task, result, session):
    # !使用信号量限制并发数
    maxsem = asyncio.Semaphore(task.pool)
    async with maxsem:
        await fetch_async(task, result, session)


async def fetch_async(task, result, session):

    async def _run():
        headers = wrap_headers(
            task.headers or
            ctypes.cast(task.session, ctypes.py_object).value.headers)
        async with session.request(
                task.method, task.url, headers=headers, *task.args,
                **task.kw) as sessReq:
            assert sessReq.status in [200, 201, 302]
            content = await sessReq.read()
            new_res = AhttpResponse(sessReq, content, task)
            result.append(new_res)

            if task.callback:
                task.callback(new_res)  # 有回调则调用
            return new_res

    max_try = 10
    maxsave = max_try
    while max_try > 0:
        try:
            await _run()
            print(f'{task}\ttimes:{maxsave - max_try}\tFetch_async Done.')
            break
        except Exception as err:
            warn(
                f'{task}\ttimes:{maxsave - max_try}\tFetch_async Err:{repr(err)}'
            )
            max_try -= 1
            await asyncio.sleep(random.random())
            continue  # 继续下一轮循环


def ahttpGet(url, params=None, **kwargs):
    task = get(url, params=params, **kwargs)
    res = task.run()
    return res


def ahttpGetAll(urls, pool=100, params=None, **kwargs):
    tasks = [get(url, params=params, **kwargs) for url in urls]
    resps = run(tasks, pool=pool)
    return resps


def get_download_url(target):
    urls = []  # 存放章节链接
    # response = etree.HTML(parse_get(target).content)
    resp = ahttpGet(target)
    response = resp.html
    _bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = response.xpath(
        '//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


def 结果处理(resps):
    texts = []
    for resp in resps:
        index = resp.index
        response = resp.html

        _name = "".join(response.xpath('//h1/text()'))
        _showtext = "".join(response.xpath('//*[@id="content"]/text()'))
        name = Ex_Re_Sub(_name, {' ': ' ', '\xa0': ' '})
        text = Ex_Replace(
            _showtext.strip("\n\r　  "),
            {
                '　　': '\n',
                ' ': ' ',
                '\', \'': '',
                # '\xa0': '',  # 表示空格  &nbsp;
                '\u3000': '',  # 全角空格
                'www.biqukan.com。': '',
                'm.biqukan.com': '',
                'wap.biqukan.com': '',
                'www.biqukan.com': '',
                '笔趣看;': '',
                '百度搜索“笔趣看小说网”手机阅读:': '',
                '请记住本书首发域名:': '',
                '请记住本书首发域名：': '',
                '笔趣阁手机版阅读网址:': '',
                '笔趣阁手机版阅读网址：': '',
                '[]': '',
                '<br />': '',
                '\r\r': '\n',
                '\r': '\n',
                '\n\n': '\n',
                '\n\n': '\n',
            },
        )
        texts.append([index, name, '    ' + text])

    return texts


def main(url):
    bookname, urls = get_download_url(url)
    resps = ahttpGetAll(urls, pool=200)

    texts = 结果处理(resps)

    texts.sort(key=lambda x: x[0])  # #排序
    aftertexts = [[row[i] for i in range(1, 3)] for row in texts]
    # @重新梳理数据，剔除序号
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'main.txt', aftertexts, br='\n')


def threadpool(urls):
    from concurrent.futures import ThreadPoolExecutor
    executor = ThreadPoolExecutor(max_workers=3)
    for data in executor.map(main, urls):
        print("map2 in main: get page {}s success".format(data))


from xjLib.log import MyLog
log = MyLog(__name__)
print = log.print
warn = log.warn

if __name__ == "__main__":
    urls = [
        'https://www.biqukan.com/38_38836/',
        'https://www.biqukan.com/2_2714/',
    ]

    threadpool(urls)
