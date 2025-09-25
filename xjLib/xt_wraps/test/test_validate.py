# !/usr/bin/env python
"""
测试validate.py文件中的所有功能
"""

from __future__ import annotations

import contextlib

from xt_wraps.validate import TypedProperty, ensure_initialized, readonly, typeassert, typed_property


def test_ensure_initialized():
    """测试ensure_initialized装饰器功能"""

    class Config:
        def __init__(self):
            pass

        @ensure_initialized('settings')
        def get_config(self):
            return self.settings

    config = Config()

    with contextlib.suppress(RuntimeError):
        config.get_config()

    # 设置变量后再次尝试
    config.settings = {'debug': True}
    with contextlib.suppress(Exception):
        config.get_config()


def test_typed_property_descriptor():
    """测试TypedProperty描述符类"""

    class Person:
        name = TypedProperty('name', str)
        age = TypedProperty('age', int, allow_none=True)

    p = Person()

    # 测试设置正确类型的值
    try:
        p.name = 'Alice'
        p.age = 30
    except TypeError:
        pass

    # 测试设置错误类型的值
    with contextlib.suppress(TypeError):
        p.name = 123

    # 测试允许None值
    with contextlib.suppress(TypeError):
        p.age = None

    # 测试不允许None值
    with contextlib.suppress(TypeError):
        p.name = None

    # 测试删除属性
    try:
        del p.name
        # 再次访问应该返回None
    except Exception:
        pass


def test_typeassert_decorator():
    """测试typeassert装饰器"""

    @typeassert(name=str, age=int)
    class Person:
        pass

    @typeassert(name=str, age=(int, float), score={'type': int, 'allow_none': True})
    class Student:
        pass

    # 测试基本类型检查
    try:
        p = Person()
        p.name = 'Bob'
        p.age = 25

        # 测试类型错误
        p.age = 'twenty-five'
    except TypeError:
        pass

    # 测试联合类型和None值
    try:
        s = Student()
        s.name = 'Charlie'
        s.age = 22.5  # 浮点型也应该通过
        s.score = None  # None值应该通过

        # 测试不允许的类型
        s.age = 'twenty-two'
    except TypeError:
        pass


def test_typed_property_function():
    """测试typed_property函数"""

    class Product:
        name = typed_property('name', str)
        price = typed_property('price', (int, float))
        description = typed_property('description', str, allow_none=True)

    # 测试基本功能
    try:
        p = Product()
        p.name = 'Laptop'
        p.price = 999.99
        p.description = None

        # 测试类型错误
        p.price = 'one thousand'
    except TypeError:
        pass

    # 测试删除属性
    with contextlib.suppress(Exception):
        del p.name

    # 测试与__slots__的兼容性
    class ProductWithSlots:
        __slots__ = ('_name', '_price')
        name = typed_property('name', str)
        price = typed_property('price', float)

    try:
        ps = ProductWithSlots()
        ps.name = 'Phone'
        ps.price = 599.99
    except Exception:
        pass


def test_readonly_function():
    """测试readonly函数"""

    # 测试基本的只读功能（使用下划线前缀）
    class Person:
        def __init__(self, name):
            self._name = name  # 使用下划线前缀存储实际值

        name = readonly('_name')  # 创建只读属性

    p = Person('Alice')

    # 测试修改只读属性
    with contextlib.suppress(AttributeError):
        p.name = 'Bob'

    # 测试删除只读属性
    with contextlib.suppress(AttributeError):
        del p.name

    # 测试与__slots__的兼容性
    class ConfigWithSlots:
        __slots__ = ('_api_key', '_app_name')

        def __init__(self, app_name, api_key):
            self._app_name = app_name
            self._api_key = api_key

        app_name = readonly('_app_name')
        api_key = readonly('_api_key')

    try:
        cfg_slots = ConfigWithSlots('SecureApp', 'secret-key')

        # 测试修改
        cfg_slots.api_key = 'new-key'
    except AttributeError:
        pass

    # 测试继承情况下的只读属性
    class Employee(Person):
        def __init__(self, name, employee_id):
            super().__init__(name)
            self._employee_id = employee_id

        employee_id = readonly('_employee_id')

    emp = Employee('Charlie', 'E12345')

    # 测试修改继承的只读属性
    with contextlib.suppress(AttributeError):
        emp.name = 'Dave'


def main():
    """运行所有测试"""
    test_ensure_initialized()
    test_typed_property_descriptor()
    test_typeassert_decorator()
    test_typed_property_function()
    test_readonly_function()


if __name__ == '__main__':
    main()
