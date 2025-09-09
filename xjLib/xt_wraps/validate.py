# !/usr/bin/env python
"""
==============================================================
Description  : 输入验证装饰器模块 - 提供函数参数的类型检查和验证功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-07 10:00:00
LastEditTime : 2025-09-07 10:00:00
FilePath     : /CODE/xjLib/xt_wraps/validate.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能：
- validate_params: 输入参数验证装饰器，同时支持同步和异步函数
- 支持多种验证方式，包括类型检查、值范围验证和自定义验证函数
- 提供灵活的参数验证配置，可按参数名或位置进行验证

主要特性：
- 统一的API设计，简化装饰器使用体验
- 自动识别并适配同步和异步函数
- 完整的异常捕获和处理机制
- 与项目其他模块保持一致的文档风格
- 支持参数类型、值范围和自定义验证规则
==============================================================
"""

import asyncio
import inspect
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union, TypeVar, cast, get_origin, get_args

from .exception import handle_exception
from .log import create_basemsg, mylog

T = TypeVar("T", bound=Callable[..., Any])


def validate_params(
    param_types: Optional[Dict[str, Type]] = None,
    param_ranges: Optional[Dict[str, Tuple[Any, Any]]] = None,
    custom_validators: Optional[Dict[str, Callable[[Any], bool]]] = None,
    required_params: Optional[Union[List[str], Set[str]]] = None,
    raise_exception: bool = True,
    default_return: Any = None,
):
    """
    参数验证装饰器 - 同时支持同步和异步函数，提供类型检查、范围验证和自定义验证功能

    核心功能：
    - 支持参数类型验证，确保输入参数符合预期类型
    - 支持参数值范围验证，限制数值型参数的取值范围
    - 支持自定义验证函数，实现复杂的业务逻辑验证
    - 支持必选参数验证，确保关键参数已提供
    - 自动识别并适配同步和异步函数
    - 完整的异常处理和日志记录机制

    Args:
        param_types: 参数字典，键为参数名，值为预期的类型
        param_ranges: 参数字典，键为参数名，值为(min, max)元组
        custom_validators: 参数字典，键为参数名，值为验证函数(返回布尔值)
        required_params: 必选参数列表或集合
        raise_exception: 验证失败时是否抛出异常，默认为True
        default_return: 验证失败且不抛出异常时的默认返回值

    Returns:
        装饰后的函数，保持原函数签名和功能

    Example:
        >>> # 基本类型验证
        >>> @validate_params(param_types={'a': int, 'b': str})
        >>> def process_data(a, b):
        >>>     return f"{b}: {a}"
        >>> 
        >>> # 带范围验证的同步函数
        >>> @validate_params(param_types={'age': int}, param_ranges={'age': (0, 120)})
        >>> def check_age(age):
        >>>     return f"年龄: {age}"
        >>> 
        >>> # 带自定义验证的异步函数
        >>> def is_valid_email(email):
        >>>     return '@' in email and '.' in email.split('@')[1]
        >>> 
        >>> @validate_params(custom_validators={'email': is_valid_email})
        >>> async def send_email(email, content):
        >>>     # 发送邮件的异步代码
        >>>     await asyncio.sleep(1)
        >>>     return f"邮件已发送至: {email}"
        >>> 
        >>> # 组合验证示例
        >>> @validate_params(
        >>>     param_types={'name': str, 'score': int},
        >>>     param_ranges={'score': (0, 100)},
        >>>     required_params=['name', 'score'],
        >>>     raise_exception=False,
        >>>     default_return="验证失败"
        >>> )
        >>> def record_score(name, score):
        >>>     return f"{name} 的分数: {score}"
        >>> 
        >>> # 位置参数验证
        >>> @validate_params(param_types={'arg0': int, 'arg1': str})
        >>> def mixed_params(a, b, c=None):
        >>>     return f"{a}, {b}, {c}"
    """
    # 处理参数默认值
    param_types = param_types or {}
    param_ranges = param_ranges or {}
    custom_validators = custom_validators or {}
    required_params = set(required_params) if required_params else set()

    # 定义实际的验证函数
    def validate_args(func: Callable, *args: Any, **kwargs: Any) -> Any:
        # 获取函数签名
        sig = inspect.signature(func)
        
        # 创建基础日志信息
        _basemsg = create_basemsg(func)
        
        # 尝试绑定参数，捕获缺少位置参数的错误
        try:
            # 绑定参数（不应用默认值，以便准确检查哪些参数被提供）
            bound_args = sig.bind_partial(*args, **kwargs)
            bound_args.apply_defaults()
        except TypeError as e:
            # 处理缺少参数的情况
            error_msg = f"参数绑定失败: {str(e)}"
            mylog.error(f"{_basemsg} | {error_msg}")
            if raise_exception:
                # 如果有定义required_params，我们可以提供更具体的错误信息
                if required_params:
                    # 检查哪些必选参数在提供的参数中缺失
                    provided_params = set(bound_args.arguments.keys() if 'bound_args' in locals() else [])
                    missing_params = required_params - provided_params
                    if missing_params:
                        param_name = next(iter(missing_params))  # 取第一个缺失的参数
                        error_msg = f"缺少必选参数: {param_name}"
                        raise ValueError(error_msg) from e
                # 否则直接抛出原始错误的包装
                raise ValueError(error_msg) from e
            return default_return
        
        # 验证必选参数
        for param in required_params:
            if param not in bound_args.arguments or bound_args.arguments[param] is inspect.Parameter.empty:
                error_msg = f"缺少必选参数: {param}"
                mylog.error(f"{_basemsg} | {error_msg}")
                if raise_exception:
                    raise ValueError(error_msg)
                return default_return
        
        # 验证参数类型
        for param_name, expected_type in param_types.items():
            # 处理位置参数，支持arg0, arg1等格式
            if param_name.startswith('arg') and param_name[3:].isdigit():
                idx = int(param_name[3:])
                if idx < len(args):
                    arg_value = args[idx]
                    # 使用自定义的类型检查函数处理泛型类型
                    if not is_instance(arg_value, expected_type):
                        type_name = get_type_name(expected_type)
                        error_msg = f"位置参数 #{idx} 应为 {type_name}，实际为 {type(arg_value).__name__}"
                        mylog.error(f"{_basemsg} | {error_msg}")
                        if raise_exception:
                            raise TypeError(error_msg)
                        return default_return
            # 处理命名参数
            elif param_name in bound_args.arguments:
                arg_value = bound_args.arguments[param_name]
                if arg_value is not None and not is_instance(arg_value, expected_type):
                    type_name = get_type_name(expected_type)
                    error_msg = f"参数 '{param_name}' 应为 {type_name}，实际为 {type(arg_value).__name__}"
                    mylog.error(f"{_basemsg} | {error_msg}")
                    if raise_exception:
                        raise TypeError(error_msg)
                    return default_return
        
        # 验证参数范围
        for param_name, (min_val, max_val) in param_ranges.items():
            if param_name in bound_args.arguments:
                arg_value = bound_args.arguments[param_name]
                if arg_value is not None:
                    # 处理同时有最小值和最大值的情况
                    if min_val is not None and max_val is not None:
                        if not (min_val <= arg_value <= max_val):
                            error_msg = f"参数 '{param_name}' 值 {arg_value} 超出范围 [{min_val}, {max_val}]"
                            mylog.error(f"{_basemsg} | {error_msg}")
                            if raise_exception:
                                raise ValueError(error_msg)
                            return default_return
                    # 处理只有最小值的情况
                    elif min_val is not None:
                        if arg_value < min_val:
                            error_msg = f"参数 '{param_name}' 值 {arg_value} 小于最小值 {min_val}"
                            mylog.error(f"{_basemsg} | {error_msg}")
                            if raise_exception:
                                raise ValueError(error_msg)
                            return default_return
                    # 处理只有最大值的情况
                    elif max_val is not None:
                        if arg_value > max_val:
                            error_msg = f"参数 '{param_name}' 值 {arg_value} 大于最大值 {max_val}"
                            mylog.error(f"{_basemsg} | {error_msg}")
                            if raise_exception:
                                raise ValueError(error_msg)
                            return default_return
        
        # 执行自定义验证
        for param_name, validator_func in custom_validators.items():
            if param_name in bound_args.arguments:
                arg_value = bound_args.arguments[param_name]
                if arg_value is not None:
                    try:
                        is_valid = validator_func(arg_value)
                        if not is_valid:
                            error_msg = f"参数 '{param_name}' 值验证失败: {arg_value}"
                            mylog.error(f"{_basemsg} | {error_msg}")
                            if raise_exception:
                                raise ValueError(error_msg)
                            return default_return
                    except ValueError as err:
                        # 如果验证器抛出ValueError，直接传递它
                        mylog.error(f"{_basemsg} | 自定义验证函数执行失败: {str(err)}")
                        if raise_exception:
                            raise
                        return default_return
                    except Exception as err:
                        error_msg = f"自定义验证函数执行失败: {str(err)}"
                        mylog.error(f"{_basemsg} | {error_msg}")
                        if raise_exception:
                            raise ValueError(error_msg) from err
                        return default_return
        
        # 所有验证通过，执行原函数
        return func(*args, **kwargs)

    # 辅助函数：检查类型，支持泛型类型
    def is_instance(obj: Any, type_hint: Type) -> bool:
        # 处理普通类型
        origin = get_origin(type_hint)
        if origin is None:
            try:
                return isinstance(obj, type_hint)
            except TypeError:
                # 如果是无法直接用isinstance检查的类型（比如typing.Any），返回True
                return True
        
        # 处理泛型类型
        if origin is list:
            if not isinstance(obj, list):
                return False
            elem_type = get_args(type_hint)[0] if get_args(type_hint) else Any
            return all(is_instance(elem, elem_type) for elem in obj)
        elif origin is dict:
            if not isinstance(obj, dict):
                return False
            key_type, val_type = get_args(type_hint) if len(get_args(type_hint)) >= 2 else (Any, Any)
            return all(is_instance(k, key_type) and is_instance(v, val_type) for k, v in obj.items())
        elif origin is tuple:
            if not isinstance(obj, tuple):
                return False
            elem_types = get_args(type_hint)
            if not elem_types:
                return True  # 空tuple类型
            if len(elem_types) == 2 and elem_types[1] is Ellipsis:
                # 处理Tuple[T, ...]形式
                elem_type = elem_types[0]
                return all(is_instance(elem, elem_type) for elem in obj)
            else:
                # 处理固定长度的tuple
                if len(obj) != len(elem_types):
                    return False
                return all(is_instance(obj[i], elem_types[i]) for i in range(len(obj)))
        elif origin is Union:
            return any(is_instance(obj, t) for t in get_args(type_hint))
        
        # 其他情况尝试使用原始的isinstance
        try:
            return isinstance(obj, origin)
        except TypeError:
            return False
    
    # 辅助函数：获取类型名称，支持泛型类型
    def get_type_name(type_hint: Type) -> str:
        origin = get_origin(type_hint)
        if origin is None:
            return getattr(type_hint, '__name__', str(type_hint))
        
        # 处理泛型类型名称
        origin_name = getattr(origin, '__name__', str(origin))
        args = get_args(type_hint)
        if args:
            arg_names = [get_type_name(arg) for arg in args]
            return f"{origin_name}[{', '.join(arg_names)}]"
        return origin_name
    
    # 使用core.py中的错误处理方式，但保留raise_exception的行为
    def decorator(func: T) -> T:
        # 定义异步包装函数
        @wraps(func)
        async def async_wrapped(*args: Any, **kwargs: Any) -> Any:
            try:
                result = validate_args(func, *args, **kwargs)
                # 如果验证函数返回了默认值，则直接返回
                if result is default_return:
                    return result
                # 否则执行原异步函数
                return await result
            except Exception as err:
                # 使用core.py中的异常处理方式
                handle_exception(err, create_basemsg(func))
                # 根据raise_exception决定是抛出异常还是返回默认值
                if raise_exception:
                    raise
                return default_return

        # 定义同步包装函数
        @wraps(func)
        def sync_wrapped(*args: Any, **kwargs: Any) -> Any:
            try:
                # 直接执行验证和函数调用
                return validate_args(func, *args, **kwargs)
            except Exception as err:
                # 使用core.py中的异常处理方式
                handle_exception(err, create_basemsg(func))
                # 根据raise_exception决定是抛出异常还是返回默认值
                if raise_exception:
                    raise
                return default_return

        # 根据函数类型返回对应的包装函数
        return (
            cast(T, async_wrapped)
            if asyncio.iscoroutinefunction(func)
            else cast(T, sync_wrapped)
        )
    
    return decorator


# 类型别名，提供更直观的API
validate_types = validate_params  # 简化的类型验证别名
validate_ranges = validate_params  # 简化的范围验证别名
validate_custom = validate_params  # 简化的自定义验证别名
