# !/usr/bin/env python3
"""
==============================================================
Description  : Python标准模块模板
Develop      : VSCode
Author       : sandorn sandorn@live.cn
LastEditTime : 2025-09-27 10:00:00
Github       : https://github.com/sandorn/home

本模块提供以下核心功能:
- 标准Python模块结构示例
- 类定义规范示例
- 函数定义规范示例

主要特性:
- 符合PEP 8规范
- 完整类型注解
- Google风格文档字符串
- 标准日志使用方式
==============================================================
"""

from __future__ import annotations

from typing import Any

from xt_log import mylog


class TemplateClass:
    """标准类模板 - 演示规范的类定义方式

    Args:
        name: 名称参数（类型：str，必填）
        value: 数值参数（类型：int，默认值：0）

    Attributes:
        name: 名称属性
        value: 数值属性

    Raises:
        TypeError: 当参数类型不正确时抛出
    """
    
    def __init__(self, name: str, value: int = 0) -> None:
        # 使用Guard Clause提前检查参数类型
        if not isinstance(name, str):
            raise TypeError('参数name必须是字符串类型')
        if not isinstance(value, int):
            raise TypeError('参数value必须是整数类型')
            
        self.name: str = name
        self.value: int = value

    def process_data(self, data: str) -> dict[str, Any]:
        """处理数据方法

        Args:
            data: 输入数据字符串

        Returns:
            dict[str, Any]: 处理结果字典

        Raises:
            TypeError: 当参数类型不正确时抛出
        """
        if not isinstance(data, str):
            raise TypeError('参数data必须是字符串类型')

        result: dict[str, Any] = {
            'status': 'success',
            'name': self.name,
            'value': self.value,
            'processed_data': f'processed_{data}'
        }
        
        mylog.info(f'处理数据: {data}')
        return result

    async def async_process(self, data: str) -> bool:
        """异步处理方法

        Args:
            data: 输入数据字符串

        Returns:
            bool: 处理状态
        """
        if not isinstance(data, str):
            raise TypeError('参数data必须是字符串类型')
            
        mylog.debug(f'异步处理: {data}')
        return True


def utility_function(input_data: str | int) -> list[str]:
    """工具函数示例

    Args:
        input_data: 输入数据，可以是字符串或整数

    Returns:
        list[str]: 处理后的字符串列表

    Raises:
        TypeError: 当参数类型不正确时抛出
    """
    if not isinstance(input_data, (str, int)):
        raise TypeError('参数input_data必须是字符串或整数')

    result: list[str] = ['processed', str(input_data)]
    mylog.info(f'工具函数处理: {input_data}')
    return result


def simple_decorator(func: Any) -> Any:
    """简单装饰器示例

    Args:
        func: 被装饰的函数

    Returns:
        Any: 包装后的函数
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        mylog.debug(f'调用函数: {func.__name__}')
        result = func(*args, **kwargs)
        mylog.debug(f'函数返回: {result}')
        return result
    
    return wrapper


# 使用示例
if __name__ == '__main__':
    """模块功能测试"""

    mylog.info('开始模块功能测试')
    
    try:
        # 示例1: 创建类实例并调用方法
        instance = TemplateClass('demo', 42)
        result = instance.process_data('test_data')
        mylog.info(f'方法调用结果: {result}')
        
        # 示例2: 使用工具函数
        result = utility_function('input_string')
        mylog.info(f'工具函数结果: {result}')
        
        # 示例3: 装饰器测试
        @simple_decorator
        def test_func(x: int) -> int:
            return x * 2
            
        result = test_func(5)
        mylog.info(f'装饰器测试结果: {result}')
        
        mylog.success('所有测试完成')
        
    except Exception as e:
        mylog.error(f'测试过程中出错: {e}')
    
    mylog.info('模块功能测试结束')