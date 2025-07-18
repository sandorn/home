# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-05-21 16:26:08
LastEditTime : 2025-05-28 10:33:29
FilePath     : /CODE/xjLib/xt_damo/__init__.py
Github       : https://github.com/sandorn/home
https://github.com/bode135/pydamo
==============================================================
"""

__name__ = "pydamo"

from .damo import DM
from .enum_wind import get_windows_by_criteria

__all__ = (DM, get_windows_by_criteria)
