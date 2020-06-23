# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-22 15:40:04
#FilePath     : /xjLib/test/Thread__doc__.py
#LastEditTime : 2020-06-22 15:40:07
#Github       : https://github.com/sandorn/home
#==============================================================
'''
'''
    限制线程:
        threadingSum = 200 #同步线程数
        for index in range(len(urls)):
            # 创建多线程
            TASKS = CustomThread(get_content, (index, urls[index]), threadingSum,daemon=True)

        for thread in TASKS.all_Thread:
            thread.join()  # join等待线程执行结束
            callback(thread.getResult())  # 线程结果执行回调函数


    单例多线程:
        _ = [SingletonThread(get_contents, (index, urls[index])) for index in range(len(urls))]

        # 循环等待线程数量，降低到2
        while True:
            thread_num = len(enumerate())
            # print("线程数量是%d" % thread_num)
            if thread_num <= 2:
                break
            time.sleep(0.1)

        print('threading-继承，书籍《' + bookname + '》完成下载', flush=True)

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
    get_ident()	线程的标识符
    currentThread().ident	线程的标识符
    daemon	布尔值，表示这个线程是否是守护线程
    isDaemon()
    setDaemon()

    Thread(group=None, target=None, name=None, args=(), kwargs={})
        group: 线程组，目前还没有实现，库引用中提示必须是None；
        target: 要执行的方法；
        name: 线程名；
        args/kwargs: 要传入方法的参数。

    Thread类方法
    __init__(group=None,target=None,name=None,args=(),kwargs={},verbose=None,daemon=None)	实例化一个线程对象，需要一个可调用的target对象，以及参数args或者kwargs。还可以传递name参数。daemon的值将会设定thread.daemon的属性
    start()	开始执行该线程
    run()	定义线程的方法。（通常开发者应该在子类中重写）
    join(timeout=None)	直至启动的线程终止之前一直挂起；除非给出了timeout(单位秒)，否则一直被阻塞
    isAlive	布尔值，表示这个线程是否还存活（驼峰式命名，python2.6版本开始已被取代）
    is_alive()

    threading.active_count()
    threading.activeCount()
    获取当前活动的(alive)线程的个数。

    threading.currentThread()
    获取当前的线程对象（Thread object）。

    threading.enumerate()
    获取当前所有活动线程的列表。

    threading.settrace(func)
    设置一个跟踪函数，用于在run()执行之前被调用。

    threading.setprofile(func)
    设置一个跟踪函数，用于在run()执行完毕之后调用。

    手册
    https://docs.python.org/3/library/threading.html#module-threading
'''
