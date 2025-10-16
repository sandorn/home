# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-06-28 17:32:08
LastEditTime : 2025-05-16 11:15:30
FilePath     : /CODE/xjLib/xt_pyqt/utils.py
Github       : https://github.com/sandorn/home
==============================================================
"""
from __future__ import annotations

import sys
from functools import wraps

from PyQt6.QtCore import QEventLoop, Qt
from PyQt6.QtWidgets import QApplication


def event_loop(func):
    """装饰器,确定鼠标显示和控制权"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # 显示等待中的鼠标
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            # 忽略用户键鼠输入
            QApplication.processEvents(
                QEventLoop.ExcludeUserInputEvents,
                QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents,
            )

            return func(*args, **kwargs)

        finally:
            QApplication.restoreOverrideCursor()  # 恢复鼠标样式
            QApplication.processEvents()  # 交还控制权

    return wrapper


def appexec(main_window):
    app = QApplication(sys.argv)
    _ = main_window()
    sys.exit(app.exec())
