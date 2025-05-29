# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-05-28 13:54:55
LastEditTime : 2025-05-28 13:54:55
FilePath     : /CODE/xjLib/xt_damo/mouse.py
Github       : https://github.com/sandorn/home
==============================================================
"""
from time import sleep
from typing import Any


class Mouse:
    def __init__(self, dmobject: Any) -> None:
        """鼠标操作控制器
        Args:
            dmobject: 大漠插件实例
        """
        if not dmobject:
            raise ValueError("dmobject cannot be None")
        self.dm = dmobject
        
    @property
    def position(self):
        ret = self.dm.GetCursorPos(x=0, y=0)[1:]
        return ret

    @position.setter
    def position(self, xy):
        x, y = xy
        self.move_to(x, y)

    def set_delay(self, delay, type="dx"):
        return self.dm.SetMouseDelay(type, delay)

    def move_r(self, x, y):
        return self.dm.MoveR(x, y)

    def move_to(self, x, y):
        return self.dm.MoveTo(x, y)

    def click_left(self, x, y, t=0.5):
        self.dm.MoveTo(x, y)

        self.dm.LeftDown()
        sleep(t)
        self.dm.LeftUp()
        return 1

    def click_right(self, x, y, t=0.5):
        self.dm.MoveTo(x, y)

        self.dm.RightDown()
        sleep(t)
        self.dm.RightUp()