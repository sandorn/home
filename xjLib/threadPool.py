# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-16 21:49:56
@LastEditors: Even.Sand
@LastEditTime: 2019-05-21 09:19:41
'''

import threading
import time
from queue import Queue

from bs4 import BeautifulSoup
from xjLib.req import get_stime
from xjLib.req import parse_url as parse_url  # session_url as parse_url
from xjLib.req import savefile as writer

lock = threading.RLock()


class WorkManager(object):
    def __init__(self, do_job, works, thread_num=25):
        self.job = do_job
        self.work_queue = Queue()  # 任务队列
        self.result_queue = Queue()  # 结果队列
        self.threads = []
        self.__init_work_queue(works)
        self.__init_thread_pool(thread_num)

    # #初始化工作队列,添加工作入队
    def __init_work_queue(self, works):
        for item in works:
            # print('__init_work_queue item:', item)  # 参数tupe
            self.work_queue.put((self.job, item))  # 将任务函数和参数传入任务队列

    # #初始化线程,同时运行线程数量有效果，原理没明白
    def __init_thread_pool(self, thread_num):
        for i in range(thread_num):
            self.threads.append(Work(self.work_queue, self.result_queue))

    # #等待所有线程运行完毕
    def wait_allcomplete(self):
        '''
        @description:等待线程结束，并取得运行结果
        @return:result_list
        '''
        for item in self.threads:
            if item.isAlive():
                item.join()

        result_list = []
        for i in range(self.result_queue.qsize()):
            res = self.result_queue.get()
            # print('wait_allcomplete:', res)
            result_list.append(res)
        return result_list


class Work(threading.Thread):
    def __init__(self, work_queue, result_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.start()  # 启动线程

    def run(self):
        # 一定不用死循环
        while not self.work_queue.empty():
            try:
                do, args = self.work_queue.get(block=False)  # 任务异步出队
                # print('Work args：', args)  # 参数list or tupe,注意检查此处
                result = do(*args)  # 传递  list or tupe 各元素
                # print('work run result:', result, flush=True)
                self.result_queue.put(result)  # 取得函数返回值
                self.work_queue.task_done()  # 通知系统任务完成
                with lock:
                    print('{}\tdone\twith\t{}\tat\t{}'.format(threading.currentThread().name, args[0], get_stime()), flush=True)
            except Exception as error:
                print(error, flush=True)
                break


def get_download_url(target):
    _urls = []
    _response = parse_url(target)
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
            _urls.append(download_url)
    return _bookname, _urls


def get_contents(index, url):
    _texts = ''
    _response = parse_url(url)
    _name = _response.h1.get_text()  # 章节名
    _showtext = _response.select('.showtxt')[0]
    for text in _showtext.stripped_strings:
        _texts += text + '\n'
    return (index, _name, _texts)


if __name__ == "__main__":
    start = time.time()
    _name, urls = get_download_url('http://www.biqukan.com//2_2704/')
    args = [(i, urls[i]) for i in range(len(urls))]
    work_manager = WorkManager(get_contents, args)  # 调用函数,参数:list内tupe,线程数量
    texts = work_manager.wait_allcomplete()
    writer(_name + '.txt', texts)
    print("threadPool cost all time: %s" % (time.time() - start), flush=True)
    # '65_65593/'  #章节少，测试用
    # '2_2704'  #231万字  #6239kb,141秒钟
    # "2_2714"   #《武炼巅峰》664万字
    # [武炼巅峰.txt]150W, 用时: 947.34 秒。
