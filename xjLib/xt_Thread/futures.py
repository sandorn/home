# !/usr/bin/env python
"""
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-12-08 11:35:18
FilePath     : /xjLib/xt_Thread/futures.py
LastEditTime : 2022-10-22 11:07:45
Github       : https://github.com/sandorn/home
==============================================================
"""

import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed


def create_future_pool(base_class):
    class FuturePool(base_class):
        def __init__(self):
            super().__init__()
            self._future_tasks = []

        def add_map(self, func, *args_iter):
            self.future_generator = self.map(func, *args_iter)

        def add_sub(self, func, *args_iter, callback=None):
            self._future_tasks += [self.submit(func, *item) for item in args_iter]
            if callback:
                (t.add_done_callback(callback) for t in self._future_tasks)

        def wait_completed(self):
            """返回结果,有序"""
            if self._future_tasks:
                return self._wait_sub_completed()
            else:
                return self._wait_map_completed()

        def _wait_map_completed(self):
            """返回结果,有序"""
            self.shutdown(wait=True)  # 新增
            return list(self.future_generator)

        def _wait_sub_completed(self):
            """等待线程池结束,返回全部结果,有序"""
            self.shutdown(wait=True)
            result_list = []
            for future in self._future_tasks:
                try:
                    res = future.result()
                    result_list.append(res)
                except Exception as err:
                    print('exception :', err)
            return result_list

        def get_sub_result(self):
            """获取结果,无序"""
            self.shutdown(wait=True)
            result_list = []
            for future in as_completed(self._future_tasks):  # 迭代生成器,统一结束'
                try:
                    resp = future.result()
                    result_list.append(resp)
                except Exception as err:
                    print('exception :', err)
            return result_list

        def submit(self, fn, *args, **kwargs):
            """AI编写，未验证。提交任务,返回future对象"""
            future = super().submit(fn, *args, **kwargs)
            self._futures.append(future)
            return future

        def wait(self, timeout=None):
            """AI编写，未验证。"""
            self.shutdown(wait=True)
            for future in as_completed(self._futures, timeout=timeout):
                future.result()

    FuturePool.__name__ = base_class.__name__  # 保留原类的名字
    return FuturePool


# #使用类工厂,动态生成基于线程或进程的类
ThreadPool = create_future_pool(ThreadPoolExecutor)
ProcessPool = create_future_pool(ProcessPoolExecutor)


class FuncInThreadPool:
    """将程序放到ThreadPoolExecutor中异步运行,返回结果"""

    def __init__(self, func, *args, **kwargs):
        self.loop = asyncio.new_event_loop()
        self.executor = ThreadPoolExecutor(max_workers=32)
        self.func, self.args, self.kwargs = func, args, kwargs
        self.start()

    def start(self):
        return self.loop.run_until_complete(self._work())

    async def _work(self):
        _args = list(zip(*self.args))
        self.result = await asyncio.gather(*[self.loop.run_in_executor(self.executor, self.func, *arg, **self.kwargs) for arg in _args])
        # return self.result


if __name__ == '__main__':
    from xt_Requests import get

    res = FuncInThreadPool(get, ['http://httpbin.org/get'] * 3)
    print(res.result)
