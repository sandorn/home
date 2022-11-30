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
from xt_Alispeech.ex_NSS import NSS_TTS


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

    def __init__fn(self, textlist=None):
        obj.__init__(self)
        self.__dict__['_qobj'] = (obj == QThread)
        self.__dict__['_target'] = NSS_TTS
        self.__dict__['textlist'] = textlist or []
        self.__dict__['datas_list'] = []
        self.__dict__['_running'] = True
        pygame.mixer.init(frequency=8000)  # @不可默认
        self.__dict__['aformat'] = 'wav'
        self.__dict__['pym'] = pygame.mixer

        self.main_monitor()  # 启动语音生成
        self.start()

    def main_monitor(self):

        def _func():
            while len(self.textlist) > 0:
                text = self.textlist.pop(0)
                task = self._target(text, {'aformat': self.aformat, 'savefile': False})
                self.datas_list.append(task[1])
                if not self._running: break

            print('pygame_play MainMonitor stoping!!!!')

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
                    pygame.mixer.Sound(_data).play()
                    print('self.py_mixer new loading......')
                    continue

                if not self._MainMonitor.is_alive():
                    # #合成语音线程结束，朗读完毕，且无未加载数据
                    if len(self.textlist) == 0 and len(self.datas_list) == 0:
                        print('all recod play finished!!!!')
                        if self._qobj: self._signal.emit()
                        self.stop()

    def stop(self):
        QThread.msleep(500)
        self._running = False
        self.pym.stop()
        print('self.py_mixer.stoping!!!!')

    _name = 'QThread' if obj is QThread else 'Thread'
    return type(f'Synt_Read_{_name}', (obj, ), {
        '_signal': pyqtSignal(),
        '__init__': __init__fn,
        'main_monitor': main_monitor,
        'run': run,
        'stop': stop,
    })


Synt_Read_Thread = create_read_thread(Thread)
Synt_Read_QThread = create_read_thread(QThread)


#####################################################
class _read_class_meta:
    '''传入字符list,连续朗读'''

    _signal = pyqtSignal()

    def __init__(self, textlist=None):
        super().__init__()
        self._qobj = isinstance(self, QThread)
        self._target = NSS_TTS
        self.textlist = textlist or []
        self.datas_list = []
        self._running = True
        pygame.mixer.init(frequency=8000)  # @不可默认
        self.aformat = 'wav'
        self.pym = pygame.mixer
        self.main_monitor()  # 启动语音生成
        self.start()

    def main_monitor(self):

        def _func():
            while len(self.textlist) > 0:
                text = self.textlist.pop(0)
                task = self._target(text, {'aformat': self.aformat, 'savefile': False})
                self.datas_list.append(task[1])
                if not self._running: break

            print('pygame_play MainMonitor stoping!!!!')

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
                    pygame.mixer.Sound(_data).play()
                    print('self.py_mixer new loading......')
                    continue

                if not self._MainMonitor.is_alive():
                    # #合成语音线程结束，朗读完毕，且无未加载数据
                    if len(self.textlist) == 0 and len(self.datas_list) == 0:
                        print('all recod play finished!!!!')
                        if self._qobj: self._signal.emit()
                        self.stop()

    def stop(self):
        QThread.msleep(500)
        self._running = False
        self.pym.stop()
        print('self.py_mixer.stoping!!!!')


def get_read_class(obj: object) -> object:
    '''type 动态混入继承，实质是调整 bases'''
    _name = 'QThread' if obj is QThread else 'Thread'
    ocl = type(f'RSynt_Read_{_name}', (_read_class_meta, obj), {})
    return ocl


RSynt_Read_Thread = get_read_class(Thread)
RSynt_Read_QThread = get_read_class(QThread)

if __name__ == '__main__':
    RSynt_Read_Thread([
        '2022世界杯小组赛C组第二轮，阿根廷2:0力克墨西哥，重新掌握出线主动权。第64分钟，梅西世界波破门，打入个人世界杯第8个进球，进球数追平马拉多纳。',
        '第87分钟，恩索·费尔南德斯锁定胜局！目前，波兰积4分，阿根廷和沙特同积3分，阿根廷以净胜球优势排名第二，墨西哥积1分。',
    ])
