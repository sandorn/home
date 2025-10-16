# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-05-21 16:26:08
LastEditTime : 2025-08-27 16:54:26
FilePath     : /CODE/xjLib/xt_damo/regsvr.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from __future__ import annotations

import ctypes
import os
from typing import Any

from win32com.client import Dispatch


def _create_dm_object():
    """创建大漠插件COM对象"""
    try:
        dm_instance = Dispatch('dm.dmsoft')
        print('创建大漠COM对象[dm.dmsoft]成功!')
        return dm_instance
    except Exception as e:
        print(f'--- 创建大漠COM对象[dm.dmsoft]失败 --- 错误: {e}')
        return None


def _runas_admin(cmd, ishide=False, waitsed=10):
    """以管理员权限运行命令"""

    # ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", f"/c {cmd}", None, 1)

    # 使用ShellExecuteEx 替代 ShellExecuteW ，以便等待进程完成
    # 结构体大小必须与ctypes.sizeof(SHELLEXECUTEINFO)一致
    class SHELLEXECUTEINFO(ctypes.Structure):
        _fields_ = [  # noqa
            ('cbSize', ctypes.c_ulong),
            ('fMask', ctypes.c_ulong),
            ('hwnd', ctypes.c_void_p),
            ('lpVerb', ctypes.c_wchar_p),
            ('lpFile', ctypes.c_wchar_p),
            ('lpParameters', ctypes.c_wchar_p),
            ('lpDirectory', ctypes.c_wchar_p),
            ('nShow', ctypes.c_int),
            ('hInstApp', ctypes.c_void_p),
            ('lpIDList', ctypes.c_void_p),
            ('lpClass', ctypes.c_wchar_p),
            ('hKeyClass', ctypes.c_void_p),
            ('dwHotKey', ctypes.c_ulong),
            ('hIcon', ctypes.c_void_p),
            ('hProcess', ctypes.c_void_p),
        ]

    sei = SHELLEXECUTEINFO()
    sei.cbSize = ctypes.sizeof(SHELLEXECUTEINFO)
    sei.fMask = 0x00000040  # SEE_MASK_NOCLOSEPROCESS
    sei.hwnd = None
    sei.lpVerb = 'runas'
    sei.lpFile = 'cmd.exe'
    sei.lpParameters = f'/C {cmd}'
    sei.lpDirectory = None
    sei.nShow = 1 if ishide else 0  # SW_HIDE

    success = ctypes.windll.shell32.ShellExecuteExW(ctypes.byref(sei))

    if success and sei.hProcess:
        # 等待进程完成，设置超时为10秒
        ctypes.windll.kernel32.WaitForSingleObject(sei.hProcess, 1000 * waitsed)
        ctypes.windll.kernel32.CloseHandle(sei.hProcess)  # 关闭进程句柄
        return True
    return False


class DmRegister:
    def __init__(self, dll_directory=''):
        """初始化大漠插件注册器，dll_directory: dm.dll所在目录或具体的dm.dll文件路径"""
        if not dll_directory:
            # 没指定目录就使用当前文件所在目录
            dll_directory = os.path.dirname(__file__)
            dll_directory = os.path.abspath(dll_directory)

        # 构建dll文件路径
        self.dll_path = dll_directory if dll_directory.endswith('.dll') else os.path.join(dll_directory, 'dm.dll')

        # 构建注册命令
        register_command = f'regsvr32.exe /s "{self.dll_path}"'

        # 初始化时设为None，后续会被赋值为大漠插件对象
        self.dm_instance: Any | None = None
        self.is_registered: bool = False
        self.execute(register_command)

    def execute(self, register_command):
        """运行注册过程，尝试创建大漠对象"""
        # 首先尝试直接创建大漠对象
        self.dm_instance = _create_dm_object()

        if self.dm_instance is not None:
            return self.dm_instance

        # 未注册时尝试注册
        print('尝试注册大漠插件...')
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()

        if is_admin:
            os.system(register_command)  # noqa: S605
            print(f'注册大漠插件： {register_command} ')
        else:
            if _runas_admin(register_command):
                print(f'以ShellExecuteEx注册大漠插件： {register_command} ')
            else:
                print('注册命令执行失败或无法获取进程句柄')

        # 注册后再次尝试创建大漠对象
        self.dm_instance = _create_dm_object()

        # 注册后仍然失败的情况
        if self.dm_instance is None:
            self.is_registered = False
            print('警告: 无法创建大漠对象！')
        else:
            self.is_registered = True
            return self.dm_instance
        return None

    def unregister(self):
        """取消注册大漠插件"""
        # 构造取消注册命令
        unregister_command = f'regsvr32.exe /u /s "{self.dll_path}"'

        if ctypes.windll.shell32.IsUserAnAdmin():
            os.system(unregister_command)  # noqa: S605
            print(f'已取消注册大漠插件： {unregister_command}')
        else:
            if _runas_admin(unregister_command):
                print(f'以ShellExecuteEx取消注册大漠插件：{unregister_command}')
            else:
                print('取消注册命令执行失败或无法获取进程句柄')
        self.is_registered = False
        self.dm_instance = None  # 清除大漠对象引用

    def __repr__(self):
        return f'dm.dll注册状态:{self.is_registered} ,大漠对象:{self.dm_instance} ,注册路径:{self.dll_path}'

    def __del__(self):
        """对象销毁时取消注册"""
        self.unregister()


if __name__ == '__main__':
    try:
        dm_reg = DmRegister()
        print(
            dm_reg,
            '\n',
            dm_reg.dm_instance.ver() if dm_reg.dm_instance else 'dm_instance is None',
        )
    except Exception as e:
        print(f'发生错误: {e}')

    print('程序结束')
