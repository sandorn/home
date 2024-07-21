# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-07-21 17:23:13
FilePath     : /CODE/xjLib/xt_thread/futures.py
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
        for item in zip(*args_iter):
            future = self.submit(fn, *item)
            if callback:
                future.add_done_callback(callback)
            self._future_tasks.append(future)

    def wait_completed(self):
        """获取结果,无序"""
        self.shutdown(wait=True)
        result_list = [future.result() for future in as_completed(self._future_tasks)]
        return result_list


class FunctionInPool:
    """将程序放到ThreadPoolExecutor中异步运行,返回结果"""

    def __init__(self, fn, *args, **kwargs):
        self.loop = asyncio.new_event_loop()
        self.executor = ThreadPoolExecutor(max_workers=32)
        self.fn, self.args, self.kwargs = fn, args, kwargs
        self.loop.run_until_complete(self._work())

    async def _work(self):
        self.result = await asyncio.gather(*[self.loop.run_in_executor(self.executor, self.fn, *arg, **self.kwargs) for arg in zip(*self.args)])
        # tasks = []
        # for arg in zip(*self.args):
        #     task = self.loop.run_in_executor(self.executor, self.fn, *arg, **self.kwargs)
        #     tasks.append(task)

        # self.result = await asyncio.gather(*tasks)
        # return self.result


if __name__ == "__main__":
    from xt_requests import get

    url_list = ["http://httpbin.org/get"] * 3
    res = FnInThreadPool(get, url_list)
    print(111111, res.result)
    # POOL = ThreadPool()
    # POOL.add_tasks(get, url_list)
    # res = POOL.wait_completed()
    # print(222222, res)
