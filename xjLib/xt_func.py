from __future__ import annotations

from collections.abc import Callable
from types import FunctionType
from typing import Any


def _create_func(code_body: str, func_name: str = None, **kwargs) -> Callable[..., Any]:
    """动态函数创建器"""
    # 从kwargs中提取关键参数
    filename = kwargs.pop('filename', 'xt_tools._create_func')
    exmethod = kwargs.pop('exmethod', 'exec')
    globals_dict = kwargs.pop('globals', {})

    # 确保globals_dict包含必要的内置函数
    globals_dict.setdefault('__builtins__', __builtins__)

    # 编译代码体Pipfreeze>requirements.txt
    module_code = compile(code_body, filename, exmethod)

    # 执行编译后的代码
    exec(module_code, globals_dict)

    # 查找函数
    if func_name:
        # 如果有指定函数名，直接查找
        if func_name not in globals_dict:
            raise NameError(f"Function '{func_name}' not found in compiled code")
        func = globals_dict[func_name]
    else:
        # 否则查找第一个函数对象
        func = None
        for obj in globals_dict.values():
            if isinstance(obj, FunctionType):
                func = obj
                break

        if func is None:
            raise ValueError('Compiled code contains no function definitions')

    return func


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


def inspect_function(func: Callable) -> None:
    """检查并打印函数属性，包括函数自身属性和__code__对象属性"""
    if not callable(func):
        raise TypeError('Expected a callable object')

    # 获取函数名称信息
    name = getattr(func, '__name__', 'unnamed')
    qualname = getattr(func, '__qualname__', name)
    print(f'\nInspecting function: {qualname}')

    # 辅助函数：打印属性值
    def print_attr(attr_name: str, value: Any, width: int = 15) -> None:
        try:
            # 特殊处理不同类型的属性
            if attr_name == '__globals__':
                keys = [k for k in value.keys() if not k.startswith('__')]
                print(f'{attr_name:{width}}: <globals dict> (Keys: {keys})')
            elif attr_name == '__closure__':
                if value:
                    cell_values = [c.cell_contents if c else None for c in value]
                    print(f'{attr_name:{width}}: {cell_values}')
                else:
                    print(f'{attr_name:{width}}: None')
            elif attr_name == 'co_code' and isinstance(value, bytes):
                print(f'{attr_name:{width}}: <bytes len={len(value)}>')
            else:
                print(f'{attr_name:{width}}: {repr(value)[:100]}')
        except Exception as e:
            print(f'{attr_name:{width}}: Error - {str(e)[:50]}')

    # 打印函数属性
    print('\nFunction attributes:')
    for attr in FUNC_ATTRS:
        print_attr(attr, getattr(func, attr, 'N/A'))

    # 打印代码对象属性（如果存在）
    if hasattr(func, '__code__'):
        print('\nCode attributes:')
        for attr in CODE_ATTRS:
            print_attr(attr, getattr(func.__code__, attr, 'N/A'), width=20)


if __name__ == '__main__':
    # 测试1: 创建简单函数
    simple_func = _create_func(
        "def simple_func(a, b=2):\n    '''Simple function'''\n    return a * b",
        func_name='simple_func',
    )
    print('\nTest 1: Simple function')
    print('Result:', simple_func(3, 4))  # 应该输出 12

    # 测试2: 创建闭包函数
    closure_func = _create_func(
        'def outer(x):\n    def inner(y):\n        return x * y\n    return inner',
        func_name='outer',
    )(5)  # 创建闭包，x=5
    print('\nTest 2: Closure function')
    print('Result:', closure_func(3))  # 应该输出 15

    # 测试3: 检查函数属性
    print('\nTest 3: Inspect simple function')
    inspect_function(simple_func)

    print('\nTest 4: Inspect closure function')
    inspect_function(closure_func)

    # 测试4: 使用默认参数创建函数
    dynamic_func = _create_func(
        'def multiply(a=3, b=6):\n    return a * b',
        func_name='multiply',
        filename='dynamic_math_func',
    )
    print('\nTest 5: Dynamic function with defaults')
    inspect_function(dynamic_func)
    print('Result:', dynamic_func())  # 应该输出 18
