# !/usr/bin/env python
"""
测试validate.py文件中的所有功能
"""

from __future__ import annotations

from xt_wraps.validate import TypedProperty, ensure_initialized, readonly, typeassert, typed_property


def test_ensure_initialized():
    """测试ensure_initialized装饰器功能"""
    print('\n====== 测试ensure_initialized装饰器 ======')

    class Config:
        def __init__(self):
            pass

        @ensure_initialized('settings')
        def get_config(self):
            return self.settings

    config = Config()

    try:
        config.get_config()
        print('错误: 未初始化的变量被访问了!')
    except RuntimeError as e:
        print(f'成功捕获未初始化变量的异常: {e}')

    # 设置变量后再次尝试
    config.settings = {'debug': True}
    try:
        result = config.get_config()
        print(f'成功访问初始化的变量: {result}')
    except Exception as e:
        print(f'错误: {e}')


def test_typed_property_descriptor():
    """测试TypedProperty描述符类"""
    print('\n====== 测试TypedProperty描述符类 ======')

    class Person:
        name = TypedProperty('name', str)
        age = TypedProperty('age', int, allow_none=True)

    p = Person()

    # 测试设置正确类型的值
    try:
        p.name = 'Alice'
        p.age = 30
        print(f'设置正确类型: name={p.name}, age={p.age}')
    except TypeError as e:
        print(f'错误: {e}')

    # 测试设置错误类型的值
    try:
        p.name = 123
        print('错误: 类型检查失败!')
    except TypeError as e:
        print(f'成功捕获类型错误: {e}')

    # 测试允许None值
    try:
        p.age = None
        print(f'设置None值成功: age={p.age}')
    except TypeError as e:
        print(f'错误: {e}')

    # 测试不允许None值
    try:
        p.name = None
        print('错误: None值检查失败!')
    except TypeError as e:
        print(f'成功捕获None值错误: {e}')

    # 测试删除属性
    try:
        del p.name
        print('删除属性成功')
        # 再次访问应该返回None
        print(f'删除后访问: name={p.name}')
    except Exception as e:
        print(f'错误: {e}')


def test_typeassert_decorator():
    """测试typeassert装饰器"""
    print('\n====== 测试typeassert装饰器 ======')

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
        print(f'Person类型检查通过: name={p.name}, age={p.age}')

        # 测试类型错误
        p.age = 'twenty-five'
        print('错误: 类型检查失败!')
    except TypeError as e:
        print(f'成功捕获Person类型错误: {e}')

    # 测试联合类型和None值
    try:
        s = Student()
        s.name = 'Charlie'
        s.age = 22.5  # 浮点型也应该通过
        s.score = None  # None值应该通过
        print(f'Student类型检查通过: name={s.name}, age={s.age}, score={s.score}')

        # 测试不允许的类型
        s.age = 'twenty-two'
        print('错误: 联合类型检查失败!')
    except TypeError as e:
        print(f'成功捕获Student类型错误: {e}')


def test_typed_property_function():
    """测试typed_property函数"""
    print('\n====== 测试typed_property函数 ======')

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
        print(f'Product属性设置成功: name={p.name}, price={p.price}, description={p.description}')

        # 测试类型错误
        p.price = 'one thousand'
        print('错误: typed_property类型检查失败!')
    except TypeError as e:
        print(f'成功捕获typed_property类型错误: {e}')

    # 测试删除属性
    try:
        del p.name
        print(f'删除属性后访问: name={p.name}')  # 应该返回None
    except Exception as e:
        print(f'错误: {e}')

    # 测试与__slots__的兼容性
    class ProductWithSlots:
        __slots__ = ('_name', '_price')
        name = typed_property('name', str)
        price = typed_property('price', float)

    try:
        ps = ProductWithSlots()
        ps.name = 'Phone'
        ps.price = 599.99
        print(f'与__slots__兼容: name={ps.name}, price={ps.price}')
    except Exception as e:
        print(f'错误: {e}')


def test_readonly_function():
    """测试readonly函数"""
    print('\n====== 测试readonly函数 ======')

    # 测试基本的只读功能（使用下划线前缀）
    class Person:
        def __init__(self, name):
            self._name = name  # 使用下划线前缀存储实际值

        name = readonly('_name')  # 创建只读属性

    p = Person('Alice')
    print(f'读取只读属性: name={p.name}')

    # 测试修改只读属性
    try:
        p.name = 'Bob'
        print('错误: 只读属性被修改了!')
    except AttributeError as e:
        print(f'成功捕获修改只读属性的异常: {e}')

    # 测试删除只读属性
    try:
        del p.name
        print('错误: 只读属性被删除了!')
    except AttributeError as e:
        print(f'成功捕获删除只读属性的异常: {e}')

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
        print(f'与__slots__兼容: app_name={cfg_slots.app_name}, api_key={cfg_slots.api_key}')

        # 测试修改
        cfg_slots.api_key = 'new-key'
        print('错误: 只读属性被修改了!')
    except AttributeError as e:
        print(f'成功捕获修改只读属性的异常: {e}')

    # 测试继承情况下的只读属性
    class Employee(Person):
        def __init__(self, name, employee_id):
            super().__init__(name)
            self._employee_id = employee_id

        employee_id = readonly('_employee_id')

    emp = Employee('Charlie', 'E12345')
    print(f'继承情况下的只读属性: name={emp.name}, employee_id={emp.employee_id}')

    # 测试修改继承的只读属性
    try:
        emp.name = 'Dave'
        print('错误: 继承的只读属性被修改了!')
    except AttributeError as e:
        print(f'成功捕获修改继承只读属性的异常: {e}')


def main():
    """运行所有测试"""
    test_ensure_initialized()
    test_typed_property_descriptor()
    test_typeassert_decorator()
    test_typed_property_function()
    test_readonly_function()
    print('\n所有测试完成!')


if __name__ == '__main__':
    main()
