# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-08-05 11:40:43
FilePath     : /CODE/xjLib/xt_thread/futures.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from os import cpu_count


class ThreadPool(ThreadPoolExecutor):
    def __init__(self):
        self.count = (cpu_count() or 4) * 4
        super().__init__(self.count)
        self._future_tasks = []

    def add_tasks(self, fn, *args_iter, callback=None):
        for item in zip(*args_iter):
            future = self.submit(fn, *item)
            if callback:
                future.add_done_callback(callback)
            self._future_tasks.append(future)

    def wait_completed(self):
        """获取结果,无序"""
        # self.shutdown(wait=True)
        result_list = [future.result() for future in as_completed(self._future_tasks)]
        return result_list


class FnInPool:
    """将程序放到ThreadPoolExecutor中异步运行,返回结果"""

    def __init__(self, fn, *args, **kwargs):
        self.count = (cpu_count() or 4) * 4
        self.fn, self.args, self.kwargs = fn, args, kwargs
        self._map() if len(args) == 1 else self._run()

    def _run(self):
        with ThreadPoolExecutor(self.count) as executor:
            future_list = [
                executor.submit(self.fn, *arg, **self.kwargs) for arg in zip(*self.args)
            ]
        self.result = [future.result() for future in as_completed(future_list)]

    def _map(self):
        with ThreadPoolExecutor(self.count) as executor:
            result_iterator = executor.map(self.fn, *self.args, **self.kwargs)
        self.result = list(result_iterator)


if __name__ == "__main__":
    from xt_requests import get

    url_list = [
        "https://www.jd.com/",
        "https://xinghuo.xfyun.cn/desk",
        "http://www.163.com/",
    ]
    res = FnInPool(get, url_list * 1)
    print(111111, res.result)
    # POOL = ThreadPool()
    # POOL.add_tasks(get, url_list)
    # res = POOL.wait_completed()
    # print(222222, res)
