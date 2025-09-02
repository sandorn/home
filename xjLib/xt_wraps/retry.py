import asyncio
from functools import wraps
from typing import Any, Callable, Tuple, Type

from tenacity import (
    RetryCallState,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random,
)
from xt_wraps.log import create_basemsg, mylog


class RetryHandler:
    # 只重试异常
    RETRY_EXCEPT = (
        # 网络连接异常
        TimeoutError,  # 超时错误
        ConnectionError,  # 连接错误
        ConnectionRefusedError,  # 连接被拒绝
        ConnectionResetError,  # 连接被重置
        ConnectionAbortedError,  # 连接被中止
        # 操作系统级I/O异常
        OSError,  # 操作系统错误（包括许多网络错误）
        # HTTP相关异常
        # HTTPError,  # HTTP错误（如404、500等）
        # TooManyRedirects,  # 重定向过多
        # # SSL/TLS相关异常
        # SSLError,  # SSL错误
        # SSLZeroReturnError,  # SSL连接被关闭
        # SSLWantReadError,  # SSL需要读取更多数据
        # SSLWantWriteError,  # SSL需要写入更多数据
        # SSLSyscallError,  # SSL系统调用错误
        # SSLEOFError,  # SSL EOF错误
        # # DNS相关异常
        # gaierror,  # 地址信息错误（DNS解析失败）
        # # 代理相关异常
        # ProxyError,  # 代理错误
        # # 请求库特定异常（如requests）
        # requests.exceptions.Timeout,
        # requests.exceptions.ConnectionError,
        # requests.exceptions.HTTPError,
        # requests.exceptions.ChunkedEncodingError,
        # requests.exceptions.ContentDecodingError,
        # # 异步HTTP客户端异常（如aiohttp）
        # aiohttp.ClientError,
        # aiohttp.ClientConnectionError,
        # aiohttp.ClientResponseError,
        # aiohttp.ClientPayloadError,
        # aiohttp.ServerTimeoutError,
        # aiohttp.ServerDisconnectedError,
        # # 其他可能的重试异常
        # BrokenPipeError,  # 管道破裂错误
        # TemporaryFailure,  # 临时故障（SMTP相关）
    )

    _basemsg: str = ""
    _default_return: Any = None

    @classmethod
    def configure(cls, basemsg: str, default_return: Any) -> None:
        """配置RetryHandler"""
        cls._basemsg = basemsg
        cls._default_return = default_return

    @classmethod
    def err_back(cls, retry_state: RetryCallState) -> Any:
        """错误回调，返回默认值"""
        ex = retry_state.outcome.exception()
        if ex:
            mylog.error(
                f"{cls._basemsg} | RetryHandler | 共 {retry_state.attempt_number} 次失败，最后错误: {ex}"
            )
        else:
            mylog.error(f"{cls._basemsg} | RetryHandler | 其他异常: {ex}")
        return cls._default_return

    @classmethod
    def before_back(cls, retry_state: RetryCallState) -> None:
        """重试前回调"""
        ex = retry_state.outcome.exception()
        if ex:
            mylog.error(
                f"{cls._basemsg} | RetryRaise | 第 {retry_state.attempt_number} 次失败, 异常: {ex}"
            )

    @classmethod
    def should_retry(cls, exception: Exception) -> bool:
        """判断是否应该重试异常"""
        return any(isinstance(exception, exc_type) for exc_type in cls.RETRY_EXCEPT)


def retry_wraps(
    fn: Callable[..., Any] = None,
    max_attempts: int = 3,
    min_wait: float = 0,
    max_wait: float = 1,
    retry_exceptions: Tuple[Type[Exception], ...] = RetryHandler.RETRY_EXCEPT,
    is_before_callback: bool = True,
    is_error_callback: bool = True,
    silent_on_no_retry: bool = True,
    default_return: Any = None,
) -> Callable:
    """
    重试装饰器 - 基于tenacity，支持同步和异步函数

    Args:
        max_attempts: 最大尝试次数
        min_wait: 最小等待时间(秒)
        max_wait: 最大等待时间(秒)
        retry_exceptions: 需要重试的异常类型元组
        is_before_callback: 是否在重试前调用回调
        is_error_callback: 是否在错误时调用回调
        silent_on_no_retry: 是否静默处理非重试异常（不抛出错误）
        default_return: 静默处理时的默认返回值
    """

    def decorator(func: Callable[..., Any]) -> Callable:
        # 设置基础消息和默认返回值
        basemsg = create_basemsg(func)
        RetryHandler.configure(basemsg, default_return)

        # 更新重试异常列表
        RetryHandler.RETRY_EXCEPT = retry_exceptions

        # 创建重试条件 - 只重试指定类型的异常
        retry_condition = retry_if_exception_type(retry_exceptions)

        # 配置tenacity的retry装饰器
        retry_decorator = retry(
            reraise=True,  # 保持为True，让异常传播到我们的包装器
            stop=stop_after_attempt(max_attempts),
            wait=wait_random(min=min_wait, max=max_wait),
            retry=retry_condition,
            before_sleep=RetryHandler.before_back if is_before_callback else None,
            retry_error_callback=RetryHandler.err_back if is_error_callback else None,
        )

        # 同步函数包装器
        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                # 使用retry_decorator包装函数调用
                # #raise：重试错误会重试足够次数，不重试错误只运行1次
                return retry_decorator(func)(*args, **kwargs)
            except Exception as e:
                if RetryHandler.should_retry(e):  # 检查是否重试异常
                    return default_return  # 重试异常在所有重试失败后返回默认值
                elif silent_on_no_retry:  # 检查是否静默处理非重试异常
                    return default_return  # 非重试异常返回默认值
                else:
                    raise  # 否则重新抛出异常

        # 异步函数包装器
        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                # 使用retry_decorator包装函数调用
                return await retry_decorator(func)(*args, **kwargs)
            except Exception as e:
                if RetryHandler.should_retry(e):  # 检查是否重试异常
                    return default_return  # 重试异常在所有重试失败后返回默认值
                elif silent_on_no_retry:  # 检查是否静默处理非重试异常
                    return default_return  # 非重试异常返回默认值
                else:
                    raise  # 否则重新抛出异常

        # 根据函数类型返回相应的包装器
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator(fn) if fn else decorator


if __name__ == "__main__":
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

    import asyncio

    print(
        "33333333|异步函数测试(不重试):", asyncio.run(test_async_no_retry())
    )  # 输出 777

    # 测试异步函数 - 重试异常，重试结束后应返回默认值
    @retry_wraps(default_return="666", max_attempts=3)
    async def test_async_retry():
        raise TimeoutError("异步超时错误")
        # return "异步函数成功"

    print("44444444|异步函数测试(重试):", asyncio.run(test_async_retry()))  # 输出 666
