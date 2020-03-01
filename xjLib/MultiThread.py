# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-01 14:55:18
@LastEditors: Even.Sand
@LastEditTime: 2020-03-01 18:56:13
https://blog.csdn.net/Magicapprentice/article/details/71597475?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task
'''

import threading
import time
import multiprocessing
from multiprocessing import Pool


class MyTMultithread(threading.Thread):
    '''
    自定义的线程函数,
    功能:使用多线程运行函数,函数的参数只有一个file,并且未实现结果值的返回
    args:
        filelist   函数的参数为列表格式，
        funname    函数的名字为字符串，函数仅有一个参数为file
        delay      每个线程之间的延迟，
        max_threads 线程的最大值
    '''

    def __init__(self, filelist, delay, funname, max_threads=50):
        threading.Thread.__init__(self)
        self.funname = funname
        self.filelist = filelist[:]
        self.delay = delay
        self.max_threads = max_threads

    def startrun(self):
        def runs():
            time.sleep(self.delay)
            while True:
                try:
                    file = self.filelist.pop()
                except IndexError as e:
                    print(e)
                    break
                else:
                    self.funname(file)

        threads = []
        while threads or self.filelist:
            for thread in threads:
                if not thread.is_alive():
                    threads.remove(thread)
            while len(threads) < self.max_threads and self.filelist:
                thread = threading.Thread(target=runs)
                thread.setDaemon(True)
                thread.start()
                threads.append(thread)


class Mymultiprocessing (MyTMultithread):
    '''
    多进程运行函数，多进程多线程运行函数
    args:
        filelist   函数的参数为列表格式，
        funname    函数的名字为字符串，函数仅有一个参数为file
        delay      每个线程\\进程之间的延迟，
        max_threads 最大的线程数
        max_multiprocess 最大的进程数
    '''

    def __init__(self, filelist, delay, funname, max_multiprocess=1, max_threads=1):
        self.funname = funname
        self.filelist = filelist[:]
        self.delay = delay
        self.max_threads = max_threads
        self.max_multiprocess = max_multiprocess
        self.num_cpus = multiprocessing.cpu_count()

    def multiprocessingOnly(self):
        '''只使用多进程'''
        num_process = min(self.num_cpus, self.max_multiprocess)
        processes = []
        while processes or self.filelist:
            for p in processes:
                if not p.is_alive():
                    # print(p.pid,p.name,len(self.filelist))
                    processes.remove(p)
            while len(processes) < num_process and self.filelist:
                try:
                    file = self.filelist.pop()
                except IndexError as e:
                    print(e)
                    break
                else:
                    p = multiprocessing.Process(target=self.funname, args=(file,))
                    p.start()
                    processes.append(p)

    def multiprocessingThreads(self):
        num_process = min(self.num_cpus, self.max_multiprocess)
        p = Pool(num_process)
        DATALISTS = []
        tempmod = len(self.filelist) % (num_process)
        CD = int((len(self.filelist) + 1 + tempmod) / (num_process))
        for i in range(num_process):
            if i == num_process:
                DATALISTS.append(self.filelist[i * CD:-1])
            DATALISTS.append(self.filelist[(i * CD):((i + 1) * CD)])

        try:
            processes = []
            for i in range(num_process):
                # print('wait add process:',i+1,time.clock())
                # print(eval(self.funname),DATALISTS[i])
                MultThread = MyTMultithread(DATALISTS[i], self.delay, self.funname, self.max_threads)

                p = multiprocessing.Process(target=MultThread.startrun())
                # print('pid & name:',p.pid,p.name)
                processes.append(p)
            for p in processes:
                print('wait join ')
                p.start()
            print('waite over')
        except Exception as e:
            print('error :', e)
        print('end process')


def func1(file):
    print(file)


if __name__ == '__main__':
    a = list(range(0, 97))
    '''
    测试使用5线程
    '''
    st = time.clock()
    asc = MyTMultithread(a, 0, 'func1', 5)
    asc.startrun()
    end = time.clock()
    print('*' * 50)
    print('多线程使用时间:', end - st)
    # 测试使用5个进程
    st = time.clock()
    asd = Mymultiprocessing(a, 0, 'func1', 5)
    asd.multiprocessingOnly()
    end = time.clock()
    print('*' * 50)
    print('多进程使用时间:', end - st)

    # 测试使用5进程10线程
    st = time.clock()
    multiPT = Mymultiprocessing(a, 0, 'func1', 5, 10)
    multiPT.multiprocessingThreads()
    end = time.clock()
    print('*' * 50)
    print('多进程多线程使用时间:', end - st)
