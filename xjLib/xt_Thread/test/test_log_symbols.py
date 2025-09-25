# !/usr/bin/env python3
"""
测试日志特殊符号快捷方法
演示如何使用新增的start、ok、fail等方法记录带特殊符号的日志
"""
from __future__ import annotations

from xt_wraps.log import mylog


def test_log_symbols():
    """测试不同级别的特殊符号日志记录"""
    # 使用新添加的快捷方法记录带特殊符号的日志
    mylog.start('开始执行任务')
    
    try:
        # 记录信息日志
        mylog.info('处理中...')
        
        # 模拟一些操作
        result = 10 / 2
        
        # 记录成功日志
        mylog.ok(f'计算成功，结果: {result}')
        
        # 记录警告日志
        mylog.warning('注意：即将处理敏感数据')
        
        # 触发异常测试失败日志
        # uncomment to test fail log
        # error_result = 10 / 0
        
    except Exception as e:
        # 记录失败日志
        mylog.fail(f'处理失败: {e!s}')
        mylog.forbidden('操作被禁止')
        mylog.stop('任务已停止')
    
    # 记录调试信息
    mylog.debug('调试信息: 这是一条普通的调试日志')
    
    print('测试完成，请查看日志输出')


if __name__ == '__main__':
    test_log_symbols()