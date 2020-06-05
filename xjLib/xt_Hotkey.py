# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-28 19:16:13
#FilePath     : /xjLib/xt_Hotkey.py
#LastEditTime : 2020-06-04 17:02:05
#Github       : https://github.com/sandorn/home
#==============================================================

原文链接：https://blog.csdn.net/lsjweiyi/article/details/79137931
'''
import win32con
import ctypes
import ctypes.wintypes
import threading

user32 = ctypes.windll.user32  # 加载user32.dll


from pysnooper import snoop


@snoop()
class Hotkey(threading.Thread):  # 创建一个Thread.threading的扩展类

    def __init__(self, ikey1=105, ikey2=106):
        super().__init__()
        self.RUN = False  # 用来传递运行一次的参数
        self.EXIT = False  # 用来传递退出的参数
        self.ikey1 = ikey1
        self.ikey2 = ikey2

    def run(self):
        if not user32.RegisterHotKey(None, self.ikey1, 0, win32con.VK_F9):
            # 注册快捷键F9并判断是否成功，该热键用于执行一次需要执行的内容。
            print("Unable to register id", self.ikey1)  # 返回一个错误信息

        if not user32.RegisterHotKey(None, self.ikey2, 0, win32con.VK_F10):
            # 注册快捷键F10并判断是否成功，该热键用于结束程序，且最好这么结束，否则影响下一次注册热键。
            print("Unable to register id", self.ikey2)

        # 以下为检测热键是否被按下，并在最后释放快捷键
        try:
            msg = ctypes.wintypes.MSG()

            while True:
                if user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:

                    if msg.message == win32con.WM_HOTKEY:
                        if msg.wParam == self.ikey1:
                            self.RUN = True
                        elif msg.wParam == self.ikey2:
                            self.EXIT = True
                            return

                    user32.TranslateMessage(ctypes.byref(msg))
                    user32.DispatchMessageA(ctypes.byref(msg))

        finally:
            # 必须得释放热键，否则下次就会注册失败，所以当程序异常退出，没有释放热键，
            # 那么下次很可能就没办法注册成功了，这时可以换一个热键测试
            user32.UnregisterHotKey(None, self.ikey1)
            user32.UnregisterHotKey(None, self.ikey2)


if __name__ == '__main__':
    hotkey = Hotkey()
    hotkey.start()

    while (True):

        if hotkey.RUN is True:
            # 这里放你要用热键启动执行的代码
            print('win32con.VK_F9,hotkey.RUN == True', 'RUN')
            hotkey.RUN = False

        elif hotkey.EXIT:
            # 这里是用于退出循环的
            print('win32con.VK_F10,hotkey.EXIT == True', 'EXIT')
            break


    # # QShortcut(QKeySequence("Escape"), self, self.close)
