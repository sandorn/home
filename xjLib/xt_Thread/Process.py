# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-31 11:36:53
LastEditTime : 2024-06-16 02:17:27
FilePath     : /CODE/xjLib/xt_Thread/Process.py
Github       : https://github.com/sandorn/home
==============================================================
"""

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
    """调用CustomProcess,Manager.dict()返回结果"""
    sem = Semaphore(24)
    return_dict = Manager().dict()
    _ = [CustomProcess(return_dict, sem, func, *args_iter, **kwargs) for args_iter in list(zip(*args))]
    CustomProcess.wait_completed()
    return return_dict.values()
