# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-02-29 23:00:26
@LastEditors: Even.Sand
@LastEditTime: 2020-03-03 23:03:07
https://blog.csdn.net/ksws0393238aa/article/details/20286405?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task
'''

import time
from threading import Thread

from lxml import etree
from xjLib.mystr import Ex_Re_Sub, get_stime, savefile
from xjLib.req import parse_get
import ahttp
sess = ahttp.Session()
texts = []  # 将爬下来的小说存列表list，做最后排序


class myThread(Thread):
    # 每创建一个线程就加入到数组中，方便日后调用
    all_Thread = []
    # 初始化线程，可以将function函数所需要的参数在初始化thread过程中加入到thread属性

    def __init__(self, thread_name, parameter):
        Thread.__init__(self, name=thread_name)
        # 暂时将function所需要的参数放在thread属性中
        self.parameter = parameter
        # 添加一个标识符，指示线程是否在进行
        self.isRunning = True
        myThread.all_Thread.append(self)

    def run(self):
        # 重写run函数，function为想要调用的函数
        # 此时function的参数可以从self.parameter中拿出来使用
        self.res = function(self.parameter)

    def getResult(self):
        try:
            return self.res
        except Exception:
            return None

    def stop(self):
        # 结束线程的标识符
        self.isRunning = False


def function(parameter):
    """以下为需要重复的单次函数操作"""
    (index, target) = parameter
    response = etree.HTML(parse_get(target).content)
    _name = response.xpath('//h1/text()')[0]
    _showtext = "".join(response.xpath('//*[@id="content"]/text()'))
    print('{}\tdone\tat\t{}'.format(index, get_stime()))
    return [index, _name, _showtext]
    '''
    # 以下为可选内容，通常线程会自动结束
    for thread in myThread.all_Thread:
        if thread.name == name:
            print(name)
            thread.stop()
            myThread.all_Thread.remove(thread)
    '''


def get_download_url(target):
    urls = []  # 存放章节链接
    response = etree.HTML(parse_get(target).content)
    _bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


def callback(future):
    index, _name, _showtext = future  # 回调函数取得返回值
    name = Ex_Re_Sub(_name, {'\'': '', ' ': ' ', '\xa0': ' ', })

    text = Ex_Re_Sub(
        _showtext,
        {
            '\'': '',
            ' ': ' ',
            '\xa0': ' ',
            '\x0a': '\n',
            # '\b;': '\n',
            '&nbsp;': ' ',
            'app2();': '',
            '笔趣看;': '',
            '\u3000': '',
            'chaptererror();': '',
            'readtype!=2&&(\'vipchapter\n(\';\n\n}': '',
            'm.biqukan.com': '',
            'wap.biqukan.com': '',
            'www.biqukan.com': '',
            'www.biqukan.com。': '',
            '百度搜索“笔趣看小说网”手机阅读:': '',
            '请记住本书首发域名:': '',
            '请记住本书首发域名：': '',
            '笔趣阁手机版阅读网址:': '',
            '笔趣阁手机版阅读网址：': '',
            '[]': '',
            '\r': '\n',
            '\n\n': '\n',
            '\n\n': '\n',
        }
    )
    texts.append([index, name, text])


def main_thread(target):
    _stime = time.time()
    bookname, urls = get_download_url(target)
    thread_list = []
    print('threading-继承，开始下载：《' + bookname + '》', flush=True)
    print(urls)
    for index in range(len(urls)):
        res = myThread("线程名:get_text", (index, urls[index]))
        res.start()
        thread_list.append(res)

    for item in thread_list:
        item.join()  # join等待线程执行结束
        back = item.getResult()  # 获取线程结果
        callback(back)

    print('threading-继承，书籍《' + bookname + '》完成下载', flush=True)

    texts.sort(key=lambda x: x[0])
    savefile(bookname + '.txt', texts)
    print('下载《{}》完成，用时:{} 秒。'.format(bookname, round(time.time() - _stime, 2)), flush=True)


if __name__ == '__main__':
    # #from xjLib.log import log
    # #log = log()
    main_thread('https://www.biqukan.com/76_76572/')
    # '65_65593'  #章节少134万字，3573kb,, 22秒
    # '2_2704'  #77万字, 2018kb, 34秒
    # "2_2714"   #《武炼巅峰》1724万字,47839kb, 211秒。30线程
    # "2_2714"   #《武炼巅峰》1724万字,47839kb, #!77秒。100线程
    # '0_790'    #《元尊》328万字， 8988KB， 45秒钟
