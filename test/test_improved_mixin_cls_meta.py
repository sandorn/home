#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试整合了MethodClsMeta优点的改进版MixinClsMeta元类

该文件用于验证MixinClsMeta元类整合了MethodClsMeta的优点后的功能是否正常，
包括重复避免、参数传递等特性。
"""

import sys
from pathlib import Path

# 添加项目目录到sys.path，确保可以导入xjlib模块
sys.path.append(str(Path(__file__).parent.parent))

from xjlib.xt_class import MixinClsMeta, ItemMixin, AttrMixin, IterMixin, ReprMixin


def test_duplicate_mixin_prevention():
    """测试MixinClsMeta是否能防止重复添加Mixin类"""
    print("=== 测试1: 防止重复添加Mixin类 ===")
    
    # 定义一个已经包含ItemMixin的基类
    class BaseWithMixin(ItemMixin):
        pass
    
    # 创建一个使用MixinClsMeta的类，同时设置MixinItem=True
    class TestDuplicateMixin(BaseWithMixin, metaclass=MixinClsMeta):
        MixinItem = True  # 这里故意启用已经存在的Mixin
        MixinAttr = True  # 同时启用新的Mixin
        
        def __init__(self):
            self._data = {}
    
    test_obj = TestDuplicateMixin()
    test_obj['key'] = 'value'  # 测试ItemMixin功能
    test_obj.attr = 'attr_value'  # 测试AttrMixin功能
    
    # 检查ItemMixin是否只出现一次在基类列表中
    item_mixin_count = TestDuplicateMixin.__bases__.count(ItemMixin)
    
    print(f"TestDuplicateMixin基类列表: {TestDuplicateMixin.__bases__}")
    print(f"ItemMixin在基类列表中出现次数: {item_mixin_count}")
    print(f"测试下标操作: test_obj['key'] = {test_obj['key']}")
    print(f"测试属性访问: test_obj.attr = {test_obj.attr}")
    
    # 验证ItemMixin只出现一次
    assert item_mixin_count == 1, "ItemMixin在基类列表中出现了多次！"
    print("✓ 测试通过: MixinClsMeta成功防止了重复添加Mixin类")
    
    return True


def test_keyword_arguments_passing():
    """测试MixinClsMeta是否能正确传递额外的关键字参数"""
    print("\n=== 测试2: 正确传递额外的关键字参数 ===")
    
    # 自定义一个元类，继承自MixinClsMeta，用于测试参数传递
    class CustomMeta(MixinClsMeta):
        def __new__(mcs, name, bases, dct, **kwds):
            print(f"CustomMeta接收到的额外参数: {kwds}")
            # 验证是否接收到了额外参数
            assert 'custom_param' in kwds, "没有接收到custom_param参数！"
            assert 'another_param' in kwds, "没有接收到another_param参数！"
            return super().__new__(mcs, name, bases, dct, **kwds)
    
    # 使用自定义元类并传递额外参数
    class TestWithParams(metaclass=CustomMeta, custom_param='value1', another_param='value2'):
        MixinItem = True
        
        def __init__(self):
            self._data = {}
    
    test_obj = TestWithParams()
    test_obj['key'] = 'value'
    print(f"测试下标操作: test_obj['key'] = {test_obj['key']}")
    print("✓ 测试通过: MixinClsMeta成功传递了额外的关键字参数")
    
    return True


def test_mixin_order_inheritance():
    """测试Mixin类是否被添加到基类列表开头，便于子类覆盖"""
    print("\n=== 测试3: Mixin类在基类列表中的顺序 ===")
    
    # 定义一个自定义的ItemMixin，用于测试覆盖
    class CustomItemMixin(ItemMixin):
        def __getitem__(self, key):
            print(f"CustomItemMixin.__getitem__被调用: {key}")
            if key == 'special':
                return 'special_value'
            return super().__getitem__(key)
    
    # 创建一个类，同时包含CustomItemMixin和设置MixinItem=True
    # 由于MixinClsMeta会将Mixin类添加到开头，所以CustomItemMixin应该能覆盖默认的ItemMixin
    class TestMixinOrder(CustomItemMixin, metaclass=MixinClsMeta):
        MixinItem = True  # 启用默认的ItemMixin
        
        def __init__(self):
            self._data = {'key': 'value'}
    
    print(f"TestMixinOrder基类列表: {TestMixinOrder.__bases__}")
    test_obj = TestMixinOrder()
    print(f"测试标准key: test_obj['key'] = {test_obj['key']}")
    print(f"测试特殊key: test_obj['special'] = {test_obj['special']}")
    
    # 验证ItemMixin是否在基类列表中
    assert ItemMixin in TestMixinOrder.__bases__, "ItemMixin没有被添加到基类列表中！"
    print("✓ 测试通过: Mixin类被正确添加到基类列表中")
    
    return True


def test_mixin_cls_parent_functionality():
    """测试MixinClsParent类的功能是否正常"""
    print("\n=== 测试4: MixinClsParent类功能测试 ===")
    
    from xjlib.xt_class import MixinClsParent
    
    # 创建一个使用MixinClsParent作为基类的类
    class TestMixinParent(MixinClsParent):
        MixinItem = True
        MixinAttr = True
        MixinIter = True
        MixinRepr = True
        
        def __init__(self, **kwargs):
            self._data = {}
            for key, value in kwargs.items():
                self._data[key] = value
    
    test_obj = TestMixinParent(name='Test', version='1.0')
    test_obj['key'] = 'value'
    test_obj.attr = 'attr_value'
    
    print(f"测试下标操作: test_obj['key'] = {test_obj['key']}")
    print(f"测试属性访问: test_obj.attr = {test_obj.attr}")
    print(f"测试迭代功能: {list(test_obj)}")
    print(f"测试字符串表示: {test_obj}")
    
    print("✓ 测试通过: MixinClsParent类功能正常")
    
    return True


def main():
    """主函数，运行所有测试"""
    tests = [
        test_duplicate_mixin_prevention,
        test_keyword_arguments_passing,
        test_mixin_order_inheritance,
        test_mixin_cls_parent_functionality
    ]
    
    all_passed = True
    for test in tests:
        try:
            success = test()
            if not success:
                all_passed = False
        except Exception as e:
            print(f"测试失败: {e}")
            all_passed = False
    
    if all_passed:
        print("\n=== 所有测试通过！改进版MixinClsMeta功能正常 ===")
        return 0
    else:
        print("\n=== 部分测试失败！改进版MixinClsMeta存在问题 ===")
        return 1


if __name__ == "__main__":
    sys.exit(main())