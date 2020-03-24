# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-02 09:07:36
@LastEditors: Even.Sand
@LastEditTime: 2020-03-22 22:46:46
高CPU占用
'''


import threading


class CustomThread(threading.Thread):
    # 每创建一个线程就加入到数组中，方便日后调用
    all_Thread = []
    rlock = threading.RLock()

    def __init__(self, func, args, threadingSum=None, name='CustomThread'):
        super().__init__(target=func, name=name, args=args)
        self.threadingSum = threadingSum
        self.__running = True  # 设置为True
        CustomThread.all_Thread.append(self)
        self.start()

    def run(self):
        if self.threadingSum:
            with self.threadingSum:
                # 调用线程函数，并将元组类型的参数值分解为单个的参数值传入线程函数
                self.Result = self._target(self.rlock, *self._args)  # 获取结果
        else:
            self.Result = self._target(self.rlock, *self._args)  # 获取结果

        '''
        while(self.__running):
            break
        else:
            time.sleep(2)
        '''

    def setMaxcs(self, arg):  # 外部修改最大线程数
        self.maxcs = arg
        self.semlock = threading.BoundedSemaphore(self.maxcs)  # 设置线程数

    def getMaxcs(self):  # 外部获得最大线程数
        return self.maxcs

    def setArgs(self, args):  # 外部修改函数参数
        self._args = args

    def getArgs(self):  # 外部获得函数参数
        return self._args

    def stop(self):
        self.__running = False  # 结束线程的标识符，未能生效

    def stoped(self):
        '''返回是否已经停止'''
        return self.__running

    def getResult(self):
        try:
            return self.Result
        except Exception:
            return None


'''
限制线程:
    threadingSum = threading.Semaphore(5) #同步线程数
    for index in range(len(urls)):
        # 创建多线程
        TASKS = CustomThread(get_content, (index, urls[index]), threadingSum)

    for thread in TASKS.all_Thread:
        thread.join()  # join等待线程执行结束
        callback(thread.getResult())  # 线程结果执行回调函数

不限制线程：
    for index in range(len(urls)):
        TASKS = CustomThread(get_content, (index, urls[index]))

    for thread in TASKS.all_Thread:
        thread.join()  # join等待线程执行结束
        callback(thread.getResult())  # 线程结果执行回调函数

'''

'''
对象	描述
Thread	表示一个执行线程的对象
Lock	锁对象
RLock	可重入锁对象，使单一线程可以（再次）获得已持有的锁（递归锁）
Condition	条件变量对象，使得一个线程等待另外一个线程满足特定的条件，比如改变状态或者某个数据值
Event　	条件变量的通用版本，任意数量的线程等待某个事件的发生，在该事件发生后所有的线程都将被激活
Semaphore	为线程间的有限资源提供一个计数器，如果没有可用资源时会被阻塞
BoundedSemaphore	于Semaphore相似，不过它不允许超过初始值
Timer	于Thread类似，不过它要在运行前等待一定时间
Barrier	创建一个障碍，必须达到指定数量的线程后才可以继续

下面是Thread类的属性和方法列表：

属性	描述
Thread类属性
name	线程名
ident	线程的标识符
daemon	布尔值，表示这个线程是否是守护线程
Thread类方法
__init__(group=None,target=None,name=None,args=(),kwargs={},verbose=None,daemon=None)	实例化一个线程对象，需要一个可调用的target对象，以及参数args或者kwargs。还可以传递name和group参数。daemon的值将会设定thread.daemon的属性
start()	开始执行该线程
run()	定义线程的方法。（通常开发者应该在子类中重写）
join(timeout=None)	直至启动的线程终止之前一直挂起；除非给出了timeout(单位秒)，否则一直被阻塞
isAlive	布尔值，表示这个线程是否还存活（驼峰式命名，python2.6版本开始已被取代）

'''
