# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-05-21 16:26:08
LastEditTime : 2025-05-21 16:38:48
FilePath     : /CODE/xjLib/pydamo/enum_wind.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from win32gui import (
    EnumWindows,
    GetClassName,
    GetWindowText,
    IsWindow,
    IsWindowEnabled,
    IsWindowVisible,
)


def get_class_winds(class_name=None):
    if class_name is None:
        return -1

    titles = set()

    def foo(hwnd, mouse):
        # 去掉下面这句就所有都输出了，但是我不需要那么多
        if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
            if GetClassName(hwnd) == class_name:
                titles.add(hwnd)

    EnumWindows(foo, 0)
    lt = [t for t in titles if t]
    lt.sort()
    # for t in lt:
    #     print(t)
    return lt


def get_title_winds(title_name=None, subset=1):
    if title_name is None:
        return -1

    titles = set()

    def foo(hwnd, mouse):
        # 去掉下面这句就所有都输出了，但是我不需要那么多
        if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
            if subset:
                if title_name in GetWindowText(hwnd):
                    titles.add(hwnd)

            if GetWindowText(hwnd) == title_name:
                titles.add(hwnd)

    EnumWindows(foo, 0)
    lt = [t for t in titles if t]
    lt.sort()
    return lt


if __name__ == "__main__":
    class_name = "阿里邮箱"
    print(get_class_winds(class_name))

    title_name = "铁男对线各种英雄MVP合集_哔哩哔哩"
    print(get_title_winds(title_name))
