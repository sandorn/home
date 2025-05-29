import ctypes
import os

from bdtime import tt
from win32com.client import Dispatch


def _Dispatch_Dm_object():
    try:
        dm = Dispatch("dm.dmsoft")  # 调用大漠插件
        print("调用大漠对象dm.dmsoft成功!")
        return dm
    except Exception as e:
        print(f"--- 调用大漠对象dm.dmsoft失败 --- 错误: {e}")
        return False


def get_regsvr_cmd():
    # dirpath_0 = os.getcwd()
    dirpath = __file__.replace('/', '\\')
    dirpath = os.path.dirname(dirpath)
    path_dll = os.path.join(dirpath, 'dm.dll')
    cmd_dll_0 = 'regsvr32 \"' + path_dll + '\" /s'
    return cmd_dll_0


class RegDM():
    def __init__(self, dirpath=''):
        cwd_0 = os.getcwd()

        if (not dirpath):
            # 没指定dm.dll就用默认的dm.dll
            dirpath = __file__.replace('/', '\\')
            dirpath = os.path.dirname(dirpath)

        if (dirpath.endswith('.dll')):
            path_dll = dirpath
        else:
            path_dll = os.path.join(dirpath, 'dm.dll')

        cmd_dll_0 = f'regsvr32 /s "{path_dll}"'

        self.dirpath_0 = cwd_0
        self.dirpath = dirpath
        self.path_dll = path_dll
        self.cmd_dll_0 = cmd_dll_0
        self.dm = False

    def reg(self):
        self.dm = _Dispatch_Dm_object()

        if self.dm is not False:
            print("大漠插件已注册！")
            print(f"大漠对象已创建: {self.dm}")
        else:
            print("大漠插件未注册，尝试注册...")
            if ctypes.windll.shell32.IsUserAnAdmin():
                os.system(self.cmd_dll_0)
                print(f"已将 {self.path_dll} 注册到系统...")
                self.dm = _Dispatch_Dm_object()
            else:
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", "cmd.exe", "/C %s" % self.cmd_dll_0, None, 1
                )
                tt.sleep(3)
                print(f"已将 {self.path_dll} 注册到系统 by runas...")
                self.dm = _Dispatch_Dm_object()  # 调用大漠插件

        return self.dm

    def unreg_dm(self):
        # 构造 regsvr32 命令
        cmd = f'regsvr32 /u /s "{self.path_dll}"'

        # 检查是否以管理员权限运行
        if ctypes.windll.shell32.IsUserAnAdmin():
            os.system(cmd)
            print(f"已取消注册 {self.path_dll}")
        else:
            # 如果不是管理员权限，尝试以管理员权限重新运行
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", "cmd.exe", f"/C {cmd}", None, 1
            )
            print(f"以管理员权限取消注册 {self.path_dll}")
            self.dm = False  # 清除大漠对象引用

    @property
    def is_reg(self):
        ret = _Dispatch_Dm_object()
        if (ret):
            return True
        else:
            return False

    def __repr__(self):
        ret = f"dm.dll注册状态:{self.is_reg} ,大漠对象:{self.dm} ,注册路径:{self.path_dll}"
        return ret


if __name__ == '__main__':
    # import platform

    # print(platform.architecture())
    Dm = RegDM()

    Dm.reg()

    print(11111111111111111, Dm)
    Dm.unreg_dm()
    print(22222222222222222, Dm)
    print("结束")