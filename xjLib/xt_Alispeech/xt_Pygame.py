# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-30 20:11:54
#LastEditTime : 2020-07-24 13:12:39
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''

from io import BytesIO
from threading import Thread

import pygame
from PyQt5.QtCore import QThread, pyqtSignal
from xt_Alispeech import ReqSynthesizer


def pygame_play(data, format='wav'):
    # @使用16000和默认,声音不行
    pygame.mixer.init(frequency=8000)
    pym = ''
    if format == 'wav':
        pym = pygame.mixer
    else:
        pym = pygame.mixer.music

    print('py_mixer new loading......')

    if format == 'wav':
        pym.Sound(data).play()
    else:
        pym.load(BytesIO(data)).play(1, 0.07)
    while pym.get_busy():
        # 正在播放，等待
        QThread.msleep(500)
        print('py_mixer.playing......')
        continue
    pym.stop()
    print('py_mixer.stoping!!!!!!')


def create_read_thread(obj):
    '''type完全动态构建类'''

    def __init__fn(self, textlist=None, format='wav'):
        obj.__init__(self)
        self.__dict__['_qobj'] = (obj == QThread)

        self.__dict__['_target'] = ReqSynthesizer
        self.__dict__['textlist'] = textlist or []
        self.__dict__['datas_list'] = []
        self.__dict__['_running'] = True
        pygame.mixer.init(frequency=8000)  # !不能使用16000和默认
        self.__dict__['format'] = format
        if self.__dict__['format'] == 'wav':
            self.__dict__['pym'] = pygame.mixer
        else:
            self.__dict__['pym'] = pygame.mixer.music

        self.main_monitor()  # 启动语音生成
        self.start()

    def main_monitor(self):

        def _func():
            while len(self.textlist) > 0:
                text = self.textlist.pop(0)
                data = self._target(text, format=self.format, savefile=False).response.content
                self.datas_list.append(data)
                if not self._running:
                    break

            print('pygame_play MainMonitor stoping!!!!!!')

        self._MainMonitor = Thread(target=_func, daemon=True, name="MainMonitor")
        self._MainMonitor.start()

    def run(self):
        while self._running:
            if self.pym.get_busy():
                # 正在播放，等待
                QThread.msleep(500)
                print('self.py_mixer.playing......')
                continue
            else:
                if len(self.datas_list) > 0:
                    # 朗读完毕，有未加载数据
                    _data = self.datas_list.pop(0)
                    if self.format == 'wav':
                        pygame.mixer.Sound(_data).play()
                    else:
                        pygame.mixer.music.load(BytesIO(_data))
                        pygame.mixer.music.play(1, 0.07)
                    print('self.py_mixer new loading......')
                    continue

                if not self._MainMonitor.is_alive():
                    # #合成语音线程结束，朗读完毕，且无未加载数据
                    if len(self.textlist) == 0 and len(self.datas_list) == 0:
                        self.stop()
                        print('all recod play finished!!!!!!')
                        if self._qobj:
                            self._signal.emit()

        # 停止标记
        self.pym.stop()
        print('self.py_mixer.stoping!!!!!!')

    def stop(self):
        self._running = False

    _name = 'QThread' if obj is QThread else 'Thread'
    return type(f'Synt_Read_{_name}', (obj, ), {
        '_signal': pyqtSignal(),
        '__init__': __init__fn,
        'main_monitor': main_monitor,
        'run': run,
        'stop': stop,
    })


Synt_Thread_read = create_read_thread(Thread)
Synt_QThread_read = create_read_thread(QThread)


class _read_class_meta:
    '''传入字符list,连续朗读'''

    _signal = pyqtSignal()

    def __init__(self, textlist=None, format='wav'):
        super().__init__()
        self._qobj = isinstance(self, QThread)
        self._target = ReqSynthesizer
        self.textlist = textlist or []
        self.datas_list = []
        self._running = True
        pygame.mixer.init(frequency=8000)  # !不可使用默认16000
        self.format = format
        if self.format == 'wav':
            self.pym = pygame.mixer
        else:
            self.pym = pygame.mixer.music
        self.main_monitor()  # 启动语音生成
        self.start()

    def main_monitor(self):

        def _func():
            while len(self.textlist) > 0:
                text = self.textlist.pop(0)
                data = self._target(text, format=self.format, savefile=False).response.content
                self.datas_list.append(data)
                if not self._running:
                    break

            print('pygame_play MainMonitor stoping!!!!!!')

        # #daemon=True,跟随主线程关闭 ,不能用双QThread嵌套
        self._MainMonitor = Thread(target=_func, daemon=True, name="MainMonitor")
        self._MainMonitor.start()

    def run(self):
        while self._running:
            if self.pym.get_busy():
                # 正在播放，等待
                QThread.msleep(500)
                print('self.py_mixer.playing......')
                continue
            else:
                if len(self.datas_list) > 0:
                    # 朗读完毕，有未加载数据
                    _data = self.datas_list.pop(0)
                    if self.format == 'wav':
                        pygame.mixer.Sound(_data).play()
                    else:
                        pygame.mixer.music.load(BytesIO(_data))
                        pygame.mixer.music.play(1, 0.07)
                    print('self.py_mixer new loading......')
                    continue

                if not self._MainMonitor.is_alive():
                    # #合成语音线程结束，朗读完毕，且无未加载数据
                    if len(self.textlist) == 0 and len(self.datas_list) == 0:
                        self.stop()
                        print('all recod play finished!!!!!!')
                        if self._qobj:
                            self._signal.emit()

        # 停止标记
        self.pym.stop()
        print('self.py_mixer.stoping!!!!!!')

    def stop(self):
        self._running = False


def get_read_class(obj: object) -> object:
    '''type 动态混入继承，实质是调整bases'''
    _name = 'QThread' if obj is QThread else 'Thread'
    ocl = type(f'Synt_Read_{_name}', (_read_class_meta, obj), {})
    return ocl


ReqSynthesizer_Thread_read = get_read_class(Thread)
ReqSynthesizer_QThread_read = get_read_class(QThread)
