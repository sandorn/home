# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-09-16 10:00:28
LastEditTime : 2024-09-16 10:01:17
FilePath     : /CODE/xjLib/xt_func.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from types import FunctionType
from typing import Any, Callable


def _create_func(code_body, **kwargs) -> Callable[..., Any]:
    """动态函数创建器"""
    kwargs.setdefault("globals", {})
    filename = kwargs.pop("filename", "xt_tools._create_func")
    exmethod = kwargs.pop("exmethod", "exec")
    module_code = compile(code_body, filename, exmethod)
    return FunctionType(module_code.co_consts[0], **kwargs)

    # FunctionType(code, globals, name=None, argdefs=None, closure=None)
    # FunctionType(wrapper.__code__, wrapper.__globals__, name=func.__name__, argdefs=wrapper.__defaults__, closure=wrapper.__closure__)


func_attr_name_list = [
    # """函数的内置属性"""
    "__closure__",
    "__code__",
    "__defaults__",
    "__dict__",
    "__doc__",
    "__globals__",
    "__name__",
]
func_code_name_list = [
    # 函数.__code__的内置属性
    "co_argcount",
    "co_cellvars",
    "co_code",
    "co_consts",
    "co_filename",
    "co_firstlineno",
    "co_flags",
    "co_freevars",
    "co_kwonlyargcount",
    "co_lnotab",
    "co_name",
    "co_names",
    "co_nlocals",
    "co_posonlyargcount",
    "co_stacksize",
    "co_varnames",
]


if __name__ == "__main__":

    def make_func() -> None:
        # #函数创建器
        foo_func = _create_func("def foo(*args):a=3;b=6;return a*b")
        print(foo_func())
        for attr in func_attr_name_list:
            ...
            # print(attr, ":", getattr(foo_func, attr))

        for attr in func_code_name_list:
            ...
            # print(f"foo_func.__code__.{attr.ljust(33)}", ":", getattr(foo_func.__code__, attr))
        print(foo_func.__globals__, foo_func.__name__)

    make_func()
