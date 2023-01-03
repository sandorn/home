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
from multiprocessing import Manager, Process

# from xt_Thread import Singleton_Mixin


class MyProcess(Process):
    '''多进程,继承自multiprocessing.Process,无结果返回'''

    all_Process = []  # 类属性或类变量,实例公用
    result_list = []  # 类属性或类变量,实例公用

    def __init__(self, func, *args, **kwargs):
        super(MyProcess, self).__init__()
        self.index = len(self.all_Process)
        self.daemon = True
        self.target = func
        self.args = args
        self.kwargs = kwargs
        self.start()
        self.all_Process.append(self)

    def run(self) -> None:
        # print(f'Parent Pid:{os.getppid()} | Pid: {self.pid} | ProcessName: {self.name}')
        self.Result = self.target(*self.args, **self.kwargs)
        self.result_list.append(self.Result)

    def stop_all(self):
        """停止线程池, 所有线程停止工作"""
        for _ in range(len(self.all_Process)):
            prc = self.all_Process.pop()
            prc.join()

    @classmethod
    def wait_completed(cls):
        """等待全部线程结束,返回结果"""
        cls.stop_all(cls)


class SingletonProcess(Process):
    """单例多进程,继承自multiprocessing.Process
    ,可取运行结果"""

    all_Process = []  # 类属性或类变量,实例公用
    result_list = []  # 类属性或类变量,实例公用

    def __init__(self, target, *args, **kwargs):
        super().__init__(target=target, args=args, kwargs=kwargs)
        self.index = len(self.all_Process)
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self.daemon = True
        self.run()
        self.all_Process.append(self)

    def run(self):
        # print(f'Parent Pid:{os.getppid()} | Pid: {os.getpid()} | ProcessName: {self.name}')
        self.Result = self._target(*self._args, **self._kwargs)
        self.result_list.append(self.Result)

    @classmethod
    def wait_completed(cls):
        """等待全部线程结束,返回结果"""
        for _ in range(len(cls.all_Process)):
            cls.all_Process.pop()
        res, cls.result_list = cls.result_list, []
        return res


class CustomProcess(Process):
    """多进程,继承自multiprocessing.Process,用Manager.Queue()返回结果"""

    all_Process = []  # 类属性或类变量,实例公用

    def __init__(self, return_dict, target, *args, **kwargs):
        super().__init__()
        self.return_dict = return_dict
        self.index = len(self.all_Process)
        self.daemon = True
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.start()
        self.all_Process.append(self)

    def run(self):
        # print(f'Parent Pid:{os.getppid()} | Pid: {self.pid} | ProcessName: {self.name}')
        self.Result = self.target(*self.args, **self.kwargs)
        self.return_dict[self.pid] = self.Result

    @classmethod
    def wait_completed(cls):
        """等待全部线程结束,返回结果"""
        for _ in range(len(cls.all_Process)):
            prc = cls.all_Process.pop()
            prc.join()


def Do_CustomProcess(func, *args, **kwargs):
    '''调用CustomProcess,Manager.dict()返回结果'''
    return_dict = Manager().dict()
    tt = [CustomProcess(return_dict, func, *args_iter, **kwargs) for args_iter in list(zip(*args))]
    CustomProcess.wait_completed()
    return list(return_dict.values())


if __name__ == '__main__':
    from multiprocessing import Pool

    from xt_File import savefile
    from xt_Ls_Bqg import get_biqugse_download_url, get_contents

    def Custom():
        url = 'http://www.biqugse.com/96703/'
        bookname, urls, titles = Do_CustomProcess(get_biqugse_download_url, [url])[0]
        res_list = Do_CustomProcess(get_contents, list(range(len(urls))), urls)
        res_list.sort(key=lambda x: x[0])  # #排序
        files = os.path.split(__file__)[-1].split(".")[0]
        savefile(f'{files}&{bookname}&Do_CustomProcess.txt', res_list, br='\n')

    # Custom()  # 用时: 70s

    def Singleton():
        url = 'http://www.biqugse.com/96703/'
        r = SingletonProcess(get_biqugse_download_url, url)
        bookname, urls, _ = r.wait_completed()[0]
        prc_list = [SingletonProcess(get_contents, index, urls[index]) for index in range(len(urls))]
        res_list = SingletonProcess.wait_completed()
        res_list.sort(key=lambda x: x[0])  # #排序
        files = os.path.split(__file__)[-1].split(".")[0]
        savefile(f'{files}&{bookname}&Do_CustomProcess.txt', res_list, br='\n')

    # Singleton()  # 用时: 102s

    def Poolapply_async():
        url = 'http://www.biqugse.com/96703/'
        bookname, urls, titles = Do_CustomProcess(get_biqugse_download_url, [url])[0]

        p = Pool(24)  # 进程池中从无到有创建三个进程,以后一直是这三个进程在执行任务
        res_l = []
        for i, url in enumerate(urls):
            res = p.apply_async(get_contents, args=(i, url))  # 异步执行任务
            res_l.append(res)
        p.close()
        p.join()
        res_list = [res.get() for res in res_l]
        res_list.sort(key=lambda x: x[0])  # #排序
        # aftertexts = [[row[i] for i in range(1, 3)] for row in texts]
        files = os.path.split(__file__)[-1].split(".")[0]
        savefile(f'{files}&{bookname}&Poolapply_async.txt', res_list, br='\n')

    # Poolapply_async()  # 用时: 19s
