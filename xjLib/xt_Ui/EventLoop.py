# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-06-28 17:32:08
LastEditTime : 2024-06-28 17:32:11
FilePath     : /CODE/xjLib/xt_Ui/EventLoop.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from functools import wraps

from PyQt6.QtCore import QEventLoop, Qt
from PyQt6.QtWidgets import QApplication


def EventLoop(function):
    """定义一个装饰器,确定鼠标显示和控制权"""

    @wraps(function)
    def warp(*args, **kwargs):
        QApplication.processEvents(QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents)  # 忽略用户的输入（鼠标和键盘）

        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)  # 显示等待中的鼠标样式

        result = function(*args, **kwargs)

        QApplication.restoreOverrideCursor()  # 恢复鼠标样式
        QApplication.processEvents()  # 交还控制权

        return result

    return warp
