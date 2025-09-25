#!/usr/bin/env python3
"""动态获取函数和代码对象属性演示脚本

此脚本展示如何通过编程方式动态获取函数对象和代码对象的属性，
而不是像xt_func.py中那样硬编码定义属性列表。
"""

from __future__ import annotations

from types import CodeType
from typing import Any


def get_function_attributes(func: callable) -> list[str]:
    """动态获取函数对象的主要属性

    Args:
        func: 函数对象

    Returns:
        函数属性名列表
    """
    if not callable(func):
        raise TypeError('Expected a callable object')

    # 使用dir()获取所有属性
    all_attrs = dir(func)

    # 过滤出以'__'开头和结尾的特殊属性（魔术方法和属性）
    # 同时排除一些不常用或无意义的属性
    special_attrs = [attr for attr in all_attrs if attr.startswith('__') and attr.endswith('__') and attr not in ('__class__', '__hash__', '__ne__', '__eq__', '__reduce__', '__reduce_ex__')]

    # 添加一些常用的非特殊属性（如果存在）
    common_attrs = []
    for attr in ['__code__', '__closure__', '__defaults__', '__dict__', '__doc__', '__globals__', '__name__', '__module__', '__qualname__']:
        if hasattr(func, attr) and attr not in special_attrs:
            special_attrs.append(attr)

    # 排序以保持一致性
    special_attrs.sort()

    return special_attrs


def get_code_attributes(code_obj: CodeType) -> list[str]:
    """动态获取代码对象的主要属性

    Args:
        code_obj: 代码对象（function.__code__）

    Returns:
        代码对象属性名列表
    """
    if not isinstance(code_obj, CodeType):
        raise TypeError('Expected a code object')

    # 使用dir()获取所有属性
    all_attrs = dir(code_obj)

    # 过滤出以'co_'开头的属性（代码对象特有的属性）
    code_attrs = [attr for attr in all_attrs if attr.startswith('co_')]

    # 排序以保持一致性
    code_attrs.sort()

    return code_attrs


def dynamic_inspect_function(func: callable) -> None:
    """使用动态获取的属性检查函数

    Args:
        func: 要检查的函数
    """
    if not callable(func):
        raise TypeError('Expected a callable object')

    # 获取函数名称信息
    name = getattr(func, '__name__', 'unnamed')
    qualname = getattr(func, '__qualname__', name)
    print(f'\n动态检查函数: {qualname}')

    # 辅助函数：打印属性值
    def print_attr(attr_name: str, value: Any, width: int = 15) -> None:
        try:
            # 特殊处理不同类型的属性
            if attr_name == '__globals__' and hasattr(value, 'keys'):
                keys = [k for k in value.keys() if not k.startswith('__')]
                print(f'{attr_name:{width}}: <globals dict> (Keys: {keys})')
            elif attr_name == '__closure__' and value is not None:
                cell_values = [c.cell_contents if c else None for c in value]
                print(f'{attr_name:{width}}: {cell_values}')
            elif attr_name == 'co_code' and isinstance(value, bytes):
                print(f'{attr_name:{width}}: <bytes len={len(value)}>')
            else:
                print(f'{attr_name:{width}}: {repr(value)[:100]}')
        except Exception as e:
            print(f'{attr_name:{width}}: Error - {str(e)[:50]}')

    # 动态获取并打印函数属性
    print('\n动态获取的函数属性:')
    func_attrs = get_function_attributes(func)
    for attr in func_attrs:
        print_attr(attr, getattr(func, attr, 'N/A'))

    # 动态获取并打印代码对象属性（如果存在）
    if hasattr(func, '__code__'):
        print('\n动态获取的代码对象属性:')
        code_attrs = get_code_attributes(func.__code__)
        for attr in code_attrs:
            print_attr(attr, getattr(func.__code__, attr, 'N/A'), width=20)


def compare_with_hardcoded(func: callable, hardcoded_func_attrs: tuple, hardcoded_code_attrs: tuple) -> None:
    """比较动态获取的属性和硬编码的属性列表

    Args:
        func: 函数对象
        hardcoded_func_attrs: 硬编码的函数属性列表
        hardcoded_code_attrs: 硬编码的代码对象属性列表
    """
    print('\n\n===== 动态属性与硬编码属性比较 =====')

    # 获取动态属性
    dynamic_func_attrs = set(get_function_attributes(func))
    hardcoded_func_set = set(hardcoded_func_attrs)

    # 函数属性比较
    print('\n函数属性比较:')
    print(f'硬编码属性数量: {len(hardcoded_func_set)}')
    print(f'动态获取属性数量: {len(dynamic_func_attrs)}')

    # 找出硬编码但动态获取中没有的属性
    missing_in_dynamic = hardcoded_func_set - dynamic_func_attrs
    if missing_in_dynamic:
        print(f'硬编码中有但动态获取中没有的属性: {missing_in_dynamic}')

    # 找出动态获取中有但硬编码中没有的属性
    extra_in_dynamic = dynamic_func_attrs - hardcoded_func_set
    if extra_in_dynamic:
        print(f'动态获取中有但硬编码中没有的属性: {extra_in_dynamic}')

    # 代码对象属性比较
    if hasattr(func, '__code__'):
        dynamic_code_attrs = set(get_code_attributes(func.__code__))
        hardcoded_code_set = set(hardcoded_code_attrs)

        print('\n代码对象属性比较:')
        print(f'硬编码属性数量: {len(hardcoded_code_set)}')
        print(f'动态获取属性数量: {len(dynamic_code_attrs)}')

        # 找出硬编码但动态获取中没有的属性
        missing_in_dynamic_code = hardcoded_code_set - dynamic_code_attrs
        if missing_in_dynamic_code:
            print(f'硬编码中有但动态获取中没有的代码属性: {missing_in_dynamic_code}')

        # 找出动态获取中有但硬编码中没有的属性
        extra_in_dynamic_code = dynamic_code_attrs - hardcoded_code_set
        if extra_in_dynamic_code:
            print(f'动态获取中有但硬编码中没有的代码属性: {extra_in_dynamic_code}')


def main():
    """主函数"""

    # 定义一个测试函数
    def test_function(a, b=10, *args, **kwargs):
        """测试函数"""
        c = 5

        def inner_function(x):
            return x + c

        return inner_function(a + b)

    # 从xt_func.py中复制的硬编码属性列表
    xt_func_attrs = ('__closure__', '__code__', '__defaults__', '__dict__', '__doc__', '__globals__', '__name__', '__module__', '__qualname__')

    xt_code_attrs = (
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

    print('===== 函数属性动态获取演示 =====')

    # 使用动态方法检查函数
    dynamic_inspect_function(test_function)

    # 比较动态获取的属性和硬编码的属性
    compare_with_hardcoded(test_function, xt_func_attrs, xt_code_attrs)

    # 创建一个闭包函数进行测试
    def outer(x):
        def inner(y):
            return x * y

        return inner

    closure_func = outer(5)
    print('\n\n===== 闭包函数属性动态获取演示 =====')
    dynamic_inspect_function(closure_func)


if __name__ == '__main__':
    main()
