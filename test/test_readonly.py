#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试readonly函数的功能
"""
from xjlib.xt_class import readonly


def test_basic_readonly():
    """测试基本的只读属性功能"""
    print("\n====== 测试基本的只读属性功能 ======")
    
    class Person:
        def __init__(self, name):
            self._name = name  # 注意：这里必须使用下划线前缀存储实际值
        name = readonly('_name')
    
    p = Person("Alice")
    print(f"读取只读属性: {p.name}")
    
    try:
        p.name = "Bob"
        print("错误: 只读属性被修改了!")
    except AttributeError as e:
        print(f"成功捕获设置只读属性的异常: {e}")
    
    try:
        del p.name
        print("错误: 只读属性被删除了!")
    except AttributeError as e:
        print(f"成功捕获删除只读属性的异常: {e}")


def test_with_slots():
    """测试与__slots__的兼容性"""
    print("\n====== 测试与__slots__的兼容性 ======")
    
    class PersonWithSlots:
        __slots__ = ('_name', '_age')
        
        def __init__(self, name, age):
            self._name = name
            self._age = age
        
        name = readonly('_name')
        age = readonly('_age')
    
    p = PersonWithSlots("Bob", 30)
    print(f"读取只读属性(name): {p.name}")
    print(f"读取只读属性(age): {p.age}")
    
    try:
        p.name = "Charlie"
        print("错误: 只读属性被修改了!")
    except AttributeError as e:
        print(f"成功捕获设置只读属性的异常: {e}")


def test_without_underscore():
    """测试不使用下划线前缀的情况"""
    print("\n====== 测试不使用下划线前缀的情况 ======")
    
    class Config:
        def __init__(self):
            self.config_value = 100
        
        value = readonly('config_value')
    
    c = Config()
    print(f"读取只读属性: {c.value}")
    
    try:
        c.value = 200
        print("错误: 只读属性被修改了!")
    except AttributeError as e:
        print(f"成功捕获设置只读属性的异常: {e}")


def test_inheritance():
    """测试继承情况下的只读属性"""
    print("\n====== 测试继承情况下的只读属性 ======")
    
    class Base:
        def __init__(self, id_value):
            self._id = id_value
        
        id = readonly('_id')
    
    class Derived(Base):
        def __init__(self, id_value, name):
            super().__init__(id_value)
            self._name = name
        
        name = readonly('_name')
    
    d = Derived(1, "Test")
    print(f"读取继承的只读属性(id): {d.id}")
    print(f"读取派生类的只读属性(name): {d.name}")
    
    try:
        d.id = 2
        print("错误: 只读属性被修改了!")
    except AttributeError as e:
        print(f"成功捕获设置继承的只读属性的异常: {e}")


def main():
    """运行所有测试"""
    test_basic_readonly()
    test_with_slots()
    test_without_underscore()
    test_inheritance()
    print("\n所有测试完成!")


if __name__ == '__main__':
    main()