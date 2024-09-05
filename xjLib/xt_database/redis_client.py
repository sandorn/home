# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-09-05 09:48:11
LastEditTime : 2024-09-05 09:58:44
FilePath     : /CODE/xjLib/xt_database/redis_client.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from typing import Optional, Union

from redis import Redis
from redis import asyncio as aioredis


class RedisManager:
    """Redis客户端管理器"""

    client: Union[Redis, aioredis.Redis, None] = None

    @classmethod
    def init_redis_client(
        cls,
        async_client: bool = False,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        max_connections: Optional[int] = None,
        **kwargs,
    ):
        """
        初始化 Redis 客户端。

        Args:
            async_client (bool): 是否使用异步客户端，默认为 False（同步客户端）
            host (str): Redis 服务器的主机名，默认为 'localhost'
            port (int): Redis 服务器的端口，默认为 6379
            db (int): 要连接的数据库编号，默认为 0
            max_connections (Optional[int]): 最大连接数。默认为 None（不限制连接数）
            **kwargs: 传递给 Redis 客户端的其他参数

        Returns:
            None
        """
        redis_method = aioredis.Redis if async_client else Redis

        if cls.client is None:
            cls.client = redis_method(
                host=host,
                port=port,
                db=db,
                max_connections=max_connections,
                **kwargs,
            )


if __name__ == "__main__":
    RedisManager.init_redis_client()
    print(RedisManager.client)
    RedisManager.init_redis_client(async_client=True)
    print(RedisManager.client)
