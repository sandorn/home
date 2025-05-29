# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-05-28 13:53:45
LastEditTime : 2025-05-28 15:24:01
FilePath     : /CODE/xjLib/xt_damo/key.py
Github       : https://github.com/sandorn/home
==============================================================
"""


from time import sleep
from typing import Any, Union

from bdtime import vk


class Key:
    def __init__(self, dmobject: Any, key: Union[str, int] = "k") -> None:
        """键盘操作控制器
        Args:
            dmobject: 大漠插件实例
            key: 默认绑定键（支持字符或键码）
        """
        if not dmobject:
            raise ValueError("dmobject cannot be None")
        self.dm = dmobject

        if key.__class__.__name__ == "str":
            self.chr = key.upper()
        else:
            self.chr = "None"
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
        if key.__class__.__name__ == "str":
            # 转换为大写后获取ASCII码（兼容小写输入）
            key = ord(key.upper())
        # 处理整数类型输入（仅限0-9）
        elif key.__class__.__name__ == "int":
            if key >= 0 and key <= 9:
                # 数字转字符串（如5→"5"）后获取ASCII码
                key = str(key)
                key = ord(key)
        return key
        
    def conv_chr(self, key):
        key = chr(key)
        return key

    def conv(self, key0):
        key = key0
        if key == vk.Constant:
            key = self.ord
        else:
            key = self.conv_ord(key)
        return key

    def state(self, key=vk.Constant):
        key = self.conv(key)
        return self.dm.GetKeyState(key)

    def press(self, key0=vk.Constant):
        key = self.conv_ord(key0)

        return self.dm.KeyPress(key)

    def down(self, key0=vk.Constant):
        key = self.conv_ord(key0)

        return self.dm.KeyDown(key)

    def up(self, key0=vk.Constant):
        key = self.conv_ord(key0)

        return self.dm.KeyUp(key)

    def down_up(self, key0=vk.Constant, t=vk.Time):
        try:
            key = self.conv_ord(key0)
            self.down(key)
            sleep(t)
            self.up(key)
        except Exception as e:
            print(f"按键操作失败: {e}")

