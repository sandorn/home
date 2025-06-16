# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-07-18 14:39:12
FilePath     : /CODE/xjLib/xt_log.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os
import sys
from datetime import datetime
from functools import wraps
from typing import Callable

from loguru import logger

# 环境判断
IS_DEV = os.getenv("ENV", "dev").lower() == "dev"

# 日志过滤器
def dev_filter(record):
    return IS_DEV

# 初始化日志配置
logger.remove()  # 移除默认配置

# 文件日志（始终记录）
logger.add(
    f"{datetime.now().strftime('%Y%m%d')}.log",
    rotation="10 MB",
    retention="30 days",
    level="DEBUG",
    encoding="utf-8",
    filter=lambda r: r["level"].no >= 20,  # INFO及以上级别
)

# 控制台日志（仅开发环境）
if IS_DEV:
    logger.add(
        sys.stderr,
        level="DEBUG",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}",
    )

def log_decorator(func: Callable) -> Callable:
    """同步函数日志装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"Entering {func.__name__} with args={args}, kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.success(f"Exiting {func.__name__} with result={result}")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise

    return wrapper

def async_log_decorator(func: Callable) -> Callable:
    """异步函数日志装饰器"""

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        logger.debug(
            f"Entering async {func.__name__} with args={args}, kwargs={kwargs}"
        )
        try:
            result = await func(*args, **kwargs)
            logger.success(f"Exiting async {func.__name__} with result={result}")
            return result
        except Exception as e:
            logger.error(f"Error in async {func.__name__}: {str(e)}")
            raise

    return async_wrapper

if __name__ == "__main__":
    # from loguru import logger

    # # 不同级别的日志记录
    # logger.debug("调试信息：变量值检查")
    # logger.info("应用程序启动完成")
    # logger.warning("配置文件使用默认值")
    # logger.error("数据库连接失败")
    # logger.critical("系统内存不足")

    # # 新增的日志级别
    # logger.success("用户注册成功")
    # logger.trace("详细的执行轨迹信息")

    # # 带参数的日志记录
    # user_id = 12345
    # action = "登录"
    # logger.info("用户 {} 执行 {} 操作", user_id, action)
    # # 移除默认处理器
    # logger.remove()

    # # 添加文件日志处理器
    # logger.add(
    #     "application.log",
    #     format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
    #     level="INFO",
    #     rotation="10 MB",
    #     retention="30 days",
    #     compression="zip"
    # )
    # import sys
    # # 添加控制台输出
    # logger.add(
    #     sys.stderr,
    #     format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}",
    #     level="DEBUG"
    # )

    # logger.info("配置完成，开始记录日志")

    # 测试同步函数装饰器
    @log_decorator
    def sync_example(a, b):
        """同步函数示例"""
        return a + b

    # 测试异步函数装饰器
    @async_log_decorator
    async def async_example(x, y):
        """异步函数示例"""
        import asyncio

        await asyncio.sleep(0.1)
        return x * y

    # 测试异常捕获
    @log_decorator
    def error_example():
        """异常测试函数"""
        raise ValueError("测试异常")

    # 执行测试
    print("=== 同步函数测试 ===")
    result = sync_example(3, 4)
    print(f"同步函数结果: {result}")

    print("\n=== 异步函数测试 ===")
    import asyncio

    async_result = asyncio.run(async_example(5, 6))
    print(f"异步函数结果: {async_result}")

    print("\n=== 异常测试 ===")
    try:
        error_example()
    except Exception as e:
        print(f"捕获到预期异常: {type(e).__name__}: {e}")

    # 环境切换测试
    print("\n=== 环境切换测试 ===")
    os.environ["ENV"] = "prod"
    print("切换到生产环境后，控制台不应有日志输出")
    sync_example(1, 2)
    os.environ["ENV"] = "dev"  # 恢复开发环境
