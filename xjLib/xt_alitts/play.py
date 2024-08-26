# !/usr/bin/env python
"""
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
"""

from threading import Thread

import pygame
from PyQt6.QtCore import QThread, pyqtSignal
from xt_alitts.ex_nss import execute_tts
from xt_thread import thread_print as print


class _read_meta_cls:
    """传入字符list,连续朗读"""

    def __init__(self, textlist=None):
        super().__init__()
        self.__isQ = isinstance(self, QThread)
        self._signal = pyqtSignal() if self.__isQ else None
        self._target = execute_tts
        self.textlist = textlist or []
        self.datas_list = []
        self._running = True
        pygame.mixer.init(frequency=8000)  # @不可默认
        self.aformat = "pcm"
        self.pym = pygame.mixer
        self.main_monitor()  # 启动语音生成
        self.start()  # type: ignore

    def main_monitor(self):
        def _func():
            while len(self.textlist) > 0:
                text = self.textlist.pop(0)
                datalist = self._target(text, readonly=True, aformat=self.aformat)
                assert isinstance(datalist, list)
                datalist.sort(key=lambda x: x[0])
                [self.datas_list.append(item[1]) for item in datalist]

                QThread.msleep(50)
                if not self._running:
                    break

            print("pygame_play MainMonitor stoping!!!!")

        # #daemon=True,跟随主线程关闭 ,不能用双QThread嵌套
        self._MainMonitor = Thread(target=_func, daemon=True, name="MainMonitor")
        self._MainMonitor.start()

    def run(self):
        while self._running:
            if self.pym.get_busy():
                # 正在播放,等待
                QThread.msleep(2000)
                print("py_mixer.playing......")
                continue
            else:
                if len(self.datas_list) > 0:
                    # 朗读完毕,有未加载数据
                    _data = self.datas_list.pop(0)
                    pygame.mixer.Sound(_data).play()
                    QThread.msleep(50)
                    print("py_mixer new loading......")
                    continue

                if (
                    not self._MainMonitor.is_alive()
                    and len(self.textlist) == 0
                    and len(self.datas_list) == 0
                ):
                    print("all recod play finished!!!!")
                    if self.__isQ:
                        self._signal.emit()  # type: ignore
                    self.stop()

    def stop(self):
        self._running = False
        self.pym.stop()
        if self.__isQ:
            self._signal.emit()
        print("py_mixer.stoping!!!!")

    def join(self):
        self.wait()
        self.stop()


def create_read_thread(meta):
    """type完全动态构建类"""

    # _name = "QThread" if meta is QThread else "Thread"

    return type(
        f"Synt_Read_{ "QThread" if meta is QThread else "Thread"}",
        (meta,),  # 父类，动态继承
        {
            "__init__": _read_meta_cls.__init__,  # 初始化函数
            "main_monitor": _read_meta_cls.main_monitor,
            "run": _read_meta_cls.run,
            "stop": _read_meta_cls.stop,
        },
    )


Synt_Read_Thread = create_read_thread(Thread)
Synt_Read_QThread = create_read_thread(QThread)

if __name__ == "__main__":
    text_list = [
        "2022世界杯小组赛C组第二轮,阿根廷2:0力克墨西哥,重新掌握出线主动权。第64分钟,梅西世界波破门,打入个人世界杯第8个进球,进球数追平马拉多纳。",
        "第87分钟,恩索·费尔南德斯锁定胜局！目前,波兰积4分,阿根廷和沙特同积3分,阿根廷以净胜球优势排名第二,墨西哥积1分。",
    ]

    Synt_Read_QThread(text_list)
