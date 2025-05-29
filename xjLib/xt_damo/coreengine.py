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
from typing import Any


class CoreEngine:
    def __init__(self, dmobject: Any) -> None:
        """核心功能封装
        Args:
            dmobject: 大漠插件实例
        """
        if not dmobject:
            raise ValueError("dmobject cannot be None")
        self.dm = dmobject

    def __repr__(self):
        ret = f"版本： {self.ver()} ID：{self.GetID()}"
        return ret

    def GetDmCount(self):
        return self.dm.GetDmCount()

    def GetID(self):
        return self.dm.GetID()

    def ver(self):
        return self.dm.ver()

    def GetDir(self, type):
        return self.dm.GetDir(type)

    def GetBasePath(self):
        return self.dm.GetBasePath()

    def GetPath(self):
        return self.dm.GetPath()

    def SetDisplayInput(self, mode):
        return self.dm.SetDisplayInput(mode)

    def SetShowErrorMsg(self, show):
        return self.dm.SetShowErrorMsg(show)

    def Capture(self, x1, y1, x2, y2, file):
        return self.dm.Capture(x1, y1, x2, y2, file)

    def FindPic(
        self,
        x1,
        y1,
        x2,
        y2,
        pic_name,
        delta_color="101010",
        sim=0.9,
        dir=0,
        # intX=0,
        # intY=0,
    ):
        return self.dm.FindPic(
            x1, y1, x2, y2, pic_name, delta_color=delta_color, sim=sim, dir=dir
        )

    def FindColor(self, x1, y1, x2, y2, color, sim, dir, intX, intY):
        # _, x0, y0 = dm.FindColor(0, 0, 1200, 800, color = "757575", sim = 1.0, dir = 1,  intX = 0, intY = 0)
        return self.dm.FindColor(x1, y1, x2, y2, color, sim, dir, intX, intY)

    def LoadPic(self, pic_name):
        return self.dm.LoadPic(pic_name)

    def FreePic(self, pic_name):
        return self.dm.FreePic(pic_name)

    def GetColor(self, x, y):
        return self.dm.GetColor(x, y)

    def GetPicSize(self, pic_name):
        return self.dm.GetPicSize(pic_name)

    def GetColorBGR(self, x, y):
        return self.dm.GetColorBGR(x, y)

    def BGR2RGB(self, bgr_color):
        return self.dm.BGR2RGB(bgr_color)

    def CmpColor(self, x, y, color, sim):
        return self.dm.CmpColor(x, y, color, sim)

    def BindWindow(
        self,
        hwnd,
        display=["normal", "gdi", "gdi2", "dx", "dx2"][1],
        mouse=["normal", "windows", "windows2", "windows3", "dx", "dx2"][1],
        keypad=["normal", "windows", "dx"][1],
        mode=[0, 1, 2, 3, 4, 5, 6, 7, 101, 103][0],
    ):
        return self.dm.BindWindow(hwnd, display, mouse, keypad, mode)

    def UnBindWindow(self):
        return self.dm.UnBindWindow()

    def IsBind(self, hwnd):
        return self.dm.IsBind(hwnd)

    def MoveWindow(self, hwnd, x, y):
        return self.dm.MoveWindow(hwnd, x, y)

    def FindWindow(self, class_name="", title_name=""):
        return self.dm.FindWindow(class_name, title_name)

    def ClientToScreen(self, hwnd, x, y):
        return self.dm.ClientToScreen(hwnd, x, y)

    def ScreenToClient(self, hwnd, x, y):
        return self.dm.ScreenToClient(hwnd, x, y)

    def FindWindowByProcess(self, process_name, class_name, title_name):
        return self.dm.FindWindowByProcess(process_name, class_name, title_name)

    def FindWindowByProcessId(self, process_id, class_, title):
        return self.dm.FindWindowByProcessId(process_id, class_, title)

    def GetClientRect(self, hwnd, x1, y1, x2, y2):
        return self.dm.GetClientRect(hwnd, x1, y1, x2, y2)

    def GetClientSize(self, hwnd, width, height):
        return self.dm.GetClientSize(hwnd, width, height)

    def GetWindowRect(self, hwnd, x1, y1, x2, y2):
        return self.dm.GetWindowRect(hwnd, x1, y1, x2, y2)

    def GetWindow(self, hwnd, flag):
        return self.dm.GetWindow(hwnd, flag)

    def GetWindowProcessPath(self, hwnd):
        return self.dm.GetWindowProcessPath(hwnd)

    def SetWindowSize(self, hwnd, width, height):
        return self.dm.SetWindowSize(hwnd, width, height)

    def SetWindowState(self, hwnd, flag):
        return self.dm.SetWindowState(hwnd, flag)

    def SetWindowText(self, hwnd, title):
        return self.dm.SetWindowText(hwnd, title)

    def SetWindowTransparent(self, hwnd, trans):
        return self.dm.SetWindowTransparent(hwnd, trans)

    def EnumWindow(self, parent, title, class_name, filter):
        return self.dm.EnumWindow(parent, title, class_name, filter)

    def EnumWindowByProcess(self, process_name, title, class_name, filter):
        return self.dm.EnumWindowByProcess(process_name, title, class_name, filter)

    def EnumWindowSuper(self, spec1, flag1, type1, spec2, flag2, type2, sort):
        return self.dm.EnumWindowSuper(spec1, flag1, type1, spec2, flag2, type2, sort)

    # endregion

    # key_mouse
    # region key_mouse
    def GetCursorPos(self, x=0, y=0):
        return self.dm.GetCursorPos(x, y)

    def GetKeyState(self, vk_code):
        return self.dm.GetKeyState(vk_code)

    def SetKeypadDelay(
        self, type=["normal", "windows", "dx"][-1], delay=[0.03, 0.01, 0.05][-1]
    ):
        return self.dm.SetKeypadDelay(type, delay)

    def SetMouseDelay(
        self, type=["normal", "windows", "dx"][-1], delay=[0.03, 0.01, 0.04][-1]
    ):
        return self.dm.SetMouseDelay(type, delay)

    def WaitKey(self, vk_code, time_out=0):
        # vk_code = 'a'
        # vk_code.__class__.__name__ == 'str'
        # vk_code.upper()
        # kk
        # if(vk_code.__class__.)
        return self.dm.WaitKey(vk_code, time_out)

    # def WaitKey(vk_code,time_out = 0):
    #     # vk_code = 'a'
    #     # vk_code.__class__.__name__ == 'str'
    #     # vk_code.upper()
    #     # kk
    #     # if(vk_code.__class__.)
    #
    #     return print(vk_code, time_out)
    # WaitKey('a')

    def KeyDown(self, vk_code):
        return self.dm.KeyDown(vk_code)

    def KeyDownChar(self, key_str):
        return self.dm.KeyDownChar(key_str)

    def KeyPress(self, vk_code):
        return self.dm.KeyPress(vk_code)

    def KeyPressChar(self, key_str):
        return self.dm.KeyPressChar(key_str)

    def KeyPressStr(self, key_str, delay):
        return self.dm.KeyPressStr(key_str, delay)

    def KeyUp(self, vk_code):
        return self.dm.KeyUp(vk_code)

    def KeyUpChar(self, key_str):
        return self.dm.KeyUpChar(key_str)

    def LeftClick(
        self,
    ):
        return self.dm.LeftClick()

    def LeftDoubleClick(
        self,
    ):
        return self.dm.LeftDoubleClick()

    def LeftDown(
        self,
    ):
        return self.dm.LeftDown()

    def LeftUp(
        self,
    ):
        return self.dm.LeftUp()

    def MiddleClick(
        self,
    ):
        return self.dm.MiddleClick()

    def MoveR(self, rx, ry):
        return self.dm.MoveR(rx, ry)

    def MoveTo(self, x, y):
        return self.dm.MoveTo(x, y)

    def MoveToEx(self, x, y, w, h):
        return self.dm.MoveToEx(x, y, w, h)

    def RightClick(
        self,
    ):
        return self.dm.RightClick()

    def RightDown(
        self,
    ):
        return self.dm.RightDown()

    def RightUp(
        self,
    ):
        return self.dm.RightUp()

    def WheelDown(
        self,
    ):
        return self.dm.WheelDown()

    def WheelUp(self):
        return self.dm.WheelUp()

    def FindData(self, hwnd, addr_range, data):
        return self.dm.FindData(hwnd, addr_range, data)

    def FindDataEx(self, hwnd, addr_range, data, step, multi_thread, mode):
        return self.dm.FindDataEx(hwnd, addr_range, data, step, multi_thread, mode)

    def DoubleToData(self, value):
        return self.dm.DoubleToData(value)

    def FloatToData(self, value):
        return self.dm.FloatToData(value)

    def GetModuleBaseAddr(self, hwnd, module):
        return self.dm.GetModuleBaseAddr(hwnd, module)

    def IntToData(self, value, type):
        return self.dm.IntToData(value, type)

    def ReadData(self, hwnd, addr, len):
        return self.dm.ReadData(hwnd, addr, len)

    def ReadDouble(self, hwnd, addr):
        return self.dm.ReadDouble(hwnd, addr)

    def ReadFloat(self, hwnd, addr):
        return self.dm.ReadFloat(hwnd, addr)

    def ReadInt(self, hwnd, addr, type):
        return self.dm.ReadInt(hwnd, addr, type)

    def ReadString(self, hwnd, addr, type, len):
        return self.dm.ReadString(hwnd, addr, type, len)

    def StringToData(self, value, type):
        return self.dm.StringToData(value, type)

    def WriteData(self, hwnd, addr, data):
        return self.dm.WriteData(hwnd, addr, data)

    def WriteDouble(self, hwnd, addr, v):
        return self.dm.WriteDouble(hwnd, addr, v)

    def WriteFloat(self, hwnd, addr, v):
        return self.dm.WriteFloat(hwnd, addr, v)

    def WriteInt(self, hwnd, addr, type, v):
        return self.dm.WriteInt(hwnd, addr, type, v)

    def WriteString(self, hwnd, addr, type, v):
        return self.dm.WriteString(hwnd, addr, type, v)

    def CopyFile(self, src_file, dst_file, over):
        return self.dm.CopyFile(src_file, dst_file, over)

    def CreateFolder(self, folder):
        return self.dm.CreateFolder(folder)

    def DecodeFile(self, file, pwd):
        return self.dm.DecodeFile(file, pwd)

    def DeleteFile(self, file):
        return self.dm.DeleteFile(file)

    def DeleteFolder(self, folder):
        return self.dm.DeleteFolder(folder)

    def DeleteIni(self, section, key, file):
        return self.dm.DeleteIni(section, key, file)

    def DeleteIniPwd(self, section, key, file, pwd):
        return self.dm.DeleteIniPwd(section, key, file, pwd)

    def DownloadFile(self, url, save_file, timeout):
        return self.dm.DownloadFile(url, save_file, timeout)

    def EncodeFile(self, file, pwd):
        return self.dm.EncodeFile(file, pwd)

    def GetFileLength(self, file):
        return self.dm.GetFileLength(file)

    def IsFileExist(self, file):
        return self.dm.IsFileExist(file)

    def MoveFile(self, src_file, dst_file):
        return self.dm.MoveFile(src_file, dst_file)

    def ReadFile(self, file):
        return self.dm.ReadFile(file)

    def ReadIni(self, section, key, file):
        return self.dm.ReadIni(section, key, file)

    def ReadIniPwd(self, section, key, file, pwd):
        return self.dm.ReadIniPwd(section, key, file, pwd)

    def SelectDirectory(self):
        return self.dm.SelectDirectory()

    def SelectFile(self):
        return self.dm.SelectFile()

    def WriteFile(self, file, content):
        return self.dm.WriteFile(file, content)

    def WriteIni(self, section, key, value, file):
        return self.dm.WriteIni(section, key, value, file)

    def WriteIniPwd(self, section, key, value, file, pwd):
        return self.dm.WriteIniPwd(section, key, value, file, pwd)

    def GetNetTime(self):
        return self.dm.GetNetTime()

    def GetOsType(self):
        return self.dm.GetOsType()

    def GetScreenHeight(self):
        return self.dm.GetScreenHeight()

    def GetScreenWidth(self):
        return self.dm.GetScreenWidth()

    def GetTime(self):
        return self.dm.GetTime()

    def Is64Bit(self):
        return self.dm.Is64Bit()

    def RunApp(self, app_path, mode):
        return self.dm.RunApp(app_path, mode)

    def Play(self, media_file):
        return self.dm.Play(media_file)

    def Stop(self, id):
        return self.dm.Stop(id)

    def Delay(self, mis):
        return self.dm.Delay(mis)

    def ExitOs(self, type):
        return self.dm.ExitOs(type)

    def Beep(self, duration=1000, f=800):
        return self.dm.Beep(f, duration)
