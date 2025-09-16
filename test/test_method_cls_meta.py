# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-14 23:18:19
LastEditTime : 2025-09-14 23:20:34
FilePath     : /CODE/test_method_cls_meta.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from __future__ import annotations

from xjlib.xt_class import MethodClsMeta
from xjlib.xt_wraps import LogCls

log = LogCls()


class TestMethodCls(metaclass=MethodClsMeta):
    """测试MethodClsMeta元类的类"""

    MixinAttr = True  # 启用属性访问支持
    MixinItem = True  # 启用下标操作支持
    MixinIter = True  # 启用迭代支持
    MixinRepr = True  # 启用友好的字符串表示支持

    def __init__(self):
        self.name = 'MethodClsMetaTest'
        self.version = '1.0'


def test_method_cls_meta():
    """测试MethodClsMeta元类的各项功能"""
    print('\n=== 开始测试MethodClsMeta元类 ===')

    # 检查是否正确添加了Mixin类的方法
    print('\n1. 检查MethodClsMeta是否正确添加了Mixin方法：')
    print(f'- 是否有__getitem__方法: {hasattr(TestMethodCls, "__getitem__")}')
    print(f'- 是否有__setitem__方法: {hasattr(TestMethodCls, "__setitem__")}')
    print(f'- 是否有__getattr__方法: {hasattr(TestMethodCls, "__getattr__")}')
    print(f'- 是否有__setattr__方法: {hasattr(TestMethodCls, "__setattr__")}')
    print(f'- 是否有__iter__方法: {hasattr(TestMethodCls, "__iter__")}')
    print(f'- 是否有__repr__方法: {hasattr(TestMethodCls, "__repr__")}')

    # 实例化并测试各项功能
    print('\n2. 测试MethodClsMeta元类创建的实例功能：')
    obj = TestMethodCls()

    # 测试属性访问功能
    print('\n测试属性访问功能 (MixinAttr):')
    print(f'- 访问存在的属性: obj.name = {obj.name}')
    obj.new_attr = 'new_value'
    print(f'- 设置新属性: obj.new_attr = {obj.new_attr}')
    print(f'- 访问不存在的属性: obj.non_existent = {obj.non_existent}')

    # 测试下标操作功能
    print('\n测试下标操作功能 (MixinItem):')
    obj['key1'] = 'value1'
    print(f"- 设置key1: obj['key1'] = {obj['key1']}")
    obj['key2'] = 'value2'
    print(f"- 设置key2: obj['key2'] = {obj['key2']}")

    # 测试迭代功能
    print('\n测试迭代功能 (MixinIter):')
    print('- 迭代对象的所有属性：')
    for key, value in obj:
        print(f'  {key}: {value}')

    # 测试字符串表示功能
    print('\n测试字符串表示功能 (MixinRepr):')
    print(f'- 对象的字符串表示: {obj}')

    print('\n=== MethodClsMeta元类测试完成 ===')


if __name__ == '__main__':
    test_method_cls_meta()
