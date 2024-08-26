# !/usr/bin/env python
"""
==============================================================
Description  : 大漠插件库
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2021-04-14 17:24:09
FilePath     : /xjLib/xt_Dm.py
LastEditTime : 2021-04-16 13:39:27
Github       : https://github.com/sandorn/home
==============================================================
https://github.com/bode135/pydamo/tree/master
大漠只能使用32位python
"""

import ctypes
import os
import random
import time

# from comtypes.client import CreateObject
# from PyGameAuto.Dm import RegDm
from win32com.client import DispatchEx
from xt_class import AttrGetMixin

ran = random.randrange
delay = time.sleep
tim = time.time

random.seed(time.time())


def randelay(rand_start_time=50, rand_end_time=400):
    """随机延迟"""
    rand_time = random.randrange(rand_start_time, rand_end_time)
    delay(rand_time)


def sp2tab(源串: str, 分割1, 分割2=None):
    m = 源串.split(分割1)
    return m if (分割2 is None) else [item.split(分割2) for item in m]


Errs_D = {
    -1: "无法连接网络,(可能防火墙拦截,如果可以正常访问大漠插件网站,那就可以肯定是被防火墙拦截)",
    -2: "进程没有以管理员方式运行. (出现在win7 win8 vista 2008.建议关闭uac)",
    0: "失败 (未知错误)",
    1: "成功",
    2: "余额不足",
    3: "绑定了本机器,但是账户余额不足50元.",
    4: "注册码错误",
    5: "你的机器或者IP在黑名单列表中或者不在白名单列表中.",
    6: "非法使用插件. ",
    7: "你的帐号因为非法使用被封禁(如果是在虚拟机中使用插件,必须使用Reg或者RegEx,不能使用RegNoMac或者RegExNoMac,否则可能会造成封号,或者封禁机器)",
    8: "ver_info不在你设置的附加白名单中.",
    77: "机器码或者IP因为非法使用,而被封禁.(如果是在虚拟机中使用插件,必须使用Reg或者RegEx,不能使用RegNoMac或者RegExNoMac,否则可能会造成封号,或者封禁机器)封禁是全局的,如果使用了别人的软件导致77,也一样会导致所有注册码均无法注册。解决办法是更换IP,更换MAC.",
    -8: "版本附加信息长度超过了20",
    -9: "版本附加信息里包含了非法字母.",
}


class DmHelper(AttrGetMixin):
    """以管理员身份运行vscode"""

    path = os.path.split(os.path.realpath(__file__))[0]

    def __init__(self):
        """创建大漠对象"""
        try:
            self.dm = DispatchEx("dm.dmsoft")
        except Exception:
            # os.system(f'regsvr32 /s {dm_path}')
            self.dm = self.unreg_invoc()

        if self.dm is not None:
            self.RegDm()

        # self.dm.setDict(0,  "C:/num.txt")
        # self.dm.useDict(0)

    @classmethod
    def unreg_invoc(cls):
        """免注册调用,返回大漠对象"""
        print(111111, cls.path)
        dms = ctypes.windll.LoadLibrary(cls.path + r"\.res\DmReg.dll")
        print(222222, dms)
        dms.SetDllPathW(cls.path + r"\.res\dm.dll", 0)
        # return CreateObject('dm.dmsoft')
        return DispatchEx("dm.dmsoft")

    def RegDm(self):  # sourcery skip: raise-specific-error
        """输入大漠注册码"""
        reg_code = "jv965720b239b8396b1b7df8b768c919e86e10f"
        ver_info = "ddsyyc365"

        dmRegSult = self.dm.Reg(reg_code, ver_info)

        if dmRegSult != 1:
            raise Exception(f"Failed to reg! {Errs_D[dmRegSult]}")

    def 绑定窗口(
        self,
        局部窗口句柄,
        显示参数="normal",
        鼠标参数="normal",
        键盘参数="normal",
        绑定模式=0,
    ):
        ret = self.dm.BindWindow(局部窗口句柄, 显示参数, 鼠标参数, 键盘参数, 绑定模式)
        return self.dm.GetLastError() if (ret != 1) else True

    # #--------------------找字单击至消失--------------------#
    def 找字单击至消失(
        self, x_1, y_1, x_2, y_2, str_name, color_format, t=1500, 中心点=False
    ):
        intx = inty = 0
        起始时间 = tim()
        index = 0
        while (tim() - 起始时间) < t:
            ret = self.dm.FindStrE(
                x_1, y_1, x_2, y_2, str_name, color_format, 0.9, intx, inty
            )
            tab = ret.split("([^\\|]+)")
            intx, inty = int(tab[2]), int(tab[3])

            if intx > 0 and inty > 0:
                self.鼠标移动单击(intx, inty, 中心点)
                index += 1
                continue

            randelay()
        return index

    # #-------------------------找字单击------------------------#
    def 找字单击(
        self, x_1, y_1, x_2, y_2, str_name, color_format, t=1000, 中心点=False
    ):
        intx = inty = 0
        起始时间 = tim()
        while (tim() - 起始时间) < t:
            ret = self.dm.FindStrE(
                x_1, y_1, x_2, y_2, str_name, color_format, 0.9, intx, inty
            )
            tab = ret.split("([^\\|]+)")
            intx, inty = int(tab[2]), int(tab[3])

            if intx > 0 and inty > 0:
                self.鼠标移动单击(intx, inty, 中心点)
                return True

            randelay()

        return False

    # #-------------------------找字返回坐标-----------------#
    def 找字返回坐标(self, x_1, y_1, x_2, y_2, str_name, color_format, t=1000):
        intx = inty = 0
        起始时间 = tim()
        while (tim() - 起始时间) < t:
            ret = self.dm.FindStrE(
                x_1, y_1, x_2, y_2, str_name, color_format, 0.9, intx, inty
            )
            tab = ret.split("([^\\|]+)")
            intx, inty = int(tab[2]), int(tab[3])

            if intx > 0 and inty > 0:
                return intx, inty

            randelay()

        return -1, -1

    # #-------------------------简易找字-----------------#
    def 简易找字(self, x_1, y_1, x_2, y_2, str_name, color_format, t=1000):
        intx = inty = 0
        起始时间 = tim()
        while (tim() - 起始时间) < t:
            ret = self.dm.FindStrFast(x_1, y_1, x_2, y_2, str_name, color_format, 0.9)
            if ret[2] == -1:
                continue
            intx, inty = ret[1], ret[2]
            if intx > 0 and inty > 0:
                return intx, inty

            randelay()

        return -1, -1

    # #--------------------找图单击至消失--------------------#
    def 找图单击至消失(
        self, x_1, y_1, x_2, y_2, pic_name, t=1500, direct=0, 中心点=False
    ):
        intx = inty = 0
        起始时间 = tim()
        index = 0
        while (tim() - 起始时间) < t:
            ret = self.dm.FindPicE(x_1, y_1, x_2, y_2, pic_name, "000000", 0.9, direct)
            tab = ret.split("([^\\|]+)")
            intx, inty = int(tab[2]), int(tab[3])

            if intx > 0 and inty > 0:
                self.鼠标移动单击(intx, inty, 中心点)
                index += 1
                continue

            randelay()
        return index

    # #----------------------找图单击---------------------#
    def 找图单击(self, x_1, y_1, x_2, y_2, pic_name, t=1000, direct=0, 中心点=False):
        intx = inty = 0
        起始时间 = tim()
        while (tim() - 起始时间) < t:
            ret = self.dm.FindPicE(x_1, y_1, x_2, y_2, pic_name, "000000", 0.9, direct)
            tab = ret.split("([^\\|]+)")
            intx, inty = int(tab[2]), int(tab[3])

            if intx > 0 and inty > 0:
                self.鼠标移动单击(intx, inty, 中心点)
                return True

            randelay()

        return False

    # #-------------------------找图返回坐标-----------------#
    def 找图返回坐标(self, x_1, y_1, x_2, y_2, pic_name, t=1000, direct=0):
        intx = inty = 0
        起始时间 = tim()
        while (tim() - 起始时间) < t:
            ret = self.dm.FindPicE(x_1, y_1, x_2, y_2, pic_name, "000000", 0.9, direct)
            tab = ret.split("([^\\|]+)")
            intx, inty = int(tab[2]), int(tab[3])
            if intx > 0 and inty > 0:
                return intx, inty

            randelay()

        return -1, -1

    # #-------------------------简易找图-----------------#
    def 简易找图(self, x_1, y_1, x_2, y_2, pic_name, t=1000, direct=0):
        intx = inty = 0
        起始时间 = tim()
        while (tim() - 起始时间) < t:
            ret = self.dm.FindPic(x_1, y_1, x_2, y_2, pic_name, "000000", 0.9, direct)
            if ret[2] == -1:
                return
            intx, inty = ret[1], ret[2]
            if intx > 0 and inty > 0:
                return intx, inty

            randelay()

        return -1, -1

    # #----------------------鼠标移动单击------------------#
    def 鼠标移动单击(self, x, y, 中心点=False):
        x, y = int(x), int(y)
        self.dm.MoveTo(x, y)
        randelay(20, 50)
        self.dm.LeftClick()
        randelay(50, 200)

        if 中心点:
            self.dm.MoveTo(x + ran(50, 300), y + ran(50, 300))

    # #----------------------识别字------------------#
    def 简易识字(self, x_1, y_1, x_2, y_2, 颜色, 相似度=0.9, t=1000):
        认字 = ""
        起始时间 = tim()

        while (tim() - 起始时间) < t:
            if 认字 := self.dm.Ocr(x_1, y_1, x_2, y_2, 颜色, 相似度):
                return 认字
            randelay(50, 200)

        return False

    def keypress(self, key_str):
        """字符串序列, 依次按顺序按下其中的字符"""
        self.dm.KeyPressStr(key_str)

    def KeyPressChar(self, key_str):
        """按下指定的虚拟键码"""
        self.dm.KeyPressChar(key_str)


if __name__ == "__main__":
    DM = DmHelper()
    print(DM.FindStrFast(1, 2, 3, 4, "D", "000000", 0.9))
