# !/usr/bin/env python3
"""
==============================================================
Description  : Redis客户端管理模块 - 提供同步和异步Redis客户端的统一管理功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-09-05 09:48:11
LastEditTime : 2025-09-18 20:00:00
FilePath     : /CODE/xjlib/xt_database/redis_client.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能:
- RedisManager: Redis客户端管理器类，支持同步和异步客户端管理
- create_redis_client: 创建Redis客户端的快捷函数，支持从DB_CFG获取配置
- 统一的参数验证和错误处理机制

主要特性:
- 支持同步和异步Redis客户端的统一管理
- 自动处理事件循环创建和管理
- 完善的参数验证和错误处理
- 详细的日志记录，便于调试和监控
==============================================================
"""

from __future__ import annotations

import asyncio
from typing import Any

from redis import Redis, asyncio as aioredis
from xt_database.cfg import DB_CFG
from xt_wraps import LogCls

logger = LogCls()


class RedisManager:
    """Redis客户端管理器 - 提供同步和异步Redis客户端的统一管理

    该类负责管理Redis客户端的生命周期，包括创建、维护和测试连接。
    支持同步和异步两种客户端模式，并提供统一的接口进行操作。

    Attributes:
        client: Redis客户端实例，可以是同步或异步类型
    """

    client: Redis | aioredis.Redis | None = None

    def __init__(self, host: str, port: int, db: int, max_connections: int | None = None, **kwargs: Any) -> None:
        """
        初始化RedisManager实例

        Args:
            host: Redis服务器主机地址
            port: Redis服务器端口号
            db: 要连接的数据库编号
            max_connections: 最大连接数，默认为None（不限制连接数）
            **kwargs: 传递给Redis客户端的其他参数

        Notes:
            1. 初始化时不会自动创建客户端连接
            2. 推荐通过create_redis_client快捷函数创建实例
            3. 获取或创建事件循环，确保异步操作能够正确执行
        """
        self.host = host
        self.port = port
        self.db = db
        self.max_connections = max_connections
        self.kwargs = kwargs

        # 获取或创建事件循环，参考syncaiomysql.py的模式
        try:
            self.loop = asyncio.get_running_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

    @classmethod
    def init_redis_client(
        cls,
        async_client: bool = False,
        host: str = 'localhost',
        port: int = 6379,
        db: int = 0,
        max_connections: int | None = None,
        **kwargs: Any,
    ) -> Redis | aioredis.Redis:
        """
        初始化Redis客户端

        该方法创建并返回一个Redis客户端实例，可以是同步或异步类型。
        初始化后的客户端会保存在类属性中，方便后续使用。

        Args:
            async_client: 是否使用异步客户端，默认为False（同步客户端）
            host: Redis服务器的主机名，默认为'localhost'
            port: Redis服务器的端口，默认为6379
            db: 要连接的数据库编号，默认为0
            max_connections: 最大连接数，默认为None（不限制连接数）
            **kwargs: 传递给Redis客户端的其他参数

        Returns:
            Redis | aioredis.Redis: 初始化后的Redis客户端实例
        """
        redis_method = aioredis.Redis if async_client else Redis

        cls.client = redis_method(
            host=host,
            port=port,
            db=db,
            max_connections=max_connections,
            **kwargs,
        )

        logger.info(f'▶️ Redis客户端初始化成功: 异步={async_client}, 主机={host}, 端口={port}, 数据库={db}')
        return cls.client

    async def _async_ping(self) -> bool:
        """异步Ping测试Redis连接

        测试异步Redis客户端的连接是否正常。

        Returns:
            bool: 连接是否正常
        """
        if not self.client or not isinstance(self.client, aioredis.Redis):
            return False
        return await self.client.ping()

    def ping(self) -> bool:
        """同步Ping测试Redis连接

        测试Redis客户端的连接是否正常，根据客户端类型自动选择同步或异步方式。

        Returns:
            bool: 连接是否正常
        """
        if not self.client:
            return False

        # 异步客户端处理
        if isinstance(self.client, aioredis.Redis):
            # 使用run_until_loop执行异步ping
            result = [False]  # 使用列表作为可变容器存储结果

            async def ping_task():
                try:
                    result[0] = await self._async_ping()
                except Exception as e:
                    logger.error(f'❌ 异步Ping失败: {e!s}')
                    result[0] = False

            try:
                self.run_until_loop([ping_task()])
            except Exception as e:
                logger.error(f'❌ 运行异步Ping任务失败: {e!s}')

            return result[0]

        # 同步客户端直接ping
        try:
            return self.client.ping()
        except Exception as e:
            logger.error(f'❌ 同步Ping失败: {e!s}')
            return False

    def run_until_loop(self, tasks: list[asyncio.Future | asyncio.Task | Any]) -> None:
        """运行异步任务直到完成

        根据事件循环的状态，选择合适的方式执行异步任务。

        Args:
            tasks: 异步任务列表

        Notes:
            1. 如果事件循环正在运行，使用create_task创建任务并保存引用
            2. 如果事件循环未运行，使用run_until_complete执行任务
        """
        created_tasks = []  # 保存创建的任务引用，避免RUF006警告
        for task in tasks:
            if self.loop.is_running():
                # 如果循环正在运行，使用create_task并保存引用
                created_tasks.append(asyncio.create_task(task))
            else:
                # 如果循环未运行，使用run_until_complete
                self.loop.run_until_complete(task)


# 快捷函数 - 提供更简便的Redis客户端创建方式
def create_redis_client(db_key: str = 'redis', async_client: bool = False, max_connections: int | None = None, **kwargs: Any) -> Redis | aioredis.Redis:
    """
    创建Redis客户端的快捷函数

    从DB_CFG配置中获取Redis连接信息，创建并返回一个Redis客户端实例。
    支持同步和异步两种客户端模式，便于在不同场景下使用。

    Args:
        db_key: 数据库配置键名，用于从DB_CFG中获取对应的Redis配置，默认为'redis'
        async_client: 是否使用异步客户端，默认为False（同步客户端）
        max_connections: 最大连接数，默认为None（不限制连接数）
        **kwargs: 传递给Redis客户端的其他参数

    Returns:
        Redis | aioredis.Redis: 初始化后的Redis客户端实例

    Raises:
        ValueError:
            - 当db_key参数不是字符串类型时抛出
            - 当DB_CFG中不存在指定的配置键时抛出
        Exception: 当创建客户端失败时抛出

    Example:
        >>> # 使用默认Redis配置创建同步客户端
        >>> redis = create_redis_client()
        >>> # 使用默认Redis配置创建异步客户端
        >>> redis_async = create_redis_client(async_client=True)
        >>> # 使用指定配置创建客户端
        >>> custom_redis = create_redis_client('custom_redis')

    Notes:
        1. 使用DB_CFG中的配置创建Redis客户端，避免硬编码连接信息
        2. 支持同步和异步两种客户端模式
        3. 配置文件应包含host、port、db等必要信息
    """
    # 参数类型验证
    if not isinstance(db_key, str):
        raise ValueError(f'❌ 配置键非字符串类型: [{type(db_key).__name__}]')

    # 配置键存在性检查
    if not hasattr(DB_CFG, db_key):
        raise ValueError(f'❌ DB_CFG数据库配置中 [{db_key}] 不存在')

    # 获取配置并创建客户端
    try:
        cfg = DB_CFG[db_key].value.copy()
        # 移除不需要的字段
        cfg.pop('type', None)

        logger.info(f'▶️ 正在创建Redis客户端，配置键: {db_key}, 异步模式: {async_client}')

        # 合并额外参数
        client_kwargs = cfg.copy()
        if max_connections is not None:
            client_kwargs['max_connections'] = max_connections
        client_kwargs.update(kwargs)

        # 创建客户端
        redis_method = aioredis.Redis if async_client else Redis
        client = redis_method(**client_kwargs)

        logger.info(f'✅ Redis客户端创建成功: 主机={client_kwargs.get("host")}, 端口={client_kwargs.get("port")}, 数据库={client_kwargs.get("db")}')
        return client
    except Exception as err:
        logger.error(f'❌ 创建Redis客户端失败: {err!s}')
        raise Exception(f'❌ Redis客户端创建失败: {err!s}') from err


async def main() -> None:
    """主函数 - 测试Redis客户端的基本功能"""
    # 测试同步客户端
    try:
        sync_redis = create_redis_client()
        sync_redis.set('test_key', 'test_value')
        logger.info(f'同步客户端: {sync_redis}')
        result = sync_redis.get('test_key')
        logger.info(f'同步操作结果: {result}')
        # 测试RedisManager类的ping方法
        manager = RedisManager('localhost', 6379, 4)
        manager.client = sync_redis
        ping_result = manager.ping()
        logger.info(f'同步客户端Ping测试结果: {ping_result}')
        sync_redis.close()
    except Exception as e:
        logger.error(f'❌ 同步客户端测试失败: {e!s}')
        import traceback
        traceback.print_exc()

    # 测试异步客户端
    try:
        async_redis = create_redis_client(async_client=True)
        logger.info(f'异步客户端: {async_redis}')
        await async_redis.set('async_key', 'async_value')
        result = await async_redis.get('async_key')
        logger.info(f'异步操作结果: {result}')

        # 测试异步ping - 直接使用异步方法
        ping_result = await async_redis.ping()
        logger.info(f'直接异步Ping测试结果: {ping_result}')

        # 使用aclose()代替close()，避免弃用警告
        await async_redis.aclose()
    except Exception as e:
        logger.error(f'❌ 异步客户端测试失败: {e!s}')
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    """示例代码，展示Redis客户端的使用方式"""
    try:
        # 获取或创建事件循环，参考syncaiomysql.py的模式
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        loop.run_until_complete(main())
        loop.close()
    except Exception as e:
        logger.error(f'❌ 测试运行失败: {e!s}')
        import traceback
        traceback.print_exc()
