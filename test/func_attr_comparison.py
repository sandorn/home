#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
函数和代码对象属性比较工具
展示硬编码属性和动态获取属性的区别
"""
import sys
from types import FunctionType, CodeType
from typing import List, Dict, Set, Any

# 硬编码的属性列表（来自xt_func.py）
FUNC_ATTRS = (
    '__closure__',
    '__code__',
    '__defaults__',
    '__dict__',
    '__doc__',
    '__globals__',
    '__name__',
    '__module__',
    '__qualname__',
)

CODE_ATTRS = (
    'co_argcount',
    'co_cellvars',
    'co_code',
    'co_consts',
    'co_filename',
    'co_firstlineno',
    'co_flags',
    'co_freevars',
    'co_kwonlyargcount',
    'co_lines',
    'co_name',
    'co_names',
    'co_nlocals',
    'co_posonlyargcount',
    'co_stacksize',
    'co_varnames',
)

def get_dynamic_function_attributes(func: callable, include_special: bool = True) -> List[str]:
    """动态获取函数对象的属性"""
    if not callable(func):
        raise TypeError('Expected a callable object')
    
    # 使用dir()获取所有属性
    all_attrs = dir(func)
    
    # 过滤出以'__'开头和结尾的特殊属性（魔术方法和属性）
    special_attrs = [
        attr for attr in all_attrs
        if attr.startswith('__') and attr.endswith('__')
    ]
    
    # 如果不包含特殊方法，移除一些常用的特殊方法
    if not include_special:
        common_special_methods = [
            '__repr__', '__str__', '__hash__', '__eq__', '__ne__', 
            '__lt__', '__le__', '__gt__', '__ge__', '__reduce__', 
            '__reduce_ex__', '__sizeof__', '__subclasshook__'
        ]
        for attr in common_special_methods:
            if attr in special_attrs:
                special_attrs.remove(attr)
    
    # 排序以保持一致性
    special_attrs.sort()
    
    return special_attrs

def get_dynamic_code_attributes(code_obj: CodeType) -> List[str]:
    """动态获取代码对象的属性"""
    if not isinstance(code_obj, CodeType):
        raise TypeError('Expected a code object')
    
    # 使用dir()获取所有属性
    all_attrs = dir(code_obj)
    
    # 过滤出以'co_'开头的属性（代码对象特有的属性）
    code_attrs = [attr for attr in all_attrs if attr.startswith('co_')]
    
    # 排序以保持一致性
    code_attrs.sort()
    
    return code_attrs

def compare_attributes(hardcoded_attrs: tuple, dynamic_attrs: List[str]) -> Dict[str, Any]:
    """比较硬编码属性和动态获取的属性"""
    hardcoded_set = set(hardcoded_attrs)
    dynamic_set = set(dynamic_attrs)
    
    return {
        'hardcoded_count': len(hardcoded_set),
        'dynamic_count': len(dynamic_set),
        'missing_in_dynamic': hardcoded_set - dynamic_set,
        'extra_in_dynamic': dynamic_set - hardcoded_set,
        'common_attrs': hardcoded_set & dynamic_set
    }

def print_comparison_results(comparison: Dict[str, Any], title: str) -> None:
    """打印比较结果"""
    print(f"\n{title}:")
    print(f"- 硬编码属性数量: {comparison['hardcoded_count']}")
    print(f"- 动态获取属性数量: {comparison['dynamic_count']}")
    print(f"- 共同属性数量: {len(comparison['common_attrs'])}")
    
    if comparison['missing_in_dynamic']:
        print(f"- 硬编码中有但动态获取中没有: {comparison['missing_in_dynamic']}")
    else:
        print("- 硬编码中所有属性都在动态获取中存在")
    
    if comparison['extra_in_dynamic']:
        print(f"- 动态获取中有但硬编码中没有: {comparison['extra_in_dynamic']}")
    else:
        print("- 动态获取中没有额外的属性")

def inspect_and_print_attr_differences(func: callable, func_name: str) -> None:
    """检查并打印函数属性的差异"""
    print(f"\n\n=== 检查函数: {func_name} ===")
    
    # 获取动态属性
    dynamic_func_attrs = get_dynamic_function_attributes(func, include_special=False)
    
    # 比较函数属性
    func_compare = compare_attributes(FUNC_ATTRS, dynamic_func_attrs)
    print_comparison_results(func_compare, "函数属性比较")
    
    # 如果函数有__code__属性，比较代码对象属性
    if hasattr(func, '__code__'):
        dynamic_code_attrs = get_dynamic_code_attributes(func.__code__)
        code_compare = compare_attributes(CODE_ATTRS, dynamic_code_attrs)
        print_comparison_results(code_compare, "代码对象属性比较")

# 测试函数
def simple_function(x, y):
    """一个简单的测试函数"""
    return x + y

# 带装饰器的函数
def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorator
def decorated_function(x):
    """带装饰器的测试函数"""
    return x * 2

# 生成器函数
def generator_function():
    """测试生成器函数"""
    for i in range(3):
        yield i

# 闭包函数
def outer_function():
    """外层函数，用于创建闭包"""
    x = 42
    def inner_function(y):
        """闭包函数"""
        return x + y
    return inner_function

# 类方法示例
class TestClass:
    """测试类"""
    class_var = 10
    
    def instance_method(self, x):
        """实例方法"""
        return self.class_var + x
    
    @classmethod
    def class_method(cls, x):
        """类方法"""
        return cls.class_var + x
    
    @staticmethod
    def static_method(x):
        """静态方法"""
        return TestClass.class_var + x

if __name__ == '__main__':
    print("函数和代码对象属性比较工具")
    print("=======================")
    print(f"Python版本: {sys.version}")
    
    # 测试各种类型的函数
    inspect_and_print_attr_differences(simple_function, "simple_function")
    inspect_and_print_attr_differences(decorated_function, "decorated_function")
    inspect_and_print_attr_differences(generator_function, "generator_function")
    inspect_and_print_attr_differences(outer_function(), "closure_function")
    
    # 测试类方法
    test_instance = TestClass()
    inspect_and_print_attr_differences(test_instance.instance_method, "instance_method")
    inspect_and_print_attr_differences(TestClass.class_method, "class_method")
    inspect_and_print_attr_differences(TestClass.static_method, "static_method")
    
    print("\n\n=== 结论 ===")
    print("1. 硬编码属性列表(FUNC_ATTRS和CODE_ATTRS)包含了Python函数和代码对象的核心属性，但并不完整")
    print("2. 可以通过编程方式(使用dir()函数)动态获取函数和代码对象的所有属性")
    print("3. 动态获取的属性比硬编码的更多，特别是包含了额外的魔术方法和内部属性")
    print("4. 不同类型的函数(普通函数、装饰器函数、生成器、闭包、类方法等)的属性会有所不同")
    print("5. 在实际应用中，可以结合使用硬编码和动态获取的方式，根据需要选择合适的属性集合")