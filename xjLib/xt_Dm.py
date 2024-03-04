# !/usr/bin/env python
# -*- coding: utf-8 -*-
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
    7:
    "你的帐号因为非法使用被封禁(如果是在虚拟机中使用插件,必须使用Reg或者RegEx,不能使用RegNoMac或者RegExNoMac,否则可能会造成封号,或者封禁机器)",
    8: "ver_info不在你设置的附加白名单中.",
    77:
    "机器码或者IP因为非法使用,而被封禁.(如果是在虚拟机中使用插件,必须使用Reg或者RegEx,不能使用RegNoMac或者RegExNoMac,否则可能会造成封号,或者封禁机器)封禁是全局的,如果使用了别人的软件导致77,也一样会导致所有注册码均无法注册。解决办法是更换IP,更换MAC.",
    -8: "版本附加信息长度超过了20",
    -9: "版本附加信息里包含了非法字母.",
}


class DmHelper:
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
            raise Exception(f'Failed to reg! {Errs_D[dmRegSult]}')

    def 绑定窗口(self,
             局部窗口句柄,
             显示参数="normal",
             鼠标参数="normal",
             键盘参数="normal",
             绑定模式=0):
        ret = self.dm.BindWindow(局部窗口句柄, 显示参数, 鼠标参数, 键盘参数, 绑定模式)
        return self.dm.GetLastError() if (ret != 1) else True

    # #--------------------找字单击至消失--------------------#
    def 找字单击至消失(self,
                x_1,
                y_1,
                x_2,
                y_2,
                str_name,
                color_format,
                t=1500,
                中心点=False):
        intx = inty = 0
        起始时间 = tim()
        index = 0
        while (tim() - 起始时间) < t:
            ret = self.dm.FindStrE(x_1, y_1, x_2, y_2, str_name, color_format,
                                   0.9, intx, inty)
            tab = ret.split("([^\\|]+)")
            intx, inty = int(tab[2]), int(tab[3])

            if intx > 0 and inty > 0:
                self.鼠标移动单击(intx, inty, 中心点)
                index += 1
                continue

            randelay()
        return index

    # #-------------------------找字单击------------------------#
    def 找字单击(self,
             x_1,
             y_1,
             x_2,
             y_2,
             str_name,
             color_format,
             t=1000,
             中心点=False):
        intx = inty = 0
        起始时间 = tim()
        while (tim() - 起始时间) < t:
            ret = self.dm.FindStrE(x_1, y_1, x_2, y_2, str_name, color_format,
                                   0.9, intx, inty)
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
            ret = self.dm.FindStrE(x_1, y_1, x_2, y_2, str_name, color_format,
                                   0.9, intx, inty)
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
            ret = self.dm.FindStrFast(x_1, y_1, x_2, y_2, str_name,
                                      color_format, 0.9)
            if ret[2] == -1:
                continue
            intx, inty = ret[1], ret[2]
            if intx > 0 and inty > 0:
                return intx, inty

            randelay()

        return -1, -1

    # #--------------------找图单击至消失--------------------#
    def 找图单击至消失(self,
                x_1,
                y_1,
                x_2,
                y_2,
                pic_name,
                t=1500,
                direct=0,
                中心点=False):
        intx = inty = 0
        起始时间 = tim()
        index = 0
        while (tim() - 起始时间) < t:
            ret = self.dm.FindPicE(x_1, y_1, x_2, y_2, pic_name, "000000", 0.9,
                                   direct)
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
            ret = self.dm.FindPicE(x_1, y_1, x_2, y_2, pic_name, "000000", 0.9,
                                   direct)
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
            ret = self.dm.FindPicE(x_1, y_1, x_2, y_2, pic_name, "000000", 0.9,
                                   direct)
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
            ret = self.dm.FindPic(x_1, y_1, x_2, y_2, pic_name, "000000", 0.9,
                                  direct)
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
        '''字符串序列, 依次按顺序按下其中的字符'''
        self.dm.KeyPressStr(key_str)

    def KeyPressChar(self, key_str):
        '''按下指定的虚拟键码'''
        self.dm.KeyPressChar(key_str)


"""
#----------------------大漠插件------------------#
# dm内部函数
# 大漠插件Foobar
CreateFoobarCustom(hwnd, x, y, pic_name, trans_color, sim) = 根据指定的位图创建一个自定义形状的窗口,返回:创建成功的窗口句柄
CreateFoobarEllipse(hwnd, x, y, w, h) = 创建一个椭圆窗口,返回:创建成功的窗口句柄
CreateFoobarRect(hwnd, x, y, w, h) = 创建一个矩形窗口,返回:创建成功的窗口句柄
CreateFoobarRoundRect(hwnd, x, y, w, h, rw, rh) = 创建一个圆角矩形窗口,返回:创建成功的窗口句柄
FoobarClearText(hwnd) = 清除指定的Foobar滚动文本区,返回:0:失败1:成功
FoobarClose(hwnd) = 关闭一个Foobar,注意, 必须调用此函数来关闭窗口,用SetWindowState也可以关闭, 但会造成内存泄漏,返回:0:失败1:成功
FoobarDrawLine(hwnd, x1, y1, x2, y2, color, style, width) = 在指定的Foobar窗口内部画线条,返回:0:失败1:成功
FoobarDrawPic(hwnd, x, y, pic_name, trans_color) = 在指定的Foobar窗口绘制图像,此图片不能是加密的图片,返回:0:失败1:成功
FoobarDrawText(hwnd, x, y, w, h, text, color, align) = 在指定的Foobar窗口绘制文字,返回:0:失败1:成功
FoobarFillRect(hwnd, x1, y1, x2, y2, color) = 在指定的Foobar窗口内部填充矩形,返回:0:失败1:成功
FoobarLock(hwnd) = 锁定指定的Foobar窗口, 不能通过鼠标来移动,返回:0:失败1:成功
FoobarPrintText(hwnd, text, color) = 向指定的Foobar窗口区域内输出滚动文字,返回:0:失败1:成功
FoobarSetFont(hwnd, font_name, size, flag) = 设置指定Foobar窗口的字体,返回:0:失败1:成功
FoobarSetSave(hwnd, file, enable, header) = 设置保存指定的Foobar滚动文本区信息到文件,返回:0:失败1:成功
FoobarTextLineGap(hwnd, line_gap) = 设置滚动文本区的文字行间距,默认是3,返回:0:失败1:成功
FoobarTextPrintDir(hwnd, dir) = 设置滚动文本区的文字输出方向,默认是0,返回:0:失败1:成功
FoobarTextRect(hwnd, x, y, w, h) = 设置指定Foobar窗口的滚动文本框范围,默认的文本框范围是窗口区域,返回:0:失败1:成功
FoobarUnlock(hwnd) = 解锁指定的Foobar窗口, 可以通过鼠标来移动,返回:0:失败1:成功
FoobarUpdate(hwnd) = 刷新指定的Foobar窗口,返回:0:失败1:成功
FoobarSetTrans(hwnd, is_trans, color, sim) = 设置指定Foobar窗口的是否透明,返回:0:失败1:成功
FoobarStartGif(hwnd, x, y, pic_name, repeat_limit, delay) = 在指定的Foobar窗口绘制gif动画,返回:0:失败1:成功
FoobarStopGif(hwnd, x, y, pic_name) = 停止在指定foobar里显示的gif动画,返回:0:失败1:成功
# 大漠插件内存
DoubleToData(value) = 把双精度浮点数转换成二进制形式,返回:字符串形式表达的二进制数据,可以用于WriteData FindData FindDataEx等接口
FindData(hwnd, addr_range, data) = 搜索指定的二进制数据, 默认步长是1, ,如果要定制步长, 请用FindDataEx,返回:返回搜索到的地址集合,地址格式如下:"addr1|addr2|addr3…|addrn",比如"400050|423435|453430"
FindDataEx(hwnd, addr_range, data, step, multi_thread, mode) = 搜索指定的二进制数据,返回:返回搜索到的地址集合,地址格式如下:"addr1|addr2|addr3…|addrn",比如"400050|423435|453430"
FindDouble(hwnd, addr_range, double_value_min, double_value_max) = 搜索指定的双精度浮点数, 默认步长是1,如果要定制步长, 请用FindDoubleEx,返回:返回搜索到的地址集合,地址格式如下:"addr1|addr2|addr3…|addrn",比如"400050|423435|453430"
FindDoubleEx(hwnd, addr_range, double_value_min, double_value_max, step, multi_thread, mode) = 搜索指定的双精度浮点数,返回:返回搜索到的地址集合,地址格式如下:"addr1|addr2|addr3…|addrn",比如"400050|423435|453430"
FindFloat(hwnd, addr_range, float_value_min, float_value_max) = 搜索指定的单精度浮点数, 默认步长是1,如果要定制步长, 请用FindFloatEx,返回:返回搜索到的地址集合,地址格式如下:"addr1|addr2|addr3…|addrn",比如"400050|423435|453430"
FindFloatEx(hwnd, addr_range, float_value_min, float_value_max, step, multi_thread, mode) = 搜索指定的单精度浮点数,返回:返回搜索到的地址集合,地址格式如下:"addr1|addr2|addr3…|addrn",比如"400050|423435|453430"
FindInt(hwnd, addr_range, int_value_min, int_value_max, type) = 搜索指定的整数, 默认步长是1,如果要定制步长, 请用FindIntEx,返回:返回搜索到的地址集合,地址格式如下:"addr1|addr2|addr3…|addrn",比如"400050|423435|453430"
FindIntEx(hwnd, addr_range, int_value_min, int_value_max, type, step, multi_thread, mode) = 搜索指定的整数,返回:返回搜索到的地址集合,地址格式如下:"addr1|addr2|addr3…|addrn",比如"400050|423435|453430"
FindString(hwnd, addr_range, string_value, type) = 搜索指定的字符串, 默认步长是1, 如果要定制步长, 请用FindStringEx,返回:返回搜索到的地址集合,地址格式如下:"addr1|addr2|addr3…|addrn",比如"400050|423435|453430"
FindStringEx(hwnd, addr_range, string_value, type, step, multi_thread, mode) = 搜索指定的字符串,返回:返回搜索到的地址集合,地址格式如下:"addr1|addr2|addr3…|addrn",比如"400050|423435|453430"
FloatToData(value) = 把单精度浮点数转换成二进制形式,返回:字符串形式表达的二进制数据,可以用于WriteData FindData FindDataEx等接口
GetModuleBaseAddr(hwnd, module) = 根据指定的窗口句柄, 获取进程下的指定模块的基址,返回:模块的基址
IntToData(value, type) = 把整数转换成二进制形式,返回:字符串形式表达的二进制数据,可以用于WriteData FindData FindDataEx等接口
ReadData(hwnd, addr, len) = 读取指定地址的二进制数据,返回:读取到的数值, 以16进制表示的字符串,每个字节以空格相隔,比如"12 34 56 78 ab cd ef"
ReadDouble(hwnd, addr) = 读取指定地址的双精度浮点数,返回:双精度浮点数:读取到的数值, 注意这里无法判断读取是否成功
ReadFloat(hwnd, addr) = 读取指定地址的单精度浮点数,返回:单精度浮点数:读取到的数值, 注意这里无法判断读取是否成功
ReadInt(hwnd, addr, type) = 读取指定地址的整数数值, 类型可以是8位, 16位 或者 32位,返回:读取到的数值, 注意这里无法判断读取是否成功
ReadString(hwnd, addr, type, len) = 读取指定地址的字符串, 可以是GBK字符串或者是Unicode字符串,必须事先知道内存区的字符串编码方式,返回:读取到的字符串, 注意这里无法判断读取是否成功
SetMemoryFindResultToFile(file) = 设置是否把所有内存查找接口的结果保存入指定文件,返回:0:失败1:成功
SetMemoryHwndAsProcessId(en) = 设置是否把所有内存接口函数中的窗口句柄当作进程ID,以支持直接以进程ID来使用内存接口,返回:0:失败1:成功
StringToData(value, type) = 把字符串转换成二进制形式,返回:字符串形式表达的二进制数据,可以用于WriteData FindData FindDataEx等接口
WriteData(hwnd, addr, data) = 对指定地址写入二进制数据,返回:0:失败1:成功
WriteDouble(hwnd, addr, v) = 对指定地址写入双精度浮点数,返回:0:失败1:成功
WriteFloat(hwnd, addr, v) = 对指定地址写入单精度浮点数,返回:0:失败1:成功
WriteInt(hwnd, addr, type, v) = 对指定地址写入整数数值, 类型可以是8位, 16位 或者 32位,返回:0:失败1:成功
WriteString(hwnd, addr, type, v) = 对指定地址写入字符串,可以是Ascii字符串或者是Unicode字符串,返回:0:失败1:成功
# 大漠插件后台设置
BindWindow(hwnd, display, mouse, keypad, mode) = 绑定指定的窗口, 并指定参数,这个窗口的屏幕颜色获取方式, 鼠标仿真模式, 键盘仿真模式, 以及模式设定,高级用户可以参考BindWindowEx更加灵活强大,返回:0:失败1:成功如果返回0, 可以调用GetLastError来查看具体失败错误码
BindWindowEx(hwnd, display, mouse, keypad, public, mode) = 绑定指定的窗口, 并指定参数,这个窗口的屏幕颜色获取方式, 鼠标仿真模式, 键盘仿真模式 高级用户使用,返回:0:失败1:成功如果返回0, 可以调用GetLastError来查看具体失败错误码
DownCpu(rate) = 降低目标窗口所在进程的CPU占用,返回:0:失败1:成功
EnableBind(enable) = 设置是否暂时关闭或者开启后台功能, 默认是开启,返回:0:失败1:成功
EnableFakeActive(enable) = 设置是否开启后台假激活功能, 默认是关闭, 一般用不到,返回:0:失败1:成功
EnableIme(enable) = 设置是否关闭绑定窗口所在进程的输入法,返回:0:失败1:成功
EnableKeypadMsg(enable) = 是否在使用dx键盘时开启windows消息, 默认开启,返回:0:失败1:成功
EnableKeypadPatch(enable) = 键盘消息发送补丁, 默认是关闭,返回:0:失败1:成功
EnableKeypadSync(enable, time_out) = 键盘消息采用同步发送模式, 默认异步,返回:0:失败1:成功
EnableMouseMsg(enable) = 是否在使用dx鼠标时开启windows消息, 默认开启,返回:0:失败1:成功
EnableMouseSync(enable, time_out) = 鼠标消息采用同步发送模式, 默认异步,返回:0:失败1:成功
EnableRealKeypad(enable) = 键盘动作模拟真实操作, 点击延时随机,返回:0:失败1:成功
EnableRealMouse(enable, mousedelay, mousestep) = 鼠标动作模拟真实操作, 带移动轨迹, 以及点击延时随机,返回:0:失败1:成功
EnableSpeedDx(enable) = 设置是否开启高速dx键鼠模式 默认是关闭,返回:0:失败1:成功
ForceUnBindWindow(hwnd) = 强制解除绑定窗口, 并释放系统资源,返回:0:失败1:成功
IsBind(hwnd) = 判定指定窗口是否已经被后台绑定, (前台无法判定),返回:0: 没绑定, 或者窗口不存在, 1: 已经绑定
LockDisplay(lock) = 锁定指定窗口的图色数据(不刷新),返回:0:失败1:成功
LockInput(lock) = 禁止外部输入到指定窗口,返回:0:失败1:成功
LockMouseRect(x1, y1, x2, y2) = 设置前台鼠标在屏幕上的活动范围,返回:0:失败1:成功
SetDisplayDelay(time) = 设置dx截图最长等待时间内部默认是3000毫秒, 一般用不到调整这个,返回:0:失败1:成功
SetSimMode(mode) = 设置前台键鼠的模拟方式,返回:0:插件没注册,-1:64位平台不支持,-2:驱动释放失败, ,-3:驱动加载失败, 可能是权限不够, 参考UAC权限设置, ,1 :成功
UnBindWindow() = 解除绑定窗口, 并释放系统资源, 一般在退出调用,返回:0:失败1:成功
# 大漠插件图色
AppPicAddr(pic_info, addr, size) = 对指定的数据地址和长度, 组合成新的参数,FindPicMem FindPicMemE 以及FindPicMemEx专用,返回:新的地址描述串
BGR2RGB(bgr_color) = 把BGR(按键格式)的颜色格式转换为RGB,返回:RGB格式的字符串
Capture(x1, y1, x2, y2, file) = 抓取指定区域(x1, y1, x2, y2)的图像, 保存为file(24位位图),返回:0:失败1:成功
CaptureGif(x1, y1, x2, y2, file, delay, time) = 抓取指定区域(x1, y1, x2, y2)的动画, 保存为gif格式,返回:0:失败1:成功
CaptureJpg(x1, y1, x2, y2, file, quality) = 抓取指定区域(x1, y1, x2, y2)的图像, 保存为file(JPG压缩格式),返回:0:失败1:成功
CapturePng(x1, y1, x2, y2, file) = 同Capture函数, 只是保存的格式为PNG,返回:0:失败1:成功
CapturePre(file) = 抓取上次操作的图色区域, 保存为file(24位位图),返回:0:失败1:成功
CmpColor(x, y, color, sim) = 比较指定坐标点(x, y)的颜色,返回:0: 颜色匹配1: 颜色不匹配
EnableDisplayDebug(enable_debug) = 开启图色调试模式,此模式会稍许降低图色和文字识别的速度,默认不开启,返回:0:失败1:成功
EnableGetColorByCapture(enable) = 允许调用GetColor GetColorBGR GetColorHSV 以及 CmpColor时,以截图的方式来获取颜色,返回:0:失败1:成功
FindColor(x1, y1, x2, y2, color, sim, dir, intX, intY) = 查找指定区域内的颜色,颜色格式"RRGGBB-DRDGDB",返回:0:没找到1:找到
FindColorE(x1, y1, x2, y2, color, sim, dir) = 查找指定区域内的颜色,颜色格式"RRGGBB-DRDGDB"用不了FindColor可以用此接口来代替,返回:返回X和Y坐标 形式如"x|y", 比如"100|200"
FindColorEx(x1, y1, x2, y2, color, sim, dir) = 查找指定区域内的所有颜色,颜色格式"RRGGBB-DRDGDB",返回:返回所有颜色信息的坐标值, 通过GetResultCount等接口解析,(由于内存限制, 返回的颜色数量最多为1800个左右
FindMulColor(x1, y1, x2, y2, color, sim) = 查找指定区域内的所有颜色,返回:0:没找到或者部分颜色没找到1:所有颜色都找到
FindMultiColor(x1, y1, x2, y2, first_color, offset_color, sim, dir, intX, intY) = 根据指定的多点查找颜色坐标,返回:0:没找到1:找到
FindMultiColorE(x1, y1, x2, y2, first_color, offset_color, sim, dir) = 根据指定的多点查找颜色坐标,用不了FindMultiColor可以用此接口来代替,返回:返回X和Y坐标 形式如"x|y", 比如"100|200"
FindMultiColorEx(x1, y1, x2, y2, first_color, offset_color, sim, dir) = 根据指定的多点查找所有颜色坐标,返回:返回所有颜色信息的坐标值, 通过GetResultCount等接口解析,由于内存限制, 返回的坐标数量最多为1800个左右,坐标是first_color所在的坐标
FindPic(x1, y1, x2, y2, pic_name, delta_color, sim, dir, intX, intY) = 查找指定区域内的图片, 位图必须是24位色格式,支持透明色, 当图像上下左右4个顶点的颜色一样时, 则这个颜色将作为透明色处理,这个函数可以查找多个图片, 只返回第一个找到的X Y坐标,返回:返回找到的图片的序号, 从0开始索引, 如果没找到返回-1
FindPicE(x1, y1, x2, y2, pic_name, delta_color, sim, dir) = 查找指定区域内的图片, 位图必须是24位色格式,支持透明色, 当图像上下左右4个顶点的颜色一样时, 则这个颜色将作为透明色处理,这个函数可以查找多个图片, 只返回第一个找到的X Y坐标, 用不了FindPic可以用此接口来代替,返回:返回找到的图片序号(从0开始索引)以及X和Y坐标 形式如"index|x|y", 比如"3|100|200"
FindPicEx(x1, y1, x2, y2, pic_name, delta_color, sim, dir) = 查找指定区域内的图片, 位图必须是24位色格式,支持透明色, 当图像上下左右4个顶点的颜色一样时, 则这个颜色将作为透明色处理,这个函数可以查找多个图片, 并且返回所有找到的图像的坐标,返回:返回的是所有找到的坐标格式如下:"id, x, y|id, x, y|id, x, y" (图片左上角的坐标),比如"0, 100, 20|2, 30, 40" 表示找到了两个,第一个, 对应的图片是图像序号为0的图片, 坐标是(100, 20),第二个是序号为2的图片, 坐标(30, 40),由于内存限制, 返回的图片数量最多为1500个左右
FindPicExS(x1, y1, x2, y2, pic_name, delta_color, sim, dir) = 查找指定区域内的图片, 位图必须是24位色格式,支持透明色, 当图像上下左右4个顶点的颜色一样时, 则这个颜色将作为透明色处理,这个函数可以查找多个图片, 并且返回所有找到的图像的坐标,此函数同FindPicEx, 只是返回值不同,返回:返回的是所有找到的坐标格式如下:"file, x, y| file, x, y| file, x, y" (图片左上角的坐标),比如"1, bmp, 100, 20|2, bmp, 30, 40" 表示找到了两个,第一个, 对应的图片是1, bmp, 坐标是(100, 20),第二个是2, bmp, 坐标(30, 40),由于内存限制, 返回的图片数量最多为1500个左右
FindPicMem(x1, y1, x2, y2, pic_info, delta_color, sim, dir, intX, intY) = 查找指定区域内的图片, 位图必须是24位色格式,支持透明色, 当图像上下左右4个顶点的颜色一样时, 则这个颜色将作为透明色处理,这个函数可以查找多个图片, 只返回第一个找到的X Y坐标, 这个函数要求图片是数据地址,返回:返回找到的图片的序号, 从0开始索引, 如果没找到返回-1
FindPicMemE(x1, y1, x2, y2, pic_info, delta_color, sim, dir) = 查找指定区域内的图片, 位图必须是24位色格式,支持透明色, 当图像上下左右4个顶点的颜色一样时, 则这个颜色将作为透明色处理,这个函数可以查找多个图片, 只返回第一个找到的X Y坐标, 这个函数要求图片是数据地址, 用不了FindPicMem可以用此接口来代替,返回:返回找到的图片序号(从0开始索引)以及X和Y坐标,形式如"index|x|y",比如"3|100|200"
FindPicMemEx(x1, y1, x2, y2, pic_info, delta_color, sim, dir) = 查找指定区域内的图片, 位图必须是24位色格式,支持透明色, 当图像上下左右4个顶点的颜色一样时, 则这个颜色将作为透明色处理,这个函数可以查找多个图片, 并且返回所有找到的图像的坐标, 这个函数要求图片是数据地址,返回:返回的是所有找到的坐标格式如下:"id, x, y|id, x, y|id, x, y" (图片左上角的坐标),比如"0, 100, 20|2, 30, 40" 表示找到了两个,第一个, 对应的图片是图像序号为0的图片, 坐标是(100, 20),第二个是序号为2的图片, 坐标(30, 40)(由于内存限制, 返回的图片数量最多为1500个左右)
FindPicS(x1, y1, x2, y2, pic_name, delta_color, sim, dir, intX, intY) = 查找指定区域内的图片, 位图必须是24位色格式,支持透明色, 当图像上下左右4个顶点的颜色一样时, 则这个颜色将作为透明色处理,这个函数可以查找多个图片, 只返回第一个找到的X Y坐标,此函数同FindPic, 只是返回值不同,返回:返回找到的图片的文件名, 没找到返回长度为0的字符串
FindShape(x1, y1, x2, y2, offset_color, sim, dir, intX, intY) = 查找指定的形状, 形状描述参考按键抓抓, 语法需用大漠综合工具的颜色转换,返回:0:没找到1:找到
FindShapeE(x1, y1, x2, y2, offset_color, sim, dir) = 查找指定的形状, 形状描述参考按键抓抓, 语法需用大漠综合工具的颜色转换, 用不了FindShape可以用此接口来代替,返回:返回X和Y坐标 形式如"x|y", 比如"100|200"
FindShapeEx(x1, y1, x2, y2, offset_color, sim, dir) = 查找所有指定的形状的坐标, 形状描述参考按键抓抓, 语法需用大漠综合工具的颜色转换,返回:返回所有形状的坐标值, 然后通过GetResultCount等接口来解析(由于内存限制, 返回的坐标数量最多为1800个左右)
FreePic(pic_name) = 释放指定的图片,此函数不必要调用, 除非你想节省内存,返回:0:失败1:成功
GetAveHSV(x1, y1, x2, y2) = 获取范围(x1, y1, x2, y2)颜色的均值, 返回格式"H, S, V",返回:颜色字符串
GetAveRGB(x1, y1, x2, y2) = 获取范围(x1, y1, x2, y2)颜色的均值, 返回格式"RRGGBB",返回:颜色字符串
GetColor(x, y) = 获取(x, y)的颜色, 颜色返回格式"RRGGBB",返回:颜色字符串(注意这里都是小写字符, 和工具相匹配)
GetColorBGR(x, y) = 获取(x, y)的颜色, 颜色返回格式"BBGGRR",返回:颜色字符串(注意这里都是小写字符, 和工具相匹配)
GetColorHSV(x, y) = 获取(x, y)的HSV颜色, 颜色返回格式"H, S, V",返回:颜色字符串
GetColorNum(x1, y1, x2, y2, color, sim) = 获取指定区域的颜色数量, 颜色格式"RRGGBB-DRDGDB",返回:颜色数量
GetPicSize(pic_name) = 获取指定图片的尺寸, 如果指定的图片已经被加入缓存, 则从缓存中获取信息, 此接口也会把此图片加入缓存,返回:形式如 "w, h" 比如"30, 20"
GetScreata(x1, y1, x2, y2) = 获取指定区域的图像, 用二进制数据的方式返回, 方便二次开发,返回:返回的是指定区域的二进制颜色数据地址,每个颜色是4个字节, 表示方式为(00RRGGBB)
GetScreataBmp(x1, y1, x2, y2, data, size) = 获取指定区域的图像, 用24位位图的数据格式返回, 方便二次开发,返回:0:失败1:成功
ImageToBmp(pic_name, bmp_name) = 转换图片格式为24位BMP格式,返回:0:失败1:成功
IsDisplayDead(x1, y1, x2, y2, t) = 判断指定的区域, 在指定的时间内(秒), 图像数据是否一直不变, (卡屏),返回:0:没有卡屏, 图像数据在变化, ,1:卡屏, 图像数据在指定的时间内一直没有变化
LoadPic(pic_name) = 预先加载指定的图片,这样在操作任何和图片相关的函数时, 将省去了加载图片的时间,调用此函数后, 没必要一定要调用FreePic, 插件自己会自动释放,另外, 此函数不是必须调用的, 所有和图形相关的函数只要调用过一次, 图片会自动加入缓存,如果想对一个已经加入缓存的图片进行修改, 那么必须先用FreePic释放此图片在缓存中占用 的内存, 然后重新调用图片相关接口, 就可以重新加载此图片,返回:0:失败1:成功
MatchPicName(pic_name) = 根据通配符获取文件集合, 方便用于FindPic和FindPicEx,返回:返回的是通配符对应的文件集合, 每个图片以|分割
RGB2BGR(rgb_color) = 把RGB的颜色格式转换为BGR(按键格式),返回:BGR格式的字符串
SetPicPwd(pwd) = 设置图片密码, 如果图片本身没有加密, 那么此设置不影响不加密的图片, 一样正常使用,返回:0:失败1:成功
# 大漠插件基本设置
GetBasePath() = 获取注册在系统中的dm.dll的路径,返回:返回dm.dll所在路径
GetDmCount() = 返回当前进程已经创建的dm对象个数,返回:个数
GetID() = 返回当前大漠对象的ID值, 这个值对于每个对象是唯一存在的可以用来判定两个大漠对象是否一致,返回:当前对象的ID值
GetLastError() = 获取插件命令的最后错误,返回:返回值表示错误值 0表示无错误,-1:使用绑定里的收费功能, 但没注册,-2:使用模式0 2 4 6时出现, 因为目标窗口有保护或没有以管理员权限打开, 或者安全软件拦截,解决办法: 关闭所有安全软件, 并且关闭系统UAC, 然后再重新尝试,如果还不行就可以肯定是目标窗口有特殊保护,-3:使用模式0 2 4 6时出现, 可能目标窗口有保护, 也可能是异常错误,-4:使用模式1 3 5 7 101 103时出现, 这是异常错误,-5:使用模式1 3 5 7 101 103时出现,解决办法就是关闭目标窗口, 重新打开再绑定即可, 也可能是运行脚本的进程没有管理员权限,-6 -7 -9:使用模式1 3 5 7 101 103时出现尝试卸载360,-8 -10:使用模式1 3 5 7 101 103时出现, 目标进程可能有保护, 也可能是插件版本过老, 试试新的或许可以解决,-11:使用模式1 3 5 7 101 103时出现, 目标进程有保护, 告诉我解决,-12:使用模式1 3 5 7 101 103时出现, 目标进程有保护,-13:使用模式1 3 5 7 101 103时出现, 目标进程有保护, 或者是因为上次的绑定没有解绑导致尝试在绑定前调用ForceUnBindWindow,-14:使用模式0 1 4 5时出现, 有可能目标机器兼容性不太好, 可以尝试其他模式, 比如2 3 6 7,-16:可能使用了绑定模式 0 1 2 3 和 101, 指定了一个子窗口, 导致不支持, 可以换模式4 5 6 7或者103来尝试,另外也可以考虑使用父窗口或者顶级窗口来避免,还有可能是目标窗口没有正常解绑,-17:模式1 3 5 7 101 103时出现, 异常错误,-18:句柄无效,-19:使用模式0 1 2 3 101时出现, 系统不支持这几个模式, 可以尝试其他模式
GetPath() = 获取全局路径, (可用于调试),返回:以字符串的形式返回当前设置的全局路径
Reg(reg_code, ver_info) = 非简单游平台使用, 调用此函数来注册,从而使用插件的高级功能, 推荐使用此函数,返回:-1:无法连接网络, (可能防火墙拦截, 如果可以正常访问大漠插件网站, 那就可以肯定是被防火墙拦截),-2:进程没有以管理员方式运行, (出现在win7 vista 2008, 建议关闭uac),0:失败 (未知错误),1:成功,2:余额不足,3:绑定了本机器, 但是账户余额不足50元,4:注册码错误,5:你的机器或者IP在黑名单列表中或者不在白名单列表中,-8:版本附加信息长度超过了10,-9:版本附加信息里包含了非法字母,空:这是不可能返回空的, 如果出现空, 肯定是版本不对
RegEx(reg_code, ver_info, ip) = 非简单游平台使用, 调用此函数来注册, 从而使用插件的高级功能, 可以根据指定的IP列表来注册, 新手不建议使用!,返回:-1:无法连接网络, (可能防火墙拦截, 如果可以正常访问大漠插件网站, 那就可以肯定是被防火墙拦截),-2:进程没有以管理员方式运行, (出现在win7 vista 2008, 建议关闭uac),0:失败 (未知错误),1:成功,2:余额不足,3:绑定了本机器, 但是账户余额不足50元,4:注册码错误,5:你的机器或者IP在黑名单列表中或者不在白名单列表中,-8:版本附加信息长度超过了10,-9:版本附加信息里包含了非法字母,空:这是不可能返回空的, 如果出现空, 肯定是版本不对
RegExNoMac(reg_code, ver_info, ip) = 非简单游平台使用, 调用此函数来注册, 从而使用插件的高级功能, 可以根据指定的IP列表来注册, 新手不建议使用! 此函数同RegEx函数的不同在于, 此函数用于注册的机器码是不带mac地址的,返回:-1:无法连接网络, (可能防火墙拦截, 如果可以正常访问大漠插件网站, 那就可以肯定是被防火墙拦截),-2:进程没有以管理员方式运行, (出现在win7 vista 2008, 建议关闭uac),0:失败 (未知错误),1:成功,2:余额不足,3:绑定了本机器, 但是账户余额不足50元,4:注册码错误,5:你的机器或者IP在黑名单列表中或者不在白名单列表中,-8:版本附加信息长度超过了10,-9:版本附加信息里包含了非法字母,空:这是不可能返回空的, 如果出现空, 肯定是版本不对
RegNoMac(reg_code, ver_info) = 非简单游平台使用, 调用此函数来注册, 从而使用插件的高级功能, 推荐使用此函数, 新手不建议使用! 此函数同Reg函数的不同在于, 此函数用于注册的机器码是不带mac地址的,返回:-1:无法连接网络, (可能防火墙拦截, 如果可以正常访问大漠插件网站, 那就可以肯定是被防火墙拦截),-2:进程没有以管理员方式运行, (出现在win7 vista 2008, 建议关闭uac),0:失败 (未知错误),1:成功,2:余额不足,3:绑定了本机器, 但是账户余额不足50元,4:注册码错误,5:你的机器或者IP在黑名单列表中或者不在白名单列表中,-8:版本附加信息长度超过了10,-9:版本附加信息里包含了非法字母,空:这是不可能返回空的, 如果出现空, 肯定是版本不对
SetDisplayInput(mode) = 设定图色的获取方式, 默认是显示器或者后台窗口(具体参考BindWindow),返回:0:失败1:成功
SetEnumWindowDelay(delay) = 设置EnumWindow EnumWindowByProcess EnumWindowSuper的最长延时,内部默认超时是5秒,返回:0:失败1:成功
SetPath(path) = 设置全局路径,设置了此路径后, 所有接口调用中,相关的文件都相对于此路径, 比如图片, 字库等,返回:0:失败1:成功
SetShowErrorMsg(show) = 设置是否弹出错误信息, 默认是打开,返回:0:失败1:成功
Ver() = 返回当前插件版本号,返回:当前插件的版本描述字符串
# 大漠插件文件
CopyFile(src_file, dst_file, over) = 拷贝文件,返回:0:失败1:成功
CreateFolder(folder) = 创建指定目录,返回:0:失败1:成功
DecodeFile(file, pwd) = 解密指定的文件,返回:0:失败1:成功
DeleteFile(file) = 删除文件,返回:0:失败1:成功
DeleteFolder(folder) = 删除指定目录,返回:0:失败1:成功
DeleteIni(section, key, file) = 删除指定的ini小节,返回:0:失败1:成功
DeleteIniPwd(section, key, file, pwd) = 删除指定的ini小节, 支持加密文件,返回:0:失败1:成功
DownloadFile(url, save_file, timeout) = 从internet上下载一个文件,返回:1:成功-1:网络连接失败-2:写入文件失败
EncodeFile(file, pwd) = 加密指定的文件,返回:0:失败1:成功
GetFileLength(file) = 获取指定的文件长度,返回:文件长度(字节数)
IsFileExist(file) = 判断指定文件是否存在,返回:0:不存在1:存在
MoveFile(src_file, dst_file) = 移动文件,返回:0:失败1:成功
ReadFile(file) = 从指定的文件读取内容,返回:读入的文件内容
ReadIni(section, key, file) = 从Ini中读取指定信息,返回:字符串形式表达的读取到的内容
ReadIniPwd(section, key, file, pwd) = 从Ini中读取指定信息,可支持加密文件,返回:字符串形式表达的读取到的内容
SelectDirectory() = 弹出选择文件夹对话框, 并返回选择的文件夹,返回:选择的文件夹全路径
SelectFile() = 弹出选择文件对话框, 并返回选择的文件,返回:选择的文件全路径
WriteFile(file, content) = 向指定文件追加字符串,返回:0:失败1:成功
WriteIni(section, key, value, file) = 向指定的Ini写入信息,返回:0:失败1:成功
WriteIniPwd(section, key, value, file, pwd) = 向指定的Ini写入信息, 支持加密文件,返回:0:失败1:成功
# 大漠插件文字识别
AddDict(index, dict_info) = 给指定的字库中添加一条字库信息,返回:0:失败1:成功
ClearDict(index) = 清空指定的字库,返回:0:失败1:成功
FetchWord(x1, y1, x2, y2, color, word) = 根据指定的范围, 以及指定的颜色描述, 提取点阵信息,类似于大漠工具里的单独提取,返回:识别到的点阵信息, 可用于AddDict如果失败, 返回空
FindStr(x1, y1, x2, y2, string, color_format, sim) = 在屏幕范围(x1, y1, x2, y2)内, 查找string(可以是任意个字符串的组合),并返回符合color_format的坐标位置, 相似度sim,返回:返回字符串的索引 没找到返回-1,比如"长安|洛阳", 若找到长安, 则返回0intX:返回X坐标, 没找到返回-1intY:返回Y坐标, 没找到返回-1
FindStrE(x1, y1, x2, y2, string, color_format, sim) = 在屏幕范围(x1, y1, x2, y2)内, 查找string(可以是任意个字符串的组合),并返回符合color_format的坐标位置, 相似度sim,(多色, 差色查找类似于Ocr接口, 不再重述), 用不了FindStr可以用此接口来代替,返回:返回字符串序号以及X和Y坐标,形式如"id|x|y",比如"0|100|200", 没找到时, id和X以及Y均为-1, "-1|-1|-1"
FindStrEx(x1, y1, x2, y2, string, color_format, sim) = 在屏幕范围(x1, y1, x2, y2)内, 查找string(可以是任意字符串的组合),并返回符合color_format的所有坐标位置, 相似度sim,(多色, 差色查找类似于Ocr接口, 不再重述),返回:返回所有找到的坐标集合,格式如下:"id, x0, y0|id, x1, y1|, , , , , , |id, xn, yn",比如"0, 100, 20|2, 30, 40" 表示找到了两个, 第一个, 对应的是序号为0的字符串, 坐标是(100, 20), 第二个是序号为2的字符串, 坐标(30, 40)
FindStrExS(x1, y1, x2, y2, string, color_format, sim) = 在屏幕范围(x1, y1, x2, y2)内, 查找string(可以是任意字符串的组合),并返回符合color_format的所有坐标位置, 相似度sim,(多色, 差色查找类似于Ocr接口, 不再重述), 此函数同FindStrEx, 只是返回值不同,返回:返回所有找到的坐标集合,格式如下:"str, x0, y0| str, x1, y1|, , , , , , | str, xn, yn",比如"长安, 100, 20|大雁塔, 30, 40" 表示找到了两个,第一个是长安 , 坐标是(100, 20),第二个是大雁塔, 坐标(30, 40)
FindStrFast(x1, y1, x2, y2, string, color_format, sim) = 同FindStr,返回:返回字符串的索引 没找到返回-1,比如"长安|洛阳", 若找到长安, 则返回0intX:返回X坐标, 没找到返回-1intY:返回Y坐标, 没找到返回-1
FindStrFastE(x1, y1, x2, y2, string, color_format, sim) = 同FindStrE, 用不了FindStrFast可以用此接口来代替,返回:返回字符串序号以及X和Y坐标,形式如"id|x|y", 比如"0|100|200",没找到时, id和X以及Y均为-1, "-1|-1|-1"
FindStrFastEx(x1, y1, x2, y2, string, color_format, sim) = 同FindStrEx,返回:返回所有找到的坐标集合,格式如下:"id, x0, y0|id, x1, y1|, , , , , , |id, xn, yn",比如"0, 100, 20|2, 30, 40" 表示找到了两个, 第一个, 对应的是序号为0的字符串, 坐标是(100, 20), 第二个是序号为2的字符串, 坐标(30, 40)
FindStrFastExS(x1, y1, x2, y2, string, color_format, sim) = 同FindStrExS,返回:返回所有找到的坐标集合,格式如下:"str, x0, y0| str, x1, y1|, , , , , , | str, xn, yn",比如"长安, 100, 20|大雁塔, 30, 40" 表示找到了两个, 第一个是长安 , 坐标是(100, 20), 第二个是大雁塔, 坐标(30, 40)
FindStrFastS(x1, y1, x2, y2, string, color_format, sim) = 同FindStrS,返回:返回找到的字符串, 没找到的话返回长度为0的字符串,intX:返回X坐标, 没找到返回-1,intY:返回Y坐标 没找到返回-1
FindStrS(x1, y1, x2, y2, string, color_format, sim) = 在屏幕范围(x1, y1, x2, y2)内, 查找string(可以是任意个字符串的组合),并返回符合color_format的坐标位置, 相似度sim,(多色, 差色查找类似于Ocr接口, 不再重述), 此函数同FindStr, 只是返回值不同,返回:返回找到的字符串, 没找到的话返回长度为0的字符串,intX:返回X坐标, 没找到返回-1intY:返回Y坐标 没找到返回-1
FindStrWithFont(x1, y1, x2, y2, string, color_format, sim, font_name, font_size, flag) = 同FindStr, 但是不使用SetDict设置的字库,而利用系统自带的字库, 速度比FindStr稍慢,返回:返回字符串的索引 没找到返回-1,比如"长安|洛阳", 若找到长安, 则返回0,intX:返回X坐标, 没找到返回-1,intY:返回Y坐标, 没找到返回-1
FindStrWithFontE(x1, y1, x2, y2, string, color_format, sim, font_name, font_size, flag) = 同FindStrE, 但是不使用SetDict设置的字库,而利用系统自带的字库, 速度比FindStrE稍慢,返回:返回字符串序号以及X和Y坐标,形式如"id|x|y",比如"0|100|200", 没找到时, id和X以及Y均为-1, "-1|-1|-1"
FindStrWithFontEx(x1, y1, x2, y2, string, color_format, sim, font_name, font_size, flag) = 同FindStrEx, 但是不使用SetDict设置的字库,而利用系统自带的字库, 速度比FindStrEx稍慢,返回:返回所有找到的坐标集合,格式如下:"id, x0, y0|id, x1, y1|, , , , , , |id, xn, yn",比如"0, 100, 20|2, 30, 40" 表示找到了两个, 第一个, 对应的是序号为0的字符串, 坐标是(100, 20), 第二个是序号为2的字符串, 坐标(30, 40)
GetDict(index, font_index) = 获取指定字库中指定条目的字库信息,返回:返回字库条目信息, 失败返回空串
GetDictCount(index) = 获取指定的字库中的字符数量,返回:字库数量
GetDictInfo(str, font_name, font_size, flag) = 根据指定的文字, 以及指定的系统字库信息, 获取字库描述信息,返回:返回字库信息, 每个字符的字库信息用"|"来分割
GetNowDict() = 获取当前使用的字库序号(0-9),返回:字库序号(0-9)
GetResultCount(ret) = 对插件部分接口的返回值进行解析, 并返回ret中的坐标个数,返回:返回ret中的坐标个数
GetResultPos(ret, index) = 对插件部分接口的返回值进行解析, 并根据指定的第index个坐标, 返回具体的值,返回:0:失败1:成功intX: 返回X坐标intY: 返回Y坐标
GetWordResultCount(str) = 在使用GetWords进行词组识别以后, 可以用此接口进行识别词组数量的计算,返回:返回词组数量
GetWordResultPos(str, index) = 在使用GetWords进行词组识别以后, 可以用此接口进行识别各个词组的坐标,返回:0:失败1:成功intX: 返回的X坐标intY: 返回的Y坐标
GetWordResultStr(str, index) = 在使用GetWords进行词组识别以后, 可以用此接口进行识别各个词组的内容,返回:返回的第index个词组内容
GetWords(x1, y1, x2, y2, color, sim) = 根据指定的范围, 以及设定好的词组识别参数(一般不用更改),识别这个范围内所有满足条件的词组, 适合在未知文字的情况下, 进行不定识别,返回:识别到的格式串, 要用到专用函数来解析
GetWordsNoDict(x1, y1, x2, y2, color) = 根据指定的范围, 以及设定好的词组识别参数(一般不用更改),识别这个范围内所有满足条件的词组, 这个识别函数不会用到字库只是识别大概形状的位置,返回:识别到的格式串, 要用到专用函数来解析
Ocr(x1, y1, x2, y2, color_format, sim) = 识别屏幕范围(x1, y1, x2, y2)内符合color_format的字符串, 相似度sim取值范围(0, 1-1, 0), sim值越大越精确, 速度越快,返回:返回识别到的字符串
OcrEx(x1, y1, x2, y2, color_format, sim) = 识别屏幕范围(x1, y1, x2, y2)内符合color_format的字符串, 相似度sim取值范围(0, 1-1, 0), sim值越大越精确, 速度越快,这个函数可以返回识别到的字符串, 以及每个字符的坐标,返回:返回识别到的字符串,格式如"识别到的信息|x0, y0|…|xn, yn"
OcrInFile(x1, y1, x2, y2, pic_name, color_format, sim) = 识别位图中区域(x1, y1, x2, y2)的文字,返回:返回识别到的字符串
SaveDict(index, file) = 保存指定的字库到指定的文件中,返回:0:失败1:成功
SetColGapNoDict(col_gap) = 高级用户使用, 在不使用字库进行词组识别前, 可设定文字的列距,默认列距是1,返回:0:失败1:成功
SetDict(index, file) = 设置字库文件,返回:0:失败1:成功
SetDictMem(index, addr, size) = 从内存中设置字库,返回:0:失败1:成功
SetDictPwd(pwd) = 设置字库的密码, 在SetDict前调用, 目前的设计是, 所有字库通用一个密码,返回:0:失败1:成功
SetExactOcr(exact_ocr) = 高级用户使用, 在使用文字识别功能前, 设定是否开启精准识别,返回:0:失败1:成功
SetMinColGap(min_col_gap) = 高级用户使用, 在识别前, 如果待识别区域有多行文字, 可以设定列间距,默认的列间距是0,如果根据情况设定, 可以提高识别精度一般不用设定,返回:0:失败1:成功
SetMinRowGap(min_row_gap) = 高级用户使用, 在识别前, 如果待识别区域有多行文字, 可以设定行间距,默认的行间距是1,如果根据情况设定, 可以提高识别精度一般不用设定,返回:0:失败1:成功
SetRowGapNoDict(row_gap) = 高级用户使用, 在不使用字库进行词组识别前, 可设定文字的行距,默认行距是1,返回:0:失败1:成功
SetWordGap(word_gap) = 高级用户使用, 在识别词组前, 可设定词组间的间隔,默认的词组间隔是5,返回:0:失败1:成功
SetWordGapNoDict(word_gap) = 高级用户使用, 在不使用字库进行词组识别前, 可设定词组间的间隔,默认的词组间隔是5,返回:0:失败1:成功
SetWordLineHeight(line_height) = 高级用户使用, 在识别词组前, 可设定文字的平均行高,默认的词组行高是10,返回:0:失败1:成功
SetWordLineHeightNoDict(line_height) = 高级用户使用, 在不使用字库进行词组识别前, 可设定文字的平均行高,默认的词组行高是10,返回:0:失败1:成功
UseDict(index) = 表示使用哪个字库文件进行识别(index范围:0-9),设置之后, 永久生效, 除非再次设定,返回:0:失败1:成功
# 大漠插件杂项
ActiveInputMethod(hwnd, input_method) = 激活指定窗口所在进程的输入法,返回:0:失败1:成功
CheckInputMethod(hwnd, input_method) = 检测指定窗口所在线程输入法是否开启,返回:0:未开启1:开启
FindInputMethod(input_method) = 检测系统中是否安装了指定输入法,返回:0:未安装1:安装了
# 大漠插件汇编
AsmAdd(asm_ins) = 添加指定的MASM汇编指令,返回:0:失败1:成功
AsmCall(hwnd, mode) = 执行用AsmAdd加到缓冲中的指令,返回:获取执行汇编代码以后的EAX的值, 一般是函数的返回值
AsmClear() = 清除汇编指令缓冲区, 用AsmAdd添加到缓冲的指令全部清除,返回:0:失败1:成功
AsmCode(base_addr) = 把汇编缓冲区的指令转换为机器码, 并用16进制字符串的形式输出,返回:机器码, 比如 "aa bb cc"这样的形式
Assemble(asm_code, base_addr, is_upper) = 把指定的机器码转换为汇编语言输出,返回:MASM汇编语言字符串
# 大漠插件窗口
ClientToScreen(hwnd, x, y) = 把窗口坐标转换为屏幕坐标,返回:0:失败1:成功
EnumWindow(parent, title, class_name, filter) = 根据指定条件, 枚举系统中符合条件的窗口,返回:字符串 :返回所有匹配的窗口句柄字符串, 格式"hwnd1, hwnd2, hwnd3"
EnumWindowByProcess(process_name, title, class_name, filter) = 根据指定进程以及其它条件, 枚举系统中符合条件的窗口,返回:返回所有匹配的窗口句柄字符串, 格式"hwnd1, hwnd2, hwnd3"
EnumWindowSuper(spec1, flag1, type1, spec2, flag2, type2, sort) = 根据两组设定条件来枚举指定窗口,返回:返回所有匹配的窗口句柄字符串,格式"hwnd1, hwnd2, hwnd3"
FindWindow(class, title) = 查找符合类名或者标题名的顶层可见窗口,返回:整形数表示的窗口句柄, 没找到返回0
FindWindowByProcess(process_name, class, title) = 根据指定的进程名字, 来查找可见窗口,返回:整形数表示的窗口句柄, 没找到返回0
FindWindowByProcessId(process_id, class, title) = 根据指定的进程Id, 来查找可见窗口,返回:整形数表示的窗口句柄, 没找到返回0
FindWindowEx(parent, class, title) = 查找符合类名或者标题名的顶层可见窗口, 如果指定了parent, 则在parent的第一层子窗口中查找,返回:整形数表示的窗口句柄, 没找到返回0
FindWindowSuper(spec1, flag1, type1, spec2, flag2, type2) = 根据两组设定条件来查找指定窗口,返回:整形数表示的窗口句柄, 没找到返回0
GetClientRect(hwnd, x1, y1, x2, y2) = 获取窗口客户区域在屏幕上的位置,返回:0:失败1:成功
GetClientSize(hwnd, width, height) = 获取窗口客户区域的宽度和高度,返回:0:失败1:成功
GetForegroundFocus() = 获取顶层活动窗口中具有输入焦点的窗口句柄,返回:返回整型表示的窗口句柄
GetForegroundWindow() = 获取顶层活动窗口,返回:返回整型表示的窗口句柄
GetMousePointWindow() = 获取鼠标指向的窗口句柄,返回:返回整型表示的窗口句柄
GetPointWindow(x, y) = 获取给定坐标的窗口句柄,返回:返回整型表示的窗口句柄
GetSpecialWindow(flag) = 获取特殊窗口,返回:以整型数表示的窗口句柄
GetWindow(hwnd, flag) = 获取给定窗口相关的窗口句柄,返回:返回整型表示的窗口句柄
GetWindowClass(hwnd) = 获取窗口的类名,返回:窗口的类名
GetWindowProcessId(hwnd) = 获取指定窗口所在的进程ID,返回:返回整型表示的是进程ID
GetWindowProcessPath(hwnd) = 获取指定窗口所在的进程的exe文件全路径,返回:返回字符串表示的是exe全路径名
GetWindowRect(hwnd, x1, y1, x2, y2) = 获取窗口在屏幕上的位置,返回:0:失败1:成功
GetWindowState(hwnd, flag) = 获取指定窗口的一些属性,返回:0:不满足条件1:满足条件
GetWindowTitle(hwnd) = 获取窗口的标题,返回:窗口的标题
MoveWindow(hwnd, x, y) = 移动指定窗口到指定位置,返回:0:失败1:成功
ScreenToClient(hwnd, x, y) = 把屏幕坐标转换为窗口坐标,返回:0:失败1:成功
SPaste(hwnd) = 向指定窗口发送粘贴命令, 把剪贴板的内容发送到目标窗口,返回:0:失败1:成功
SString(hwnd, str) = 向指定窗口发送文本数据,返回:0:失败1:成功
SString2(hwnd, str) = 向指定窗口发送文本数据,返回:0:失败1:成功
SStringIme(str) = 向绑定的窗口发送文本数据, 必须配合dx, public, input, ime属性,返回:0:失败1:成功
SetClientSize(hwnd, width, height) = 设置窗口客户区域的宽度和高度,返回:0:失败1:成功
SetWindowSize(hwnd, width, height) = 设置窗口的大小,返回:0:失败1:成功
SetWindowState(hwnd, flag) = 设置窗口的状态,返回:0:失败1:成功
SetWindowText(hwnd, title) = 设置窗口的标题,返回:0:失败1:成功
SetWindowTransparent(hwnd, trans) = 设置窗口的透明度,返回:0:失败1:成功
EnumProcess(name) = 根据指定进程名, 枚举系统中符合条件的进程PID, 并且按照进程打开顺序排序,返回:字符串 :返回所有匹配的进程PID, 并按打开顺序排序,格式"pid1, pid2, pid3"
EnumWindowByProcessId(pid, title, class_name, filter) = 根据指定进程pid以及其它条件, 枚举系统中符合条件的窗口,返回:返回所有匹配的窗口句柄字符串,格式"hwnd1, hwnd2, hwnd3"
# 大漠插件答题
FaqCancel() = 可以把上次FaqPost的发送取消, 接着下一次FaqPost,返回:0:失败1:成功
FaqCapture(x1, y1, x2, y2, quality, delay, time) = 截取指定范围内的动画或者图像, 并返回此句柄,返回:图像或者动画句柄
FaqCaptureFromFile(x1, y1, x2, y2, file, quality) = 截取指定图片中的图像, 并返回此句柄,返回:图像或者动画句柄
FaqFetch() = 获取由FaqPost发送后, 由服务器返回的答案,返回:函数调用失败, 返回"Error:错误描述",函数调用成功, 返回"OK:答案"",根据FaqPost中 request_type取值的不同, 返回值不同",当request_type 为0时, 答案的格式为"x, y",当request_type 为1时, 答案的格式为"1" "2" "3" "4" "5" "6",当request_type 为2时, 答案就是要求的答案 比如 "李白" ",当request_type 为3时, 答案的格式为"x1, y1|x2, y2" 比如 "20, 30|78, 68",如果返回为空字符串, 表示FaqPost还未处理完毕, 或者没有调用过FaqPost
FaqGetSize(handle) = 获取句柄所对应的数据包的大小, 单位是字节,返回:数据包大小, 一般用于判断数据大小, 选择合适的压缩比率
FaqPost(server, handle, request_type, time_out) = 发送指定的图像句柄到指定的服务器, 并立即返回(异步操作),返回:0:失败, 一般是FaqPost还没处理完1:成功
FaqS(server, handle, request_type, time_out) = 发送指定的图像句柄到指定的服务器, 并等待返回结果(同步等待),返回:函数调用失败, 返回"Error:错误描述"",函数调用成功, 返回"OK:答案"",根据request_type取值的不同, 返回值不同",当request_type 为0时, 答案的格式为"x, y",当request_type 为1时, 答案的格式为"1" "2" "3" "4" "5" "6",当request_type 为2时, 答案就是要求的答案 比如 "李白" ",当request_type 为3时, 答案的格式为"x1, y1|x2, y2" 比如 "20, 30|78, 68"
# 大漠插件算法
ExcludePos(all_pos, type, x1, y1, x2, y2) = 根据部分Ex接口的返回值, 排除指定范围区域内的坐标,返回:经过筛选以后的返回值, 格式和type指定的一致
FindNearestPos(all_pos, type, x, y) = 根据部分Ex接口的返回值, 然后在所有坐标里找出距离指定坐标最近的那个坐标,返回:返回的格式和type有关,如果type为0, 那么返回的格式是"id, x, y",如果type为1, 那么返回的格式是"x, y"
SortPosDistance(all_pos, type, x, y) = 根据部分Ex接口的返回值, 然后对所有坐标根据对指定坐标的距离进行从小到大的排序,返回:返回的格式和type指定的格式一致
# 大漠插件系统
Beep(f, duration) = 蜂鸣器,返回:0:失败1:成功
CheckFontSmooth() = 检测当前系统是否有开启屏幕字体平滑,返回:0:系统没开启平滑字体, 1:系统有开启平滑字体
CheckUAC() = 检测当前系统是否有开启UAC(用户账户控制),返回:0:没开启UAC1:开启了UAC
Delay(mis) = 延时指定的毫秒, 过程中不阻塞UI操作, 高级语言使用返回:0:失败1:成功
DisableFontSmooth() = 关闭当前系统屏幕字体平滑, 同时关闭系统的ClearType功能,返回:0:失败1:成功
DisablePowerSave() = 关闭电源管理, 不会进入睡眠,返回:0:失败1:成功
DisableScreenSave() = 关闭屏幕保护,返回:0:失败1:成功
ExitOs(type) = 退出系统(注销 重启 关机),返回:0:失败1:成功
GetClipboard() = 获取剪贴板的内容,返回:以字符串表示的剪贴板内容
GetDir(type) = 得到系统的路径,返回:返回路径
GetDiskSerial() = 获取本机的硬盘序列号, 支持ide scsi硬盘,要求调用进程必须有管理员权限, 否则返回空串,返回:字符串表达的硬盘序列号
GetMachineCode() = 获取本机的机器码, (带网卡),此机器码用于插件网站后台, 要求调用进程必须有管理员权限, 否则返回空串, 函数原型:,返回:字符串表达的机器机器码
GetMachineCodeNoMac() = 获取本机的机器码, (不带网卡),要求调用进程必须有管理员权限, 否则返回空串,返回:字符串表达的机器机器码
GetNetTime() = 从网络获取当前北京时间,返回:时间格式, 和now返回一致, 比如"2001-11-01 23:14:08"
GetNetTimeSafe() = 从网络获取当前北京时间, 同GetNetTime,此接口数据是加密传送, 以免被人破解,返回:时间格式, 和now返回一致, 比如"2001-11-01 23:14:08"
GetOsType() = 得到操作系统的类型,返回:0:win95/98/me/nt4, 01:xp/20002:20033:win7/vista/2008
GetScreepth() = 获取屏幕的色深,返回:返回系统颜色深度, (16或者32等)
GetScreenHeight() = 获取屏幕的高度,返回:返回屏幕的高度
GetScreenWidth() = 获取屏幕的宽度,返回:返回屏幕的宽度
GetTime() = 获取当前系统从开机到现在所经历过的时间, 单位是毫秒,返回:时间(单位毫秒)
Is64Bit() = 判断当前系统是否是64位操作系统,返回:0:不是64位系统1:是64位系统
Play(media_file) = 播放指定的MP3或者wav文件,返回:0:失败非0表示当前播放的ID可以用Stop来控制播放结束
RunApp(app_path, mode) = 运行指定的应用程序,返回:0:失败1:成功
SetClipboard(value) = 设置剪贴板的内容,返回:0:失败1:成功
SetDisplayAcceler(level) = 设置当前系统的硬件加速级别,返回:0:失败, 1:成功
SetScreen(width, height, depth) = 设置系统的分辨率 系统色深,返回:0:失败1:成功
SetUAC(enable) = 设置当前系统的UAC(用户账户控制),返回:0:操作失败1:操作成功
Stop(id) = 停止指定的音乐,返回:0:失败1:成功
# 大漠插件键鼠, QML
GetCursorPos(x, y) = 获取鼠标位置,返回:0:失败1:成功
GetCursorShape() = 获取鼠标特征码,当BindWindow或者BindWindowEx中的mouse参数含有dx, mouse, cursor时,获取到的是后台鼠标特征,否则是前台鼠标特征, 后台特征码是收费功能,返回:成功时, 返回鼠标特征码,  失败时, 返回空的串
GetCursorShapeEx(type) = 获取鼠标特征码,当BindWindow或者BindWindowEx中的mouse参数含有dx, mouse, cursor时,获取到的是后台鼠标特征,否则是前台鼠标特征, 后台特征码是收费功能,返回:成功时, 返回鼠标特征码,  失败时, 返回空的串
GetCursorSpot() = 获取鼠标热点位置,参考工具中抓取鼠标后, 那个闪动的点就是热点坐标, 不是鼠标坐标,当BindWindow或者BindWindowEx中的mouse参数含有dx, mouse, cursor时,获取到的是后台鼠标热点位置,否则是前台鼠标热点位置, 后台热点位置是收费功能,返回:成功时, 返回形如"x, y"的字符串  失败时, 返回空的串
GetKeyState(vk_code) = 获取指定的按键状态, (前台信息, 不是后台),返回:0:弹起1:按下
KeyDown(vk_code) = 按住指定的虚拟键码,返回:0:失败1:成功
KeyDownChar(key_str) = 按住指定的虚拟键码,返回:0:失败1:成功
KeyPress(vk_code) = 按下指定的虚拟键码,返回:0:失败1:成功
KeyPressChar(key_str) = 按下指定的虚拟键码,返回:0:失败1:成功
KeyPressStr(key_str, delay) = 根据指定的字符串序列, 依次按顺序按下其中的字符,返回:0:失败1:成功
KeyUp(vk_code) = 弹起来虚拟键vk_code,返回:0:失败1:成功
KeyUpChar(key_str) = 弹起来虚拟键key_str,返回:0:失败1:成功
LeftClick() = 按下鼠标左键,返回:0:失败1:成功
LeftDoubleClick() = 双击鼠标左键,返回:0:失败1:成功
LeftDown() = 按住鼠标左键,返回:0:失败1:成功
LeftUp() = 弹起鼠标左键,返回:0:失败1:成功
MiddleClick() = 按下鼠标中键,返回:0:失败1:成功
MoveR(rx, ry) = 鼠标相对于上次的位置移动rx, ry,返回:0:失败1:成功
MoveTo(x, y) = 把鼠标移动到目的点(x, y),返回:0:失败1:成功
MoveToEx(x, y, w, h) = 把鼠标移动到目的范围内的任意一点,返回:返回要移动到的目标点,格式为x, y,比如MoveToEx 100, 100, 10, 10, 返回值可能是101, 102
RightClick() = 按下鼠标右键,返回:0:失败1:成功
RightDown() = 按住鼠标右键,返回:0:失败1:成功
RightUp() = 弹起鼠标右键,返回:0:失败1:成功
SetKeypadDelay(type, delay) = 设置按键时, 键盘按下和弹起的时间间隔,某些窗口可能需要调整这个参数才可以正常按键,返回:0:失败1:成功
SetMouseDelay(type, delay) = 设置鼠标单击或者双击时, 鼠标按下和弹起的时间间隔,某些窗口可能需要调整这个参数才可以正常点击,返回:0:失败1:成功
WaitKey(vk_code, time_out) = 等待指定的按键按下 (前台, 不是后台),返回:0:超时1:指定的按键按下
WheelDown() = 滚轮向下滚,返回:0:失败1:成功
WheelUp() = 滚轮向上滚,返回:0:失败1:成功
# 大漠插件防护盾
DmGuard(enable, type) = 针对部分检测措施的保护盾,返回:0:失败1:成功
"""

if __name__ == "__main__":
    DM = DmHelper()
    print(DM.dm.ver())
