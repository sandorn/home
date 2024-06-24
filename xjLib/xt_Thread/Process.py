# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-31 11:36:53
LastEditTime : 2024-06-20 15:16:31
FilePath     : /CODE/xjLib/xt_Thread/Process.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from multiprocessing import Manager, Process, Semaphore


class CustomProcess(Process):
    """多进程,继承自multiprocessing.Process,用Manager返回结果"""

    all_Process = []  # 类属性或类变量,实例公用

    def __init__(self, result_dict, semaphore, fn, *args, **kwargs):
        super().__init__()
        self.result_dict = result_dict
        self.index = len(self.all_Process)
        self.semaphore = semaphore  # @有问题，进程太多导致电脑卡死
        self.daemon = True
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.start()
        self.all_Process.append(self)

    def run(self):
        # print(f'Pid: {os.getpid()} \t|\t {multiprocessing.current_process()}|{self.pid}|{self.name}')
        with self.semaphore:  # @有问题，进程太多导致电脑卡死
            self.result_dict[self.pid] = self.fn(*self.args, **self.kwargs)

    @classmethod
    def wait_completed(cls):
        """等待全部线程结束,返回结果"""
        while cls.all_Process:
            prc = cls.all_Process.pop()
            prc.join()


def Do_CustomProcess(fn, *args, **kwargs):
    """调用CustomProcess,Manager.dict()返回结果"""
    max_processes = 3  # 同时运行的进程数量
    semaphore = Semaphore(max_processes)
    return_dict = Manager().dict()
    for args_iter in list(zip(*args)):
        CustomProcess(return_dict, semaphore, fn, *args_iter, **kwargs)
    CustomProcess.wait_completed()
    return return_dict.values()
