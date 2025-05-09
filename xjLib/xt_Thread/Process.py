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

import sys
from multiprocessing import Manager, Process, Semaphore, get_context


class CustomProcess(Process):
    _context = get_context("spawn")  # 显式使用spawn上下文
    all_processes = []

    def __init__(
        self,
        *args,
        result_dict,
        semaphore,
        func,
        start_idx,
        end_idx,
        **kwargs,
    ):
        super().__init__()
        self.result_dict = result_dict 
        self.semaphore = semaphore
        self.func = func
        self.args = args
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.kwargs = kwargs  # 单独保存函数参数
        self.daemon = True
        self.start()
        CustomProcess.all_processes.append(self)

    def run(self):
        with self.semaphore:
            for idx in range(self.start_idx, self.end_idx):
                try:
                    args_for_idx = [arg[idx] for arg in self.args]
                    result = self.func(
                        *args_for_idx, **self.kwargs
                    ) 
                    self.result_dict[idx] = result
                except Exception as e:
                    self.result_dict[idx] = f"Error processing index {idx}: {str(e)}"

    @classmethod
    def wait_completed(cls):
        processes = cls.all_processes.copy()
        cls.all_processes.clear()
        for process in processes:
            process.join()


def Do_CustomProcess(func, *args, **kwargs):
    # Windows特殊处理
    if sys.platform == "win32":
        import __main__
        __main__.__dict__[func.__name__] = func

    max_workers = kwargs.pop("max_workers", 12) 

    # 参数校验
    base_length = len(args[0])
    for arg in args[1:]:
        if len(arg) != base_length:
            raise ValueError("所有参数列表长度必须一致")

    with Manager() as manager:
        result_dict = manager.dict()
        global_semaphore = Semaphore(max_workers)

        total_tasks = base_length
        chunk_size = max(1, total_tasks // max_workers)
        chunks = [
            (i, min(i + chunk_size, total_tasks))
            for i in range(0, total_tasks, chunk_size)
        ]

        for start_idx, end_idx in chunks:
            CustomProcess(
                *args,
                result_dict=result_dict,
                semaphore=global_semaphore,
                func=func,
                start_idx=start_idx,
                end_idx=end_idx,
                **kwargs,  # 传递函数参数
            )

        CustomProcess.wait_completed()

        return [result_dict[i] for i in range(total_tasks)]


## 测试见--/CODE/项目包/ProessPool-8星.py
