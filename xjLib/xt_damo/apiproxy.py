import math
import random
from time import sleep, time
from typing import Any


class _timed_loop:
    """超时循环上下文管理器"""

    def __init__(self, timeout):
        self.timeout = timeout
        self.start = time() * 1000

    def __iter__(self):
        while not self._expired():
            yield

    def _expired(self):
        return self.timeout > 0 and (time() * 1000 - self.start) >= self.timeout

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class ApiProxy:
    def __init__(self, dmobject: Any) -> None:
        """高级功能封装
        Args:
            dmobject: 大漠插件实例
        """
        if not dmobject:
            raise ValueError("dmobject cannot be None")
        self.dm = dmobject

    # 新增辅助方法
    def _timeout_expired(self, start, timeout):
        return timeout > 0 and (time() * 1000 - start) >= timeout

    def _valid_coordinates(self, x, y):
        return x > 0 and y > 0

    def 绑定窗口(
        self,
        局部窗口句柄,
        显示参数="gdi",
        鼠标参数="windows3",
        键盘参数="windows",
        公共参数="dx.public.fake.window.min|dx.public.hack.speed",
        绑定模式=101,
    ):
        _state = True
        ret = self.dm.BindWindowEx(
            局部窗口句柄, 显示参数, 鼠标参数, 键盘参数, 公共参数, 绑定模式
        )
        if ret != 1:
            print("窗口绑定失败!错误代码:" + self.dm.GetLastError())
            _state = False

        return _state

    def 解绑窗口(self):
        ret = self.dm.UnBindWindow()
        return ret == 1

    # 示例：获取窗口标题
    def 获取窗口标题(self, 窗口句柄):
        return self.dm.GetWindowTitle(窗口句柄)

    def _parse_result(self, ret):
        """解析坐标结果，增加容错处理"""
        parts = (ret or "").split("|")
        try:
            return int(parts[1]), int(parts[2]) if len(parts) >= 3 and parts[
                1
            ].isdigit() and parts[2].isdigit() else (0, 0)
        except (ValueError, IndexError):
            return (0, 0)

    def _find_and_act(
        self,
        x1,
        y1,
        x2,
        y2,
        find_func,
        target,
        timeout=0,
        click=False,
        center=False,
        disappear=False,
        confidence=0.9,
    ):
        """通用查找执行方法（参数命名优化）"""
        state = False
        delay = random.randint(50, 400) / 1000
        start = time() * 1000

        while not self._timeout_expired(start, timeout):
            # 统一查找逻辑
            x, y = self._parse_result(find_func(x1, y1, x2, y2, target))

            # 结果处理
            if self._valid_coordinates(x, y):
                if click:
                    self.dm.鼠标移动单击(x, y, center)
                state = True
                if not disappear:
                    break
            elif disappear:
                break

            sleep(delay)

        return state, x, y

    def 找字单击至消失(self, x1, y1, x2, y2, text, color, timeout=0, center=False):
        """优化参数命名和lambda表达式"""
        return self._find_and_act(
            x1,
            y1,
            x2,
            y2,
            lambda x1, y1, x2, y2, t: self.dm.FindStrE(x1, y1, x2, y2, t, color, 0.9),
            text,
            timeout,
            click=True,
            center=center,
            disappear=True,
        )

    def 找字单击(self, x1, y1, x2, y2, text, color, timeout=0, center=False):
        return self._find_and_act(
            x1,
            y1,
            x2,
            y2,
            lambda x1, y1, x2, y2, t: self.dm.FindStrE(x1, y1, x2, y2, t, color, 0.9),
            text,
            timeout,
            click=True,
            center=center,
        )

    def 找字返回坐标(self, x1, y1, x2, y2, text, color, timeout=0):
        state, (x, y) = False, (0, 0)
        with self._timed_loop(timeout) as loop:
            for _ in loop:
                x, y = self._parse_result(
                    self.dm.FindStrE(x1, y1, x2, y2, text, color, 0.9)
                )
                if self._valid_coordinates(x, y):
                    state = True
                    break
        return state, x, y

    def 简易找字(self, x_1, y_1, x_2, y_2, 字名, 颜色值, t=0):
        return self._find_and_act(
            x_1, y_1, x_2, y_2, lambda *args: self.dm.FindStrE(*args, 0.9), 字名, t
        )

    def 找图单击至消失(
        self, x1, y1, x2, y2, name, timeout=0, scan_mode=0, center=False
    ):
        """优化参数命名和lambda表达式"""
        return self._find_and_act(
            x1,
            y1,
            x2,
            y2,
            lambda x1, y1, x2, y2, n: self.dm.FindPicE(
                x1, y1, x2, y2, n, "000000", 0.9, scan_mode
            ),
            name,
            timeout,
            click=True,
            center=center,
            disappear=True,
        )

    def 找图单击(self, x1, y1, x2, y2, name, timeout=0, scan_mode=0, center=False):
        return self._find_and_act(
            x1,
            y1,
            x2,
            y2,
            lambda x1, y1, x2, y2, n: self.dm.FindPicE(
                x1, y1, x2, y2, n, "000000", 0.9, scan_mode
            ),
            name,
            timeout,
            click=True,
            center=center,
        )

    def 找图返回坐标(self, x1, y1, x2, y2, name, timeout=0, scan_mode=0):
        """复用_find_and_act逻辑"""
        state, x, y = self._find_and_act(
            x1,
            y1,
            x2,
            y2,
            lambda x1, y1, x2, y2, n: self.dm.FindPicE(
                x1, y1, x2, y2, n, "000000", 0.9, scan_mode
            ),
            name,
            timeout,
        )
        return state, x, y

    def 简易找图(self, x1, y1, x2, y2, name, timeout=0, scan_mode=0):
        return self._find_and_act(
            x1,
            y1,
            x2,
            y2,
            lambda x1, y1, x2, y2, n: self.dm.FindPicE(
                x1, y1, x2, y2, n, "000000", 0.9, scan_mode
            ),
            name,
            timeout,
        )

    def 鼠标移动单击(self, x, y, autoResetPosition=False):
        """带随机延迟的鼠标点击操作"""
        sleep_mis = random.randint(50, 200)
        self.dm.MoveTo(x, y)
        self.dm.LeftClick()
        sleep(sleep_mis / 1000)
        if autoResetPosition:
            self.dm.MoveTo(x + random.randint(50, 300), y + random.randint(50, 300))

    def sendkey(self, vk_code, delays=20):
        self.dm.KeyDown(vk_code)
        sleep(delays / 1000)
        self.dm.KeyUp(vk_code)

    def 简易识字(self, x1, y1, x2, y2, color, confidence=0.9, timeout=0):
        """优化后的OCR识别方法"""

        def ocr_operation():
            result = self.dm.Ocr(x1, y1, x2, y2, color, confidence)
            return result if result else None

        if timeout > 0:
            with self._timed_loop(timeout) as loop:
                for _ in loop:
                    if text := ocr_operation():
                        return text
                    sleep(random.uniform(0.05, 0.4))
        else:
            if text := ocr_operation():
                return text
        return False

    def 圆形渐开找鼠标(
        self, 
        起点X,          # 螺旋轨迹的起始X坐标（像素）
        起点Y,          # 螺旋轨迹的起始Y坐标（像素）
        特征码,         # 目标光标的特征码（由dm.GetCursorShape返回值确定）
        radius=1,       # 初始螺旋半径（像素单位，控制轨迹与起点的初始距离）
        step=1,         # 半径增长步长（每20度增加的像素值，控制螺旋展开速度）
        圈数=6          # 最大螺旋圈数（控制轨迹覆盖范围，防止无限循环）
    ):
        """
        通过渐开螺旋轨迹移动鼠标，查找指定特征码的光标并执行点击
        
        轨迹特点：以[起点X,起点Y]为中心，初始半径为radius，
                每20度（即每2次内层循环）半径增加step，形成向外扩展的螺旋轨迹
        
        Returns:
            bool: 找到目标光标并点击返回True，否则遍历完所有圈数后返回False
        """
        # 1度对应的弧度值（用于角度转弧度计算）
        radian_per_degree = math.radians(1)  

        # 外层循环控制螺旋圈数
        for _ in range(圈数):
            # 内层循环以10度为步长遍历360度圆周（共36个采样点/圈）
            for angle in range(0, 360, 10):
                # 将角度转换为弧度（数学函数需要弧度制输入）
                current_radian = angle * radian_per_degree
                
                # 计算当前角度对应的螺旋坐标（极坐标转笛卡尔坐标）
                x = 起点X + radius * math.cos(current_radian)
                y = 起点Y + radius * math.sin(current_radian)
                
                # 移动鼠标到计算出的坐标位置
                self.dm.MoveTo(x, y)
                
                # 检查当前光标是否符合目标特征码
                if self.dm.GetCursorShape() == 特征码:
                    self.dm.LeftClick()  # 找到目标后执行左键点击
                    return True          # 立即返回成功状态
                
                # 每20度（即每2次内层循环）增加半径，形成渐开效果
                if angle % 20 == 0:
                    radius += step
                
                # 控制鼠标移动节奏（1ms延迟防止过快移动）
                sleep(0.001)
        
        # 遍历完所有圈数未找到目标，返回失败
        return False

    def 散点渐开找鼠标(
        self, 起点坐标X, 起点坐标Y, 鼠标特征码, radius=2, radius步长=0.6, 圈数判定=80
    ):
        for _ in range(圈数判定):
            xzb = 起点坐标X + math.cos(radius) + radius * math.sin(radius)
            yzb = 起点坐标Y + math.sin(radius) - radius * math.cos(radius)
            self.dm.MoveTo(xzb, yzb)
            mouse_tz = self.dm.GetCursorShape()
            if mouse_tz == 鼠标特征码:
                self.dm.LeftClick()
                return True
            radius += radius步长
            sleep(0.001)
        return False

    def 椭圆渐开找鼠标(
        self,
        起点坐标X,
        起点坐标Y,
        鼠标特征码,
        宽度radius=0.5,
        高度radius=8,
        radius步长=0.5,
        圈数判定=6,
    ):
        seed = 3.1415926535897 / 180

        for _ in range(圈数判定):
            for angle in range(0, 360, 10):
                xzb = 起点坐标X + 宽度radius * math.cos(angle * seed)
                yzb = 起点坐标Y + 高度radius * math.sin(angle * seed)
                self.dm.MoveTo(xzb, yzb)
                sleep(0.001)
                mouse_tz = self.dm.GetCursorShape()
                if mouse_tz == 鼠标特征码:
                    self.dm.LeftClick()
                    return True
                if angle % 20 == 0:
                    宽度radius += radius步长
                    高度radius += radius步长
                sleep(0.001)
            sleep(0.001)
        return False

    def 方形渐开找鼠标(self, 起点坐标X, 起点坐标Y, 鼠标特征码, 步长=10, 圈数判定=6):
        m = 0
        xzb = 起点坐标X
        yzb = 起点坐标Y
        for _ in range(圈数判定):
            for _ in range(m):
                xzb += 步长
                self.dm.MoveTo(xzb, yzb)
                mouse_tz = self.dm.GetCursorShape()
                if mouse_tz == 鼠标特征码:
                    self.dm.LeftClick()
                    return True
            for _ in range(m + 6):
                yzb -= 步长
                self.dm.MoveTo(xzb, yzb)
                mouse_tz = self.dm.GetCursorShape()
                if mouse_tz == 鼠标特征码:
                    self.dm.LeftClick()
                    return True
            m += 1
            for _ in range(m):
                xzb -= 步长
                self.dm.MoveTo(xzb, yzb)
                mouse_tz = self.dm.GetCursorShape()
                if mouse_tz == 鼠标特征码:
                    self.dm.LeftClick()
                    return True
            for _ in range(m + 6):
                yzb += 步长
                self.dm.MoveTo(xzb, yzb)
                mouse_tz = self.dm.GetCursorShape()
                if mouse_tz == 鼠标特征码:
                    self.dm.LeftClick()
                    return True
            m += 1
            sleep(0.001)
        return False
