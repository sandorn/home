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
import time
from ctypes import wintypes

import psutil
import win32api
# import win32com.client
import win32con
import win32gui
import win32process
# import win32ui

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


def isVisible(hwnd):
    # 获取DWM状态
    cloaked = ctypes.c_bool()
    ctypes.windll.dwmapi.DwmGetWindowAttribute(hwnd, 14, ctypes.byref(cloaked), ctypes.sizeof(cloaked))

    # 获取窗口可见性状态
    _style = win32con.WS_VISIBLE | win32con.WS_MINIMIZE
    _exStyle = win32con.WS_EX_APPWINDOW | win32con.WS_EX_TOOLWINDOW | win32con.WS_EX_NOACTIVATE

    isVisible = ctypes.windll.user32.IsWindowVisible(hwnd)
    styleState = ctypes.windll.user32.GetWindowLongW(hwnd, win32con.GWL_STYLE) & _style
    exStyleState = ctypes.windll.user32.GetWindowLongW(hwnd, win32con.GWL_EXSTYLE) & _exStyle

    # 判断窗口状态
    if cloaked.value: return None
    elif isVisible and styleState and not exStyleState:
        return True
    else:
        return False


# isUnicode函数：判断窗口是否Unicode窗口
def isUnicode(hwnd):
    # 获取窗口所属的进程ID
    processID = ctypes.c_ulong()
    ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(processID))

    # 打开进程获取进程相关信息
    processHandle = ctypes.windll.kernel32.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, processID)
    # 获取进程的PEB结构体信息
    peb = ctypes.c_ulong()
    result = ctypes.windll.kernel32.ReadProcessMemory(processHandle, ctypes.cast(peb, ctypes.c_void_p), ctypes.byref(peb), ctypes.sizeof(peb), None)

    # 获取进程的ANSI code page和Unicode code page信息
    ansiCodePage = ctypes.c_ulong()
    unicodeCodePage = ctypes.c_ulong()
    result = ctypes.windll.kernel32.ReadProcessMemory(processHandle, ctypes.cast(peb.value + 0x038, ctypes.c_void_p), ctypes.byref(ansiCodePage), ctypes.sizeof(ansiCodePage), None)
    result = ctypes.windll.kernel32.ReadProcessMemory(processHandle, ctypes.cast(peb.value + 0x03C, ctypes.c_void_p), ctypes.byref(unicodeCodePage), ctypes.sizeof(unicodeCodePage), None)

    isUnicode = unicodeCodePage.value != 0
    # 关闭进程句柄，释放资源
    ctypes.windll.kernel32.CloseHandle(processHandle)

    return isUnicode


# waitEx函数：等待窗口出现
def waitEx(parentHwnd=None, index=1, classNamePattern=None, titlePattern=None, controlId=None):
    hwnd = None
    count = 0

    while True:
        hwndList = []
        if parentHwnd is None:
            win32gui.EnumWindows(lambda h, p: p.append(h), hwndList)
        else:
            win32gui.EnumChildWindows(parentHwnd, lambda h, p: p.append(h), hwndList)
        hwndList = [hwnd for hwnd in hwndList if classNamePattern in win32gui.GetClassName(hwnd) and titlePattern in win32gui.GetWindowText(hwnd)]
        if len(hwndList) >= index:
            hwnd = hwndList[index - 1]
            if controlId is not None:
                hwnd = win32gui.GetDlgItem(hwnd, controlId)
            break

        time.sleep(0.5)
        count += 1
        if count > 10:
            break

    return hwnd


# findEx函数：查找窗口
def findEx(parent=None, index=0, className=None, title=None, controlId=None, style=None, nStyle=None):
    count = 0
    hwndList = []
    hwnd = None

    if parent is not None:
        win32gui.EnumChildWindows(parent, lambda h, p: p.append(h), hwndList)
    else:
        win32gui.EnumWindows(lambda h, p: p.append(h), hwndList)

    for hwndfind in hwndList:
        if className is not None and className not in win32gui.GetClassName(hwndfind):
            continue
        if title is not None and title not in win32gui.GetWindowText(hwndfind):
            continue
        if controlId is not None and controlId != win32gui.GetDlgCtrlID(hwndfind):
            continue
        if style is not None or nStyle is not None:
            if (win32gui.GetWindowLong(hwndfind, win32con.GWL_STYLE) & style != style):
                continue
            if (win32gui.GetWindowLong(hwndfind, win32con.GWL_EXSTYLE) & nStyle != nStyle):
                continue

        hwnd = hwndfind
        if index:
            count += 1
            if count >= index: break

    if hwnd is None and className is not None and title is not None:
        hwndList = []
        win32gui.EnumWindows(lambda h, p: p.append((h, win32gui.GetWindowText(h), win32gui.GetWindowThreadProcessId(h)[0], win32gui.GetWindowThreadProcessId(h)[1])), hwndList)
        for hwndfind, hwndtitle, threadId, processId in hwndList:
            if className not in win32gui.GetClassName(hwndfind):
                continue
            if title not in hwndtitle:
                continue
            if win32gui.GetWindow(hwndfind, win32gui.GW_OWNER) != parent:
                continue
            if style is not None or nStyle is not None:
                if (win32gui.GetWindowLong(hwndfind, win32con.GWL_STYLE) & style != style):
                    continue
                if (win32gui.GetWindowLong(hwndfind, win32con.GWL_EXSTYLE) & nStyle != nStyle):
                    continue

            hwnd = hwndfind
            break

    return hwnd


import threading


# closeAndWait函数：关闭窗口并等待消息处理完成
def closeAndWait(hwnd):
    # 发送WM_CLOSE消息
    win32api.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

    # 定义事件对象，用于等待消息处理完成
    event = threading.Event()

    # 定义消息处理函数
    def callback(hwnd, msg, wparam, lparam):
        if hwnd == hwnd and msg == win32con.WM_DESTROY:
            event.set()
            return 0
        else:
            return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    # 注册消息处理函数
    win32gui.SetWindowLong(hwnd, win32con.GWL_WNDPROC, callback)
    # 等待消息处理完成
    event.wait()
    # 恢复原来的消息处理函数
    win32gui.SetWindowLong(hwnd, win32con.GWL_WNDPROC, win32gui.DefWindowProc)


# removeBorder函数：移除窗口边框
def removeBorder(hwnd):
    # 修改窗口样式
    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE) & ~0xCF0000)
    # 重新设置窗口位置
    win32gui.SetWindowPos(hwnd, None, 0, 0, 0, 0, win32con.SWP_FRAMECHANGED | win32con.SWP_NOACTIVATE | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOZORDER)


# orphanWindow函数：将窗口设为子窗口，并且移除控件
def orphanWindow(ctrl, hwnd):
    # 移除窗口边框
    removeBorder(hwnd)
    # 将窗口设为子窗口
    win32gui.SetParent(hwnd, ctrl.GetSafeHwnd())
    # 移除控件
    ctrl.orphanWindow(False, hwnd)


def click(hwnd, cmdId=None, *args):
    if not cmdId: win32api.PostMessage(hwnd, win32api.BM_CLICK, 0, 0)
    else: _, cid = findMenu(hwnd, cmdId, *args)
    if cid: win32api.PostMessage(hwnd, win32api.WM_COMMAND, cid, 0)
    else: win32api.PostMessage(hwnd, win32api.WM_COMMAND, cmdId, 0)


def findSubMenu(hMenu, label, *args):
    '''查找子菜单并返回菜单句柄和菜单ID'''
    if not hMenu: return hMenu, None
    count = user32.GetMenuItemCount(hMenu)
    if count < 1: return None, None

    if isinstance(label, str):
        buf = ctypes.create_unicode_buffer(1024)
        for pos in range(count):
            user32.GetMenuString(hMenu, pos, buf, 512, 0x400)
            target = buf.value.replace("\&", "")
            if label in target:
                label = pos + 1
                break

    if isinstance(label, int):
        if not (1 <= label <= count):
            return None, None
        menuId = user32.GetMenuItemID(hMenu, label - 1)
        if menuId != -1: return hMenu, menuId
        if not args: return hMenu, None
        hMenu = user32.GetSubMenu(hMenu, label - 1)
        return findSubMenu(hMenu, *args)


def findMenu(hwnd=None, *args):
    if not hwnd: hwnd = user32.GetDesktopWindow()
    return findSubMenu(user32.GetMenuP(hwnd), *args)


if __name__ == "__main__":
    # print(GetDesktopWindow())
    # print(GetClassName(GetForegroundWindow()))
    # for item in EnumWindows():
    # print(item)
    res = FindWindow(None, classname='Chrome_WidgetWin_1')
    print(GetWindowText(res), GetClassName(res))
    print(findEx(className='Chrome_WidgetWin_1'))
    # win10环境下模拟鼠标点击
    import win32api, win32con
    win32api.SetCursorPos((100, 100))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

