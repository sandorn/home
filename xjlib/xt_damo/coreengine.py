# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-05-28 10:33:05
LastEditTime : 2025-05-28 10:33:11
FilePath     : /CODE/xjLib/xt_damo/CoreEngine.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from __future__ import annotations

from typing import Any


class CoreEngine:
    def __init__(self, dm_instance: Any) -> None:
        """核心功能封装
        Args:
            dm_instance: 大漠插件实例
        """
        if not dm_instance:
            raise ValueError('dmobject cannot be None')
        self.dm_instance = dm_instance

    def __repr__(self):
        return f'版本： {self.ver()} ID：{self.GetID()}'

    def GetDmCount(self):
        return self.dm_instance.GetDmCount()

    def GetID(self):
        return self.dm_instance.GetID()

    def ver(self):
        return self.dm_instance.ver()

    def GetDir(self, types: int = 0):
        """
        0 : 获取当前路径
        1 : 获取系统路径(system32路径)
        2 : 获取windows路径(windows所在路径)
        3 : 获取临时目录路径(temp)
        4 : 获取当前进程(exe)所在的路径
        """
        return self.dm_instance.GetDir(types)

    def GetBasePath(self):
        return self.dm_instance.GetBasePath()

    def GetPath(self):
        return self.dm_instance.GetPath()

    def SetDisplayInput(self, mode):
        return self.dm_instance.SetDisplayInput(mode)

    def SetShowErrorMsg(self, show):
        return self.dm_instance.SetShowErrorMsg(show)

    def Capture(self, x1, y1, x2, y2, file):
        return self.dm_instance.Capture(x1, y1, x2, y2, file)

    def FindPic(
        self,
        x1,
        y1,
        x2,
        y2,
        pic_name,
        delta_color='101010',
        sim=0.9,
        dir=0,
        # intX=0,
        # intY=0,
    ):
        return self.dm_instance.FindPic(x1, y1, x2, y2, pic_name, delta_color=delta_color, sim=sim, dir=dir)

    def FindColor(self, x1, y1, x2, y2, color, sim, dir, intX, intY):
        # _, x0, y0 = dm.FindColor(0, 0, 1200, 800, color = "757575", sim = 1.0, dir = 1,  intX = 0, intY = 0)
        return self.dm_instance.FindColor(x1, y1, x2, y2, color, sim, dir, intX, intY)

    def LoadPic(self, pic_name):
        return self.dm_instance.LoadPic(pic_name)

    def FreePic(self, pic_name):
        return self.dm_instance.FreePic(pic_name)

    def GetColor(self, x, y):
        return self.dm_instance.GetColor(x, y)

    def GetPicSize(self, pic_name):
        return self.dm_instance.GetPicSize(pic_name)

    def GetColorBGR(self, x, y):
        return self.dm_instance.GetColorBGR(x, y)

    def BGR2RGB(self, bgr_color):
        return self.dm_instance.BGR2RGB(bgr_color)

    def CmpColor(self, x, y, color, sim):
        return self.dm_instance.CmpColor(x, y, color, sim)

    def BindWindow(
        self,
        hwnd,
        display=['normal', 'gdi', 'gdi2', 'dx', 'dx2'][1],
        mouse=['normal', 'windows', 'windows2', 'windows3', 'dx', 'dx2'][3],
        keypad=['normal', 'windows', 'dx'][1],
        mode=[0, 1, 2, 3, 4, 5, 6, 7, 101, 103][8],
    ):
        return self.dm_instance.BindWindow(hwnd, display, mouse, keypad, mode)

    def UnBindWindow(self):
        return self.dm_instance.UnBindWindow()

    def IsBind(self, hwnd):
        return self.dm_instance.IsBind(hwnd)

    def MoveWindow(self, hwnd, x, y):
        return self.dm_instance.MoveWindow(hwnd, x, y)

    def FindWindow(self, class_name='', title_name=''):
        return self.dm_instance.FindWindow(class_name, title_name)

    def ClientToScreen(self, hwnd, x, y):
        return self.dm_instance.ClientToScreen(hwnd, x, y)

    def ScreenToClient(self, hwnd, x, y):
        return self.dm_instance.ScreenToClient(hwnd, x, y)

    def FindWindowByProcess(self, process_name, class_name, title_name):
        return self.dm_instance.FindWindowByProcess(process_name, class_name, title_name)

    def FindWindowByProcessId(self, process_id, class_, title):
        return self.dm_instance.FindWindowByProcessId(process_id, class_, title)

    def GetClientRect(self, hwnd, x1, y1, x2, y2):
        return self.dm_instance.GetClientRect(hwnd, x1, y1, x2, y2)

    def GetClientSize(self, hwnd, width, height):
        return self.dm_instance.GetClientSize(hwnd, width, height)

    def GetWindowRect(self, hwnd, x1, y1, x2, y2):
        return self.dm_instance.GetWindowRect(hwnd, x1, y1, x2, y2)

    def GetWindow(self, hwnd, flag):
        return self.dm_instance.GetWindow(hwnd, flag)

    def GetWindowProcessPath(self, hwnd):
        return self.dm_instance.GetWindowProcessPath(hwnd)

    def SetWindowSize(self, hwnd, width, height):
        return self.dm_instance.SetWindowSize(hwnd, width, height)

    def SetWindowState(self, hwnd, flag):
        return self.dm_instance.SetWindowState(hwnd, flag)

    def SetWindowText(self, hwnd, title):
        return self.dm_instance.SetWindowText(hwnd, title)

    def SetWindowTransparent(self, hwnd, trans):
        return self.dm_instance.SetWindowTransparent(hwnd, trans)

    def EnumWindow(self, parent, title, class_name, filter):
        return self.dm_instance.EnumWindow(parent, title, class_name, filter)

    def EnumWindowByProcess(self, process_name, title, class_name, filter):
        return self.dm_instance.EnumWindowByProcess(process_name, title, class_name, filter)

    def EnumWindowSuper(self, spec1, flag1, type1, spec2, flag2, type2, sort):
        return self.dm_instance.EnumWindowSuper(spec1, flag1, type1, spec2, flag2, type2, sort)

    def GetCursorPos(self, x=0, y=0):
        return self.dm_instance.GetCursorPos(x, y)

    def GetKeyState(self, vk_code):
        return self.dm_instance.GetKeyState(vk_code)

    def SetKeypadDelay(self, type=['normal', 'windows', 'dx'][-1], delay=[0.03, 0.01, 0.05][-1]):
        return self.dm_instance.SetKeypadDelay(type, delay)

    def SetMouseDelay(self, type=['normal', 'windows', 'dx'][-1], delay=[0.03, 0.01, 0.04][-1]):
        return self.dm_instance.SetMouseDelay(type, delay)

    def WaitKey(self, vk_code, time_out=0):
        # vk_code = 'a'
        # vk_code.__class__.__name__ == 'str'
        # vk_code.upper()
        # kk
        # if(vk_code.__class__.)
        return self.dm_instance.WaitKey(vk_code, time_out)

    def KeyDown(self, vk_code):
        return self.dm_instance.KeyDown(vk_code)

    def KeyDownChar(self, key_str):
        return self.dm_instance.KeyDownChar(key_str)

    def KeyPress(self, vk_code):
        return self.dm_instance.KeyPress(vk_code)

    def KeyPressChar(self, key_str):
        return self.dm_instance.KeyPressChar(key_str)

    def KeyPressStr(self, key_str, delay):
        return self.dm_instance.KeyPressStr(key_str, delay)

    def KeyUp(self, vk_code):
        return self.dm_instance.KeyUp(vk_code)

    def KeyUpChar(self, key_str):
        return self.dm_instance.KeyUpChar(key_str)

    def LeftClick(self):
        return self.dm_instance.LeftClick()

    def LeftDoubleClick(self):
        return self.dm_instance.LeftDoubleClick()

    def LeftDown(self):
        return self.dm_instance.LeftDown()

    def LeftUp(self):
        return self.dm_instance.LeftUp()

    def MiddleClick(self):
        return self.dm_instance.MiddleClick()

    def MoveR(self, rx, ry):
        return self.dm_instance.MoveR(rx, ry)

    def MoveTo(self, x, y):
        return self.dm_instance.MoveTo(x, y)

    def MoveToEx(self, x, y, w, h):
        return self.dm_instance.MoveToEx(x, y, w, h)

    def RightClick(self):
        return self.dm_instance.RightClick()

    def RightDown(self):
        return self.dm_instance.RightDown()

    def RightUp(self):
        return self.dm_instance.RightUp()

    def WheelDown(self):
        return self.dm_instance.WheelDown()

    def WheelUp(self):
        return self.dm_instance.WheelUp()

    def FindData(self, hwnd, addr_range, data):
        return self.dm_instance.FindData(hwnd, addr_range, data)

    def FindDataEx(self, hwnd, addr_range, data, step, multi_thread, mode):
        return self.dm_instance.FindDataEx(hwnd, addr_range, data, step, multi_thread, mode)

    def DoubleToData(self, value):
        return self.dm_instance.DoubleToData(value)

    def FloatToData(self, value):
        return self.dm_instance.FloatToData(value)

    def GetModuleBaseAddr(self, hwnd, module):
        return self.dm_instance.GetModuleBaseAddr(hwnd, module)

    def IntToData(self, value, type):
        return self.dm_instance.IntToData(value, type)

    def ReadData(self, hwnd, addr, len):
        return self.dm_instance.ReadData(hwnd, addr, len)

    def ReadDouble(self, hwnd, addr):
        return self.dm_instance.ReadDouble(hwnd, addr)

    def ReadFloat(self, hwnd, addr):
        return self.dm_instance.ReadFloat(hwnd, addr)

    def ReadInt(self, hwnd, addr, type):
        return self.dm_instance.ReadInt(hwnd, addr, type)

    def ReadString(self, hwnd, addr, type, len):
        return self.dm_instance.ReadString(hwnd, addr, type, len)

    def StringToData(self, value, type):
        return self.dm_instance.StringToData(value, type)

    def WriteData(self, hwnd, addr, data):
        return self.dm_instance.WriteData(hwnd, addr, data)

    def WriteDouble(self, hwnd, addr, v):
        return self.dm_instance.WriteDouble(hwnd, addr, v)

    def WriteFloat(self, hwnd, addr, v):
        return self.dm_instance.WriteFloat(hwnd, addr, v)

    def WriteInt(self, hwnd, addr, type, v):
        return self.dm_instance.WriteInt(hwnd, addr, type, v)

    def WriteString(self, hwnd, addr, type, v):
        return self.dm_instance.WriteString(hwnd, addr, type, v)

    def CopyFile(self, src_file, dst_file, over):
        return self.dm_instance.CopyFile(src_file, dst_file, over)

    def CreateFolder(self, folder):
        return self.dm_instance.CreateFolder(folder)

    def DecodeFile(self, file, pwd):
        return self.dm_instance.DecodeFile(file, pwd)

    def DeleteFile(self, file):
        return self.dm_instance.DeleteFile(file)

    def DeleteFolder(self, folder):
        return self.dm_instance.DeleteFolder(folder)

    def DeleteIni(self, section, key, file):
        return self.dm_instance.DeleteIni(section, key, file)

    def DeleteIniPwd(self, section, key, file, pwd):
        return self.dm_instance.DeleteIniPwd(section, key, file, pwd)

    def DownloadFile(self, url, save_file, timeout):
        return self.dm_instance.DownloadFile(url, save_file, timeout)

    def EncodeFile(self, file, pwd):
        return self.dm_instance.EncodeFile(file, pwd)

    def GetFileLength(self, file):
        return self.dm_instance.GetFileLength(file)

    def IsFileExist(self, file):
        return self.dm_instance.IsFileExist(file)

    def MoveFile(self, src_file, dst_file):
        return self.dm_instance.MoveFile(src_file, dst_file)

    def ReadFile(self, file):
        return self.dm_instance.ReadFile(file)

    def ReadIni(self, section, key, file):
        return self.dm_instance.ReadIni(section, key, file)

    def ReadIniPwd(self, section, key, file, pwd):
        return self.dm_instance.ReadIniPwd(section, key, file, pwd)

    def SelectDirectory(self):
        return self.dm_instance.SelectDirectory()

    def SelectFile(self):
        return self.dm_instance.SelectFile()

    def WriteFile(self, file, content):
        return self.dm_instance.WriteFile(file, content)

    def WriteIni(self, section, key, value, file):
        return self.dm_instance.WriteIni(section, key, value, file)

    def WriteIniPwd(self, section, key, value, file, pwd):
        return self.dm_instance.WriteIniPwd(section, key, value, file, pwd)

    def GetNetTime(self):
        return self.dm_instance.GetNetTime()

    def GetOsType(self):
        return self.dm_instance.GetOsType()

    def GetScreenHeight(self):
        return self.dm_instance.GetScreenHeight()

    def GetScreenWidth(self):
        return self.dm_instance.GetScreenWidth()

    def GetTime(self):
        return self.dm_instance.GetTime()

    def Is64Bit(self):
        return self.dm_instance.Is64Bit()

    def RunApp(self, app_path, mode):
        return self.dm_instance.RunApp(app_path, mode)

    def Play(self, media_file):
        return self.dm_instance.Play(media_file)

    def Stop(self, id):
        return self.dm_instance.Stop(id)

    def Delay(self, mis):
        return self.dm_instance.Delay(mis)

    def ExitOs(self, type):
        return self.dm_instance.ExitOs(type)

    def Beep(self, duration=1000, f=800):
        return self.dm_instance.Beep(f, duration)
