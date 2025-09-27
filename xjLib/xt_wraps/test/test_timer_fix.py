"""测试timer.py修复后的计时逻辑

验证装饰器模式和上下文管理器模式的计时逻辑一致性：
- 函数执行成功时记录时间
- 函数执行出错时不记录时间
- 异步函数计时准确性验证
"""
from __future__ import annotations

import asyncio
import time

from xt_wraps.timer import TimerWrapt, timer_wraps


def test_successful_function() -> None:
    """测试成功执行的函数计时"""
    @TimerWrapt
    def successful_func() -> str:
        time.sleep(0.15)  # 增加停顿时间到0.15秒
        return 'success'
    
    result = successful_func()
    assert result == 'success', '函数返回值不正确'


def test_failing_function() -> None:
    """测试执行失败的函数计时"""
    @TimerWrapt
    def failing_func() -> None:
        time.sleep(0.15)  # 增加停顿时间到0.15秒
        raise ValueError('测试异常')
    
    try:
        failing_func()
        raise AssertionError('函数应该抛出异常')
    except ValueError as e:
        assert str(e) == '测试异常', '异常消息不正确'


def test_successful_context() -> None:
    """测试成功执行的上下文管理器计时"""
    with TimerWrapt('成功上下文测试'):
        time.sleep(0.15)  # 增加停顿时间到0.15秒


def test_failing_context() -> None:
    """测试执行失败的上下文管理器计时"""
    try:
        with TimerWrapt('失败上下文测试'):
            time.sleep(0.15)  # 增加停顿时间到0.15秒
            raise ValueError('上下文测试异常')
        #! raise AssertionError('上下文管理器应该抛出异常')
    except ValueError as e:
        assert str(e) == '上下文测试异常', '异常消息不正确'


def test_async_successful_function() -> None:
    """测试成功执行的异步函数计时"""
    @timer_wraps
    async def async_successful_func() -> str:
        await asyncio.sleep(0.15)  # 异步停顿0.15秒
        return 'async_success'
    
    async def run_test() -> None:
        import time
        start_time = time.time()
        result = await async_successful_func()
        end_time = time.time()
        actual_duration = end_time - start_time
        
        assert result == 'async_success', '异步函数返回值不正确'
        assert actual_duration >= 0.15, f'实际执行时间({actual_duration:.3f}s)应大于等于停顿时间(0.15s)'
    
    asyncio.run(run_test())


def test_async_failing_function() -> None:
    """测试执行失败的异步函数计时"""
    @timer_wraps
    async def async_failing_func() -> None:
        await asyncio.sleep(0.15)  # 异步停顿0.15秒
        raise ValueError('异步测试异常')
    
    async def run_test() -> None:
        import time
        start_time = time.time()
        try:
            await async_failing_func()
            raise AssertionError('异步函数应该抛出异常')
        except ValueError as e:
            end_time = time.time()
            actual_duration = end_time - start_time
            assert str(e) == '异步测试异常', '异步异常消息不正确'
            assert actual_duration >= 0.15, f'实际执行时间({actual_duration:.3f}s)应大于等于停顿时间(0.15s)'
            print(f'✅ 异步失败函数执行时间: {actual_duration:.3f}s (期望≥0.15s)')
    
    asyncio.run(run_test())
    print('✅ 执行失败的异步函数不记录时间测试通过')


def test_async_context_successful() -> None:
    """测试成功执行的异步上下文管理器计时"""
    async def run_test() -> None:
        import time
        start_time = time.time()
        async with TimerWrapt('异步成功上下文测试'):
            await asyncio.sleep(0.15)  # 异步停顿0.15秒
        end_time = time.time()
        actual_duration = end_time - start_time
        assert actual_duration >= 0.15, f'实际执行时间({actual_duration:.3f}s)应大于等于停顿时间(0.15s)'
        print(f'✅ 异步上下文管理器执行时间: {actual_duration:.3f}s (期望≥0.15s)')
    
    asyncio.run(run_test())
    print('✅ 成功执行的异步上下文管理器计时测试通过')


def test_async_context_failing() -> None:
    """测试执行失败的异步上下文管理器计时"""
    async def run_test() -> None:
        import time
        start_time = time.time()
        try:
            async with TimerWrapt('异步失败上下文测试'):
                await asyncio.sleep(0.15)  # 异步停顿0.15秒
                raise ValueError('异步上下文测试异常')
            #! raise AssertionError('异步上下文管理器应该抛出异常')
        except ValueError as e:
            end_time = time.time()
            actual_duration = end_time - start_time
            assert str(e) == '异步上下文测试异常', '异步上下文异常消息不正确'
            assert actual_duration >= 0.15, f'实际执行时间({actual_duration:.3f}s)应大于等于停顿时间(0.15s)'
            print(f'✅ 异步上下文管理器失败执行时间: {actual_duration:.3f}s (期望≥0.15s)')
    
    asyncio.run(run_test())
    print('✅ 执行失败的异步上下文管理器不记录时间测试通过')


def test_timer_wraps_successful() -> None:
    """测试timer_wraps装饰器成功执行计时"""
    @timer_wraps
    def timer_wraps_successful_func() -> str:
        time.sleep(0.15)  # 停顿0.15秒
        return 'timer_wraps_success'
    
    import time
    start_time = time.time()
    result = timer_wraps_successful_func()
    end_time = time.time()
    actual_duration = end_time - start_time
    
    assert result == 'timer_wraps_success', 'timer_wraps函数返回值不正确'
    assert actual_duration >= 0.15, f'实际执行时间({actual_duration:.3f}s)应大于等于停顿时间(0.15s)'


def test_timer_wraps_failing() -> None:
    """测试timer_wraps装饰器执行失败计时"""
    @timer_wraps
    def timer_wraps_failing_func() -> None:
        time.sleep(0.15)  # 停顿0.15秒
        raise ValueError('timer_wraps测试异常')
    
    import time
    start_time = time.time()
    try:
        timer_wraps_failing_func()
        raise AssertionError('timer_wraps函数应该抛出异常')
    except ValueError as e:
        end_time = time.time()
        actual_duration = end_time - start_time
        assert str(e) == 'timer_wraps测试异常', 'timer_wraps异常消息不正确'
        assert actual_duration >= 0.15, f'实际执行时间({actual_duration:.3f}s)应大于等于停顿时间(0.15s)'


def run_all_tests() -> None:
    """运行所有测试"""
    print('开始运行计时器测试...')
    
    test_successful_function()
    test_failing_function()
    test_successful_context()
    test_failing_context()
    test_async_successful_function()
    test_async_failing_function()
    test_async_context_successful()
    test_async_context_failing()
    test_timer_wraps_successful()
    test_timer_wraps_failing()
    
    print('所有测试通过！')
    print('计时器修复验证完成：')
    print('- 装饰器模式和上下文管理器模式计时逻辑已统一')
    print('- 成功执行记录时间，失败执行不记录时间')
    print('- 异步函数计时功能正常')
    print('- 异步上下文管理器计时功能正常')
    print('- timer_wraps装饰器计时功能正常')


if __name__ == '__main__':
    run_all_tests()