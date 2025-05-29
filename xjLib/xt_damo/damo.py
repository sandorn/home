# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-05-21 16:26:08
LastEditTime : 2025-05-28 14:42:20
FilePath     : /CODE/xjLib/xt_damo/damo.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from time import sleep

from apiproxy import ApiProxy
from coreengine import CoreEngine
from regsvr import RegDM

_Reg_code = "jv965720b239b8396b1b7df8b768c919e86e10f"
_Ver_info = "ddsyyc365"

keyinKey = (
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

keyinMouse = (
    "position",
    "set_delay",
    "move_r",
    "move_to",
    "click_left",
    "click_right",
)

keyinApiProxy = (
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
    "鼠标移动单击",
    "sendkey",
    "简易识字",
    "圆形渐开找鼠标",
    "散点渐开找鼠标",
    "椭圆渐开找鼠标",
    "方形渐开找鼠标",
)


class DM:
    def __init__(self, dm_dirpath=None):
        reg_dm = RegDM(dm_dirpath)
        self.dm = reg_dm.reg()
        self.CoreEngine = CoreEngine(self.dm)
        self.ApiProxy = ApiProxy(self.dm)
        self.Key = Key(self.dm)
        self.Mouse = Mouse(self.dm)
        self.RegDM = reg_dm

        self.dm.Reg(_Reg_code, _Ver_info)

        print("版本：", self.ver(), "，ID：", self.GetID())

        if not all([self.dm, self.CoreEngine, self.ApiProxy]):
            raise RuntimeError("模块初始化失败")

    def unreg_dm(self):
        self.RegDM.unreg_dm()
        self.dm = False
        self.CoreEngine = False
        self.ApiProxy = False
        self.Key = False
        self.Mouse = False
        self.RegDM = False

    def __repr__(self):
        ret = f"版本： {self.ver()} ID：{self.GetID()}"
        return ret

    def __getattr__(self, key: str):
        try:
            if key in ("__repr__", "unreg_dm"):
                if __name__ == "__main__":
                    print(f"AttrGetMixin: {key} in self.__dict__")
                return self.__dict__[key]
            elif key in keyinKey:
                if __name__ == "__main__":
                    print(f"AttrGetMixin: {key} in self.Key")
                return getattr(self.Key, key)
            elif key in keyinMouse:
                if __name__ == "__main__":
                    print(f"AttrGetMixin: {key} in self.Mouse")
                return getattr(self.Mouse, key)
            elif key in keyinApiProxy:
                if __name__ == "__main__":
                    print(f"AttrGetMixin: {key} in self.ApiProxy")
                return getattr(self.ApiProxy, key)

            else:
                if __name__ == "__main__":
                    print(f"AttrGetMixin: {key} in self.dm")
                return getattr(self.dm, key)
            return super().__getattribute__(key)

        except AttributeError:
            return None


if __name__ == "__main__":
    from key import Key
    from mouse import Mouse

    dm = DM()
    print(dm.ver())
    ms = Mouse(dm)
    print(111111111, ms.position)
    x, y = (1300, 800)
    ms.move_to(x, y)
    sleep(1)
    ms.click_left(x, y, 2)
    sleep(1)
    ms.click_right(x, y, 1)

    print(222222222, ms.position)
    dm.LeftClick()
    print(333333333, ms.position)

    # 键盘操作
    kk = Key(dm)
    kk.down_up("A", 1)  # 测试用，1秒后按下a键
    dm.down_up("B")  # 按下a键
    dm.unreg_dm()  # 取消注册大漠插件
