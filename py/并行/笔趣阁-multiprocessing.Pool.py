# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Descripttion: 使用multiprocessing.pool多进程
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@LastEditors: Even.Sand
@Date: 2019-05-08 18:31:14
@LastEditTime: 2019-05-25 18:07:54
努努书坊 - 小说在线阅读   https://www.kanunu8.com/
'''

import time
import multiprocessing
from bs4 import BeautifulSoup
from xjLib.req import parse_url as parse_url
from xjLib.req import savefile as writer
from xjLib.req import get_stime


def get_download_url(target):
    url_list = []
    response = parse_url(target)
    _response = BeautifulSoup(response.content, 'lxml')
    [s.extract() for s in _response(["script", "style"])]
    _bookname = _response.find('h2').get_text()
    # 搜索文档树,找出div标签中class为listmain的所有子标签
    _div = str(_response.find_all('div', class_='listmain')[0])
    download_soup = BeautifulSoup(_div, features="html5lib")

    # 开始记录内容标志位,只要正文卷下面的链接,最新章节列表链接剔除
    begin_flag = False

    # 遍历 dl 标签下所有子节点
    for child in download_soup.dl.children:
        # 找到正文卷,使能标志位
        if child.string.strip() == '《' + _bookname + '》正文卷':
            begin_flag = True
        # 爬取链接并下载链接内容
        if begin_flag and child.name == 'dd':
            download_url = 'http://www.biqukan.com/' + child.find('a').get('href')
            url_list.append(download_url)
    return _bookname, url_list


def get_contents(lock, index, target):
    _texts = ''
    response = parse_url(target)
    _response = BeautifulSoup(response.content, 'lxml')
    [s.extract() for s in _response(["script", "style"])]
    _name = _response.h1.get_text()  # 章节名
    _showtext = _response.select('.showtxt')[0]
    for text in _showtext.stripped_strings:
        _texts += text + '\n'

    with lock:
        print('{} done with {} at {}'.format(multiprocessing.current_process().name, index, get_stime()), flush=True)
    return [index, _name, _texts]


def main_Pool(target):
    _stime = time.time()
    # 父进程创建Queue\lock，传给个子进程：
    lock = multiprocessing.Manager().Lock()

    print('开始下载：《{}》\t{}\t获取下载链接......'.format(target, get_stime()), flush=True)
    bookname, urls = get_download_url(target)
    print('multiprocessing.pool，开始下载：《' + bookname + '》', flush=True)
    mypool = multiprocessing.Pool(25)  # !进程数
    # 创建多进程队列
    future_tasks = []
    for i in range(len(urls)):
        item = mypool.apply_async(get_contents, args=(lock, i, urls[i]))
        # pool.apply_async(func=task,callback=_callba)
        future_tasks.append(item)
    mypool.close()  # 关闭进程池,不再接受请求
    mypool.join()  # 等待进程池中的事件执行完毕，回收进程池

    texts = []  # 将爬下来的小说都存在里面
    for i, item in enumerate(future_tasks):
        _text = item.get()  # join后获取进程返回值
        texts.append(_text)

    print('\n multiprocessing.pool，书籍《' + bookname + '》完成下载', flush=True)
    writer(bookname + '.txt', texts)
    print('{} 结束，\t用时:{} 秒。'.format(get_stime(), round(time.time() - _stime, 2)), flush=True)


if __name__ == '__main__':
    main_Pool('https://www.biqukan.com/2_2704/')

# 本人电脑用时约70秒，6239KB
