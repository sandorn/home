# !/usr/bin/env python3
"""
==============================================================
Description  : {模块描述}
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-20 10:54:48
LastEditTime : 2025-09-24 00:31:07
FilePath     : D:/CODE/xjlib/template.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能:
- {核心功能1}
- {核心功能2}
- {核心功能3}

主要特性:
- {特性1}
- {特性2}
- {特性3}
==============================================================
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from functools import wraps

# 导入必要的模块
from typing import Any, ParamSpec, TypeVar

from xt_wraps.log import mylog as logger

# 类型变量定义
t = TypeVar('t')
P = ParamSpec('P')
R = TypeVar('R')


class TemplateClass:
    """{类名称} - {类描述}

    该类{详细描述}。

    Args:
        param1: {参数1描述}（类型：{参数1类型}，必填）
        param2: {参数2描述}（类型：{参数2类型}，默认值：{参数2默认值}）
        param3: {参数3描述}（类型：{参数3类型}，默认值：{参数3默认值}）

    Attributes:
        attr1: {属性1描述}
        attr2: {属性2描述}
        attr3: {属性3描述}

    Raises:
        ValueError: {抛出ValueError的情况}
        TypeError: {抛出TypeError的情况}

    Example:
        >>> # 创建实例示例
        >>> instance = TemplateClass(param1={参数1示例值})
        >>> # 使用方法示例
        >>> result = instance.example_method({方法参数示例})
        >>> print(result)
        {方法返回示例}
    """
    def __init__(self, param1: str, param2: int = 0, param3: list[str] | None = None):
        # 初始化代码
        self.attr1 = param1
        self.attr2 = param2
        self.attr3 = param3 or []

    def example_method(self, arg1: str, arg2: int | None = None) -> dict[str, Any]:
        """{方法名称} - {方法描述}

        {方法详细描述}

        Args:
            arg1: {参数1描述}
            arg2: {参数2描述}（默认值：None）

        Returns:
            {返回值类型}: {返回值描述}

        Raises:
            ValueError: {抛出ValueError的情况}
            TypeError: {抛出TypeError的情况}

        Example:
            >>> instance = TemplateClass({类参数示例})
            >>> result = instance.example_method({方法参数示例})
            >>> print(result)
            {方法返回示例}
        """
        # 使用Guard Clause提前检查参数类型
        if not isinstance(arg1, str):
            raise TypeError('参数arg1必须是字符串类型')

        # 方法的主体逻辑
        result = {'status': 'success', 'data': f'processed {arg1}'}
        if arg2 is not None:
            result['data'] += f' with {arg2}'

        return result

    async def async_example_method(self, arg1: str) -> bool:
        """异步{方法名称} - {方法描述}

        {方法详细描述}

        Args:
            arg1: {参数1描述}

        Returns:
            bool: {返回值描述}

        Example:
            >>> instance = TemplateClass({类参数示例})
            >>> result = await instance.async_example_method({方法参数示例})
            >>> print(result)
            {方法返回示例}
        """
        # 异步方法实现代码示例
        # 实际使用时可以包含异步操作，如异步数据库查询、网络请求等
        return True


# 独立函数示例
def utility_function(input_value: str | int, optional_param: bool = False) -> list[str]:
    """{函数名称} - {函数描述}

    {函数详细描述}

    Args:
        input_value: {参数1描述}
        optional_param: {参数2描述}（默认值：False）

    Returns:
        {返回值类型}: {返回值描述}

    Raises:
        ValueError: {抛出ValueError的情况}
        TypeError: {抛出TypeError的情况}

    Example:
        >>> result = utility_function({参数示例}, True)
        >>> print(result)
        {返回值示例}
    """
    # 使用Guard Clause提前检查参数类型
    if not isinstance(input_value, (str, int)):
        raise TypeError('参数input_value必须是字符串或整数类型')

    # 函数主体逻辑
    result = ['processed', str(input_value)]
    if optional_param:
        result.append('optional')

    return result


# 装饰器工厂函数示例
def create_decorator(**decorator_kwargs: Any) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """创建一个通用装饰器的工厂函数

    Args:
        **decorator_kwargs: 传递给装饰器的额外参数

    Returns:
        Callable: 一个装饰器函数
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # 装饰器逻辑
            # 例如：记录日志、性能统计、异常处理等
            return func(*args, **kwargs)
        return wrapper
    return decorator


# 异步/同步通用装饰器
def sync_async_decorator(func):
    """通用同步/异步装饰器
    
    自动处理同步和异步函数的装饰器，简化类型注解。
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            async def async_wrapped():
                logger.debug(f'异步执行: {func.__name__}')
                return await func(*args, **kwargs)
            return async_wrapped()
        logger.debug(f'同步执行: {func.__name__}')
        return func(*args, **kwargs)
    
    return wrapper


# 使用示例
if __name__ == '__main__':
    """本模块功能测试与使用示例

    提供本模块的主要功能演示和使用方法，包括:
    1. {示例1}
    2. {示例2}
    3. {示例3}
    """

    logger.start('开始模块功能测试')
    logger.info('=========================')
    
    try:
        # 示例1: 创建类实例并调用方法
        logger.info('\n=== 示例1: 基本功能测试 ===')
        instance = TemplateClass('demo_value', 42)
        result = instance.example_method('test_argument')
        logger.info(f'方法调用结果: {result}')
        
        # 示例2: 使用可选参数
        logger.info('\n=== 示例2: 可选参数测试 ===')
        result = utility_function(123, optional_param=True)
        logger.info(f'工具函数结果: {result}')
        
        # 示例3: 异常处理
        logger.info('\n=== 示例3: 异常处理测试 ===')
        try:
            result = utility_function(None)  # 故意传入错误类型的参数
        except TypeError as e:
            logger.warning(f'预期的异常: {e}')
            
        logger.ok('所有测试完成')
    except Exception as e:
        logger.fail(f'测试过程中出错: {e}')
    
    logger.info('=========================')
    logger.stop('结束模块功能测试')