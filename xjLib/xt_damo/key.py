# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-05-28 13:53:45
LastEditTime : 2025-06-05 14:01:02
FilePath     : /CODE/xjLib/xt_damo/key.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from __future__ import annotations

from time import sleep
from typing import Any

from bdtime import vk


class Key:
    def __init__(self, dm_instance: Any, key: str | int = 'k') -> None:
        """
        键盘操作控制器初始化方法

        参数:
            dm_instance: 大漠插件实例，用于调用底层键盘操作API
            key: 默认绑定的按键，支持字符串或整数形式(默认值:"k")

        功能说明:
            1. 参数校验: 确保dmobject不为空
            2. 初始化实例属性:
            - self.dm: 存储大漠插件实例
            - self.chr: 存储按键的字符形式(大写)
            - self.ord: 存储按键的ASCII码(通过conv_ord方法转换)
        """
        if not dm_instance:
            raise ValueError('dmobject cannot be None')
        self.dm_instance = dm_instance

        # 处理按键字符形式
        if isinstance(key, str):
            self.chr = key.upper()  # 统一转为大写
        elif isinstance(key, int):
            self.chr = str(key).upper()
        else:
            self.chr = 'None'  # 非字符串类型默认值

        # 转换按键为ASCII码
        self.ord = self.conv_ord(key)

    def get_ord(self, key):
        key = key.upper()
        return ord(key)

    def __main__(self):
        return self.ord

    def conv_ord(self, key0):
        """
        将输入的键值（字符串或数字）转换为对应的ASCII码值
        Args:
            key0 (str/int): 待转换的键值（支持字符串字符或0-9的整数）
        Returns:
            int: 转换后的ASCII码值
        处理规则：
            - 输入为字符串时：转换为大写后取ASCII码（如输入"a"→"A"→65）
            - 输入为整数时（0-9）：先转换为对应数字的字符串形式，再取ASCII码（如输入5→"5"→53）
        """
        key = key0  # 暂存原始输入值
        # 处理字符串类型输入
        if key.__class__.__name__ == 'str':
            # 转换为大写后获取ASCII码（兼容小写输入）
            key = ord(key.upper())
        # 处理整数类型输入（仅限0-9）
        elif key.__class__.__name__ == 'int' and key >= 0 and key <= 9:
            # 数字转字符串（如5→"5"）后获取ASCII码
            key = str(key)
            key = ord(key)
        return key

    def conv_chr(self, key):
        return chr(key)

    def conv(self, key0):
        key = key0
        return self.ord if key == vk.Constant else self.conv_ord(key)

    def state(self, key=vk.Constant):
        key = self.conv(key)
        return self.dm_instance.GetKeyState(key)

    def press(self, key0=vk.Constant):
        key = self.conv_ord(key0)

        return self.dm_instance.KeyPress(key)

    def down(self, key0=vk.Constant):
        key = self.conv_ord(key0)

        return self.dm_instance.KeyDown(key)

    def up(self, key0=vk.Constant):
        key = self.conv_ord(key0)

        return self.dm_instance.KeyUp(key)

    def down_up(self, key0=vk.Constant, t=vk.Time):
        try:
            key = self.conv_ord(key0)
            self.down(key)
            sleep(t)
            self.up(key)
        except Exception as e:
            raise KeyError(f'按键操作失败: {e}') from e
