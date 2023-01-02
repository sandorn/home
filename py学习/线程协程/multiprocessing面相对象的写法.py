# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2023-01-02 00:48:57
LastEditTime : 2023-01-02 00:48:59
FilePath     : /py学习/线程协程/multiprocessing面相对象的写法.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import multiprocessing
import time


def worker(delay, count):
    for num in range(count):
        print(f"{num}, 进程ID:{multiprocessing.current_process().pid}, 进程名称:{multiprocessing.current_process().name}")
        # 延迟运行
        time.sleep(delay)
    return f'{delay * 20}worker done!'


class MyProcess(multiprocessing.Process):

    all_Process = []  # 类属性或类变量,实例公用
    result_list = []  # 类属性或类变量,实例公用

    def __init__(self, func, *args, **kwargs):
        super(MyProcess, self).__init__()
        self.daemon = True
        self.target = func
        self.args = args
        self.kwargs = kwargs
        self.start()
        self.all_Process.append(self)

    def run(self) -> None:
        self.Result = self.target(*self.args, **self.kwargs)
        print(f"子进程:{self.name}执行完毕，返回结果:{self.Result}")
        self.result_list.append(self.Result)
        return self.Result


if __name__ == '__main__':
    for i in range(5):
        process = MyProcess(worker, delay=i // 2, count=3)
    print(1111111111111111111111111111111111, MyProcess.all_Process)

    for process in MyProcess.all_Process:
        process.join()
        print(process.Result)
