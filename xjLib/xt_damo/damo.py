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

from __future__ import annotations

from time import sleep
from typing import Any

from apiproxy import ApiProxy
from coreengine import CoreEngine
from key import Key
from mouse import Mouse
from regsvr import DmRegister

_Reg_code = 'jv965720b239b8396b1b7df8b768c919e86e10f'
_Ver_info = 'ddsyyc365'

errs = {
    -1: '无法连接网络',
    -2: '进程没有以管理员方式运行，win7 win8 vista 2008 建议关闭uac)',
    0: '失败 (未知错误)',
    1: '成功',
    2: '余额不足',
    3: '绑定了本机器,但是账户余额不足50元.',
    4: '注册码错误',
    5: '你的机器或者IP在黑名单列表中或者不在白名单列表中.',
    6: '非法使用插件.',
    7: '你的帐号因为非法使用被封禁.',
    8: 'ver_info不在你设置的附加白名单中.',
    77: '机器码或者IP因为非法使用,而被封禁.',
    -8: '版本附加信息长度超过了20',
    -9: '版本附加信息里包含了非法字母.',
}


class DmExcute:
    def __init__(self, dm_dirpath: str | None = None):
        self.RegDM = DmRegister(dm_dirpath)
        self.dm_instance = self.RegDM.dm_instance
        self.Key = Key(self.dm_instance)
        self.Mouse = Mouse(self.dm_instance)
        self.ApiProxy = ApiProxy(self.dm_instance)
        self.CoreEngine = CoreEngine(self.dm_instance)
        # 动态映射组件
        self._components = {
            'Key': self.Key,
            'Mouse': self.Mouse,
            'ApiProxy': self.ApiProxy,
            'CoreEngine': self.CoreEngine,
        }

        # 更严格的检查，确保dm_instance不为None
        if self.dm_instance is None:
            raise RuntimeError('大漠插件实例初始化失败')

        # 确保不为None
        if not all([self.Key, self.Mouse, self.CoreEngine, self.ApiProxy]):
            raise RuntimeError('模块初始化失败')

        tmp_ret = self.dm_instance.Reg(_Reg_code, _Ver_info)

        if tmp_ret != 1:
            print(f'授权失败,错误代码：{tmp_ret} | 授权问题： {errs.get(tmp_ret, "未知错误")}')
            raise RuntimeError(f'授权失败,错误代码：{tmp_ret} | 授权问题： {errs.get(tmp_ret, "未知错误")}')

    def __repr__(self) -> str:
        """返回对象的字符串表示"""
        try:
            return f'版本：{self.ver()} , ID：{self.GetID()}'
        except Exception as e:
            return f'获取版本和ID时出错: {e}'

    def __getattr__(self, key: str) -> Any:
        for _, component in self._components.items():
            if hasattr(component, key):
                return getattr(component, key)

        # 最后尝试大漠原生方法，确保dm_instance不为None
        if self.dm_instance is not None:
            try:
                return getattr(self.dm_instance, key)
            except AttributeError:
                pass

        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")


def conv_to_rgb(color: str) -> tuple[int, int, int]:
    """将16进制颜色字符串转换为RGB元组"""
    rgb_str = [color[:2], color[2:4], color[4:6]]
    rgb = [int(i, 16) for i in rgb_str]
    return tuple(rgb)


if __name__ == '__main__':
    dm = DmExcute()
    print(dm)
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
        print(f'--- {i} --- Mouse position: {x_i}, target_x: {xy_v}, delta_x: {delta_x}')

        sleep(0.1)
        x, y = dm.position
        color = dm.GetColor(x, y)

        print(color, '鼠标位置颜色RGB值:', conv_to_rgb(color))

        """
        ### 更灵活的实现方式建议
        1. 1.使用类方法自动发现
        # 自动收集类的所有公共方法（不以下划线开头的方法）
        ```
        def get_public_methods(cls):
            return [name for name in dir(cls) if not name.startswith('_') and callable(getattr(cls, name))]

        # 然后在主类中使用
        key_methods = get_public_methods(Key)
        mouse_methods = get_public_methods(Mouse)
        ```
        2. 1.使用装饰器注册方法
        ```
        class DmExcute:
            _registered_methods = {}
            
            @classmethod
            def register_method(cls, name, obj, method_name):
                cls._registered_methods[name] = (obj, method_name)
            
            def __init__(self, dm_dirpath=None):
                # 初始化代码不变
                # 注册方法
                for method_name in dir(self.Key):
                    if not method_name.startswith('_'):
                        self.register_method(method_name,self.Key, method_name)
                # 同理注册其他类的方法
                
            def __getattr__(self, key):
                if key in self._registered_methods:
                    obj, method_name = self._registered_methods[key]
                    return getattr(obj, method_name)
                # 其他查找逻辑
        ```
        3. 1.使用混入类和元类
        ```
        class MethodDelegationMeta(type):
            def __new__(mcs, name, bases, attrs):
                # 定义需要委托的组件类列表
                component_classes = [Key, Mouse, ApiProxy, CoreEngine]
                
                # 为每个组件类创建方法映射字典
                attrs['_method_mappings'] = {}
                
                # 遍历所有组件类，收集公共方法
                for component_cls in component_classes:
                    # 获取所有公共方法名
                    methods = [attr for attr in dir(component_cls) 
                            if not attr.startswith('_') 
                            and callable(getattr(component_cls, attr))]
                    
                    # 建立方法到组件类的映射
                    for method_name in methods:
                        attrs['_method_mappings'][method_name] = component_cls.__name__
                
                return super().__new__(mcs, name, bases, attrs)

        class DmExcute(metaclass=MethodDelegationMeta):
            def __init__(self, dm_dirpath=None):
                # 初始化代码...
            
            def __getattr__(self, key):
                # 检查是否有映射的方法
                if hasattr(self, '_method_mappings') and key in self._method_mappings:
                    component_name = self._method_mappings[key]
                    component = getattr(self, component_name)
                    return getattr(component, key)
                
                # 原有查找逻辑...
        ```
        4. 1.使用动态属性映射
        ```
        class DmExcute:
            def __init__(self, dm_dirpath=None):
                # 初始化代码不变
                
                # 动态映射组件
                self._components = {
                    'Key': self.Key,
                    'Mouse': self.Mouse,
                    'ApiProxy': self.ApiProxy,
                    'CoreEngine': self.CoreEngine
                }
            
            def __getattr__(self, key):
                # 遍历所有组件查找方法
                for comp_name, component in self._components.
                items():
                    if hasattr(component, key):
                        return getattr(component, key)
                # 其他查找逻辑
        ```
        """
