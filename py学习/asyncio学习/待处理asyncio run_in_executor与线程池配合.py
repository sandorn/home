# !/usr/bin/env python
"""
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-03 13:34:20
LastEditors  : Please set LastEditors
LastEditTime : 2021-03-15 16:33:55
"""

# 使用多线程：在协程中集成阻塞io
import asyncio
from concurrent.futures import ThreadPoolExecutor

from xt_file import savefile
from xt_requests import get_parse as parse_get
from xt_str import Re_Sub as Ex_Re_Sub


def get_url(target):
    urls = []  # 存放章节链接
    resp = parse_get(target)
    response = resp.html

    _bookname = response.xpath("//h2/text()", first=True)[0]
    全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = "https://www.biqukan.com" + item
        urls.append(_ZJHERF)
    return _bookname, urls


def get_contents(target):
    resp = parse_get(target)
    response = resp.html

    _name = response.xpath("//h1/text()", first=True)[0]
    _showtext = "".join(response.xpath('//*[@id="content"]/text()'))

    name = Ex_Re_Sub(_name, {"'": "", " ": " "})
    text = Ex_Re_Sub(_showtext, {"'": "", " ": " ", "\b;": "\n", "&nbsp;": " ", "app2();": "", "笔趣看;": "", "\u3000": "", "chaptererror();": "", "readtype!=2&&('vipchapter\n(';\n\n}": "", "m.biqukan.com": "", "wap.biqukan.com": "", "www.biqukan.com": "", "www.biqukan.com。": "", "百度搜索“笔趣看小说网”手机阅读:": "", "请记住本书首发域名:": "", "请记住本书首发域名：": "", "笔趣阁手机版阅读网址:": "", "笔趣阁手机版阅读网址：": "", "[]": "", "\r": "\n", "\n\n": "\n"})

    return [name, "    " + text]


if __name__ == "__main__":
    import time

    start_time = time.time()
    new_loop = asyncio.new_event_loop()
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(100)
    tasks = []
    urls = [
        "https://www.biqukan.com/38_38836/",
        # 'https://www.biqukan.com/0_790/',
        "https://www.biqukan.com/10_10736/",
        "https://www.biqukan.com/2_2714/",
    ]
    for url in urls:
        task = loop.run_in_executor(executor, get_url, url)
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))

    text = {}
    new_tasks = {}

    for index in range(len(tasks)):
        _bookname, url_list = tasks[index].result()
        print(_bookname, len(url_list))
        text[_bookname] = []
        new_tasks[_bookname] = []

        for url in url_list:
            task2 = loop.run_in_executor(executor, get_contents, url)
            new_tasks[_bookname].append(task2)
        loop.run_until_complete(asyncio.wait(new_tasks[_bookname]))

        for i in range(len(new_tasks[_bookname])):
            nameandtext = new_tasks[_bookname][i].result()
            text[_bookname].append(nameandtext)
        savefile(_bookname + ".txt", text[_bookname], br="\n")
    # 沧元图 734
    # [沧元图.txt]保存完成,	file size: 5317.39 KB。
    # 九星霸体诀 4221
    # [九星霸体诀.txt]保存完成,	file size: 33.80 MB。
    # 武炼巅峰 5821
    # [武炼巅峰.txt]保存完成,	file size: 50.39 MB。
"""
# asyncio run_in_executor与线程池配合_Python_mixintu的博客-CSDN博客
# https://blog.csdn.net/mixintu/article/details/102472276
def get_url(url):
    # 通过socket请求html
    url = urlparse(url)
    host = url.netloc
    path = url.path
    if path == "":
        path = "/"

    # 建立socket连接
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client.setblocking(False)
    client.connect((host, 80))  # 阻塞不会消耗cpu

    # 不停的询问连接是否建立好， 需要while循环不停的去检查状态
    # 做计算任务或者再次发起其他的连接请求

    client.send(
        "GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n".format(path, host).encode("utf8"))

    data = b""
    while True:
        d = client.recv(1024)
        if d:
            data += d
        else:
            break

    data = data.decode("utf8")
    html_data = data.split("\r\n\r\n")[1]
    print(html_data)
    client.close()


if __name__ == "__main__":
    import time
    start_time = time.time()
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(3)
    tasks = []
    for url in range(20):
        url = "http://shop.projectsedu.com/goods/{}/".format(url)
        # 返回 task
        task = loop.run_in_executor(executor, get_url, url)
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))
    print("last time:{}".format(time.time()-start_time))
"""
