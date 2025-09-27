"""
Test the @exc_wraps decorator
"""
from __future__ import annotations

import asyncio

from xt_wraps.exception import exc_wraps, handle_exception


# 测试基本的同步函数异常处理
@exc_wraps(re_raise=False, default_return='default_value')
def test_sync_function():
    raise ValueError('This is a test error')


# 测试同步函数正常执行
@exc_wraps()
def test_sync_normal():
    return 'normal_result'


# 测试特定异常捕获
@exc_wraps(allowed_exceptions=(ZeroDivisionError,), re_raise=False, default_return=0)
def test_specific_exception():
    return 1 / 0


# 测试异步函数异常处理
@exc_wraps(re_raise=False, default_return='async_default')
async def test_async_function():
    raise RuntimeError('This is an async test error')


# 测试异步函数正常执行
@exc_wraps()
async def test_async_normal():
    return 'async_normal_result'


# 测试自定义错误消息
@exc_wraps(custom_message='Custom error occurred', re_raise=False)
def test_custom_message():
    raise Exception('Original error message')


def test_handle_exception():
    """测试 handle_exception 函数"""
    try:
        raise ValueError('Test handle_exception')
    except Exception as e:
        result = handle_exception(e, re_raise=False, default_return='handled')
        return result


# 测试异常重抛
@exc_wraps(re_raise=True)
def test_reraise_exception():
    raise ValueError('This should be re-raised')


# 测试不记录堆栈信息
@exc_wraps(log_traceback=False, re_raise=False)
def test_no_traceback():
    raise ValueError('This should not log traceback')


async def main():
    """主测试函数"""
    print('Testing exc_wraps decorator...')
    
    # 测试同步函数异常处理
    result = test_sync_function()
    print(f'Sync function with exception: {result}')
    
    # 测试同步函数正常执行
    result = test_sync_normal()
    print(f'Sync function normal: {result}')
    
    # 测试特定异常捕获
    result = test_specific_exception()
    print(f'Specific exception handling: {result}')
    
    # 测试自定义错误消息
    result = test_custom_message()
    print(f'Custom message handling: {result}')
    
    # 测试 handle_exception 函数
    result = test_handle_exception()
    print(f'Handle exception function: {result}')
    
    # 测试不记录堆栈信息
    result = test_no_traceback()
    print(f'No traceback logging: {result}')
    
    # 测试异步函数异常处理
    result = await test_async_function()
    print(f'Async function with exception: {result}')
    
    # 测试异步函数正常执行
    result = await test_async_normal()
    print(f'Async function normal: {result}')
    
    # 测试异常重抛
    try:
        test_reraise_exception()
    except ValueError as e:
        print(f'Exception re-raised as expected: {e}')
    
    print('All tests completed!')


if __name__ == '__main__':
    asyncio.run(main())