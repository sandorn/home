# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-03-02 19:41:37
LastEditTime : 2023-03-02 19:42:51
FilePath     : /CODE/xjLib/xt_Win32.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import ctypes

import psutil
import win32api
import win32com.client
import win32con
import win32gui
import win32process
import win32ui

from ctypes import wintypes

user32 = ctypes.windll.user32  # 加载user32.dll
kernel32 = ctypes.windll.kernel32  # 加载kernel32.dll


def GetForegroundWindow():
    '''获取当前窗口句柄'''
    return user32.GetForegroundWindow()


def GetWindowText(hwnd):
    '''获取句柄对应窗口标题'''
    return win32gui.GetWindowText(hwnd)


def GetCursorPos():
    '''返回鼠标的坐标'''
    x, y = win32api.GetCursorPos()
    return x, y


def enum_windows():
    hwnd_title = {}

    def callback(hwnd, hwnd_title):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title[hwnd] = win32gui.GetWindowText(hwnd)

    win32gui.EnumWindows(callback, hwnd_title)

    return hwnd_title


def GetWindowRect(hwnd):
    '''通过窗口句柄 获取当前窗口的【左、上、右、下】四个方向的坐标位置'''
    return win32gui.GetWindowRect(hwnd)


def GetWindowPlacement(hwnd):
    '''获取窗口位置'''
    return win32gui.GetWindowPlacement(hwnd)


def WindowFromPoint(x, y):
    '''通过坐标获取坐标下的【窗口句柄】'''
    return win32gui.WindowFromPoint(x, y)


def WindowFromPos():
    '''获取当前鼠标下的【窗口句柄】'''
    return win32gui.WindowFromPoint(win32api.GetCursorPos())


def GetWindowDC(hwnd):
    '''通过句柄获取【窗口设备上下文】'''
    return win32gui.GetWindowDC(hwnd)


def GetDesktopWindow():
    '''获取桌面窗口句柄'''
    return win32gui.GetDesktopWindow()


def GetWindowThreadProcessId(hwnd):
    '''通过窗口句柄获取 【线程ID 和 进程ID】'''
    return win32process.GetWindowThreadProcessId(hwnd)


def GetProcessName(process_id):
    '''通过进程ID获取【进程名称】'''
    return psutil.Process(process_id).name()


def GetProcessPath(process_id):
    '''通过进程ID 获取【标准路径】'''
    return psutil.Process(process_id).exe()


def GetProcessCpu(process_id):
    '''通过进程ID 获取当前程序的【CPU利用率】'''
    return psutil.Process(process_id).cpu_percent()


def GetProcessMem(process_id):
    '''通过进程ID获取 当前程序的【CPU利用率】'''
    return psutil.Process(process_id).memory_percent()


def GetProcessThreadsNum(process_id):
    '''通过进程ID 获取当前程序的【线程数量】'''
    return psutil.Process(process_id).num_threads()


def FindWindow(windowname, classname=None):
    '''通过窗口类名和窗口标题名获取窗口句柄'''
    return win32gui.FindWindow(classname, windowname)


def GetClassName(hwnd):
    '''通过句柄获取窗口类名'''
    return win32gui.GetClassName(hwnd)


def SetWindowTop(hwnd):
    '''通过句柄窗口置顶'''
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)


def SetWindowDown(hwnd):
    '''通过句柄取消窗口置顶'''
    win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)


def SetForegroundWindow(hwnd):
    '''通过句柄将窗口放到最前面'''
    win32gui.SetForegroundWindow(hwnd)


def SetWindowPos(hwnd, x, y, w, h):
    '''通过句柄设置窗口位置和大小'''
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x, y, w, h, win32con.SWP_SHOWWINDOW)


def IsWindowEnabled(hwnd):
    '''检测当前句柄是否存在'''
    return win32gui.IsWindowEnabled(hwnd)


def IsWindowVisible(hwnd):
    '''检测当前句柄是否存在'''
    return win32gui.IsWindowVisible(hwnd)


def IsWindow(hwnd):
    '''检测当前句柄是否存在'''
    return win32gui.IsWindow(hwnd)


def SetWindowMax(hwnd):
    '''通过句柄最大化窗口'''
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)


def SetWindowMin(hwnd):
    '''通过句柄最小化窗口'''
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)


def SetWindowHide(hwnd):
    '''通过句柄隐藏窗口'''
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)


def SetWindowShow(hwnd):
    '''通过句柄显示窗口'''
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)


def SetWindowRestore(hwnd):
    '''通过句柄还原窗口'''
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)


def SetWindowClose(hwnd):
    '''通过句柄关闭窗口'''
    win32gui.SendMessage(hwnd, win32con.WM_CLOSE)


def SetWindowKill(hwnd):
    '''通过句柄强制关闭窗口'''
    win32gui.PostMessage(hwnd, win32con.WM_QUIT)


def SetWindowText(hwnd, title):
    '''通过句柄更改窗口标题'''
    win32gui.SetWindowText(hwnd, title)
    # win32gui.SendMessage(hwnd, 12, 0, title)


def SetWindowIcon(hwnd, icon):
    '''通过句柄更改窗口图标'''
    win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, icon)


def SetWindowIconSmall(hwnd, icon):
    '''通过句柄更改窗口小图标'''
    win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_SMALL, icon)


def SetWindowIconPath(hwnd, iconpath):
    '''通过句柄更改窗口图标'''
    icon = win32gui.LoadImage(0, iconpath, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE | win32con.LR_SHARED)
    win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, icon)


def SetWindowIconPathSmall(hwnd, iconpath):
    '''通过句柄更改窗口小图标'''
    icon = win32gui.LoadImage(0, iconpath, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE | win32con.LR_SHARED)
    win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_SMALL, icon)


def GetPixel(hwnd, x, y):
    '''通过句柄获取窗口RGB颜色'''
    hdc = win32gui.GetDC(hwnd)
    color = win32gui.GetPixel(hdc, x, y)
    win32gui.ReleaseDC(hwnd, hdc)
    return color


def EnumWindows():

    def win_enum_handler(hwnd, window_list):
        '''将窗口句柄添加到列表中'''
        window_list.append({
            'HWND': hwnd,
            'TEXT': win32gui.GetWindowText(hwnd),
            'NAME': win32gui.GetClassName(hwnd),
            # 'IDDD': win32api.GetWindowLong(hwnd, win32con.GWL_ID),
            'ID': getThreadProcessId(hwnd),
        })

    windows = []
    win32gui.EnumWindows(win_enum_handler, windows)

    return windows


get_thread_process_id_c = user32.GetWindowThreadProcessId
get_thread_process_id_c.argtypes = (wintypes.HWND, ctypes.POINTER(wintypes.DWORD))


def getThreadProcessId(hwnd):
    process_id = wintypes.DWORD()
    get_thread_process_id_c(hwnd, ctypes.byref(process_id))
    return process_id.value


def postThreadMessage(hwnd, msgType, wParam, lParam):
    process_id = wintypes.DWORD()
    pro_id = get_thread_process_id_c(hwnd, ctypes.byref(process_id))
    win32api.PostThreadMessage(pro_id, msgType, wParam, lParam)


def quit(hwnd):
    postThreadMessage(hwnd, win32con.WM_QUIT, 0, 0)


def close(hwnd):
    win32api.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)


if __name__ == "__main__":
    # print(GetDesktopWindow())
    # print(GetClassName(GetForegroundWindow()))
    # for item in EnumWindows():
    #     print(item)
    print(FindWindow("无标题 - 记事本"))
    close(FindWindow("无标题 - 记事本"))
