# !/usr/bin/env python3
"""
测试重构后的xt_log包
"""
from __future__ import annotations

from xt_log import mylog


def test_basic_logging() -> None:
    """测试基本日志功能"""
    mylog.info('这是一条普通信息日志')
    mylog.debug('这是一条调试日志')
    mylog.warning('这是一条警告日志')
    mylog.error('这是一条错误日志')
    mylog.success('这是一条成功日志')


def test_callfrom_feature() -> None:
    """测试callfrom功能"""
    def some_function() -> None:
        mylog.info('在some_function中记录日志', callfrom=some_function)
    
    some_function()


def test_multiple_args() -> None:
    """测试多参数日志"""
    mylog('第一条日志', '第二条日志', '第三条日志')


def test_level_change() -> None:
    """测试日志级别调整"""
    mylog.info('调整日志级别前 - 这条应该显示')
    mylog.set_level('WARNING')
    mylog.info('调整日志级别后 - 这条不应该显示')
    mylog.warning('调整日志级别后 - 这条应该显示')
    mylog.set_level('DEBUG')  # 恢复默认级别


def main() -> None:
    """主测试函数"""
    print('开始测试xt_log包...')
    
    test_basic_logging()
    test_callfrom_feature()
    test_multiple_args()
    test_level_change()
    
    print('测试完成！')


if __name__ == '__main__':
    main()