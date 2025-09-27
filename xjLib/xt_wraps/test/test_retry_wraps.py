"""
测试 retry_wraps 装饰器
"""
from __future__ import annotations

import asyncio

from xt_wraps import retry_wraps


# 测试同步函数重试
@retry_wraps(max_attempts=3, min_wait=0.1, max_wait=0.2)
def test_sync_retry():
    """测试同步函数重试"""
    print('Sync function called, raising exception...')
    raise ConnectionError('Network error for testing')


# 测试同步函数正常执行
@retry_wraps()
def test_sync_normal():
    """测试同步函数正常执行"""
    return 'Sync function success'


# 测试异步函数重试
@retry_wraps(max_attempts=3, min_wait=0.1, max_wait=0.2)
async def test_async_retry():
    """测试异步函数重试"""
    print('Async function called, raising exception...')
    raise ConnectionError('Network error for testing')


# 测试异步函数正常执行
@retry_wraps()
async def test_async_normal():
    """测试异步函数正常执行"""
    return 'Async function success'


# 测试自定义异常类型
@retry_wraps(retry_exceptions=(ValueError,), max_attempts=2)
def test_custom_exception():
    """测试自定义异常类型"""
    print('Custom exception function called, raising ValueError...')
    raise ValueError('Value error for testing')


# 测试默认返回值
@retry_wraps(default_return='default_result', max_attempts=2)
def test_default_return():
    """测试默认返回值"""
    print('Default return function called, raising exception...')
    raise RuntimeError('Runtime error for testing')


async def main():
    """主测试函数"""
    print('Testing retry_wraps decorator...')
    
    # 测试同步函数正常执行
    result = test_sync_normal()
    print(f'Sync normal result: {result}')
    
    # 测试异步函数正常执行
    result = await test_async_normal()
    print(f'Async normal result: {result}')
    
    # 测试同步函数重试（会失败并记录日志）
    try:
        result = test_sync_retry()
        print(f'Sync retry result: {result}')
    except Exception as e:
        print(f'Sync retry exception: {e}')
    
    # 测试异步函数重试（会失败并记录日志）
    try:
        result = await test_async_retry()
        print(f'Async retry result: {result}')
    except Exception as e:
        print(f'Async retry exception: {e}')
    
    # 测试自定义异常类型
    try:
        result = test_custom_exception()
        print(f'Custom exception result: {result}')
    except Exception as e:
        print(f'Custom exception error: {e}')
    
    # 测试默认返回值
    result = test_default_return()
    print(f'Default return result: {result}')
    
    print('All tests completed!')


if __name__ == '__main__':
    asyncio.run(main())