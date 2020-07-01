# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-30 15:52:34
#FilePath     : /项目包/百度关键字/单一文件控制台执行.py
#LastEditTime : 2020-06-30 16:33:06
#Github       : https://github.com/sandorn/home
#==============================================================
'''
# ！/usr/bin/env python
# -*- coding:utf -8-*-

import time
from retrying import retry
import requests
from bs4 import BeautifulSoup
import threading
from queue import Queue

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
            item.join()

        result_list = []
        for i in range(self.result_queue.qsize()):
            res = self.result_queue.get()
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
                    print('{}\tdone\twith\t{}\tat\t{}'.format(
                        threading.currentThread().name, args[0], get_stime()))
            except Exception as error:
                print(error, flush=True)
                break


def get_stime():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    stamp = "%s.%03d" % (data_head, data_secs)
    return stamp


myhead = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate,sdch, br',
    'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'close',
    'Proxy-Connection': 'no-cache'
}


def parse_url(url,
              params=None,
              headers=myhead,
              proxies=None,
              timeout=6,
              ecode='utf-8',
              wait_random_min=200,
              wait_random_max=3000,
              stop_max_attempt_number=100):
    @retry(wait_random_min=wait_random_min,
           wait_random_max=wait_random_max,
           stop_max_attempt_number=stop_max_attempt_number)
    def _parse_url(url):
        response = requests.get(url,
                                params=params,
                                headers=headers,
                                proxies=proxies,
                                timeout=timeout)
        assert response.status_code == 200
        return response.content.decode(ecode)

    try:
        response = _parse_url(url)
        soup = BeautifulSoup(response, 'lxml')
        [s.extract() for s in soup(["script", "style"])]
    except requests.exceptions.ConnectionError as e:
        print('ConnectionError:', e, url, flush=True)
        soup = None
    except requests.exceptions.ChunkedEncodingError as e:
        print('ChunkedEncodingError:', e, url, flush=True)
        soup = None
    except Exception as e:
        print('Unfortunitely Unknow Error:', e, url, flush=True)
        soup = None
    return soup


def fd():
    import win32ui
    _dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
    _dlg.SetOFNInitialDir('c:/')  # 设置打开文件对话框中的初始显示目录
    _dlg.DoModal()
    filename = _dlg.GetPathName()  # 获取选择的文件名称
    return filename


def make_urls(pages):
    '''
    _k = []
    _file = fd()
    if not _file:
        return False
    res = _file.split('.')[0:-1]  # 文件名，含完整路径，去掉后缀
    with open(_file) as f:
        for row in f.readlines():
            row = row.strip()  # 默认删除空白符  '#^\s*$'
            if len(row) == 0:
                break  # 去除行len为0的行
            _k.append(row)
    keys = sorted(set(_k), key=_k.index)
    #为方便演示，用list直接替代读文件
    '''
    keys = [
        "减肥计划", "减肥运动", "如何减肥", "怎么减肥", "有效减肥", "郑多燕减肥", "减肥视频", "减肥", "减肥方法",
        "减肥食谱", "   ", "减肚子", "腰腹减肥", "\t", "减腰", "减肥法", "减肥法"
    ]
    keys = ['健身']
    out_url = [(
        key,
        page,
        "https://www.baidu.com/s?wd={}&pn={}".format(key, page * 10),
    ) for key in keys for page in range(pages)]
    return 'baidu', out_url
    # return res[0], out_url


def getkeys(key, page, url):
    _texts = []
    result = parse_url(url=url)
    '''
    #方法1
    tagh3 = result.find_all('h3')
    index = 0
    for h3 in tagh3:
        href = h3.find('a').get('href')
        title = h3.find('a').text
        if '百度' in title:
            break
        if not href.startswith('http'):
            break
        baidu_url = requests.get(url=href, headers=myhead, allow_redirects=False)  # 禁止跳转
        real_url = baidu_url.headers['Location']  # 得到网页原始地址
        if real_url.startswith('http'):
            index += 1
            _texts.append([index, title, real_url])
    #方法1结束
    '''

    # 方法2，效果与方法1相同
    allTags = result.findAll(
        'div', ['result-op c-container xpath-log', 'result c-container'])
    # 'result-op c-container xpath-log'   #百度自己内容
    index = 0
    for tag in allTags:
        href = tag.h3.a['href']
        title = tag.h3.a.text
        if '百度' in title:
            break
        if not href.startswith('http'):
            break
        baidu_url = requests.get(url=href,
                                 headers=myhead,
                                 allow_redirects=False)
        real_url = baidu_url.headers['Location']  # 得到网页原始地址
        if real_url.startswith('http'):
            index += 1
            _texts.append([key, page, index, title, real_url])
    # 方法2结束

    return _texts


def savefile(_filename, lists):
    # 函数说明:将爬取的文章lists写入文件
    print('[' + _filename + ']开始保存......', end='', flush=True)
    lists.sort()

    with open(_filename, 'a', encoding='utf-8') as f:
        f.seek(0)
        f.truncate()
        for lists_line in lists:
            for index, item in enumerate(lists_line):
                f.write('key:' + item[0] + '\tpage:' + str(item[1]) +
                        '\tindex:' + str(item[2]) + '\ttitle:' + item[3] +
                        '\turl:' + item[4] + '\n')

    print('[' + _filename + ']保存完成。', flush=True)


def main():
    start = time.time()
    try:
        _name, urls = make_urls(10)
    except Exception as e:
        print(e)
        return False

    work_manager = WorkManager(getkeys, urls)  # 调用函数,参数:list内tupe,线程数量
    texts = work_manager.wait_allcomplete()
    savefile(_name + '_百度词频.txt', texts)
    print("threadPool cost all time: %s" % (time.time() - start), flush=True)


if __name__ == "__main__":
    main()
    # threadPool cost all time: 27.787729501724243
