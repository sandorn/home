# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-06-20 16:25:48
FilePath     : /CODE/xjLib/xt_Thread/futures.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed


class ThreadPool(ThreadPoolExecutor):
    def __init__(self):
        super().__init__()
        self._future_tasks = []

    def add_tasks(self, fn, *args_iter, callback=None):
        for item in args_iter[0]:
            future = self.submit(fn, item)
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


class FnInThreadPool:
    """将程序放到ThreadPoolExecutor中异步运行,返回结果"""

    def __init__(self, fn, *args, **kwargs):
        self.loop = asyncio.new_event_loop()
        self.executor = ThreadPoolExecutor(max_workers=32)
        self.fn, self.args, self.kwargs = fn, args, kwargs
        return self.loop.run_until_complete(self._work())

    async def _work(self):
        _args = list(zip(*self.args))
        self.result = await asyncio.gather(*[self.loop.run_in_executor(self.executor, self.fn, *arg, **self.kwargs) for arg in _args])
        # return self.result


if __name__ == '__main__':
    from xt_Requests import get

    # res = FnInThreadPool(get, ['http://httpbin.org/get', 'http://httpbin.org/get', 'http://httpbin.org/get'])
    # print(res.result)
    POOL = ThreadPool()
    POOL.add_tasks(get, ('http://httpbin.org/get', 'http://httpbin.org/get', 'http://httpbin.org/get'))
    res = POOL.wait_completed()
    print(res)
