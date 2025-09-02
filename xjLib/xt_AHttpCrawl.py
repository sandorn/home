# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2025-09-02 12:40:19
FilePath     : /CODE/xjLib/xt_ahttpcrawl.py
Github       : https://github.com/sandorn/home
==============================================================
"""


import asyncio
import functools
import os
import selectors
from concurrent.futures import ThreadPoolExecutor

# 根据操作系统选择合适的事件循环策略
if os.name == 'nt':  # Windows系统
    class MyPolicy(asyncio.DefaultEventLoopPolicy):
        def new_event_loop(self):
            # return asyncio.ProactorEventLoop()
            return asyncio.SelectorEventLoop()
else:  # 非Windows系统
    class MyPolicy(asyncio.DefaultEventLoopPolicy):
        def new_event_loop(self):
            selector = selectors.SelectSelector()
            return asyncio.SelectorEventLoop(selector)

asyncio.set_event_loop_policy(MyPolicy())


class AioHttpCrawl:
    def __init__(self): ...

    def add_pool(self, func, args_list, callback=None):
        """添加函数(同步异步均可)及参数,异步运行，返回结果\n
        [(url,),{'index':index}] for index, url in enumerate(urls_list,1)]"""
        return asyncio.run(self.multi_fetch(func, args_list, callback=callback))

    async def multi_fetch(self, func, args_list, callback=None):
        _loop = asyncio.get_running_loop()

        tasks = []
        with ThreadPoolExecutor(160) as executor:
            for arg, kwargs in args_list:
                partial_func = functools.partial(func, *arg, **kwargs)
                task = _loop.run_in_executor(executor, partial_func)
                if callback:
                    task.add_done_callback(callback)
                tasks.append(task)

        return await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    from xt_requests import get
    myaio = AioHttpCrawl()
    url_list = [
        "https://www.163.com",
        "https://www.126.com",
        "https://www.bigee.cc/book/6909/2.html",
    ]

    args_list = [
        [("https://www.163.com",), {"index": 3}],
        [("https://www.126.com",), {"index": 2}],
        [("https://httpbin.org/get",), {"index": 4}],
    ]
    print(111111111, myaio.add_pool(get, args_list))

