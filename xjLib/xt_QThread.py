# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-28 21:06:12
#LastEditTime : 2020-05-29 17:28:53
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''

from PyQt5.QtCore import QThread
from threading import Lock


class CustomQThread(QThread):
    """单例多线程，继承自threading.Thread"""
    __instance_lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls.__instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self._target = func
        self._args = args
        self._kwargs = kwargs
        self._running = True
        self.start()

    def run(self):
        # 调用线程函数，并将元组类型的参数值分解为单个的参数值传入线程函数
        self.Result = self._target(*self._args, **self._kwargs)
        # 获取结果
        self.result_list.append(self.Result)

    def __del__(self):
        #线程状态改变与线程终止
        self._running = False
        self.wait()

    def stop(self):
        self._running = False
        self.terminate()  # #强制结束线程
        ##quit()  exit() 均无效


'''''
重写QThread例子


class readthread(QThread):

    def __init__(self, _text):
        super().__init__()
        self._running = True
        self._text = _text
        self.start()

    def run(self):
        pygame.mixer.init(frequency=8000)  #!使用16000和默认,声音不行
        for index, text in enumerate(self._text):
            if not text.strip():
                continue

            if not self._running:
                return

            # #mp3,可设置播放起止时间
            data = postRESTful(
                appkey, token, text, format='mp3', speech_rate=-40)

            if not self._running:
                return
            pygame.mixer.music.load(BytesIO(data))
            pygame.mixer.music.play(1, 0.07)
            while pygame.mixer.music.get_busy():
                QThread.msleep(200)
                if not self._running:
                    print('self.py_mixer.stoping!!!!!!')
                    pygame.mixer.music.stop()
                    return
                print('self.py_mixer.playing......')

            # #wav,不能设置播放起止时间
            data = postRESTful(appkey, token, text, speech_rate=-40)

            if not self._running:
                return
            pygame.mixer.Sound(data).play()
            while pygame.mixer.get_busy():
                QThread.msleep(200)
                if not self._running:
                    print('self.py_mixer.stoping!!!!!!')
                    pygame.mixer.stop()
                    return
                print('self.py_mixer.playing......')

    def stop(self):
        self._running = False


##连续朗读


class readthread(QThread):

    def __init__(self, textlist):
        super().__init__()
        self._running = True
        self.textlist = textlist
        self.start()

    def run(self):
        datas_list = []
        pygame.mixer.init(frequency=8000)  #!使用16000和默认,声音不行

        data = ''

        while True:
            if len(self.textlist) > 0:
                ##文本未空
                text = self.textlist.pop(0)
                if data == '':
                    ##用QThread线程获取语音
                    thread = QThread()
                    thread.run = postRESTful
                    # @wav,无需  format
                    data = thread.run(
                        appkey, token, text, format='mp3', speech_rate=-40)
                    datas_list.append(data)
                    data = ''

            if not self._running:
                ##停止标记
                print('self.py_mixer.stoping!!!!!!')
                # @wav, pygame.mixer.stop()
                pygame.mixer.music.stop()
                break

            if pygame.mixer.music.get_busy():
                # @wav, pygame.mixer.get_busy():
                ##正在播放，等待
                QThread.msleep(500)
                # print('self.py_mixer.playing......')
                continue
            else:
                QThread.msleep(500)
                if len(datas_list) > 0:
                    ##朗读完毕，有未加载数据
                    _data = datas_list.pop(0)
                    pygame.mixer.music.load(BytesIO(_data))
                    # @wav,无需BytesIO，不能设置播放起止时间，pygame.mixer.Sound(_data).play()
                    pygame.mixer.music.play(1, 0.07)
                    print('self.py_mixer.playing......')
                    continue
                else:
                    ##朗读完毕，且无未加载数据
                    self._running = False
                    print('self.py_mixer.stoping!!!!!!')
                    # @wav, pygame.mixer.stop()
                    pygame.mixer.music.stop()
                    break

    def stop(self):
        self._running = False
''' ''
