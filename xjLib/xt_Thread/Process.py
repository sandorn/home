# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-31 11:36:53
LastEditTime : 2022-12-31 11:40:09
FilePath     : /xjLib/xt_Thread/Process.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import os
from multiprocessing import Manager, Process, Semaphore


class CustomProcess(Process):
    """多进程,继承自multiprocessing.Process,用Manager返回结果"""

    all_Process = []  # 类属性或类变量,实例公用

    def __init__(self, result_dict, sem, target, *args, **kwargs):
        super().__init__()
        self.result_dict = result_dict
        self.index = len(self.all_Process)
        self.daemon = True
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.sem = sem
        self.start()
        self.all_Process.append(self)

    def run(self):
        # print(f'Pid: {os.getpid()} \t|\t {multiprocessing.current_process()}|{self.pid}|{self.name}')
        with self.sem:
            self.result_dict[self.pid] = self.target(*self.args, **self.kwargs)

    @classmethod
    def wait_completed(cls):
        """等待全部线程结束,返回结果"""
        while cls.all_Process:
            prc = cls.all_Process.pop()
            prc.join()


def Do_CustomProcess(func, *args, **kwargs):
    '''调用CustomProcess,Manager.dict()返回结果'''
    sem = Semaphore(24)
    return_dict = Manager().dict()
    # Create the list of CustomProcess objects
    tt = [
        CustomProcess(return_dict, sem, func, *args_iter, **kwargs)
        for args_iter in list(zip(*args))
    ]
    # Wait until all the processes have completed
    CustomProcess.wait_completed()
    # Return the values from the Manager dict
    return return_dict.values()


if __name__ == '__main__':

    from xt_File import savefile
    from xt_Ls_Bqg import get_contents, get_download_url

    def Custom():
        url = 'https://www.biqukan8.cc/0_288/'
        bookname, urls, titles = Do_CustomProcess(get_download_url, [url])[0]
        res_list = Do_CustomProcess(get_contents, list(range(10)), urls[:10])
        res_list.sort(key=lambda x: x[0])  # #排序
        files = os.path.split(__file__)[-1].split(".")[0]
        savefile(f'{files}&{bookname}&Do_CustomProcess.txt', res_list, br='\n')

    Custom()  # 用时: 14s[10]

    def Poolapply_async():
        from multiprocessing import Pool
        url = 'https://www.biqukan8.cc/0_288/'
        bookname, urls, titles = Do_CustomProcess(get_download_url, [url])[0]

        p = Pool(32)  # 进程池中从无到有创建三个进程,以后一直是这三个进程在执行任务
        res_l = []

        for i, url in enumerate(urls[:10]):
            res = p.apply_async(get_contents, args=(i, url))  # 异步执行任务
            res_l.append(res)
        p.close()
        p.join()
        res_list = [res.get() for res in res_l]
        res_list.sort(key=lambda x: x[0])  # #排序
        # aftertexts = [[row[i] for i in range(1, 3)] for row in texts]
        files = os.path.split(__file__)[-1].split(".")[0]
        savefile(f'{files}&{bookname}&Poolapply_async.txt', res_list, br='\n')

    # Poolapply_async()  # 用时: 29s[10] 60s
