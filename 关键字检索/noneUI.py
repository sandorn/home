# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@LastEditors: Even.Sand
@Date: 2019-05-08 19:18:48
@LastEditTime: 2019-05-24 00:05:40
'''
import os
import time
import threading
from pyquery import PyQuery
from concurrent.futures import ThreadPoolExecutor    # 线程池模块
from concurrent.futures import as_completed
from xjLib.req import get_stime
from xjLib.req import parse_url

lock = threading.RLock()


def make_urls(_file, pages):
    _k = []
    _file = os.path.dirname(__file__) + "/" + _file
    with open(_file) as f:
        for row in f.readlines():
            row = row.strip()  # 默认删除空白符  #  '#^\s*$'
            if len(row) == 0:
                continue  # len为0的行,跳出本次循环
            _k.append(row)
    keys = sorted(set(_k), key=_k.index)
    out_url = [(key, page, "https://www.baidu.com/s?wd={}&pn={}".format(key, page * 10)) for key in keys for page in range(pages)]
    return out_url


def getkeys(target):
    (key, page, url) = target
    _texts = []
    response = parse_url(url=url)
    result = PyQuery(response.text)  # content.decode('uft-8')

    index = 0
    for each in result("h3 a").items():
        # #获取显示字符和网页链接
        index += 1
        href = each.attr('href')
        title = each.text()

        # # 剔除百度自营内容
        if '百度' in title:
            continue
        if not href.startswith('http'):
            continue

        # #获取真实网址
        baidu_url = parse_url(url=href, allow_redirects=False)
        real_url = baidu_url.headers['Location']  # 得到网页原始地址
        if '.baidu.com' in real_url:
            continue
        if real_url.startswith('http'):
            _texts.append([key, page, index, title, real_url])
    with lock:
        print('{}\tdone\twith\t{}\tat\t{}'.format(threading.currentThread().name, key, get_stime()), flush=True)
    return _texts


def savefile(_filename, lists):
    # 函数说明:将爬取的文章lists写入文件
    print('[' + _filename + ']开始保存......', end='', flush=True)
    lists.sort()

    with open(_filename, 'a', encoding='utf-8') as f:
        f.write('key' + '\tpage' + '\tindex' + '\ttitle' + '\turl' + '\n')
        for lists_line in lists:
            for index, item in enumerate(lists_line):
                f.write(item[0] + '\t' + str(item[1]) + '\t' + str(item[2]) + '\t' + item[3] + '\t' + item[4] + '\n')

    print('[' + _filename + ']保存完成。', flush=True)


def main():
    start = time.time()
    texts = []  # 用于存放结果
    _file = "关键词 (015).txt"
    _name = _file.split('.')[0]  # 文件名，含完整路径，去掉后缀

    try:
        urls = make_urls(_file, 1)
    except Exception as e:
        print(e)
        return False

    with ThreadPoolExecutor(20) as p:
        future_tasks = [p.submit(getkeys, url) for url in urls]
        thread_results = [task.result() for task in as_completed(future_tasks)]
        texts = [item for item in thread_results if item != '']

    savefile(_name + '_百度词频.txt', texts)
    print("threadPool cost all time: %s 秒" % (time.time() - start), flush=True)


if __name__ == "__main__":
    main()
