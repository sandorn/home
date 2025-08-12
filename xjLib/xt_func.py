from types import FunctionType
from typing import Any, Callable


def _create_func(code_body: str, func_name: str = None, **kwargs) -> Callable[..., Any]:
    """动态函数创建器"""
    # 从kwargs中提取关键参数
    filename = kwargs.pop("filename", "xt_tools._create_func")
    exmethod = kwargs.pop("exmethod", "exec")
    globals_dict = kwargs.pop("globals", {})

    # 确保globals_dict包含必要的内置函数
    globals_dict.setdefault("__builtins__", __builtins__)

    # 编译代码体
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
            raise ValueError("Compiled code contains no function definitions")

    return func


FUNC_ATTRS = (
    "__closure__",
    "__code__",
    "__defaults__",
    "__dict__",
    "__doc__",
    "__globals__",
    "__name__",
    "__module__",
    "__qualname__",
)

CODE_ATTRS = (
    "co_argcount",
    "co_cellvars",
    "co_code",
    "co_consts",
    "co_filename",
    "co_firstlineno",
    "co_flags",
    "co_freevars",
    "co_kwonlyargcount",
    "co_lines",
    "co_name",
    "co_names",
    "co_nlocals",
    "co_posonlyargcount",
    "co_stacksize",
    "co_varnames",
)


def inspect_function(func: Callable) -> None:
    """检查函数属性"""
    if not callable(func):
        raise TypeError("Expected a callable object")

    name = getattr(func, "__name__", "unnamed")
    qualname = getattr(func, "__qualname__", name)
    print(f"\nInspecting function: {qualname}")

    print("\nFunction attributes:")
    for attr in FUNC_ATTRS:
        try:
            value = getattr(func, attr, "N/A")
            if attr == "__globals__":
                # 特殊处理全局变量字典
                keys = list(value.keys())
                filtered_keys = [k for k in keys if not k.startswith("__")]
                print(f"{attr:15}: <globals dict> (Keys: {filtered_keys})")
            elif attr == "__closure__":
                # 特殊处理闭包
                if value:
                    cell_values = [c.cell_contents if c else None for c in value]
                    print(f"{attr:15}: {cell_values}")
                else:
                    print(f"{attr:15}: None")
            else:
                print(f"{attr:15}: {repr(value)[:100]}")
        except Exception as e:
            print(f"{attr:15}: Error - {str(e)[:50]}")

    if hasattr(func, "__code__"):
        print("\nCode attributes:")
        for attr in CODE_ATTRS:
            try:
                value = getattr(func.__code__, attr, "N/A")
                # 特殊处理字节码
                if attr == "co_code" and isinstance(value, bytes):
                    print(f"{attr:20}: <bytes len={len(value)}>")
                else:
                    print(f"{attr:20}: {repr(value)[:100]}")
            except Exception as e:
                print(f"{attr:20}: Error - {str(e)[:50]}")


if __name__ == "__main__":
    # 测试1: 创建简单函数
    simple_func = _create_func(
        "def simple_func(a, b=2):\n    '''Simple function'''\n    return a * b",
        func_name="simple_func",
    )
    print("\nTest 1: Simple function")
    print("Result:", simple_func(3, 4))  # 应该输出 12

    # 测试2: 创建闭包函数
    closure_func = _create_func(
        "def outer(x):\n    def inner(y):\n        return x * y\n    return inner",
        func_name="outer",
    )(5)  # 创建闭包，x=5
    print("\nTest 2: Closure function")
    print("Result:", closure_func(3))  # 应该输出 15

    # 测试3: 检查函数属性
    print("\nTest 3: Inspect simple function")
    inspect_function(simple_func)

    print("\nTest 4: Inspect closure function")
    inspect_function(closure_func)

    # 测试4: 使用默认参数创建函数
    dynamic_func = _create_func(
        "def multiply(a=3, b=6):\n    return a * b",
        func_name="multiply",
        filename="dynamic_math_func",
    )
    print("\nTest 5: Dynamic function with defaults")
    inspect_function(dynamic_func)
    print("Result:", dynamic_func())  # 应该输出 18
