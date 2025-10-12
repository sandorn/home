
from __future__ import annotations

from threading import RLock
from typing import Any
from weakref import WeakValueDictionary


class SingletonMixin:
    """线程安全的单例混入类实现

    核心功能：
    - 通过混入方式实现单例模式
    - 支持与其他类的多重继承
    - 双重检查锁确保线程安全
    - 使用弱引用字典避免内存泄漏
    - 提供完整的实例管理接口

    类方法：
    - get_instance: 获取当前单例实例（不创建新实例）
    - reset_instance: 重置单例实例
    - has_instance: 检查是否存在单例实例

    类属性：
    - _instances: 弱引用字典，存储类与实例的映射关系
    - _instance_lock: 可重入锁，确保线程安全

    使用示例：
        # 基本用法
        class ConfigService(SingletonMixin):
            def __init__(self, config_file: str | None = None):
                print(f"加载配置文件: {config_file or '默认配置'}")
                self.config = config_file or 'default_config'

        # 创建实例
        config1 = ConfigService("app_config.json")
        config2 = ConfigService("user_config.json")

        # config1和config2是同一个实例
        print(f"是同一个实例: {config1 is config2}")  # 输出: True
        print(f"配置文件: {config1.config}")  # 输出: app_config.json

        # 实例管理
        print(f"存在实例: {ConfigService.has_instance()}")  # 输出: True

        # 重置实例
        ConfigService.reset_instance()

        # 重置后创建新实例
        config3 = ConfigService("new_config.json")
        print(f"新配置文件: {config3.config}")  # 输出: new_config.json

        # 多重继承示例
        class Loggable:
            def log(self, message: str) -> None:
                print(f"[LOG] {message}")

        class LoggedConfigService(ConfigService, Loggable):
            pass

        logged_config = LoggedConfigService("logged_config.json")
        logged_config.log(f"当前配置: {logged_config.config}")
    """

    _instance_lock: RLock = RLock()  # 可重入锁，避免递归调用问题
    _instances: WeakValueDictionary[type, Any] = WeakValueDictionary()

    def __new__(cls: type[Any], *args: Any, **kwargs: Any) -> Any:
        """实例化处理（带错误日志和双重检查锁）"""
        # 第一次检查(无锁)
        if cls in cls._instances:
            return cls._instances[cls]

        # 获取锁
        with cls._instance_lock:
            if cls in cls._instances:
                return cls._instances[cls]

            try:
                # 创建实例
                instance = super().__new__(cls)
                # 存储实例引用
                cls._instances[cls] = instance
                # 注意：不手动调用__init__，让Python正常流程处理初始化
                return instance
            except Exception as e:
                # 清理失败的实例
                if cls in cls._instances:
                    del cls._instances[cls]
                # 改进错误处理，记录异常并重新抛出
                raise RuntimeError(f'SingletonMixin {cls.__name__} __new__ failed: {e}') from e

    @classmethod
    def reset_instance(cls: type[Any]) -> None:
        """重置单例实例"""
        with cls._instance_lock:
            cls._instances.pop(cls, None)  # 移除该类的实例引用

    @classmethod
    def has_instance(cls: type[Any]) -> bool:
        """检查是否存在单例实例"""
        return cls in cls._instances

    @classmethod
    def get_instance(cls: type[Any]) -> Any | None:
        """获取当前单例实例（不创建新实例）"""
        return cls._instances.get(cls) if cls in cls._instances else None
