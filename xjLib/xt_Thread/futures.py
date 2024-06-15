# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-06-16 01:34:21
FilePath     : /CODE/xjLib/xt_Thread/futures.py
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

        def add_tasks(self, func, *args_iter, callback=None):
            for item in args_iter:
                future = self.submit(func, *item)
                if callback:
                    future.add_done_callback(callback)
                self._future_tasks.append(future)

        def wait_completed(self):
            return self.__wait_completed()

        def __wait_completed(self):
            """获取结果,无序"""
            self.shutdown(wait=True)
            result_list = [future.result() for future in as_completed(self._future_tasks)]
            return result_list

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
        #     self.start()
        # def start(self):
        return self.loop.run_until_complete(self._work())

    async def _work(self):
        _args = list(zip(*self.args))
        self.result = await asyncio.gather(*[self.loop.run_in_executor(self.executor, self.func, *arg, **self.kwargs) for arg in _args])
        # return self.result


if __name__ == '__main__':
    from xt_Requests import get

    res = FuncInThreadPool(get, ['http://httpbin.org/get'] * 3)
    print(res.result)
