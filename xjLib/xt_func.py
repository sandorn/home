# !/usr/bin/env python
"""
==============================================================
Description  : 函数工具模块 - 提供动态函数创建、属性检查和分析工具
Develop      : VSCode
Author       :
Date         :
LastEditTime :
FilePath     : /CODE/xjLib/xt_func.py

本模块提供以下核心功能:
- _create_func: 动态创建函数对象，支持自定义代码体、文件名和全局变量
- inspect_function: 检查并打印函数属性，包括函数自身属性和__code__对象属性
- get_dynamic_function_attributes: 动态获取函数对象的所有属性
- get_dynamic_code_attributes: 动态获取代码对象的所有属性
- compare_attributes: 比较硬编码属性和动态获取的属性

主要特性:
- 支持动态函数创建，可指定函数名、代码体和执行环境
- 提供函数属性的静态和动态检查方式
- 支持过滤特殊方法和属性
- 完整的类型注解支持
- 友好的属性展示和格式化输出
==============================================================
"""

from __future__ import annotations

from collections.abc import Callable
from types import CodeType, FunctionType
from typing import Any

from xt_wraps import LogCls

log = LogCls()


def _create_func(code_body: str, func_name: str | None = None, **kwargs) -> Callable[..., Any]:
    """动态函数创建器

    Args:
        code_body: 函数的源代码字符串
        func_name: 函数名称，如果为None则查找第一个函数对象
        **kwargs: 可选参数，包括:
            - filename: 文件名，默认为'xt_tools._create_func'
            - exmethod: 执行模式，默认为'exec'
            - globals: 全局变量字典

    Returns:
        创建的函数对象

    Raises:
        NameError: 指定的函数名不存在
        ValueError: 编译后的代码不包含任何函数定义
        SyntaxError: 代码语法错误
        SecurityWarning: 该函数使用exec执行代码，处理不可信输入时存在安全风险

    安全注意事项:
        1. 该函数使用exec执行代码，只应处理可信的输入
        2. 在生产环境中使用时，应对输入代码进行严格验证
        3. 避免将外部用户输入直接传递给此函数

    示例:
        >>> simple_func = _create_func('def add(a, b=2):\n    return a + b', func_name='add')
        >>> simple_func(3)  # 返回 5
        5
    """
    # 从kwargs中提取关键参数
    filename = kwargs.pop('filename', 'xt_tools._create_func')
    exmethod = kwargs.pop('exmethod', 'exec')
    globals_dict = kwargs.pop('globals', {})

    # 确保globals_dict包含必要的内置函数
    globals_dict.setdefault('__builtins__', __builtins__)

    # 编译代码体
    module_code = compile(code_body, filename, exmethod)

    # 执行编译后的代码
    # ruff: noqa: S102  # 允许使用exec执行用户提供的函数定义代码
    exec(module_code, globals_dict)

    # 查找函数
    if func_name:
        # 如果有指定函数名，直接查找
        if func_name not in globals_dict:
            raise NameError(f"函数 '{func_name}' 未在编译后的代码中找到")
        func = globals_dict[func_name]
    else:
        # 否则查找第一个函数对象
        func = None
        for obj in globals_dict.values():
            if isinstance(obj, FunctionType):
                func = obj
                break

        if func is None:
            raise ValueError('编译后的代码不包含任何函数定义')

    return func


FUNC_ATTRS = ('__closure__', '__code__', '__defaults__', '__dict__', '__doc__', '__globals__', '__name__', '__module__', '__qualname__')

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


def get_dynamic_function_attributes(func: callable, include_special: bool = True) -> list[str]:
    """动态获取函数对象的所有属性

    Args:
        func: 函数对象
        include_special: 是否包含特殊方法（如__repr__、__str__等）

    Returns:
        排序后的函数属性名列表

    Raises:
        TypeError: 输入对象不是可调用对象

    示例:
        >>> def sample_func():
        ...     pass
        >>> attrs = get_dynamic_function_attributes(sample_func, include_special=False)
        >>> log(attrs)  # 输出函数的主要属性列表
    """
    if not callable(func):
        raise TypeError('预期输入为可调用对象')

    # 使用dir()获取所有属性
    all_attrs = dir(func)

    # 过滤出以'__'开头和结尾的特殊属性（魔术方法和属性）
    special_attrs = [attr for attr in all_attrs if attr.startswith('__') and attr.endswith('__')]

    # 如果不包含特殊方法，移除一些常用的特殊方法
    if not include_special:
        common_special_methods = ['__repr__', '__str__', '__hash__', '__eq__', '__ne__', '__lt__', '__le__', '__gt__', '__ge__', '__reduce__', '__reduce_ex__', '__sizeof__', '__subclasshook__']
        for attr in common_special_methods:
            if attr in special_attrs:
                special_attrs.remove(attr)

    # 排序以保持一致性
    special_attrs.sort()

    return special_attrs


def get_dynamic_code_attributes(code_obj: CodeType) -> list[str]:
    """动态获取代码对象的所有属性

    Args:
        code_obj: 代码对象（通过function.__code__获取）

    Returns:
        排序后的代码对象属性名列表

    Raises:
        TypeError: 输入对象不是代码对象

    示例:
        >>> def sample_func():
        ...     pass
        >>> code_attrs = get_dynamic_code_attributes(sample_func.__code__)
        >>> log(code_attrs)  # 输出代码对象的属性列表
    """
    if not isinstance(code_obj, CodeType):
        raise TypeError('预期输入为代码对象')

    # 使用dir()获取所有属性
    all_attrs = dir(code_obj)

    # 过滤出以'co_'开头的属性（代码对象特有的属性）
    code_attrs = [attr for attr in all_attrs if attr.startswith('co_')]

    # 排序以保持一致性
    code_attrs.sort()

    return code_attrs


def compare_attributes(hardcoded_attrs: tuple[str, ...], dynamic_attrs: list[str]) -> dict[str, Any]:
    """比较硬编码属性和动态获取的属性

    Args:
        hardcoded_attrs: 硬编码的属性元组
        dynamic_attrs: 动态获取的属性列表

    Returns:
        包含比较结果的字典，包括:
        - hardcoded_count: 硬编码属性数量
        - dynamic_count: 动态获取属性数量
        - missing_in_dynamic: 硬编码中有但动态获取中没有的属性
        - extra_in_dynamic: 动态获取中有但硬编码中没有的属性
        - common_attrs: 共同拥有的属性

    示例:
        >>> hardcoded = ('__name__', '__code__', '__doc__')
        >>> dynamic = get_dynamic_function_attributes(sample_func)
        >>> result = compare_attributes(hardcoded, dynamic)
        >>> log(f'共同属性: {result["common_attrs"]}')
    """
    hardcoded_set = set(hardcoded_attrs)
    dynamic_set = set(dynamic_attrs)

    return {
        'hardcoded_count': len(hardcoded_set),
        'dynamic_count': len(dynamic_set),
        'missing_in_dynamic': hardcoded_set - dynamic_set,
        'extra_in_dynamic': dynamic_set - hardcoded_set,
        'common_attrs': hardcoded_set & dynamic_set,
    }


def log_attr(attr_name: str, obj: Any, width: int = 15) -> None:
    """打印属性及其值"""
    try:
        # 获取属性值
        value = getattr(obj, attr_name, 'N/A')

        # 特殊处理不同类型的属性
        if attr_name == '__globals__' and isinstance(value, dict):
            # 过滤掉内置的全局变量
            keys = [k for k in value if not k.startswith('__')]
            log(f'{attr_name:{width}}: <全局变量> (键: {keys})')
        elif attr_name == '__closure__' and value is not None:
            # 获取闭包中的值
            cell_values = [c.cell_contents if c else None for c in value]
            log(f'{attr_name:{width}}: {cell_values}')
        elif attr_name == 'co_code' and isinstance(value, bytes):
            # 代码对象的字节码表示
            log(f'{attr_name:{width}}: <字节码 len={len(value)}>')
        else:
            # 其他属性正常打印，限制长度
            log(f'{attr_name:{width}}: {repr(value)[:100]}')
    except Exception as e:
        # 处理可能的异常
        log(f'{attr_name:{width}}: 错误 - {str(e)[:50]}')


def inspect_function(func: Callable, use_dynamic_attrs: bool = False, include_special_methods: bool = False) -> None:
    """检查并打印函数属性，包括函数自身属性和__code__对象属性

    Args:
        func: 要检查的可调用对象
        use_dynamic_attrs: 是否使用动态获取的属性列表，默认为False（使用硬编码属性列表）
        include_special_methods: 使用动态属性时，是否包含特殊方法（如__repr__、__str__等）

    Raises:
        TypeError: 输入对象不是可调用对象

    示例:
        >>> def sample_func(x, y=10):
        ...     return x + y
        >>> inspect_function(sample_func)  # 使用硬编码属性列表
        >>> inspect_function(sample_func, use_dynamic_attrs=True)  # 使用动态属性列表
    """
    if not callable(func):
        raise TypeError('预期输入为可调用对象')

    # 获取函数名称信息
    name = getattr(func, '__qualname__', getattr(func, '__name__', 'unnamed'))
    log(f'\n检查函数: {name}')

    # 选择要使用的属性列表
    attrs = get_dynamic_function_attributes(func, include_special_methods) if use_dynamic_attrs else FUNC_ATTRS

    # 打印函数属性
    log('\n函数属性:')
    for attr in attrs:
        log_attr(attr, func)

    # 打印代码对象属性（如果存在）
    if hasattr(func, '__code__'):
        code_attrs = get_dynamic_code_attributes(func.__code__) if use_dynamic_attrs else CODE_ATTRS
        log('\n代码对象属性:')
        for attr in code_attrs:
            log_attr(attr, func.__code__, width=20)


if __name__ == '__main__':
    """主程序：展示模块功能的使用示例"""
    import sys

    # 测试1: 创建简单函数
    simple_func = _create_func(
        "def simple_func(a, b=2):\n    '''简单函数示例'''\n    return a * b",
        func_name='simple_func',
    )
    log('\n测试1: 简单函数')
    log('结果:', simple_func(3, 4))  # 应该输出 12

    # 测试2: 创建闭包函数
    closure_func = _create_func(
        'def outer(x):\n    def inner(y):\n        return x * y\n    return inner',
        func_name='outer',
    )(5)  # 创建闭包，x=5
    log('\n测试2: 闭包函数')
    log('结果:', closure_func(3))  # 应该输出 15

    # 展示硬编码和动态属性获取的对比
    log('\n=== 对比硬编码属性和动态获取的属性 ===')

    # 获取动态属性
    dynamic_func_attrs = get_dynamic_function_attributes(simple_func, include_special=False)
    dynamic_code_attrs = get_dynamic_code_attributes(simple_func.__code__)

    # 比较函数属性
    func_compare = compare_attributes(FUNC_ATTRS, dynamic_func_attrs)
    log('\n函数属性比较:')
    log(f'- 硬编码属性数量: {func_compare["hardcoded_count"]}')
    log(f'- 动态获取属性数量: {func_compare["dynamic_count"]}')
    log(f'- 硬编码中有但动态获取中没有: {func_compare["missing_in_dynamic"]}')
    log(f'- 动态获取中有但硬编码中没有: {func_compare["extra_in_dynamic"]}')
    log(f'- 共同属性: {func_compare["common_attrs"]}')

    # 比较代码对象属性
    code_compare = compare_attributes(CODE_ATTRS, dynamic_code_attrs)
    log('\n代码对象属性比较:')
    log(f'- 硬编码属性数量: {code_compare["hardcoded_count"]}')
    log(f'- 动态获取属性数量: {code_compare["dynamic_count"]}')
    log(f'- 硬编码中有但动态获取中没有: {code_compare["missing_in_dynamic"]}')
    log(f'- 动态获取中有但硬编码中没有: {code_compare["extra_in_dynamic"]}')
    log(f'- 共同属性: {code_compare["common_attrs"]}')

    log('\n\n=== 使用硬编码属性列表 (默认行为) ===')
    # 测试3: 检查函数属性 - 使用硬编码属性
    log('\n测试3: 检查简单函数 (硬编码属性)')
    inspect_function(simple_func, use_dynamic_attrs=False)

    log('\n\n=== 使用动态属性列表 ===')
    # 测试4: 检查函数属性 - 使用动态属性
    log('\n测试4: 检查简单函数 (动态属性)')
    inspect_function(simple_func, use_dynamic_attrs=True, include_special_methods=False)

    log('\n测试5: 检查闭包函数 (动态属性)')
    inspect_function(closure_func, use_dynamic_attrs=True, include_special_methods=False)

    # 测试6: 使用默认参数创建函数
    dynamic_func = _create_func(
        'def multiply(a=3, b=6):\n    return a * b',
        func_name='multiply',
        filename='dynamic_math_func',
    )
    log('\n测试6: 带默认参数的动态函数')
    inspect_function(dynamic_func, use_dynamic_attrs=True, include_special_methods=False)
    log('结果:', dynamic_func())  # 应该输出 18

    # 打印模块版本和Python环境信息
    log('\n\n=== 环境信息 ===')
    log(f'Python版本: {sys.version}')
    log('模块功能: 函数动态创建、属性检查和分析工具')
    log('主要函数: _create_func, inspect_function, get_dynamic_function_attributes, get_dynamic_code_attributes, compare_attributes')
