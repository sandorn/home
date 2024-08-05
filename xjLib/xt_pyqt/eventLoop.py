# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-06-28 17:32:08
LastEditTime : 2024-07-18 09:50:44
FilePath     : /CODE/xjLib/xt_pyqt/eventLoop.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from PyQt6.QtCore import QEventLoop, Qt
from PyQt6.QtWidgets import QApplication
from wrapt import decorator


@decorator
def event_loop(func, instance, args, kwargs):
    """装饰器,确定鼠标显示和控制权"""
    QApplication.processEvents(
        QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents
    )  # 忽略用户键鼠输入
    QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)  # 显示等待中的鼠标

    result = func(*args, **kwargs)

    QApplication.restoreOverrideCursor()  # 恢复鼠标样式
    QApplication.processEvents()  # 交还控制权
    return result
