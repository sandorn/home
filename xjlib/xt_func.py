# !/usr/bin/env python3
"""
函数工具模块 - 动态函数创建与属性分析工具

核心功能:
- 动态创建函数对象
- 函数属性检查与分析
- 代码对象属性获取
- 属性比较工具

主要特性:
- 安全的动态函数创建
- 完整的类型注解
- 友好的错误处理
- 灵活的属性检查
"""

from __future__ import annotations

from collections.abc import Callable
from types import CodeType, FunctionType
from typing import Any

from xtlog import mylog as log


def _create_func(code_body: str, func_name: str | None = None, **kwargs) -> Callable[..., Any]:
    """动态创建函数对象

    通过字符串代码动态创建函数，支持自定义执行环境和全局变量。

    Args:
        code_body: 函数源代码字符串
        func_name: 目标函数名，None时自动查找第一个函数
        **kwargs: 额外参数
            - filename: 文件名标识，默认'xt_func._create_func'
            - exmethod: 执行模式，默认'exec'
            - globals: 全局变量字典

    Returns:
        创建的函数对象

    Raises:
        NameError: 指定函数名不存在
        ValueError: 代码中无函数定义
        SyntaxError: 代码语法错误

    Warning:
        使用exec执行代码，仅处理可信输入！

    Example:
        >>> func = _create_func('def add(a, b=2): return a + b', 'add')
        >>> func(3)  # 5
    """
    # 提取参数
    filename = kwargs.pop('filename', 'xt_func._create_func')
    exmethod = kwargs.pop('exmethod', 'exec')
    globals_dict = kwargs.pop('globals', {})

    # 设置全局环境
    globals_dict.setdefault('__builtins__', __builtins__)

    try:
        # 编译并执行代码
        module_code = compile(code_body, filename, exmethod)
        exec(module_code, globals_dict)  # noqa: S102
    except SyntaxError as e:
        raise SyntaxError(f'代码语法错误: {e}') from e

    # 查找目标函数
    if func_name:
        if func_name not in globals_dict:
            raise NameError(f"函数 '{func_name}' 未找到")
        return globals_dict[func_name]

    # 自动查找第一个函数
    for obj in globals_dict.values():
        if isinstance(obj, FunctionType):
            return obj

    raise ValueError('代码中未找到任何函数定义')


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


def get_dynamic_function_attributes(func: Callable[..., Any], include_special: bool = True) -> list[str]:
    """获取函数对象的所有属性名

    Args:
        func: 目标函数对象
        include_special: 是否包含特殊方法（__repr__等）

    Returns:
        排序后的属性名列表

    Raises:
        TypeError: 输入不是可调用对象

    Example:
        >>> attrs = get_dynamic_function_attributes(sample_func, False)
        >>> print(attrs)  # ['__code__', '__name__', ...]
    """
    if not callable(func):
        raise TypeError('输入必须是可调用对象')

    # 获取所有属性并过滤
    all_attrs = dir(func)
    special_attrs = [attr for attr in all_attrs if attr.startswith('__') and attr.endswith('__')]

    # 过滤常用特殊方法
    if not include_special:
        common_methods = {'__repr__', '__str__', '__hash__', '__eq__', '__ne__', '__lt__', '__le__', '__gt__', '__ge__', '__reduce__', '__reduce_ex__', '__sizeof__', '__subclasshook__'}
        special_attrs = [attr for attr in special_attrs if attr not in common_methods]

    return sorted(special_attrs)


def get_dynamic_code_attributes(code_obj: CodeType) -> list[str]:
    """获取代码对象的所有属性名

    Args:
        code_obj: 代码对象（通过function.__code__获取）

    Returns:
        排序后的属性名列表

    Raises:
        TypeError: 输入不是代码对象

    Example:
        >>> attrs = get_dynamic_code_attributes(func.__code__)
        >>> print(attrs)  # ['co_argcount', 'co_code', ...]
    """
    if not isinstance(code_obj, CodeType):
        raise TypeError('输入必须是代码对象')

    # 获取并过滤代码对象属性
    all_attrs = dir(code_obj)
    code_attrs = [attr for attr in all_attrs if attr.startswith('co_')]

    return sorted(code_attrs)


def compare_attributes(hardcoded_attrs: tuple[str, ...], dynamic_attrs: list[str]) -> dict[str, Any]:
    """比较硬编码和动态获取的属性

    Args:
        hardcoded_attrs: 硬编码属性元组
        dynamic_attrs: 动态获取属性列表

    Returns:
        比较结果字典:
        - hardcoded_count: 硬编码属性数量
        - dynamic_count: 动态属性数量
        - missing_in_dynamic: 硬编码有但动态没有
        - extra_in_dynamic: 动态有但硬编码没有
        - common_attrs: 共同属性

    Example:
        >>> result = compare_attributes(('__name__',), ['__name__', '__code__'])
        >>> print(result['common_attrs'])  # {'__name__'}
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
    """格式化打印对象属性

    Args:
        attr_name: 属性名
        obj: 目标对象
        width: 属性名显示宽度
    """
    try:
        value = getattr(obj, attr_name, 'N/A')

        # 特殊属性处理
        if attr_name == '__globals__' and isinstance(value, dict):
            keys = [k for k in value if not k.startswith('__')]
            print(f'{attr_name:{width}}: <全局变量> (键: {keys})')
        elif attr_name == '__closure__' and value is not None:
            cell_values = [getattr(c, 'cell_contents', None) if c else None for c in value]
            print(f'{attr_name:{width}}: {cell_values}')
        elif attr_name == 'co_code' and isinstance(value, bytes):
            print(f'{attr_name:{width}}: <字节码 len={len(value)}>')
        else:
            # 限制显示长度
            print(f'{attr_name:{width}}: {repr(value)[:100]}')
    except Exception as e:
        print(f'{attr_name:{width}}: 错误 - {str(e)[:50]}')


def inspect_function(func: Callable[..., Any], use_dynamic_attrs: bool = False, include_special_methods: bool = False) -> None:
    """检查并打印函数属性

    Args:
        func: 目标函数对象
        use_dynamic_attrs: 是否使用动态属性列表
        include_special_methods: 是否包含特殊方法

    Raises:
        TypeError: 输入不是可调用对象

    Example:
        >>> inspect_function(sample_func)
        >>> inspect_function(sample_func, use_dynamic_attrs=True)
    """
    if not callable(func):
        raise TypeError('输入必须是可调用对象')

    # 获取函数名
    name = getattr(func, '__qualname__', getattr(func, '__name__', 'unnamed'))
    log(f'检查函数: {name}')

    # 选择属性列表
    attrs = get_dynamic_function_attributes(func, include_special_methods) if use_dynamic_attrs else FUNC_ATTRS

    # 打印函数属性
    print('函数属性:')
    for attr in attrs:
        print(f'{attr:20}: {getattr(func, attr, "N/A")}')

    # 打印代码对象属性
    if hasattr(func, '__code__'):
        code_attrs = get_dynamic_code_attributes(func.__code__) if use_dynamic_attrs else CODE_ATTRS
        print('代码对象属性:')
        for attr in code_attrs:
            print(f'{attr:20}: {getattr(func.__code__, attr, "N/A")}')


def create_simple_func(name: str, code: str, **kwargs) -> Callable[..., Any]:
    """快速创建简单函数的便捷方法

    Args:
        name: 函数名
        code: 函数体代码（不包含def语句）
        **kwargs: 传递给_create_func的额外参数

    Returns:
        创建的函数对象

    Example:
        >>> func = create_simple_func('add', 'return a + b')
        >>> func(1, 2)  # 3
    """
    full_code = f'def {name}({kwargs.pop("params", "a, b")}):    {code}'
    return _create_func(full_code, name, **kwargs)


def get_function_info(func: Callable[..., Any]) -> dict[str, Any]:
    """获取函数的详细信息

    Args:
        func: 目标函数

    Returns:
        包含函数信息的字典
    """
    if not callable(func):
        raise TypeError('输入必须是可调用对象')

    info = {
        'name': getattr(func, '__name__', 'unnamed'),
        'qualname': getattr(func, '__qualname__', 'unnamed'),
        'module': getattr(func, '__module__', None),
        'doc': getattr(func, '__doc__', None),
        'annotations': getattr(func, '__annotations__', {}),
        'defaults': getattr(func, '__defaults__', None),
        'kwdefaults': getattr(func, '__kwdefaults__', None),
    }

    if hasattr(func, '__code__'):
        code = func.__code__
        info.update({
            'argcount': code.co_argcount,
            'posonlyargcount': code.co_posonlyargcount,
            'kwonlyargcount': code.co_kwonlyargcount,
            'nlocals': code.co_nlocals,
            'stacksize': code.co_stacksize,
            'filename': code.co_filename,
            'firstlineno': code.co_firstlineno,
            'varnames': code.co_varnames,
            'names': code.co_names,
        })

    return info


if __name__ == '__main__':
    """演示模块功能"""
    import sys

    log('=== xt_func 模块演示 ===')

    # 1. 创建简单函数
    log('1. 创建简单函数')
    add_func = create_simple_func('add', 'return a + b')
    log(f'add_func(3, 4) = {add_func(3, 4)}')

    # 2. 创建复杂函数
    log('2. 创建复杂函数')
    complex_func = _create_func(
        """
def complex_func(x, y=10, *args, **kwargs):
    '''复杂函数示例'''
    result = x * y
    if args:
        result += sum(args)
    if kwargs:
        result += len(kwargs)
    return result
""",
        'complex_func',
    )

    log(f'complex_func(2, 3, 1, 2, extra=1) = {complex_func(2, 3, 1, 2, extra=1)}')

    # 3. 获取函数信息
    log('3. 函数信息')
    info = get_function_info(complex_func)
    log(f'函数名: {info["name"]}')
    log(f'参数数量: {info["argcount"]}')
    log(f'局部变量: {info["nlocals"]}')

    # 4. 属性比较
    log('4. 属性比较')
    dynamic_attrs = get_dynamic_function_attributes(add_func, False)
    comparison = compare_attributes(FUNC_ATTRS, dynamic_attrs)
    log(f'共同属性数量: {len(comparison["common_attrs"])}')

    # 5. 函数检查
    log('5. 函数属性检查')
    inspect_function(add_func, use_dynamic_attrs=True, include_special_methods=False)

    log('=== 环境信息 ===')
    log(f'Python版本: {sys.version.split()[0]}')
    log('模块功能: 动态函数创建与属性分析')
