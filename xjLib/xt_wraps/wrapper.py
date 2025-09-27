# !/usr/bin/env python3
"""
==============================================================
Description  : 核心装饰器工具模块 - 提供同步/异步函数通用装饰器工厂
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-08-28 11:06:38
LastEditTime : 2025-09-06 10:00:00
FilePath     : /CODE/xjlib/xt_wraps/deco.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from __future__ import annotations

import asyncio
import random
import time
import traceback
from collections.abc import Callable
from functools import wraps
from time import perf_counter, sleep
from typing import Any, TypeVar

from xt_wraps.log import mylog

# 类型别名
ExceptionTypes = tuple[type[Exception], ...]
T = TypeVar('T')


def wraps_fact(wrapper_func: Callable) -> Callable:
    """
    通用装饰器 - 简化同步/异步装饰器的编写

    这个装饰器允许你专注于装饰逻辑，而无需关心同步/异步函数的差异。
    它会自动检测函数类型并选择合适的包装器。
    """

    def decorator(func: Callable) -> Callable:
        """实际的装饰器实现"""

        if asyncio.iscoroutinefunction(func):
            # 异步函数装饰器
            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                """异步函数包装器"""
                # 如果包装器函数也是异步的，直接await调用
                if asyncio.iscoroutinefunction(wrapper_func):
                    return await wrapper_func(func, args, kwargs)
                # 包装器函数是同步的，直接调用
                return wrapper_func(func, args, kwargs)

            return async_wrapper
        # 同步函数装饰器

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            """同步函数包装器"""
            # 如果包装器函数是异步的，需要在事件循环中运行
            if asyncio.iscoroutinefunction(wrapper_func):
                try:
                    # 尝试获取当前运行的事件循环
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    # 没有正在运行的事件循环，创建一个新的
                    return asyncio.run(wrapper_func(func, args, kwargs))
                else:
                    # 有正在运行的事件循环，创建任务
                    coro = wrapper_func(func, args, kwargs)
                    # 在同步上下文中等待协程完成
                    task = loop.create_task(coro)
                    # 使用asyncio.wait_for等待任务完成，避免阻塞
                    return asyncio.run_coroutine_threadsafe(task, loop).result()
            else:
                # 包装器函数是同步的，直接调用
                return wrapper_func(func, args, kwargs)

        return sync_wrapper

    return decorator


def handle_exception(
    errinfo: Exception,
    re_raise: bool = False,
    default_return: Any = None,
    callfrom: Callable | None = None,
    log_traceback: bool = True,
    custom_message: str | None = None,
) -> Any:
    """
    统一的异常处理函数，提供完整的异常捕获、记录和处理机制

    Args:
        errinfo: 异常对象
        re_raise: 是否重新抛出异常，默认False（不抛出，返回默认值）
        default_return: 不抛出异常时的默认返回值，default_return为None时返回错误信息字符串
        callfrom: 调用来源函数，用于日志记录
        log_traceback: 是否记录完整堆栈信息，默认True
        custom_message: 自定义错误提示信息，默认None

    Returns:
        Any: 如果re_raise=True，重新抛出异常；否则返回default_return或错误信息字符串
    """
    # 构建错误信息
    error_type = type(errinfo).__name__
    error_msg = str(errinfo)

    # 统一的日志格式
    error_message = f'{error_type} | {error_msg}'
    if custom_message:
        error_message = f'{custom_message} | {error_message}'

    # 记录警告日志
    mylog.error(error_message, callfrom=callfrom)

    # 如果需要，记录完整堆栈信息
    if log_traceback:
        mylog.error(f'堆栈信息: {traceback.format_exc()}', callfrom=callfrom)

    # 根据需要重新抛出异常
    if re_raise:
        raise errinfo
    return error_message if default_return is None else default_return


# 创建计时装饰器
@wraps_fact
async def timer_wrapper(f, args, kwargs):
    """计时包装器"""
    start_time = perf_counter()
    try:
        # 根据被装饰函数的类型决定是否使用await
        if asyncio.iscoroutinefunction(f):
            return await f(*args, **kwargs)
        return f(*args, **kwargs)
    finally:
        end_time = perf_counter()
        mylog.info(f'{f.__name__} 执行耗时: {end_time - start_time:.4f}秒')


# 创建日志装饰器
@wraps_fact
async def log_wrapper(f, args, kwargs):
    """日志包装器"""
    # 记录函数调用和参数
    mylog.debug('调用函数 {}，参数: {}, 关键字参数: {}', f.__name__, args, kwargs, callfrom=f)

    try:
        # 根据被装饰函数的类型决定是否使用await
        if asyncio.iscoroutinefunction(f):
            result = await f(*args, **kwargs)
        else:
            result = f(*args, **kwargs)

        # 记录函数返回值
        mylog.success('函数 {} 执行成功，返回值: {}', f.__name__, result, callfrom=f)
        return result
    except Exception as e:
        # 记录异常
        mylog.error('函数 {} 执行时发生异常: {}', f.__name__, str(e), callfrom=f)
        raise


# 创建重试装饰器
def retry_wrapper(max_attempts: int = 3, min_wait: float = 0.0, max_wait: float = 1.0, retry_exceptions: tuple = (Exception,)):
    """
    创建重试装饰器的工厂函数

    Args:
        max_attempts: 最大尝试次数，默认为3次
        min_wait: 重试间隔的最小等待时间(秒)，默认为0.0秒
        max_wait: 重试间隔的最大等待时间(秒)，默认为1.0秒
        retry_exceptions: 需要重试的异常类型元组，默认为所有异常
    """

    @wraps_fact
    async def _retry_wrapper_inner(func, args, kwargs):
        """重试包装器"""
        last_exception = None

        for attempt in range(max_attempts):
            try:
                mylog.debug('第 {} 次尝试调用函数 {}', attempt + 1, func.__name__, callfrom=func)
                if asyncio.iscoroutinefunction(func):
                    # 异步函数直接await
                    return await func(*args, **kwargs)
                # 同步函数直接调用
                return func(*args, **kwargs)
            except retry_exceptions as e:
                last_exception = e
                mylog.warning('第 {} 次尝试失败: {}', attempt + 1, str(e), callfrom=func)

                # 如果不是最后一次尝试，则等待一段时间后重试
                if attempt < max_attempts - 1:
                    wait_time = random.uniform(min_wait, max_wait)  # noqa: S311
                    mylog.info('等待 {:.2f} 秒后进行下一次尝试', wait_time, callfrom=func)
                    # 异步等待或同步等待
                    if asyncio.iscoroutinefunction(func):
                        await asyncio.sleep(wait_time)
                    else:
                        time.sleep(wait_time)
            except Exception as e:
                # 不在重试异常列表中的异常直接抛出
                mylog.error('函数 {} 发生非重试异常: {}', func.__name__, str(e), callfrom=func)
                raise

        # 所有尝试都失败了
        mylog.error('函数 {} 在 {} 次尝试后仍然失败', func.__name__, max_attempts, callfrom=func)
        raise last_exception

    return _retry_wrapper_inner


# 创建异常处理装饰器
def exception_wrapper(re_raise: bool = True, default_return: Any = None, allowed_exceptions: ExceptionTypes = (Exception,), log_traceback: bool = True, custom_message: str | None = None):
    """
    创建异常处理装饰器的工厂函数

    Args:
        re_raise: 是否重新抛出异常，默认True
        default_return: 发生异常时的默认返回值，None时返回错误信息字符串
        allowed_exceptions: 允许捕获的异常类型元组，默认捕获所有异常
        log_traceback: 是否记录完整堆栈信息，默认True
        custom_message: 自定义错误提示信息，默认None
    """

    @wraps_fact
    async def _exception_wrapper_inner(func, args, kwargs):
        """异常处理包装器"""
        try:
            if asyncio.iscoroutinefunction(func):
                # 异步函数直接await
                return await func(*args, **kwargs)
            # 同步函数直接调用
            return func(*args, **kwargs)
        except allowed_exceptions as err:
            return handle_exception(err, re_raise, default_return, func, log_traceback, custom_message)
        except Exception as err:
            mylog.critical(f'函数 {func.__name__} 发生未处理异常: {type(err).__name__} - {err!s}', callfrom=func)
            if re_raise:
                raise err

    return _exception_wrapper_inner


# 创建缓存装饰器
def cache_wrapper(expire_time: int = 60):
    """
    创建缓存装饰器的工厂函数

    Args:
        expire_time: 缓存过期时间（秒），默认60秒
    """
    cache_storage = {}

    @wraps_fact
    async def _cache_wrapper_inner(func, args, kwargs):
        """缓存包装器"""
        # 创建缓存键
        cache_key = f'{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}'

        # 检查缓存是否存在且未过期
        if cache_key in cache_storage:
            result, timestamp = cache_storage[cache_key]
            if time.time() - timestamp < expire_time:
                mylog.debug('函数 {} 使用缓存结果', func.__name__, callfrom=func)
                return result
            # 缓存过期，删除旧缓存
            del cache_storage[cache_key]

        # 执行函数并缓存结果
        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            # 存储结果和时间戳
            cache_storage[cache_key] = (result, time.time())
            mylog.debug('函数 {} 执行并缓存结果', func.__name__, callfrom=func)
            return result
        except Exception as e:
            mylog.error('函数 {} 执行时发生异常: {}', func.__name__, str(e), callfrom=func)
            raise

    return _cache_wrapper_inner


# 创建权限验证装饰器
def permission_wrapper(required_permissions: list[str] | None = None):
    """
    创建权限验证装饰器的工厂函数

    Args:
        required_permissions: 所需权限列表，默认为None（不需要特定权限）
    """

    @wraps_fact
    async def _permission_wrapper_inner(func, args, kwargs):
        """权限验证包装器"""
        # 获取当前用户上下文（这里简化处理，实际项目中可能从请求上下文获取）
        # 在实际应用中，你可能需要从线程局部存储或请求上下文中获取用户信息
        current_user_permissions = getattr(func, '_user_permissions', ['admin'])  # 默认具有管理员权限

        # 检查权限
        if required_permissions:
            missing_permissions = [perm for perm in required_permissions if perm not in current_user_permissions]
            if missing_permissions:
                error_msg = f'权限不足，缺少权限: {missing_permissions}'
                mylog.warning(error_msg, callfrom=func)
                raise PermissionError(error_msg)

        mylog.debug('函数 {} 权限验证通过', func.__name__, callfrom=func)

        # 执行函数
        try:
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)
        except Exception as e:
            mylog.error('函数 {} 执行时发生异常: {}', func.__name__, str(e), callfrom=func)
            raise

    return _permission_wrapper_inner


# 使用装饰器
@timer_wrapper
def sync_function(x: int, y: int) -> int:
    """同步函数"""
    sleep(0.1)
    return x + y


@timer_wrapper
async def async_function(x: int, y: int) -> int:
    """异步函数"""
    await asyncio.sleep(0.1)
    return x * y


# 使用日志装饰器
@log_wrapper
def sync_function_with_log(x: int, y: int) -> int:
    """带日志的同步函数"""
    return x + y


@log_wrapper
async def async_function_with_log(x: int, y: int) -> int:
    """带日志的异步函数"""
    await asyncio.sleep(0.1)
    return x * y


# 使用重试装饰器
# 创建一个重试装饰器实例
retry_on_exception = retry_wrapper(max_attempts=3, min_wait=0.1, max_wait=0.5, retry_exceptions=(ValueError, ConnectionError))


@retry_on_exception
def unstable_function(x: int) -> int:
    """不稳定的函数，有一定概率抛出异常"""
    if random.random() < 0.7:  # 70%的概率失败  # noqa: S311
        raise ValueError('随机错误')
    return x * 2


@retry_on_exception
async def async_unstable_function(x: int) -> int:
    """异步不稳定的函数，有一定概率抛出异常"""
    if random.random() < 0.7:  # 70%的概率失败  # noqa: S311
        raise ConnectionError('异步连接错误')
    await asyncio.sleep(0.1)
    return x * 3


# 使用异常处理装饰器
# 创建一个异常处理装饰器实例
safe_exception_handler = exception_wrapper(re_raise=False, default_return='默认值', allowed_exceptions=(ValueError, TypeError), custom_message='函数执行出错')


@safe_exception_handler
def function_with_exception(x: int) -> int:
    """可能会抛出异常的函数"""
    if x < 0:
        raise ValueError('x不能为负数')
    if x == 0:
        raise TypeError('x不能为零')
    return x * 10


@safe_exception_handler
async def async_function_with_exception(x: int) -> int:
    """可能会抛出异常的异步函数"""
    if x < 0:
        raise ValueError('x不能为负数')
    if x == 0:
        raise TypeError('x不能为零')
    await asyncio.sleep(0.1)
    return x * 20


# 使用缓存装饰器
# 创建一个缓存装饰器实例
cache_result = cache_wrapper(expire_time=30)  # 30秒过期


@cache_result
def expensive_function(n: int) -> int:
    """计算密集型函数，用于演示缓存效果"""
    mylog.info('执行昂贵的计算...')
    # 模拟计算密集型操作
    return sum(i * i for i in range(n))


@cache_result
async def async_expensive_function(n: int) -> int:
    """异步计算密集型函数，用于演示缓存效果"""
    mylog.info('执行异步昂贵的计算...')
    # 模拟异步计算密集型操作
    await asyncio.sleep(0.1)
    return sum(i * i for i in range(n))


# 使用权限验证装饰器
# 创建一个权限验证装饰器实例
admin_required = permission_wrapper(required_permissions=['admin'])
user_required = permission_wrapper(required_permissions=['user'])


@admin_required
def admin_only_function(data: str) -> str:
    """只有管理员才能访问的函数"""
    return f'管理员操作: {data}'


@user_required
async def user_function(data: str) -> str:
    """用户权限可访问的函数"""
    await asyncio.sleep(0.1)
    return f'用户操作: {data}'


if __name__ == '__main__':
    
    # 简单测试
    print('=== 测试同步函数 ===')
    result1 = sync_function(3, 4)
    print(f'同步函数结果: {result1}')

    print('\n=== 测试异步函数 ===')

    async def test_async():
        result2 = await async_function(5, 6)
        print(f'异步函数结果: {result2}')

    asyncio.run(test_async())

    print('\n=== 测试带日志的同步函数 ===')
    result3 = sync_function_with_log(7, 8)
    print(f'带日志的同步函数结果: {result3}')

    print('\n=== 测试带日志的异步函数 ===')

    async def test_async_log():
        result4 = await async_function_with_log(9, 10)
        print(f'带日志的异步函数结果: {result4}')

    asyncio.run(test_async_log())

    print('\n=== 测试重试装饰器（同步函数） ===')
    try:
        result5 = unstable_function(5)
        print(f'不稳定函数结果: {result5}')
    except Exception as e:
        print(f'不稳定函数最终失败: {e}')

    print('\n=== 测试重试装饰器（异步函数） ===')

    async def test_async_retry():
        try:
            result6 = await async_unstable_function(6)
            print(f'异步不稳定函数结果: {result6}')
        except Exception as e:
            print(f'异步不稳定函数最终失败: {e}')

    asyncio.run(test_async_retry())

    print('\n=== 测试异常处理装饰器（同步函数） ===')
    result7 = function_with_exception(-5)  # 会触发ValueError
    print(f'负数输入结果: {result7}')

    result8 = function_with_exception(0)  # 会触发TypeError
    print(f'零输入结果: {result8}')

    result9 = function_with_exception(5)  # 正常执行
    print(f'正常输入结果: {result9}')

    print('\n=== 测试异常处理装饰器（异步函数） ===')

    async def test_async_exception():
        result10 = await async_function_with_exception(-3)  # 会触发ValueError
        print(f'异步负数输入结果: {result10}')

        result11 = await async_function_with_exception(0)  # 会触发TypeError
        print(f'异步零输入结果: {result11}')

        result12 = await async_function_with_exception(3)  # 正常执行
        print(f'异步正常输入结果: {result12}')

    asyncio.run(test_async_exception())

    print('\n=== 测试缓存装饰器（同步函数） ===')
    # 第一次调用
    result13 = expensive_function(1000)
    print(f'昂贵函数结果1: {result13}')

    # 第二次调用（应该使用缓存）
    result14 = expensive_function(1000)
    print(f'昂贵函数结果2: {result14}')

    print('\n=== 测试缓存装饰器（异步函数） ===')

    async def test_async_cache():
        # 第一次调用
        result15 = await async_expensive_function(1000)
        print(f'异步昂贵函数结果1: {result15}')

        # 第二次调用（应该使用缓存）
        result16 = await async_expensive_function(1000)
        print(f'异步昂贵函数结果2: {result16}')

    asyncio.run(test_async_cache())

    print('\n=== 测试权限验证装饰器 ===')
    # 设置函数的用户权限（模拟）
    admin_only_function._user_permissions = ['admin']
    user_function._user_permissions = ['user']

    try:
        result17 = admin_only_function('敏感数据')
        print(f'管理员函数结果: {result17}')
    except PermissionError as e:
        print(f'权限错误: {e}')

    async def test_async_permission():
        try:
            result18 = await user_function('普通数据')
            print(f'用户函数结果: {result18}')
        except PermissionError as e:
            print(f'权限错误: {e}')

    asyncio.run(test_async_permission())
