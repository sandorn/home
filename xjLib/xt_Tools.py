# !/usr/bin/env python
"""
#==============================================================
#Descripttion : 函数超时、函数默认值装饰、动态创建函数、重试装饰器2种、获取对象帮助
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-03 18:42:56
#FilePath     : /xjLib/xt_Tools.py
#LastEditTime : 2020-07-30 12:43:08
#Github       : https://github.com/sandorn/home
#==============================================================
拒绝重复造轮子!python实用工具类及函数大推荐! - 知乎
https://zhuanlan.zhihu.com/p/31644562
https://github.com/ShichaoMa
"""

import time
import traceback
from copy import deepcopy
from functools import wraps
from types import FunctionType
from typing import Any, Callable, Optional, Type

import wrapt


class ExceptContext:
    def __init__(self, exception: Type[Exception] = Exception, func_name: str = "", errback: Optional[Callable[..., Any]] = None, finalback: Optional[Callable[..., Any]] = None):
        self.errback = errback or self.default_res_errback
        self.finalback = finalback or self.default_res_finalback
        self.exception = exception
        self.has_error = False
        self.func_name = func_name

    def __enter__(self):
        return self

    def __exit__(self, exc_type: str, exc_val: str, exc_tb: str):
        if isinstance(exc_val, self.exception):
            self.has_error = True
            return_code = self.errback(self.func_name, exc_type, exc_val, exc_tb)
        else:
            return_code = False
        self.finalback(self.has_error)
        return return_code

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        @wrapt.decorator
        def wrapper(func: Callable[..., Any], instance: Optional[Any], args: tuple[Any], kwargs: dict[Any, Any]) -> Any:
            with self:
                return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def default_res_errback(func_name: str, exc_type: str, exc_val: str, exc_tb: str):
        print(f"Exception in {func_name}: {exc_val}, {exc_tb}")
        return True

    @staticmethod
    def default_res_finalback(has_error: bool): ...


def call_later(callback_fn: str, call_args: tuple = (), immediately: bool = True, interval: int = 1) -> Callable[..., Any]:
    """
    被装饰的方法需要大量调用,随后需要调用保存方法,但是因为被装饰的方法访问量很高,而保存方法开销很大
    所以设计在装饰方法持续调用一定间隔后,再调用保存方法。规定间隔内,无论调用多少次被装饰方法,保存方法只会
    调用一次,除非  immediately=True
    callback_fn   : 随后需要调用的方法名
    call_args  : 随后需要调用的方法所需要的参数
    immediately: 是否立即调用
    interval   : 调用间隔
    return     :
    """

    @wrapt.decorator
    def decorate(func: Callable[..., Any], instance: Optional[Any], args: tuple[Any], kwargs: dict[Any, Any]) -> Any:
        self = args[0]
        try:
            return func(*args, **kwargs)
        finally:
            if immediately:
                getattr(self, callback_fn)(*call_args)
            else:
                now = time.time()
                if now - self.__dict__.get("last_call_time", 0) > interval:
                    getattr(self, callback_fn)(*call_args)
                    self.__dict__["last_call_time"] = now

    return decorate


def freshdefault(func: Callable[..., Any]) -> Callable[..., Any]:
    """装饰函数,使可变对象[list|dict]可以作为默认值"""
    default_args = func.__defaults__
    ftypes = func.__annotations__  # 函数注解

    @wraps(func)
    def wrapper(*args: tuple[Any], **kwargs: dict[Any, Any]) -> Any:
        if default_args:
            func.__defaults__ = deepcopy(default_args)
        if ftypes:
            for key in ftypes.keys():
                if key not in kwargs.keys():
                    kwargs[key] = deepcopy(ftypes[key])
        return func(*args, **kwargs)

    return wrapper


def _create_func(code_body, **kwargs) -> Callable[..., Any]:
    """动态函数创建器"""
    kwargs.setdefault("globals", {})
    filename = kwargs.pop("filename", "xt_tools._create_func")
    exmethod = kwargs.pop("exmethod", "exec")
    module_code = compile(code_body, filename, exmethod)
    return FunctionType(module_code.co_consts[0], **kwargs)

    # FunctionType(code, globals, name=None, argdefs=None, closure=None)
    # FunctionType(wrapper.__code__, wrapper.__globals__, name=func.__name__, argdefs=wrapper.__defaults__, closure=wrapper.__closure__)


func_attr_name_list: list[str] = [
    # #函数的内置属性
    "__closure__",
    "__code__",
    "__defaults__",
    # "__default_ress__",
    "__dict__",
    "__doc__",
    "__globals__",
    "__name__",
]
func_code_name_list: list[str] = [
    # #函数.__code__的内置属性
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


@wrapt.decorator
def catch_wraps(func, instance, args, kwargs) -> Any | None:
    try:
        return func(*args, **kwargs)
    except Exception as err:
        print(f"catch_wraps: [{func.__name__}]\tError: {err!r}")
        return None


def try_except_wraps(max_retries=3, delay=0.2, step=0.1, sleep_fn=time.sleep, validate_fn=None, callback_fn=None, default_res=None):
    """
    函数执行出现异常时自动重试的简单装饰器
    :param f: function 执行的函数。
    :param max_retries: int 最多重试次数。
    :param delay: int/float 每次重试的延迟,单位秒。
    :param step: int/float 每次重试后延迟递增,单位秒。
    :param sleep_fn: 实现延迟的方法,默认为time.sleep_fn。
    在一些异步框架,如tornado中,使用time.sleep会导致阻塞,可以传入自定义的方法来实现延迟。
    自定义方法函数签名应与time.sleep相同,接收一个参数,为延迟执行的时间。
    可用于记录异常日志,中断重试等。
    如处理函数正常执行,并返回True,则表示告知重试装饰器异常已经处理,重试装饰器终止重试,并且不会抛出任何异常。
    如处理函数正常执行,没有返回值或返回除True以外的结果,则继续重试。
    如处理函数抛出异常,则终止重试,并将处理函数的异常抛出。
    :param validate_fn: 验证函数,用于验证执行结果,并确认是否继续重试。
    函数签名应接收一个参数,每次被装饰的函数完成且未抛出任何异常时,调用验证函数,将执行的结果传入。
    如验证函数正常执行,且返回False,则继续重试,即使被装饰的函数完成且未抛出任何异常。
    如验证函数正常执行,没有返回值或返回除False以外的结果,则终止重试,并将函数执行结果返回。
    如验证函数抛出异常,且异常属于被重试装饰器捕获的类型,则继续重试。
    如验证函数抛出异常,且异常不属于被重试装饰器捕获的类型,则将验证函数的异常抛出。
    :param callback_fn: 回调函数,处理结果。
    :param default_res: 默认值/默认值生成函数
    :return: 被装饰函数的执行结果。
    """

    @wrapt.decorator
    def wrapper(func, instance, args, kwargs):
        func_exc = None
        for index in range(max_retries):
            try:
                result = func(*args, **kwargs)
                if callable(validate_fn) and validate_fn(result) is False:
                    continue
                return callback_fn(result) if callable(callback_fn) else result
            except Exception as ex:
                func_exc, _ = ex, traceback.format_exc()
                sleep_fn(delay + step * index)  # #延迟重试

        print(f"try_except_wraps: [{func.__name__}]\tError: {func_exc!r}")
        return default_res() if callable(default_res) else default_res

    return wrapper


def retry_on_exception(max_retry=3):
    """Retry 3 times if the function throws an exception."""

    @wrapt.decorator
    def wrapper(func, instance, args, kwargs):
        for _ in range(max_retry):
            try:
                return func(*args, **kwargs)
            except Exception as err:
                print(f"retry_on_exception: [{func.__name__}]\tError: {err!r}")
        return None

    return wrapper


if __name__ == "__main__":

    @try_except_wraps()
    def simple() -> float:
        """简单函数"""
        return 6 / 0

    @catch_wraps
    def readFile(filename) -> None:
        with open(file=filename) as f:
            print(len(f.readlines()))

    def add(a, b) -> float:
        with ExceptContext():
            return int(x=a) / int(x=b)

    @try_except_wraps()
    def assertSumIsPositive(a, b) -> float:
        return int(x=a) / int(x=b)

    @retry_on_exception()
    def checkLen(a, b) -> float:
        return int(a) / int(b)

    def fre() -> None:
        # 可变对象默认装饰器
        @freshdefault
        def extend_list(v, li=[]):
            li.append(v)
            return li

        list1 = extend_list(99)
        list2 = extend_list([1, 2, 3, 4], [])
        list3 = extend_list("a")
        print(list1)
        print(list2)
        print(list3, list1)

        print(list1 is list3)

    def fu() -> None:
        # #函数创建器
        foo_func = _create_func("def foo():a=3;return 3")

        print(foo_func())

        for attr in func_attr_name_list:
            ...
            # print(attr, ":", getattr(foo_func, attr))

        for attr in func_code_name_list:
            ...
            # print(f"foo_func.__code__.{attr.ljust(33)}", ":", getattr(foo_func.__code__, attr))
        print(foo_func.__dict__)

    print(simple())
    # readFile("UnexistFile.txt")
    # print(add(123, 0))
    # print(assertSumIsPositive(6, 0))
    # print(checkLen(a=5, b=0))

    # fre()
    # fu()
