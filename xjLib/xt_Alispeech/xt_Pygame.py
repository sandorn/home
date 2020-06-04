# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-30 20:11:54
#LastEditTime : 2020-06-03 14:10:36
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''

import io
import time
from io import BytesIO
from threading import Lock, Thread

import pygame
from PyQt5.QtCore import QThread, pyqtSignal

from xt_Alispeech import ReqSynthesizer


def play_callback(data, format='wav'):
    # !使用16000和默认,声音不行
    pygame.mixer.init(frequency=8000)

    if format == 'mp3':
        print('pygame.mixer.music.loading.....')
        pygame.mixer.music.load(io.BytesIO(data))
        pygame.mixer.music.play(1, 0.07)
        print()
        while pygame.mixer.music.get_busy():
            print('pygame.mixer.music.playing.....')
            time.sleep(0.500)

    if format == 'wav':
        pygame.mixer.Sound(data).play()
        print('pygame.mixer.Sound.loading.....')
        while pygame.mixer.get_busy():
            print('pygame.mixer.playing.....')
            time.sleep(0.500)

    pygame.mixer.stop()
    print('pygame.mixer.stop!!！')
    return


class ReqSynthesizer_QThread_read(QThread):
    '''传入字符list,连续朗读'''

    _signal = pyqtSignal()
    __instance_lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls.__instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, textlist=[], format='wav', *args, **kwargs):
        super().__init__()
        self._target = ReqSynthesizer
        self._args = args
        self._kwargs = kwargs
        self.textlist = textlist
        self.datas_list = []
        self._running = True
        pygame.mixer.init(frequency=8000)  #!使用16000和默认,声音不行
        self.format = format
        if self.format == 'wav':
            self.pym = pygame.mixer
        else:
            self.pym = pygame.mixer.music
        self.main_monitor()  ##启动语音生成
        self.start()

    def main_monitor(self):
        def _func():
            while len(self.textlist) > 0:
                text = self.textlist.pop(0)
                data = self._target(text, format=self.format, audioFile=None, *self._args, **self._kwargs)['data']
                self.datas_list.append(data)
                if not self._running:
                    break

            print('MainMonitor stoping!!!!!!')

        ##daemon=True,跟随主线程关闭 ,不能用双QThread嵌套
        self._MainMonitor = Thread(target=_func, daemon=True, name="MainMonitor")
        self._MainMonitor.start()

    def run(self):
        while self._running:
            if self.pym.get_busy():
                ##正在播放，等待
                QThread.msleep(500)
                print('self.py_mixer.playing......')
                continue
            else:
                if len(self.datas_list) > 0:
                    ##朗读完毕，有未加载数据
                    _data = self.datas_list.pop(0)
                    if self.format == 'wav':
                        pygame.mixer.Sound(_data).play()
                    else:
                        pygame.mixer.music.load(BytesIO(_data))
                        pygame.mixer.music.play(1, 0.07)
                    print('self.py_mixer new loading......')
                    continue
                elif len(self.textlist) == 0 and len(self.datas_list) == 0:
                    ##朗读完毕，且无未加载数据
                    self.stop()
                    print('all recod play finished!!!!!!')
                    self._signal.emit()

        ##停止标记
        self.pym.stop()
        print('self.py_mixer.stoping!!!!!!')

    def stop(self):
        self._running = False


class ReqSynthesizer_Thread_read(Thread):
    '''传入字符list,连续朗读'''

    _signal = pyqtSignal()
    __instance_lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls.__instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, textlist=[], format='wav', *args, **kwargs):
        super().__init__()
        self._target = ReqSynthesizer
        self._args = args
        self._kwargs = kwargs
        self.textlist = textlist
        self.datas_list = []
        self._running = True
        pygame.mixer.init(frequency=8000)  #!使用16000和默认,声音不行
        self.format = format
        if self.format == 'wav':
            self.pym = pygame.mixer
        else:
            self.pym = pygame.mixer.music
        self.main_monitor()  ##启动语音生成
        self.start()

    def main_monitor(self):
        def _func():
            while len(self.textlist) > 0:
                text = self.textlist.pop(0)
                data = self._target(text, format=self.format, audioFile=None, *self._args, **self._kwargs)['data']
                self.datas_list.append(data)
                if not self._running:
                    break

            print('MainMonitor stoping!!!!!!')

        ##daemon=True,跟随主线程关闭 ,下面为Thread
        self._MainMonitor = Thread(target=_func, daemon=True, name="MainMonitor")
        self._MainMonitor.start()

    def run(self):

        while self._running:
            if self.pym.get_busy():
                ##正在播放，等待
                QThread.msleep(500)
                print('self.py_mixer.playing......')
                continue
            else:
                if len(self.datas_list) > 0:
                    ##朗读完毕，有未加载数据
                    _data = self.datas_list.pop(0)
                    if self.format == 'wav':
                        pygame.mixer.Sound(_data).play()
                    else:
                        pygame.mixer.music.load(BytesIO(_data))
                        pygame.mixer.music.play(1, 0.07)
                    print('self.py_mixer new loading......')
                    continue
                elif len(self.textlist) == 0 and len(self.datas_list) == 0:
                    ##朗读完毕，且无未加载数据
                    self.stop()
                    print('all recod play finished!!!!!!')
                    self._signal.emit()

        ##停止
        self.pym.stop()
        print('self.py_mixer.stoping!!!!!!')

    def stop(self):
        self._running = False
