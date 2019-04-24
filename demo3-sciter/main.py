# ！/usr/bin/env python
# -*-coding:utf-8-*-
'''
@Software:   VSCode
@File    :   main.py
@Time    :   2019/04/24 18:38:09
@Author  :   Even Sand
@Version :   1.0
@Contact :   sandorn@163.com
@License :   (C)Copyright 2019-2019, NewSea
@Desc    :   None
'''


# 导入sciter支持,必须安装pysciter
import sciter
import ctypes
import json
import os
from os import path as osPath, getcwd, mkdir

from multiprocessing import Process, Queue
from threading import Thread
from EventManager import EventManager
from FunManager import ServiceEvent, GuiCallBack

# 设置dpi, 防止程序在高分屏下发虚
ctypes.windll.user32.SetProcessDPIAware(2)


def startServiceP(_GuiQueue, _ServiceQueue, cfg):
    '''开启一个服务进程'''
    funMap = ServiceEvent(_GuiQueue, cfg)
    EventManager(_ServiceQueue, funMap).Start()


def queueLoop(_GuiQueue, funCall):
    guiCallBack = GuiCallBack(funCall)
    EventManager(_GuiQueue, guiCallBack).Start()


class Frame(sciter.Window):
    def __init__(self):
        '''
            ismain=False, ispopup=False, ischild=False, resizeable=True,
            parent=None, uni_theme=False, debug=True,
            pos=None,  pos=(x, y)
            size=None
        '''
        super().__init__(ismain=True, debug=True)
        self.set_dispatch_options(enable=True, require_attribute=False)
        self.cfg = self.initCfg()

    def _document_ready(self, target):
        '''在文档加载后执行，如果设置启动画面，可以在这里结束'''

        # 创建用于接收服务进程传递的回馈任务的队列，此队列线程安全
        self.GuiQueue = Queue()
        # 创建用于接收界面进程发送的任务的队列，此队列线程安全
        self.ServiceQueue = Queue()
        p = Process(target=startServiceP,
                    args=(self.GuiQueue, self.ServiceQueue, self.cfg))
        p.daemon = True  #设置为守护进程,保证主进程退出时子进程也会退出
        p.start()
        t = Thread(target=queueLoop, args=(self.GuiQueue, self.call_function))
        t.daemon = True
        t.start()

    def initCfg(self):
        cfg = {}
        # 代理，没有可不用设置
        # cfg['proxies'] = '127.0.0.1:61274'
        # 加载图片列表
        filename = "list.txt"
        if osPath.exists(filename):
            with open(filename, "r") as f:
                cfg['picList'] = f.read().strip().split("\n")
        # 设置图片的保存位置
        current_folder = getcwd()
        cfg['pic_temp'] = osPath.join(current_folder, 'pic_temp')
        if not osPath.isdir(cfg['pic_temp']):
            mkdir(cfg['pic_temp'])
        return cfg

    def clickMe(self):
        # 点击页面上的按钮后，只将任务添加到服务队列，耗时很短，因此不会发生界面卡顿现象
        self.__putService('getPicByList')

    def __putService(self, f, m=None):
        '''接收界面事件并转发'''
        self.ServiceQueue.put({'fun': f, 'msg': m})


if __name__ == '__main__':
    frame = Frame()
    frame.load_file(
        os.path.split(os.path.realpath(__file__))[0] + "/Gui/main.html")
    frame.run_app()
