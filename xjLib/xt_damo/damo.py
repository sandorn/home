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
from key import Key
from mouse import Mouse
from regsvr import RegDM

_Reg_code = "jv965720b239b8396b1b7df8b768c919e86e10f"
_Ver_info = "ddsyyc365"

KeyMethonTuple = (
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

MouseMethonTuple = (
    "position",
    "set_delay",
    "move_r",
    "move_to",
    "click_left",
    "click_right",
)

ApiProxyMethonTuple = (
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

class DM:
    def __init__(self, dm_dirpath=None):
        reg_dm = RegDM(dm_dirpath)
        self.dm = reg_dm.reg()
        self.CoreEngine = CoreEngine(self.dm)
        self.ApiProxy = ApiProxy(self.dm)
        self.Key = Key(self.dm)
        self.Mouse = Mouse(self.dm)
        self.RegDM = reg_dm

        _ret = self.dm.Reg(_Reg_code, _Ver_info)
        if _ret != 1:
            raise (f"授权失败,错误代码：{_ret} | 授权问题： errs[_ret]")

        if not all([self.dm, self.CoreEngine, self.ApiProxy]):
            raise RuntimeError("模块初始化失败")

        print("版本：", self.ver(), "，ID：", self.GetID())

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
        if key in ("__repr__", "unreg_dm"):
            return self.__dict__[key]

        # 使用字典映射替代多个if-elif
        method_mapping = {
            **{k: (self.Key, k) for k in KeyMethonTuple},
            **{k: (self.Mouse, k) for k in MouseMethonTuple},
            **{k: (self.ApiProxy, k) for k in ApiProxyMethonTuple},
        }

        if key in method_mapping:
            obj, attr = method_mapping[key]
            return getattr(obj, attr)

        # 最后尝试大漠原生方法
        try:
            if __name__ == "__main__":
                print(f"AttrGet: {key} in self.dm")
            return getattr(self.dm, key)
        except AttributeError:
            return None


if __name__ == "__main__":

    dm = DM()
    print(dm.ver())
    ms = Mouse(dm)
    print(111111111, ms.position)
    x, y = (1300, 800)
    ms.move_to(x, y)
    print(222222222, ms.position)
    ms.click_right(x, y, 2)
    sleep(1)
    dm.LeftClick()
    print(333333333, ms.position)
    sleep(1)
    # 键盘操作
    kk = Key(dm)
    kk.down_up("A", 1)  # 测试用，1秒后按下a键
    dm.down_up("B")  # 按下a键
    sleep(1)
    dm.unreg_dm()  # 取消注册大漠插件
