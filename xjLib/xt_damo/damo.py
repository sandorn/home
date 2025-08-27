# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-05-21 16:26:08
LastEditTime : 2025-06-06 10:18:51
FilePath     : /CODE/xjLib/xt_damo/damo.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from time import sleep
from typing import Any, Optional, Tuple

from apiproxy import ApiProxy
from coreengine import CoreEngine
from key import Key
from mouse import Mouse
from regsvr import DmRegister

_Reg_code = "jv965720b239b8396b1b7df8b768c919e86e10f"
_Ver_info = "ddsyyc365"

key_methods = (
    "get_ord",
    "conv_ord",
    "conv_chr",
    "conv",
    "state",
    "press",
    "down",
    "up",
    "down_up",
)

mouse_methods = (
    "position",
    "set_delay",
    "move_r",
    "move_to",
    "click_left",
    "click_right",
    "safe_click",
)

apiproxy_methods = (
    "绑定窗口",
    "解绑窗口",
    "获取窗口标题",
    "找字单击至消失",
    "找字单击",
    "找字返回坐标",
    "简易找字",
    "找图单击至消失",
    "找图单击",
    "找图返回坐标",
    "简易找图",
    "简易识字",
    "圆形渐开找鼠标",
    "散点渐开找鼠标",
    "椭圆渐开找鼠标",
    "方形渐开找鼠标",
)

coreengine_methods = (
    "GetDmCount",
    "GetID",
    "ver",
    "GetDir",
    "GetBasePath",
    "GetPath",
    "SetDisplayInput",
    "SetShowErrorMsg",
    "Capture",
    "FindPic",
    "FindColor",
    "LoadPic",
    "FreePic",
    "GetColor",
    "GetPicSize",
    "GetColorBGR",
    "BGR2RGB",
    "CmpColor",
    "BindWindow",
    "UnBindWindow",
    "IsBind",
    "MoveWindow",
    "FindWindow",
    "ClientToScreen",
    "ScreenToClient",
    "FindWindowByProcess",
    "FindWindowByProcessId",
    "GetClientRect",
    "GetClientSize",
    "GetWindowRect",
    "GetWindow",
    "GetWindowProcessPath",
    "SetWindowSize",
    "SetWindowState",
    "SetWindowText",
    "SetWindowTransparent",
    "EnumWindow",
    "EnumWindowByProcess",
    "EnumWindowSuper",
    "GetCursorPos",
    "GetKeyState",
    "SetKeypadDelay",
    "SetMouseDelay",
    "WaitKey",
    "KeyDown",
    "KeyDownChar",
    "KeyPress",
    "KeyPressChar",
    "KeyPressStr",
    "KeyUp",
    "KeyUpChar",
    "LeftClick",
    "LeftDoubleClick",
    "LeftDown",
    "LeftUp",
    "MiddleClick",
    "MoveR",
    "MoveTo",
    "MoveToEx",
    "RightClick",
    "RightDown",
    "RightUp",
    "WheelDown",
    "WheelUp",
    "FindData",
    "FindDataEx",
    "DoubleToData",
    "FloatToData",
    "GetModuleBaseAddr",
    "IntToData",
    "ReadData",
    "ReadDouble",
    "ReadFloat",
    "ReadInt",
    "ReadString",
    "StringToData",
    "WriteData",
    "WriteDouble",
    "WriteFloat",
    "WriteInt",
    "WriteString",
    "CopyFile",
    "CreateFolder",
    "DecodeFile",
    "DeleteFile",
    "DeleteFolder",
    "DeleteIni",
    "DeleteIniPwd",
    "DownloadFile",
    "EncodeFile",
    "GetFileLength",
    "IsFileExist",
    "MoveFile",
    "ReadFile",
    "ReadIni",
    "ReadIniPwd",
    "SelectDirectory",
    "SelectFile",
    "WriteFile",
    "WriteIni",
    "WriteIniPwd",
    "GetNetTime",
    "GetOsType",
    "GetScreenHeight",
    "GetScreenWidth",
    "GetTime",
    "Is64Bit",
    "RunApp",
    "Play",
    "Stop",
    "Delay",
    "ExitOs",
    "Beep",
)

errs = {
    -1: "无法连接网络",
    -2: "进程没有以管理员方式运行，win7 win8 vista 2008 建议关闭uac)",
    0: "失败 (未知错误)",
    1: "成功",
    2: "余额不足",
    3: "绑定了本机器,但是账户余额不足50元.",
    4: "注册码错误",
    5: "你的机器或者IP在黑名单列表中或者不在白名单列表中.",
    6: "非法使用插件.",
    7: "你的帐号因为非法使用被封禁.",
    8: "ver_info不在你设置的附加白名单中.",
    77: "机器码或者IP因为非法使用,而被封禁.",
    -8: "版本附加信息长度超过了20",
    -9: "版本附加信息里包含了非法字母.",
}


class DmExcute:
    def __init__(self, dm_dirpath: Optional[str] = None):
        self.RegDM = DmRegister(dm_dirpath)
        self.dm_instance = self.RegDM.dm_instance
        self.Key = Key(self.dm_instance)
        self.Mouse = Mouse(self.dm_instance)
        self.ApiProxy = ApiProxy(self.dm_instance)
        self.CoreEngine = CoreEngine(self.dm_instance)

        # 更严格的检查，确保dm_instance不为None
        if self.dm_instance is None:
            raise RuntimeError("大漠插件实例初始化失败")

        # 确保不为None
        if not all([self.Key, self.Mouse, self.CoreEngine, self.ApiProxy]):
            raise RuntimeError("模块初始化失败")

        _ret = self.dm_instance.Reg(_Reg_code, _Ver_info)

        if _ret != 1:
            raise RuntimeError(
                f"授权失败,错误代码：{_ret} | 授权问题： {errs.get(_ret, '未知错误')}"
            )

    def __repr__(self) -> str:
        """返回对象的字符串表示"""
        _str = ""
        try:
            version = self.ver()
            dm_id = self.GetID()
            _str = f"版本：{version} , ID：{dm_id}"
        except Exception as e:
            _str = f"获取版本和ID时出错: {e}"
        return _str

    def __getattr__(self, key: str) -> Any:
        if key in ("__repr__", "unreg"):
            return self.__dict__[key]

        # 使用字典映射替代多个if-elif
        method_mapping = {
            **{k: (self.Key, k) for k in key_methods},
            **{k: (self.Mouse, k) for k in mouse_methods},
            **{k: (self.ApiProxy, k) for k in apiproxy_methods},
            **{k: (self.CoreEngine, k) for k in coreengine_methods},
        }

        if key in method_mapping:
            obj, attr = method_mapping[key]
            # 确保obj不为None
            if obj is not None:
                try:
                    return getattr(obj, attr)
                except AttributeError:
                    pass

        # 最后尝试大漠原生方法，确保dm_instance不为None
        if self.dm_instance is not None:
            try:
                if __name__ == "__main__":
                    print(f"AttrGet: {key} in self.dm_instance")
                return getattr(self.dm_instance, key)
            except AttributeError:
                pass

        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{key}'"
        )


def conv_to_rgb(color: str) -> Tuple[int, int, int]:
    """将16进制颜色字符串转换为RGB元组"""
    RGB_str = [color[:2], color[2:4], color[4:6]]
    RGB = [int(i, 16) for i in RGB_str]
    return tuple(RGB)  # type: ignore


if __name__ == "__main__":
    dm = DmExcute()
    print(dm.ver())
    print(111111111, dm.position)
    x, y = dm.position
    dm.safe_click(x + 100, y + 100)
    print(222222222, dm.position)
    dm.safe_click(x, y)
    dm.LeftClick()
    print(333333333)
    # 键盘操作
    # dm.down_up("A", 1)  # 测试用，1秒后按下a键
    # dm.down_up("B")

    xy_ls = [[10, 0], [10, 0], [10, 0], [-10, 0], [-10, 0], [-10, 0]]
    x_ls = []

    for i in range(20):
        xy_i = i % len(xy_ls)
        xy_v = xy_ls[xy_i]
        dm.move_r(*xy_v)

        x_i = dm.position[0]
        x_ls.append(x_i)
        delta_x = 0 if len(x_ls) < 2 else x_ls[-1] - x_ls[-2]
        print(
            f"--- {i} --- Mouse position: {x_i}, target_x: {xy_v}, delta_x: {delta_x}"
        )

        sleep(0.1)
        x, y = dm.position
        color = dm.GetColor(x, y)

        print(color, "鼠标位置颜色RGB值:", conv_to_rgb(color))
