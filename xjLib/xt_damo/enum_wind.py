# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-05-21 16:26:08
LastEditTime : 2025-06-05 10:56:49
FilePath     : /CODE/xjLib/xt_damo/enum_wind.py
Github       : https://github.com/sandorn/home
==============================================================
"""
from __future__ import annotations

from win32gui import EnumWindows, GetClassName, GetWindowText, IsWindow, IsWindowEnabled, IsWindowVisible


def _is_valid_window(hwnd):
    """检查窗口是否有效"""
    return IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd)


def get_windows_by_criteria(class_name=None, title_name=None, subset=True):
    """统一窗口查找接口"""
    if not any([class_name, title_name]):
        return -1

    hwnds = set()

    def callback(hwnd, _):
        if _is_valid_window(hwnd):
            if class_name and GetClassName(hwnd) == class_name:
                hwnds.add(hwnd)
            if title_name:
                text = GetWindowText(hwnd)
                if (subset and title_name in text) or text == title_name:
                    hwnds.add(hwnd)

    EnumWindows(callback, 0)
    return sorted(hwnds)


def get_class_winds(class_name=None):
    if class_name is None:
        return -1

    titles = set()

    def foo(hwnd, mouse):
        if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd) and GetClassName(hwnd) == class_name:
            titles.add(hwnd)

    EnumWindows(foo, 0)
    lt = [t for t in titles if t]
    lt.sort()
    return lt


def get_title_winds(title_name=None, subset=1):
    if title_name is None:
        return -1

    titles = set()

    def foo(hwnd, mouse):
        if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
            if subset and title_name in GetWindowText(hwnd):
                titles.add(hwnd)

            if GetWindowText(hwnd) == title_name:
                titles.add(hwnd)

    EnumWindows(foo, 0)
    lt = [t for t in titles if t]
    lt.sort()
    return lt


if __name__ == "__main__":
    # class_name = "阿里邮箱"
    # print(get_class_winds(class_name))

    title_name = "[管理员]"
    print(get_title_winds(title_name))

    title_name = "[管理员]"
    print(get_windows_by_criteria(title_name=title_name))
