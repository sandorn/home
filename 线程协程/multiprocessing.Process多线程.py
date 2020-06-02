'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-14 19:23:06
@LastEditors: Even.Sand
@LastEditTime: 2020-03-12 18:19:41

Python爬虫进阶六之多进程的用法 - 周小董 - CSDN博客
https://blog.csdn.net/xc_zhou/article/details/80823878
另外你还可以通过 cpu_count() 方法还有 active_children() 方法获取当前机器的 CPU 核心数量以及得到目前所有的运行的进程。
'''
import multiprocessing
import time
from multiprocessing import Lock, Process


def process(num):
    time.sleep(num / 10)
    print('Process:', num)


def main():
    for i in range(5):
        p = multiprocessing.Process(target=process, args=(i,))
        p.start()

    print('CPU number:' + str(multiprocessing.cpu_count()))
    for p in multiprocessing.active_children():
        print('Child process name: ' + p.name + ' id: ' + str(p.pid))

    print('Process Ended')


class MyPro(Process):
    def __init__(self, loop, lock):
        Process.__init__(self)
        self.loop = loop
        self.lock = lock

    def run(self):
        for count in range(self.loop):
            time.sleep(0.1)
            self.lock.acquire()
            print('Pid: ' + str(self.pid) + ' LoopCount: ' + str(count))
            self.lock.release()


def main_daemon():
    lock = Lock()
    for i in range(5):
        p = MyPro(i, lock)
        p.daemon = True
        p.start()
        p.join()
    print('Main process Ended!')


if __name__ == '__main__':
    # main()
    main_daemon()
