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

import multiprocessing
import os
from multiprocessing import Lock, Pool, Process, Queue

from xt_Thread import Singleton_Mixin

# from multiprocessing.queues import Queue


class CustomProcess(Process, Singleton_Mixin):
    """多进程,继承自multiprocessing.Process"""

    all_Process = []  # 类属性或类变量,实例公用

    def __init__(self, index: int, target, *args, **kwargs):
        super().__init__(target=target, args=args, kwargs=kwargs)
        self.index = index
        # self.daemon = True
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self.all_Process.append(self)
        self.start()

    def run(self):
        print(f'Parent Pid:{os.getppid()} | Pid: {self.pid} | LoopCount: {self.index}')
        self.Result = self._target(*self._args, **self._kwargs)
        return self.Result

    def wait_completed(self):
        """停止进程池, 所有进程停止工作"""
        for _prc in self.all_Process:
            _prc.join()
            # return _prc.Result

    # return self.Result


if __name__ == '__main__':
    url = 'http://www.biqugse.com/96703/'
    from xt_Ls_Bqg import get_biqugse_download_url
    ccr = CustomProcess(1, get_biqugse_download_url, url)
    print(ccr.wait_completed())
