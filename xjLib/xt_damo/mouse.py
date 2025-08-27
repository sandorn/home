# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-05-28 13:54:55
LastEditTime : 2025-05-30 15:57:04
FilePath     : /CODE/xjLib/xt_damo/mouse.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import random
from time import sleep
from typing import Any, Tuple


class Mouse:
    def __init__(self, dm_instance: Any) -> None:
        """
        鼠标操作控制器初始化

        参数:
            dmobject: 大漠插件实例，用于调用底层鼠标操作API

        异常:
            ValueError: 当dmobject为None时抛出
        """
        if not dm_instance:
            raise ValueError("dmobject cannot be None")
        self.dm_instance = dm_instance

    @property
    def position(self):
        """
        获取当前鼠标位置

        返回:
            tuple: (x, y)坐标元组
        """
        ret = self.dm_instance.GetCursorPos(x=0, y=0)[1:]
        return ret

    @position.setter
    def position(self, xy: Tuple[int, int]) -> None:
        """设置鼠标位置

        Args:
            xy: 包含(x, y)坐标的元组

        Raises:
            ValueError: 如果坐标格式不正确
            TypeError: 如果输入不是可迭代对象

        示例:
            >>> mouse.position = (100, 200)
        """
        try:
            x, y = xy
            if not (isinstance(x, int) and isinstance(y, int)):
                raise ValueError("坐标值必须为整数")
            self.move_to(x, y)
        except (TypeError, ValueError) as e:
            raise ValueError("请输入格式为(x, y)的坐标元组") from e

    def set_delay(self, delay, type="dx"):
        """
        设置鼠标操作延迟

        参数:
            delay: 延迟时间(毫秒)
            type: 延迟类型(默认"dx")
        """
        return self.dm_instance.SetMouseDelay(type, delay)

    def move_r(self, x, y):
        """
        相对移动鼠标

        参数:
            x: x轴偏移量
            y: y轴偏移量
        """
        return self.dm_instance.MoveR(x, y)

    def move_to(self, x, y):
        """
        绝对移动鼠标到指定坐标

        参数:
            x: 目标x坐标
            y: 目标y坐标
        """
        return self.dm_instance.MoveTo(x, y)

    def click_left(self, x, y, t=0.5):
        """
        执行左键点击

        参数:
            x: 点击位置x坐标
            y: 点击位置y坐标
            t: 按键按下持续时间(秒，默认0.5)
        """
        self.dm_instance.MoveTo(x, y)
        self.dm_instance.LeftDown()
        sleep(t)
        self.dm_instance.LeftUp()
        return 1

    def click_right(self, x, y, t=0.5):
        """
        执行右键点击

        参数:
            x: 点击位置x坐标
            y: 点击位置y坐标
            t: 按键按下持续时间(秒，默认0.5)
        """
        self.dm_instance.MoveTo(x, y)
        self.dm_instance.RightDown()
        sleep(t)
        self.dm_instance.RightUp()

    def safe_click(self, x: int, y: int, autoResetPos: bool = False) -> None:
        """安全的鼠标点击操作
        Args:
            x: 目标X坐标
            y: 目标Y坐标
            autoResetPos: 是否返回原位
        """
        try:
            x0, y0 = self.position
            self.dm_instance.MoveTo(x, y)
            self.dm_instance.LeftClick()
            sleep(random.randint(50, 400) / 1000)
            if autoResetPos:
                self.dm_instance.MoveTo(
                    x0 + random.randint(50, 300), y0 + random.randint(50, 300)
                )
        except Exception as e:
            self._last_error = str(e)
            print(f"_safe_click点击操作失败: {self._last_error}")
