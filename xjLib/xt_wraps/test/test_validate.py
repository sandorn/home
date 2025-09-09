# !/usr/bin/env python
"""
输入验证装饰器测试文件
"""

import asyncio
import unittest
from typing import List

from ..validate import validate_params, validate_types, validate_ranges, validate_custom

# 计数器，用于跟踪测试用例序号
test_counter = {
    'basic_type_validation': 1.1,
    'range_validation': 1.2,
    'required_params': 1.3,
    'custom_validator': 1.4,
    'no_exception_mode': 1.5,
    'positional_args_validation': 1.6,
    'alias_functions': 1.7,
    'async_type_validation': 2.1,
    'async_custom_validator': 2.2,
    'async_combined_validation': 2.3
}


class TestValidateParams(unittest.TestCase):
    
    def test_basic_type_validation(self):
        """测试基本的类型验证功能"""
        print(f"{test_counter['basic_type_validation']} 测试基本的类型验证功能")
        @validate_params(param_types={'a': int, 'b': str})
        def process_data(a, b):
            return f"{b}: {a}"
        
        # 正确类型的参数
        result = process_data(123, "test")
        self.assertEqual(result, "test: 123")
        
        # 错误类型的参数
        with self.assertRaises(TypeError):
            process_data("123", "test")
        
        with self.assertRaises(TypeError):
            process_data(123, 456)
    
    def test_range_validation(self):
        """测试参数范围验证功能"""
        print(f"{test_counter['range_validation']} 测试参数范围验证功能")
        @validate_params(param_types={'age': int}, param_ranges={'age': (0, 120)})
        def check_age(age):
            return f"年龄: {age}"
        
        # 范围内的参数
        result = check_age(25)
        self.assertEqual(result, "年龄: 25")
        
        # 超出范围的参数
        with self.assertRaises(ValueError):
            check_age(150)
        
        with self.assertRaises(ValueError):
            check_age(-10)
    
    def test_required_params(self):
        """测试必选参数验证功能"""
        print(f"{test_counter['required_params']} 测试必选参数验证功能")
        @validate_params(required_params=['name', 'age'])
        def register_user(name, age, email=None):
            return f"用户注册成功: {name}, {age}岁"
        
        # 提供所有必选参数
        result = register_user("张三", 30)
        self.assertEqual(result, "用户注册成功: 张三, 30岁")
        
        # 缺少必选参数
        with self.assertRaises(ValueError):
            register_user("李四")
    
    def test_custom_validator(self):
        """测试自定义验证函数功能"""
        print(f"{test_counter['custom_validator']} 测试自定义验证函数功能")
        # 定义自定义验证函数
        def is_valid_email(email):
            return '@' in email and '.' in email.split('@')[1]
        
        @validate_params(custom_validators={'email': is_valid_email})
        def send_email(email, content):
            return f"邮件已发送至: {email}"
        
        # 验证通过的参数
        result = send_email("test@example.com", "测试内容")
        self.assertEqual(result, "邮件已发送至: test@example.com")
        
        # 验证失败的参数
        with self.assertRaises(ValueError):
            send_email("invalid-email", "测试内容")
    
    def test_no_exception_mode(self):
        """测试不抛出异常模式"""
        print(f"{test_counter['no_exception_mode']} 测试不抛出异常模式")
        @validate_params(
            param_types={'score': int},
            param_ranges={'score': (0, 100)},
            raise_exception=False,
            default_return="验证失败"
        )
        def record_score(name, score):
            return f"{name} 的分数: {score}"
        
        # 验证通过的情况
        result1 = record_score("张三", 85)
        self.assertEqual(result1, "张三 的分数: 85")
        
        # 验证失败但不抛出异常的情况
        result2 = record_score("李四", 150)
        self.assertEqual(result2, "验证失败")
        
        result3 = record_score("王五", "not a number")
        self.assertEqual(result3, "验证失败")
    
    def test_positional_args_validation(self):
        """测试位置参数验证功能"""
        print(f"{test_counter['positional_args_validation']} 测试位置参数验证功能")
        @validate_params(param_types={'arg0': int, 'arg1': str})
        def mixed_params(a, b, c=None):
            return f"{a}, {b}, {c}"
        
        # 正确的位置参数类型
        result = mixed_params(123, "test", "optional")
        self.assertEqual(result, "123, test, optional")
        
        # 错误的位置参数类型
        with self.assertRaises(TypeError):
            mixed_params("123", "test")
    
    def test_alias_functions(self):
        """测试类型别名功能"""
        print(f"{test_counter['alias_functions']} 测试类型别名功能")
        # 测试validate_types别名
        @validate_types(param_types={'x': int, 'y': int})
        def add(x, y):
            return x + y
        
        result = add(10, 20)
        self.assertEqual(result, 30)
        
        # 测试validate_ranges别名
        @validate_ranges(param_ranges={'value': (0, 100)})
        def clamp_value(value):
            return value
        
        result = clamp_value(50)
        self.assertEqual(result, 50)
        
        # 测试validate_custom别名
        def is_even(num):
            return num % 2 == 0
        
        @validate_custom(custom_validators={'num': is_even})
        def process_even(num):
            return num * 2
        
        result = process_even(4)
        self.assertEqual(result, 8)


class TestAsyncValidateParams(unittest.IsolatedAsyncioTestCase):
    
    async def test_async_type_validation(self):
        """测试异步函数的类型验证"""
        print(f"{test_counter['async_type_validation']} 测试异步函数的类型验证")
        @validate_params(param_types={'a': int, 'b': str})
        async def async_process_data(a, b):
            await asyncio.sleep(0.1)  # 模拟异步操作
            return f"{b}: {a}"
        
        # 正确类型的参数
        result = await async_process_data(123, "test")
        self.assertEqual(result, "test: 123")
        
        # 错误类型的参数
        with self.assertRaises(TypeError):
            await async_process_data("123", "test")
    
    async def test_async_custom_validator(self):
        """测试异步函数的自定义验证"""
        print(f"{test_counter['async_custom_validator']} 测试异步函数的自定义验证")
        # 定义自定义验证函数
        def is_valid_email(email):
            return '@' in email and '.' in email.split('@')[1]
        
        @validate_params(custom_validators={'email': is_valid_email})
        async def async_send_email(email, content):
            await asyncio.sleep(0.1)  # 模拟异步操作
            return f"邮件已发送至: {email}"
        
        # 验证通过的参数
        result = await async_send_email("test@example.com", "测试内容")
        self.assertEqual(result, "邮件已发送至: test@example.com")
        
        # 验证失败的参数
        with self.assertRaises(ValueError):
            await async_send_email("invalid-email", "测试内容")
    
    async def test_async_combined_validation(self):
        """测试异步函数的组合验证"""
        print(f"{test_counter['async_combined_validation']} 测试异步函数的组合验证")
        def is_non_empty_list(items):
            return isinstance(items, list) and len(items) > 0
        
        @validate_params(
            param_types={'name': str, 'scores': List[int]},
            custom_validators={'scores': is_non_empty_list},
            required_params=['name', 'scores']
        )
        async def async_calculate_average(name, scores):
            await asyncio.sleep(0.1)  # 模拟异步操作
            avg = sum(scores) / len(scores)
            return f"{name}的平均分: {avg}"
        
        # 验证通过的参数
        result = await async_calculate_average("张三", [85, 90, 95])
        self.assertEqual(result, "张三的平均分: 90.0")
        
        # 验证失败的参数
        with self.assertRaises(ValueError):
            await async_calculate_average("李四", [])


if __name__ == '__main__':
    unittest.main()