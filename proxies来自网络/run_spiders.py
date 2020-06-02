# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-23 11:47:12
@LastEditors: Even.Sand
@LastEditTime: 2020-03-24 09:07:37
'''

from settings import RUN_SPIDERS_INTERVEL  # 这些都是settings.py模块的一些变量
from dbpool import mysqlPool  # 要把可用代理IP存入mongodb数据库
from gevent.pool import Pool  # 导入协程池
from log import logger
from validator import check_proxy
from settings import SPIDERS
import sys
import importlib
import schedule
import time


# 可能有人会问为什么要用协程，因为requests.get()请求的时候会等待时间，我们可以利用这一部分时间做其他事情
sys.path.append("../..")
sys.path.append("..")


class RunSpiders(object):

    def __init__(self):
        self.mongo_pool = mysqlPool()  # 创建一个数据库对象
        self.coroutine_pool = Pool()  # 创建协程池

    def get_spider_from_settings(self):
        for full_class_name in SPIDERS:  # 动态导入模块
            module_name, class_name = full_class_name.rsplit('.', maxsplit=1)
            module = importlib.import_module(module_name)
            clss = getattr(module, class_name)
            spider = clss()
            # print(spider)
            yield spider

    def run(self):
        spiders = self.get_spider_from_settings()

        for spider in spiders:  # 开启多协程去分别运行多个爬虫
            self.coroutine_pool.apply_async(self.run_one, args=(spider,))

        self.coroutine_pool.join()  # 等全部爬虫都运行完，再结束这个函数

    def run_one(self, spider):
        try:  # try一下，以防某个爬虫失败导入异常，从而程序异常结束
            for proxy in spider.get_proxies():
                proxy = check_proxy(proxy)
                if proxy.speed != -1:
                    self.mongo_pool.insert(proxy)  # 把代理ip信息插入到数据库里面
        except Exception as err:
            logger.exception(err)

    @classmethod  # 定义一个类方法，之后可以通过类名来调用
    def start(cls):  # 这个cls参数，是它自己就带的
        rs = RunSpiders()
        rs.run()
        schedule.every(RUN_SPIDERS_INTERVEL).hours.do(rs.run)
        # 这个意思就是每隔RUN_SPIDERS_INTERVAL小时，就执行一遍rs.run函数
        while True:
            schedule.run_pending()  # 这个就是检查时间到两个小时了没
            time.sleep(60)


if __name__ == '__main__':  # 检查本模块是否可用
    RunSpiders.start()
    # rs = RunSpiders()
    # rs.run()
