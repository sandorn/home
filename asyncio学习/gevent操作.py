# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-12 11:58:34
@LastEditors: Even.Sand
@LastEditTime: 2020-03-12 12:00:42
'''
import gevent
from gevent import Greenlet


class MyGreen(Greenlet):
    def __init__(self, timeout, msg):
        Greenlet.__init__(self)
        self.timeout = timeout
        self.msg = msg

    def _run(self):
        print("I'm from subclass of Greenlet and want to say: %s" % (self.msg,))
        gevent.sleep(self.timeout)
        print("I'm from subclass of Greenlet and done!")


class TestMultigreen(object):
    def __init__(self, timeout=0):
        self.timeout = timeout

    def run(self):
        green0 = gevent.spawn(self._task, 0, 'just 0 test')  # 方式一：使用gevent的spawn方法创建greenlet实例
        green1 = Greenlet.spawn(self._task, 1, 'just 1 test')  # 方式一：使用Greenlet的spawn方法创建greenlet实例
        green2 = MyGreen(self.timeout, 'just 2 test')  # 方式二：使用自定义的Greenlet子类创建实例，需要调用start()手动将greenlet实例加入到 coroutine 的调度队列中
        green2.start()

        gevent.joinall([green0, green1, green2])
        print('Tasks done!')

    def _task(self, pid, msg):
        print("I'm task %d and want to say: %s" % (pid, msg))
        gevent.sleep(self.timeout)
        print("Task %d done." % (pid,))


if __name__ == '__main__':
    test = TestMultigreen()
    test.run()
