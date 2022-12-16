# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:50
LastEditTime : 2022-12-03 16:19:00
FilePath     : /xjLib/xt_Alispeech/xt_Pygame.py
Github       : https://github.com/sandorn/home
==============================================================
'''
from io import BytesIO
from threading import Thread

import pygame
from PyQt5.QtCore import QThread, pyqtSignal
from xt_Alispeech.ex_NSS import TODO_TTS


def pygame_play(data, format='wav'):
    pygame.mixer.init(frequency=8000)
    pym = ''
    if format == 'wav':
        pym = pygame.mixer
        pym.Sound(data).play()
    else:
        pym = pygame.mixer.music
        pym.load(BytesIO(data)).play(1, 0.07)  # type: ignore
    print('py_mixer new loading......')

    while pym.get_busy():
        # 正在播放,等待
        QThread.msleep(2000)
        print('py_mixer.playing......')
        continue
    pym.stop()
    print('py_mixer.stoping!!!!!!')


def create_read_thread(meta):
    '''type完全动态构建类'''

    def __init__fn(self, textlist=None):
        meta.__init__(self)
        self.__dict__['__isQ'] = (meta == QThread)
        self.__dict__['_target'] = TODO_TTS
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
                datalist = self._target(text, {'aformat': self.aformat}, readonly=True)
                datalist.sort(key=lambda x: x[0])
                [self.datas_list.append(item[1]) for item in datalist]
                QThread.msleep(50)

                if not self._running: break

            print('pygame_play MainMonitor stoping!!!!')

        self._MainMonitor = Thread(target=_func, daemon=True, name="MainMonitor")
        self._MainMonitor.start()

    def run(self):
        while self._running:
            if self.pym.get_busy():
                # 正在播放,等待
                QThread.msleep(2000)
                print('self.py_mixer.playing......')
                continue
            else:
                if len(self.datas_list) > 0:
                    # 朗读完毕,有未加载数据
                    _data = self.datas_list.pop(0)
                    pygame.mixer.Sound(_data).play()
                    QThread.msleep(50)
                    print('self.py_mixer new loading......')
                    continue

                if not self._MainMonitor.is_alive():
                    # #合成语音线程结束,朗读完毕,且无未加载数据
                    if len(self.textlist) == 0 and len(self.datas_list) == 0:
                        print('all recod play finished!!!!')
                        if self.__isQ: self._signal.emit()
                        self.stop()

    def stop(self):
        self._running = False
        self.pym.stop()
        QThread.msleep(50)
        print('self.py_mixer.stoping!!!!')

    _name = 'QThread' if meta is QThread else 'Thread'
    return type(f'Synt_Read_{_name}', (meta, ), {
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
        self.__isQ = isinstance(self, QThread)
        self._target = TODO_TTS
        self.textlist = textlist or []
        self.datas_list = []
        self._running = True
        pygame.mixer.init(frequency=8000)  # @不可默认
        self.aformat = 'wav'
        self.pym = pygame.mixer
        self.main_monitor()  # 启动语音生成
        self.start()  # type: ignore

    def main_monitor(self):

        def _func():
            while len(self.textlist) > 0:
                text = self.textlist.pop(0)
                datalist = self._target(text, {'aformat': self.aformat}, readonly=True)
                assert isinstance(datalist, list)
                datalist.sort(key=lambda x: x[0])
                [self.datas_list.append(item[1]) for item in datalist]

                QThread.msleep(50)
                if not self._running: break

            print('pygame_play MainMonitor stoping!!!!')

        # #daemon=True,跟随主线程关闭 ,不能用双QThread嵌套
        self._MainMonitor = Thread(target=_func, daemon=True, name="MainMonitor")
        self._MainMonitor.start()

    def run(self):
        while self._running:
            if self.pym.get_busy():
                # 正在播放,等待
                QThread.msleep(2000)
                print('self.py_mixer.playing......')
                continue
            else:
                if len(self.datas_list) > 0:
                    # 朗读完毕,有未加载数据
                    _data = self.datas_list.pop(0)
                    pygame.mixer.Sound(_data).play()
                    QThread.msleep(50)
                    print('self.py_mixer new loading......')
                    continue

                if not self._MainMonitor.is_alive():
                    # #合成语音线程结束,朗读完毕,且无未加载数据
                    if len(self.textlist) == 0 and len(self.datas_list) == 0:
                        print('all recod play finished!!!!')
                        if self.__isQ: self._signal.emit()  # type: ignore
                        self.stop()

    def stop(self):
        self._running = False
        self.pym.stop()
        QThread.msleep(50)
        print('self.py_mixer.stoping!!!!')


def get_read_class(meta):
    '''type 动态混入继承,实质是调整 bases'''
    _name = 'QThread' if meta is QThread else 'Thread'
    _read_class = type(f'RSynt_Read_{_name}', (_read_class_meta, meta), {})
    return _read_class


class RSynt_Read_Thread(_read_class_meta, Thread):
    ...


RSynt_Read_QThread = get_read_class(QThread)

if __name__ == '__main__':
    # import snoop
    text_list = [
        '2022世界杯小组赛C组第二轮,阿根廷2:0力克墨西哥,重新掌握出线主动权。第64分钟,梅西世界波破门,打入个人世界杯第8个进球,进球数追平马拉多纳。',
        '第87分钟,恩索·费尔南德斯锁定胜局！目前,波兰积4分,阿根廷和沙特同积3分,阿根廷以净胜球优势排名第二,墨西哥积1分。',
    ]

    RSynt_Read_Thread(text_list)
