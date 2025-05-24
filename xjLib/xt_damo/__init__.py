# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-05-21 16:26:08
LastEditTime : 2025-05-23 17:24:18
FilePath     : /CODE/xjLib/pydamo/__init__.py
Github       : https://github.com/sandorn/home
==============================================================
"""
__name__ = "pydamo"

from .damo import DM, Key, Mouse, Time, run_in_bat, tt, vk
from .enum_wind import get_class_winds

__all__ =  (Time, vk, tt, DM, Key, Mouse, run_in_bat, get_class_winds)
