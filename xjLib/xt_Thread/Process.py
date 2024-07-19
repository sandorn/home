# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-31 11:36:53
LastEditTime : 2024-07-19 15:36:26
FilePath     : /CODE/xjLib/xt_thread/Process.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from multiprocessing import Manager, Process, Semaphore


class CustomProcess(Process):
    """
    进程内顺序执行,继承自multiprocessing.Process,用Manager返回结果
    """

    all_Process = []  # 类属性或类变量,实例公用

    def __init__(self, result_dict, maxsem, func, *args, **kwargs):
        super().__init__()
        self.result_dict = result_dict
        self.semaphore = Semaphore(maxsem)
        self.daemon = True
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.start()
        self.all_Process.append(self)

    def run(self):
        # print(f'Pid: {os.getpid()} \t|\t {multiprocessing.current_process()}|{self.pid}|{self.name}')
        with self.semaphore:
            for index, args_iter in enumerate(list(zip(*self.args)), start=1):
                self.result_dict[index] = self.func(*args_iter, **self.kwargs)

    @classmethod
    def wait_completed(cls):
        """等待全部线程结束,返回结果"""
        while cls.all_Process:
            prc = cls.all_Process.pop()
            prc.join()


def Do_CustomProcess(func, maxsem=12, *args, **kwargs):
    """调用CustomProcess,Manager.dict()返回结果"""
    result_dict = Manager().dict()
    CustomProcess(result_dict, maxsem, func, *args, **kwargs)
    CustomProcess.wait_completed()
    return result_dict.values()
