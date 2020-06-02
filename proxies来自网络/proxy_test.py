# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-23 12:05:43
@LastEditors: Even.Sand
@LastEditTime: 2020-03-24 09:04:37

目的:检查代理IP可用性,保证代理池中代理IP基本可用
思路
1.在proxy. _test.py中, 创建ProxyTester类
2.提供-一个run 方法,用于处理检测代理IP核心逻辑
    2.1.从数据库中获取所有代理IP
    2.2.遍历代理IP列表
    2.3.检查代理可用性
        如果代理不可用，让代理分数-1,如果代理分数等于0就从数据库中删除该代理，否则更新该代理IP
        如果代理可用,就恢复该代理的分数,更新到数据库中
3.为了提高检查的速度,使用异步来执行检测任务
      3.1把要检测的代理IP,放到队列中
      3.2把检查一个代理可用性的代码,抽取到一一个方法中;从队列中获取代理IP,进行检查;检查完毕,
         调度队列的task_done方法
      3.3通过异步回调,使用死循环不断执行这个方法，
      3.4开启多个一个异步任务,来处理代理IP的检测;可以通过配置文件指定异步数量
4.使用schedule 模块,每隔一定的时间,执行一-次检测任务
      4.1定义类方法start ,用于启动检测模块
      4.2在start方法中
         创建本类对象
         调用run方法
         每间隔一定时间,执行一下run方法
'''

from settings import MAX_SCORE, TEST_PROXIES_ASYNC_COUNT, TEST_PROXIES_INTERVAL
from validator import check_proxy
from gevent.pool import Pool  # 导入代理池
from gevent import monkey
import schedule
from queue import Queue
import time
import sys
from dbpool import mysqlPool
# monkey.patch_all()  # 打上猴子补丁，python代理池的构建3——爬取代理ip 里面有对应链接
monkey.patch_socket()

sys.path.append("..")


class ProxyTest(object):

    def __init__(self):
        self.dbpool = mysqlPool()
        self.coroutine_pool = Pool()
        self.queue = Queue()  # 定义一个队列，用来放置数据库里面代理ip

    def __check_callback(self, temp):
        # 这个的意思就是一直等到队列里面没有代理ip了才停止执行self.__check_one这个函数
        self.coroutine_pool.apply_async(self.__check_one, callback=self.__check_callback)

    def run(self):
        proxies = self.dbpool.find_all()

        for proxy in proxies:
            # print(proxy.__dict__)
            self.queue.put(proxy)
            # self.__check_one(proxy)
        for i in range(TEST_PROXIES_ASYNC_COUNT):
            # 这个TEST_PROXIES_ASYNC_COUNT是一个变量，这个for就是来控制去检查ip是否可用最多开TEST_PROXIES_ASYNC_COUNT
            # 个数量的代理池，因为代理ip数据库中可能有好多，这样的话你给每一个代理ip都开一个协程。也会给系统带来很大负担
            self.coroutine_pool.apply_async(self.__check_one, callback=self.__check_callback)
        self.queue.join()  # 注意，这个是让先执行完的等一下没执行完得

    def __check_one(self):
        proxy = self.queue.get()
        proxy = check_proxy(proxy)
        if proxy.speed == -1:
            proxy.score -= 1
            if proxy.score == 0:
                self.dbpool.delete(proxy)
            else:
                self.dbpool.update(proxy)
        else:
            proxy.score = MAX_SCORE
            self.dbpool.update(proxy)
        self.queue.task_done()

    @classmethod  # 类方法
    def start(cls):
        db = ProxyTest()
        db.run()
        schedule.every(TEST_PROXIES_INTERVAL).hours.do(db.run)
        while True:
            schedule.run_pending()
            time.sleep(60)


if __name__ == '__main__':
    ProxyTest.start()
