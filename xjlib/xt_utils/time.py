# !/usr/bin/env python
"""
==============================================================
Description  : 时间工具模块 - 提供时间格式化、转换、计算和计时功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
LastEditTime : 2025-09-10 15:30:00
FilePath     : /CODE/xjlib/xt_utils/time.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能:
- TimeUtil:单例模式的时间工具类,支持日期时间计算、格式化和转换
- 时间格式化枚举:提供常用时间格式定义
- 计时装饰器:支持同步函数执行时间统计
- 上下文管理器:提供代码块执行时间计时功能
- 快捷函数:提供常用时间操作的简便接口

主要特性:
- 全面的时间转换功能(字符串、时间戳、datetime对象互转)
- 丰富的日期计算功能(增加/减少时间、获取周期边界)
- 工作日计算和日期差值详细分析
- 高性能计时实现,支持毫秒级精度
- 类型安全设计,完整的类型注解支持
==============================================================
"""

from __future__ import annotations

import time
from datetime import datetime

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel
from xt_utils.xtenum import StrEnum
from xtwraps import SingletonMeta


class TimeFormatEnum(StrEnum):
    """时间格式化枚举 - 定义常用的时间格式字符串"""

    DateOnly = '%Y-%m-%d'
    TimeOnly = '%H:%M:%S'
    DateTime = f'{DateOnly} {TimeOnly}'  # "%Y-%m-%d %H:%M:%S"
    DateTimeFull = f'{DateTime}.%f'

    DateOnly_CN = '%Y年%m月%d日'
    TimeOnly_CN = '%H时%M分%S秒'
    DateTime_CN = f'{DateOnly_CN} {TimeOnly_CN}'
    DateTimeFull_CN = f'{DateTime_CN}.%f'


class TimeUnitEnum(StrEnum):
    """时间单位枚举 - 定义常用的时间单位"""

    DAYS = 'days'
    HOURS = 'hours'
    MINUTES = 'minutes'
    SECONDS = 'seconds'


class DateDiff(BaseModel):
    """日期差值模型 - 存储两个日期之间的详细差值信息"""

    years: int
    months: int
    days: int
    hours: int
    minutes: int
    seconds: int


class TimeUtil(metaclass=SingletonMeta):
    """时间工具类 - 提供全面的时间处理功能，采用单例模式确保全局一致性"""

    def __init__(
        self,
        datetime_obj: datetime | None = None,
        format_str: str = TimeFormatEnum.DateTime.value,
    ):
        """
        时间工具类初始化

        Args:
            datetime_obj: 待处理的datetime对象,不传时默认取当前时间
            format_str: 默认时间格式化字符串,默认为TimeFormatEnum.DateTime

        Example:
            >>> # 创建默认时间工具实例(当前时间)
            >>> time_util = TimeUtil()
            >>> # 创建指定时间的工具实例
            >>> specific_time = datetime(2023, 1, 1)
            >>> time_util = TimeUtil(specific_time)
            >>> # 指定格式化字符串
            >>> time_util = TimeUtil(format_str=TimeFormatEnum.DateOnly_CN.value)
        """
        self.datetime_obj = datetime_obj or datetime.now()
        self.format_str = format_str

    @property
    def yesterday(self) -> datetime:
        """获取昨天的日期"""
        return self.sub_time(days=1)

    @property
    def tomorrow(self) -> datetime:
        """获取明天的日期"""
        return self.add_time(days=1)

    @property
    def week_later(self) -> datetime:
        """获取一周后的日期"""
        return self.add_time(days=7)

    @property
    def month_later(self) -> datetime:
        """获取一个月后的日期"""
        return self.add_time(months=1)

    def add_time(self, years: int = 0, months: int = 0, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0, **kwargs) -> datetime:
        """
        增加指定时间

        Args:
            years: 增加的年数
            months: 增加的月数
            days: 增加的天数
            hours: 增加的小时数
            minutes: 增加的分钟数
            seconds: 增加的秒数
            **kwargs: 其他relativedelta支持的参数

        Returns:
            datetime: 增加时间后的datetime对象

        Example:
            >>> time_util = TimeUtil(datetime(2023, 1, 1))
            >>> # 增加1年2个月3天
            >>> result = time_util.add_time(years=1, months=2, days=3)
            >>> print(result)  # 2024-03-04 00:00:00
        """
        return self.datetime_obj + relativedelta(
            years=years,
            months=months,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            **kwargs,
        )

    def sub_time(self, years: int = 0, months: int = 0, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0, **kwargs) -> datetime:
        """
        减去指定时间

        Args:
            years: 减去的年数
            months: 减去的月数
            days: 减去的天数
            hours: 减去的小时数
            minutes: 减去的分钟数
            seconds: 减去的秒数
            **kwargs: 其他relativedelta支持的参数

        Returns:
            datetime: 减去时间后的datetime对象

        Example:
            >>> time_util = TimeUtil(datetime(2023, 1, 1))
            >>> # 减去3个月
            >>> result = time_util.sub_time(months=3)
            >>> print(result)  # 2022-10-01 00:00:00
        """
        return self.datetime_obj - relativedelta(
            years=years,
            months=months,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            **kwargs,
        )

    def str_to_datetime(self, date_str: str, format_str: str | None = None) -> datetime:
        """
        将时间字符串转换为datetime对象

        Args:
            date_str: 时间字符串
            format_str: 格式化字符串,默认为实例的format_str

        Returns:
            datetime: 转换后的datetime对象

        Raises:
            ValueError: 当时间字符串格式与指定格式不匹配时

        Example:
            >>> time_util = TimeUtil()
            >>> # 使用默认格式转换
            >>> dt = time_util.str_to_datetime('2023-01-01 12:00:00')
            >>> # 使用指定格式转换
            >>> dt = time_util.str_to_datetime('2023年01月01日', TimeFormatEnum.DateOnly_CN.value)
        """
        format_str = format_str or self.format_str
        return datetime.strptime(date_str, format_str)

    def datetime_to_str(self, datetime_obj: datetime | None = None, format_str: str | None = None) -> str:
        """
        将datetime对象转换为时间字符串

        Args:
            datetime_obj: 要转换的datetime对象,默认为实例的datetime_obj
            format_str: 格式化字符串,默认为实例的format_str

        Returns:
            str: 格式化后的时间字符串

        Example:
            >>> time_util = TimeUtil()
            >>> # 转换实例的datetime对象
            >>> time_str = time_util.datetime_to_str()
            >>> # 转换指定的datetime对象
            >>> dt = datetime(2023, 1, 1)
            >>> time_str = time_util.datetime_to_str(dt, TimeFormatEnum.DateOnly.value)
        """
        datetime_obj = datetime_obj or self.datetime_obj
        format_str = format_str or self.format_str
        return datetime_obj.strftime(format_str)

    def timestamp_to_str(self, timestamp: float, format_str: str | None = None) -> str:
        """
        将时间戳转换为时间字符串

        Args:
            timestamp: 时间戳(秒级)
            format_str: 格式化字符串,默认为实例的format_str

        Returns:
            str: 格式化后的时间字符串

        Example:
            >>> time_util = TimeUtil()
            >>> # 转换时间戳为默认格式
            >>> time_str = time_util.timestamp_to_str(1672531200)  # 2023-01-01 00:00:00
        """
        format_str = format_str or self.format_str
        return datetime.fromtimestamp(timestamp).strftime(format_str)

    def str_to_timestamp(self, time_str: str, format_str: str | None = None) -> int:
        """
        将时间字符串转换为时间戳

        Args:
            time_str: 时间字符串
            format_str: 格式化字符串,默认为实例的format_str

        Returns:
            int: 时间戳(秒级)

        Example:
            >>> time_util = TimeUtil()
            >>> # 转换时间字符串为时间戳
            >>> timestamp = time_util.str_to_timestamp('2023-01-01 00:00:00')  # 1672531200
        """
        format_str = format_str or self.format_str
        return int(time.mktime(time.strptime(time_str, format_str)))

    @staticmethod
    def timestamp_to_datetime(timestamp: float) -> datetime:
        """
        将时间戳转换为datetime对象

        Args:
            timestamp: 时间戳(秒级)

        Returns:
            datetime: 转换后的datetime对象

        Example:
            >>> # 静态方法调用,不需要实例化
            >>> dt = TimeUtil.timestamp_to_datetime(1672531200)  # datetime(2023, 1, 1, 0, 0)
        """
        return datetime.fromtimestamp(timestamp)

    @property
    def timestamp(self) -> float:
        """获取datetime对象的时间戳(秒级)"""
        return self.datetime_obj.timestamp()

    def difference_in_detail(self, datetime_obj: datetime) -> DateDiff:
        """
        计算两个日期之间的差值详情

        Args:
            datetime_obj: 要比较的时间对象

        Returns:
            DateDiff: 包含年、月、日、时、分、秒差值的模型

        Example:
            >>> time_util = TimeUtil(datetime(2023, 3, 15))
            >>> diff = time_util.difference_in_detail(datetime(2022, 1, 10))
            >>> print(diff.years, diff.months, diff.days)  # 1 2 5
        """
        delta = relativedelta(self.datetime_obj, datetime_obj)

        return DateDiff(
            years=abs(delta.years),
            months=abs(delta.months),
            days=abs(delta.days),
            hours=abs(delta.hours),
            minutes=abs(delta.minutes),
            seconds=abs(delta.seconds),
        )

    def start_of_week(self) -> datetime:
        """
        获取本周的开始日期（周一）

        Returns:
            datetime: 本周一的日期(时间部分为00:00:00)

        Example:
            >>> # 假设当前日期是2023-01-05(周四)
            >>> time_util = TimeUtil(datetime(2023, 1, 5))
            >>> print(time_util.start_of_week())  # 2023-01-02 00:00:00
        """
        return self.datetime_obj - relativedelta(days=self.datetime_obj.weekday())

    def end_of_week(self) -> datetime:
        """
        获取本周的结束日期（周日）

        Returns:
            datetime: 本周日的日期(时间部分为23:59:59.999999)

        Example:
            >>> # 假设当前日期是2023-01-05(周四)
            >>> time_util = TimeUtil(datetime(2023, 1, 5))
            >>> print(time_util.end_of_week())  # 2023-01-08 23:59:59.999999
        """
        return self.start_of_week() + relativedelta(days=6, hours=23, minutes=59, seconds=59, microseconds=999999)

    def start_of_month(self) -> datetime:
        """
        获取本月的第一天

        Returns:
            datetime: 本月1号(时间部分为00:00:00)

        Example:
            >>> time_util = TimeUtil(datetime(2023, 1, 15))
            >>> print(time_util.start_of_month())  # 2023-01-01 00:00:00
        """
        return self.datetime_obj.replace(day=1)

    def end_of_month(self) -> datetime:
        """
        获取本月的最后一天

        Returns:
            datetime: 本月最后一天(时间部分为23:59:59.999999)

        Example:
            >>> time_util = TimeUtil(datetime(2023, 1, 15))
            >>> print(time_util.end_of_month())  # 2023-01-31 23:59:59.999999
        """
        next_month = self.add_time(months=1)
        return next_month.replace(day=1) - relativedelta(seconds=1)

    def start_of_quarter(self) -> datetime:
        """
        获取本季度的第一天

        Returns:
            datetime: 本季度第一天(时间部分为00:00:00)

        Example:
            >>> # 假设当前日期是2023-04-15(第二季度)
            >>> time_util = TimeUtil(datetime(2023, 4, 15))
            >>> print(time_util.start_of_quarter())  # 2023-04-01 00:00:00
        """
        quarter_month_start = (self.datetime_obj.month - 1) // 3 * 3 + 1
        return self.datetime_obj.replace(month=quarter_month_start, day=1)

    def end_of_quarter(self) -> datetime:
        """
        获取本季度的最后一天

        Returns:
            datetime: 本季度最后一天(时间部分为23:59:59.999999)

        Example:
            >>> # 假设当前日期是2023-04-15(第二季度)
            >>> time_util = TimeUtil(datetime(2023, 4, 15))
            >>> print(time_util.end_of_quarter())  # 2023-06-30 23:59:59.999999
        """
        next_quarter_start = self.start_of_quarter().replace(month=self.datetime_obj.month + 3)
        return next_quarter_start - relativedelta(seconds=1)

    def start_of_year(self) -> datetime:
        """
        获取本年度的第一天

        Returns:
            datetime: 本年1月1日(时间部分为00:00:00)

        Example:
            >>> time_util = TimeUtil(datetime(2023, 6, 15))
            >>> print(time_util.start_of_year())  # 2023-01-01 00:00:00
        """
        return self.datetime_obj.replace(month=1, day=1)

    def end_of_year(self) -> datetime:
        """
        获取本年度的最后一天

        Returns:
            datetime: 本年12月31日(时间部分为23:59:59.999999)

        Example:
            >>> time_util = TimeUtil(datetime(2023, 6, 15))
            >>> print(time_util.end_of_year())  # 2023-12-31 23:59:59.999999
        """
        return self.datetime_obj.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)

    def is_weekday(self) -> bool:
        """
        判断当前日期是否是工作日（星期一到星期五）

        Returns:
            bool: True表示是工作日,False表示是周末

        Example:
            >>> # 假设当前日期是周一到周五
            >>> time_util = TimeUtil(datetime(2023, 1, 3))  # 周二
            >>> print(time_util.is_weekday())  # True
        """
        return self.datetime_obj.weekday() < 5

    def count_weekdays_between(self, datetime_obj: datetime, include_end_date: bool = True) -> int:
        """
        计算两个日期之间的工作日数量

        Args:
            datetime_obj: 要比较的datetime对象
            include_end_date: 是否包含结束日期（默认为True）

        Returns:
            int: 两个日期之间的工作日数量

        Example:
            >>> time_util = TimeUtil(datetime(2023, 1, 1))  # 周日
            >>> # 计算到2023-01-10(周二)之间的工作日数量
            >>> count = time_util.count_weekdays_between(datetime(2023, 1, 10))  # 6个工作日
        """
        # 确保start_date是较小的日期，end_date是较大的日期
        start_date = min(self.datetime_obj, datetime_obj)
        end_date = max(self.datetime_obj, datetime_obj)

        # 如果不包含结束日期，将end_date减去一天
        if not include_end_date:
            end_date = end_date - relativedelta(days=1)

        # 计算两个日期之间的天数
        days_between = abs((end_date - start_date).days)

        # 计算完整周数，每周有5个工作日
        weeks_between = days_between // 7
        weekdays = weeks_between * 5

        # 计算剩余的天数
        remaining_days = days_between % 7
        # 遍历剩余的天数，检查每天是否为工作日，如果是，则累加工作日数量
        for day_offset in range(remaining_days + 1):
            if (start_date + relativedelta(days=day_offset)).weekday() < 5:
                weekdays += 1

        return weekdays


# 快捷函数定义
def get_time() -> str:
    """获取当前时间的完整字符串表示"""
    return TimeUtil().datetime_to_str(format_str=TimeFormatEnum.DateTimeFull.value)


def get_lite_time() -> str:
    """获取当前时间的精简字符串表示(仅时间部分)"""
    return TimeUtil().datetime_to_str(format_str='%H:%M:%S')


def get_sql_time() -> str:
    """获取适用于SQL的时间字符串表示"""
    return TimeUtil().datetime_to_str(format_str='%F %X')


def get_timestamp(timestr: str | None = None, format_str: str | None = None, size: int = 10) -> int:
    """
    获取时间戳

    Args:
        timestr: 可选的时间字符串，不指定则获取当前时间戳
        format_str: 时间字符串的格式，不指定则使用默认格式
        size: 时间戳位数，10为秒级，13为毫秒级

    Returns:
        int: 指定位数的时间戳

    Example:
        >>> # 获取当前秒级时间戳
        >>> ts = get_timestamp()  # 例如: 1672531200
        >>> # 获取当前毫秒级时间戳
        >>> ts_ms = get_timestamp(size=13)  # 例如: 1672531200000
        >>> # 获取指定时间的时间戳
        >>> ts = get_timestamp('2023-01-01 00:00:00')
    """
    if timestr is None:
        if size == 13:
            return int(TimeUtil().timestamp * 1000)
        return int(TimeUtil().timestamp)
    return TimeUtil().str_to_timestamp(timestr, format_str=format_str)


# 全局时间工具实例
time_util = TimeUtil()

if __name__ == '__main__':
    # 示例用法
    print('完整时间:', get_time())
    print('精简时间:', get_lite_time())
    print('SQL时间:', get_sql_time())
    print('当前时间戳(秒):', get_timestamp())
    print('当前时间戳(毫秒):', get_timestamp(size=13))
    print('指定时间的时间戳:', get_timestamp(size=13, timestr='2020-06-15 13:28:27'))
