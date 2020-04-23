# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion:
python线程池ThreadPoolExecutor与进程池ProcessPoolExecutor - Harvard_Fly - 博客园
https://www.cnblogs.com/FG123/p/9704233.html

ThreadPoolExecutor线程池 - weixin_37426504的博客 - CSDN博客
https://blog.csdn.net/weixin_37426504/article/details/88657260
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-23 09:13:38
@LastEditors: Even.Sand
@LastEditTime: 2020-04-17 21:16:42
'''
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
#from concurrent.futures import ProcessPoolExecutor


def Bysubmit():
    '''
    通过submit函数提交执行的函数到线程池中，done()判断线程执行的状态：
    初始状态4个task都是未完成状态，2.5秒后task1和task2执行完成，
    task3和task由于是sleep(3) sleep(4)所以仍然是未完成的sleep状态
    '''

    def get_thread_time(times):
        time.sleep(times)
        return times

    # 创建线程池  指定最大容纳数量为4
    executor = ThreadPoolExecutor(max_workers=4)
    # 通过submit提交执行的函数到线程池中
    task1 = executor.submit(get_thread_time, (1))
    task2 = executor.submit(get_thread_time, (2))
    task3 = executor.submit(get_thread_time, (3))
    task4 = executor.submit(get_thread_time, (4))
    print("Bysubmit task1:{} ".format(task1.done()))
    print("Bysubmit task2:{}".format(task2.done()))
    print("Bysubmit task3:{} ".format(task3.done()))
    print("Bysubmit task4:{}".format(task4.done()))
    time.sleep(2.5)
    print('Bysubmit after 2.5s {}'.format('-' * 20))

    done_map = {
        "Bysubmit task1": task1.done(),
        "Bysubmit task2": task2.done(),
        "Bysubmit task3": task3.done(),
        "Bysubmit task4": task4.done()
    }
    # 2.5秒之后，线程的执行状态
    for task_name, done in done_map.items():
        if done:
            print("{}:Bysubmit completed".format(task_name))


def Bywait():
    '''
    通过wait()判断线程执行的状态：
    wait(fs, timeout=None, return_when=ALL_COMPLETED)，
    wait接受3个参数，fs表示执行的task序列；timeout表示等待的最长时间，超过这个时间即使线程未执行完成也将返回；
    return_when表示wait返回结果的条件，默认为ALL_COMPLETED全部执行完成再返回：
    可以看到在timeout 2.5时，task1和task2执行完毕，task3和task4仍在执行中
    '''
    from concurrent.futures import (ThreadPoolExecutor, wait)

    def get_thread_time(times):
        time.sleep(times)
        return times

    executor = ThreadPoolExecutor(max_workers=4)
    task_list = [
        executor.submit(get_thread_time, times) for times in [1, 2, 3, 4]
    ]
    i = 1
    for task in task_list:
        print("Bywait task{}:{}".format(i, task))
        i += 1
    print(wait(task_list, timeout=2.5))


def Bymap():
    '''
    map(fn, *iterables, timeout=None)，
    第一个参数fn是线程执行的函数；
    第二个参数接受一个可迭代对象；
    第三个参数timeout跟wait()的timeout一样，
    但由于map是返回线程执行的结果，如果timeout小于线程执行时间会抛异常TimeoutError。
    # @map的返回是有序的，它会根据第二个参数的顺序返回执行的结果：
    '''

    def get_thread_time(times):
        time.sleep(times)
        return times

    executor = ThreadPoolExecutor(max_workers=4)

    i = 1
    for result in executor.map(get_thread_time, [2, 3, 1, 4]):
        print("Bymap task{}:{}".format(i, result))
        i += 1


def Byas_completed():
    from collections import OrderedDict
    from concurrent.futures import (ThreadPoolExecutor, as_completed)

    def get_thread_time(times):
        time.sleep(times)
        return times

    executor = ThreadPoolExecutor(max_workers=4)
    task_list = [
        executor.submit(get_thread_time, times) for times in [2, 3, 1, 4]
    ]
    task_to_time = OrderedDict(
        zip(["task1", "task2", "task3", "task4"], [2, 3, 1, 4]))
    task_map = OrderedDict(zip(task_list, ["task1", "task2", "task3", "task4"]))

    for result in as_completed(task_list):
        task_name = task_map.get(result)
        print("Byas_completed {}:{}".format(task_name,
                                            task_to_time.get(task_name)))


def fibBythread():

    def fib(n):
        if n < 3:
            return 1
        return fib(n - 1) + fib(n - 2)

    start_time = time.time()
    executor = ThreadPoolExecutor(max_workers=4)
    task_list = [executor.submit(fib, n) for n in range(3, 35)]
    thread_results = [task.result() for task in as_completed(task_list)
                     ]  # @简化结果获取
    print(thread_results)
    print("ThreadPoolExecutor fib time is: {}".format(time.time() - start_time))


def fib(n):
    if n < 3:
        return 1
    return fib(n - 1) + fib(n - 2)


'''
ProcessPoolExecutor在使用上和ThreadPoolExecutor大致是一样的，它们在futures中的方法也是相同的，但是对于map()方法ProcessPoolExecutor会多一个参数chunksize(ThreadPoolExecutor中这个参数没有任何作用)，chunksize将迭代对象切成块，将其作为分开的任务提交给pool，对于很大的iterables，设置较大chunksize可以提高性能。
'''


def as_completed2():

    def get_html(times):
        time.sleep(times)
        print("as_completed2 get page {}s finished".format(times))
        return times

    executor = ThreadPoolExecutor(max_workers=2)
    urls = [10, 2, 20]  # 并不是真的url
    all_task = [executor.submit(get_html, (url)) for url in urls]
    # @datas = [data for data in all_task if data != '']
    for future in as_completed(all_task):
        data = future.result()
        print("as_completed2 in main: get page {}s success".format(data))


def map2():

    def get_html(times):
        time.sleep(times)
        print("map2 get page {}s finished".format(times))
        return times

    executor = ThreadPoolExecutor(max_workers=2)
    urls = [10, 2, 20]  # 并不是真的url
    for data in executor.map(get_html, urls):
        print("map2 in main: get page {}s success".format(data))
    '''
    使用map方法，无需提前使用submit方法，map方法与python标准库中的map含义相同，都是将序列中的每个元素都执行同一个函数。上面的代码就是对urls的每个元素都执行get_html函数，并分配各线程池。可以看到执行结果与上面的as_completed方法的结果不同，输出顺序和urls列表的顺序相同，就算2s的任务先执行完成，也会先打印出3s的任务先完成，再打印2s的任务完成。
    '''


def wait2():
    from concurrent.futures import wait, ALL_COMPLETED  # , FIRST_COMPLETED

    def get_html(times):
        time.sleep(times)
        print("wait2 get page {}s finished".format(times))
        return times

    executor = ThreadPoolExecutor(max_workers=2)
    urls = [10, 2, 20]  # 并不是真的url
    all_task = [executor.submit(get_html, (url)) for url in urls]
    wait(all_task, return_when=ALL_COMPLETED)
    print('wait2 done')


if __name__ == '__main__':
    Bywait()
    '''Bysubmit()
    Bymap()
    Byas_completed()
    fibBythread()

    start_time = time.time()
    executor = ProcessPoolExecutor(max_workers=4)
    task_list = [executor.submit(fib, n) for n in range(3, 35)]
    process_results = [task.result() for task in as_completed(task_list)]  # @简化结果获取
    print(process_results)
    print("ProcessPoolExecutor time is: {}".format(time.time() - start_time))'''
    # as_completed2()
    # map2()
    wait2()
