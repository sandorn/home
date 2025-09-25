# !/usr/bin/env python3

"""
测试MySQL数据库连接的autocommit参数是否生效

该脚本通过以下步骤验证autocommit是否生效：
1. 创建一个数据库连接，设置autocommit=True
2. 执行插入操作但不显式调用commit
3. 关闭连接
4. 重新创建一个新的数据库连接
5. 查询之前插入的数据，检查是否存在

如果autocommit生效，那么即使没有显式调用commit，数据也应该被保存
"""
from __future__ import annotations

import logging

from xt_database.mysql import create_mysql_engine
from xt_wraps.log import LogCls

# 配置日志
logger = LogCls(level=logging.INFO)


class AutoCommitTester:
    def __init__(self):
        # 测试表名
        self.test_table = 'test_autocommit_validation'
        
        # 测试数据
        self.test_data = {
            'name': 'autocommit_test',
            'value': 'test_value',
            'created_at': 'CURRENT_TIMESTAMP'
        }
        
    def setup_test_environment(self):
        """设置测试环境，创建测试表"""
        logger.info('\n===== 设置测试环境 =====')
        
        # 创建数据库连接
        db = create_mysql_engine()
        
        # 删除已存在的测试表
        drop_sql = f'DROP TABLE IF EXISTS `{self.test_table}`'
        db.execute(drop_sql)
        logger.info(f'✅ 已删除旧测试表（如果存在）: {self.test_table}')
        
        # 创建测试表
        create_sql = f"""
        CREATE TABLE `{self.test_table}` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(100) NOT NULL,
            `value` VARCHAR(255) NOT NULL,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        db.execute(create_sql)
        logger.info(f'✅ 已创建测试表: {self.test_table}')
        
    def test_autocommit_enabled(self):
        """测试autocommit=True的情况"""
        logger.info('\n===== 测试autocommit=True =====')
        
        # 1. 创建启用了autocommit的连接
        logger.info('▶️ 创建启用了autocommit的数据库连接')
        db = create_mysql_engine(autocommit=True)
        
        try:
            # 2. 插入数据但不显式commit
            logger.info(f'▶️ 插入测试数据，但不显式调用commit: {self.test_data}')
            insert_sql = f'INSERT INTO `{self.test_table}` (`name`, `value`) VALUES (%s, %s)'
            params = (self.test_data['name'], self.test_data['value'])
            row_count = db.execute(insert_sql, params)
            logger.info(f'✅ 插入操作完成，影响行数: {row_count}')
            
            # 注意：这里故意不调用commit
            logger.info('ℹ️ 注意：没有显式调用commit，依赖autocommit自动提交')
            
        finally:
            # 3. 关闭连接
            logger.info('▶️ 关闭数据库连接')
        
        # 4. 创建新的连接来验证数据是否被保存
        logger.info('▶️ 创建新的数据库连接以验证数据是否持久化')
        verify_db = create_mysql_engine()
        
        try:
            # 5. 查询数据
            logger.info('▶️ 查询之前插入的数据')
            query_sql = f'SELECT * FROM `{self.test_table}` WHERE `name` = %s'
            results = verify_db.query(query_sql, [self.test_data['name']])
            
            # 6. 验证结果
            if results and len(results) > 0:
                logger.info(f'✅ 验证成功！数据已自动提交并持久化存储。查询结果: {results}')
                return True
            logger.error('❌ 验证失败！数据没有自动提交，查询结果为空。')
            return False
        finally: ...
    
    def test_autocommit_disabled(self):
        """测试autocommit=False的情况"""
        logger.info('\n===== 测试autocommit=False =====')
        
        # 清理测试表中的数据
        cleanup_db = create_mysql_engine()
        cleanup_db.execute(f'DELETE FROM `{self.test_table}`')
        cleanup_db.execute('COMMIT')  # 确保清理操作生效
        
        # 1. 创建禁用了autocommit的连接
        logger.info('▶️ 创建禁用了autocommit的数据库连接')
        db = create_mysql_engine(autocommit=False)
        
        try:
            # 2. 插入数据但不显式commit
            logger.info(f'▶️ 插入测试数据，但不显式调用commit: {self.test_data}')
            insert_sql = f'INSERT INTO `{self.test_table}` (`name`, `value`) VALUES (%s, %s)'
            params = (self.test_data['name'], self.test_data['value'])
            row_count = db.execute(insert_sql, params)
            logger.info(f'✅ 插入操作完成，影响行数: {row_count}')
            
            # 注意：这里故意不调用commit
            logger.info('ℹ️ 注意：没有显式调用commit，且autocommit=False')
            
        finally:
            # 3. 关闭连接
            logger.info('▶️ 关闭数据库连接')
        
        # 4. 创建新的连接来验证数据是否被保存
        logger.info('▶️ 创建新的数据库连接以验证数据是否持久化')
        verify_db = create_mysql_engine()
        
        # 5. 查询数据
        logger.info('▶️ 查询之前插入的数据')
        query_sql = f'SELECT * FROM `{self.test_table}` WHERE `name` = %s'
        results = verify_db.query(query_sql, [self.test_data['name']])
        
        # 6. 验证结果
        if not results or len(results) == 0:
            logger.info('✅ 验证成功！数据没有被自动提交（符合预期）。')
            return True
        logger.error('❌ 验证失败！数据被意外提交，查询结果不为空。')
        return False

    def cleanup_test_environment(self):
        """清理测试环境，删除测试表"""
        logger.info('\n===== 清理测试环境 =====')
        
        # 创建数据库连接
        db = create_mysql_engine()
        
        try:
            # 删除测试表
            drop_sql = f'DROP TABLE IF EXISTS `{self.test_table}`'
            db.execute(drop_sql)
            logger.info(f'✅ 已删除测试表: {self.test_table}')
            
        finally: ...
    
    def run_all_tests(self):
        """运行所有测试"""
        logger.info('\n------------------------------------------------------------')
        logger.info('                    MySQL autocommit参数验证测试')
        logger.info('------------------------------------------------------------')
        
        try:
            # 设置测试环境
            self.setup_test_environment()
            
            # 运行测试
            test_results = {
                'autocommit_enabled': False,
                'autocommit_disabled': False
            }
            
            # 测试autocommit=True
            test_results['autocommit_enabled'] = self.test_autocommit_enabled()
            
            # 测试autocommit=False
            test_results['autocommit_disabled'] = self.test_autocommit_disabled()
            
            # 输出测试结果摘要
            logger.info('\n------------------------------------------------------------')
            logger.info('                    测试结果摘要')
            logger.info('------------------------------------------------------------')
            
            passed_count = sum(test_results.values())
            total_count = len(test_results)
            
            for test_name, passed in test_results.items():
                status = '✅ 通过' if passed else '❌ 失败'
                logger.info(f'{test_name}: {status}')
            
            logger.info(f'总测试数: {total_count}, 通过数: {passed_count}, 通过率: {passed_count / total_count * 100:.2f}%')
            
        finally:
            # 清理测试环境
            self.cleanup_test_environment()


if __name__ == '__main__':
    tester = AutoCommitTester()
    tester.run_all_tests()