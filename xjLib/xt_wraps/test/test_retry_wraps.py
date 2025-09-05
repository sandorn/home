# !/usr/bin/env python
import asyncio

from xt_wraps.retry import retry_wraps


# 测试成功的同步函数
@retry_wraps()
def success_sync_func():
    print("成功的同步函数执行")
    return "同步函数成功结果"


# 测试成功的异步函数
@retry_wraps()
async def success_async_func():
    print("成功的异步函数执行")
    return "异步函数成功结果"


# 测试会失败但重试后成功的同步函数
@retry_wraps(max_attempts=4)
def eventually_success_sync_func():
    # 这是一个闭包变量，用来记录尝试次数
    if not hasattr(eventually_success_sync_func, "attempts"):
        eventually_success_sync_func.attempts = 0
    eventually_success_sync_func.attempts += 1
    print(f"尝试同步函数第 {eventually_success_sync_func.attempts} 次")
    if eventually_success_sync_func.attempts < 3:
        raise ValueError(f"故意失败第 {eventually_success_sync_func.attempts} 次")
    return "同步函数最终成功"


# 测试会失败但重试后成功的异步函数
@retry_wraps(max_attempts=4)
async def eventually_success_async_func():
    # 这是一个闭包变量，用来记录尝试次数
    if not hasattr(eventually_success_async_func, "attempts"):
        eventually_success_async_func.attempts = 0
    eventually_success_async_func.attempts += 1
    print(f"尝试异步函数第 {eventually_success_async_func.attempts} 次")
    if eventually_success_async_func.attempts < 3:
        raise ValueError(f"故意失败第 {eventually_success_async_func.attempts} 次")
    return "异步函数最终成功"


# 测试始终失败的同步函数
@retry_wraps(max_attempts=2)
def always_fail_sync_func():
    print("失败的同步函数执行")
    raise RuntimeError("同步函数始终失败")

# 测试始终失败的异步函数
@retry_wraps(max_attempts=2)
async def always_fail_async_func():
    print("失败的异步函数执行")
    raise RuntimeError("异步函数始终失败")

# 测试不重试特定异常的函数
@retry_wraps
def specific_exception_func(x, y):
    print(f"计算 {x} / {y}")
    if y == 0:
        raise ZeroDivisionError("除数不能为零")
    if y == 1:
        raise ValueError("y不能为1")  # 这个异常会被重试
    return x / y

async def main():
    print("\n===== 测试成功的同步函数 ======")
    try:
        result = success_sync_func()
        print(f"结果: {result}")
    except Exception as e:
        print(f"意外错误: {e}")

    print("\n===== 测试成功的异步函数 ======")
    try:
        result = await success_async_func()
        print(f"结果: {result}")
    except Exception as e:
        print(f"意外错误: {e}")

    print("\n===== 测试最终成功的同步函数 ======")
    try:
        result = eventually_success_sync_func()
        print(f"结果: {result}")
    except Exception as e:
        print(f"错误: {e}")

    print("\n===== 测试最终成功的异步函数 ======")
    try:
        result = await eventually_success_async_func()
        print(f"结果: {result}")
    except Exception as e:
        print(f"错误: {e}")

    print("\n===== 测试始终失败的同步函数 ======")
    try:
        result = always_fail_sync_func()
        print(f"结果: {result}")
    except Exception as e:
        print(f"预期的错误: {e}")

    print("\n===== 测试始终失败的异步函数 ======")
    try:
        result = await always_fail_async_func()
        print(f"结果: {result}")
    except Exception as e:
        print(f"预期的错误: {e}")

    print("\n===== 测试不重试特定异常的函数 ======")
    try:
        result = specific_exception_func(10, 0)  # 这个应该不重试
        print(f"结果: {result}")
    except Exception as e:
        print(f"预期不重试的错误: {type(e).__name__}: {e}")

    try:
        result = specific_exception_func(10, 1)  # 这个应该重试
        print(f"结果: {result}")
    except Exception as e:
        print(f"预期重试后的错误: {type(e).__name__}: {e}")

    try:
        result = specific_exception_func(10, 2)  # 这个应该成功
        print(f"结果: {result}")
    except Exception as e:
        print(f"意外错误: {e}")

if __name__ == "__main__":
    asyncio.run(main())

    # 测试同步函数 - 不重试异常，应返回默认值
    @retry_wraps(default_return="999")
    def test_sync_no_retry():
        raise ValueError("raise by test_func")
        # return "同步函数成功"

    print("11111111|同步函数测试(不重试):", test_sync_no_retry())  # 输出 999

    # 测试同步函数 - 重试异常，重试结束后应返回默认值
    @retry_wraps(default_return="888", max_attempts=3)
    def test_sync_retry():
        raise TimeoutError("超时错误")
        # return "同步函数成功"

    print("22222222|同步函数测试(重试):", test_sync_retry())  # 输出 888

    # 测试异步函数 - 不重试异常，应返回默认值
    @retry_wraps(default_return="777")
    async def test_async_no_retry():
        raise ValueError("异步随机失败")
        # return "异步函数成功"

    print(
        "33333333|异步函数测试(不重试):", asyncio.run(test_async_no_retry())
    )  # 输出 777

    # 测试异步函数 - 重试异常，重试结束后应返回默认值
    @retry_wraps(default_return="666", max_attempts=3)
    async def test_async_retry():
        raise TimeoutError("异步超时错误")
        # return "异步函数成功"

    print("44444444|异步函数测试(重试):", asyncio.run(test_async_retry()))  # 输出 666
