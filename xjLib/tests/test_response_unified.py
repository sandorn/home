# !/usr/bin/env python3
"""
==============================================================
测试文件     : test_response_unified.py
功能描述     : 测试统一响应处理模块的功能和兼容性
开发工具     : VSCode
作者         : Even.Sand
联系方式     : sandorn@163.com
创建时间     : 2025-09-19 17:15:00
==============================================================
"""

from __future__ import annotations

import asyncio
import time
import unittest

from xt_ahttp import AHttpLoop, ahttp_get
from xt_requests import SessionClient, get
from xt_response_unified import ResponseFactory
from xtlog import mylog


class TestResponseUnified(unittest.TestCase):
    """测试统一响应处理模块"""

    def setUp(self) -> None:
        """设置测试环境"""
        self.test_urls = {
            'sync': 'https://www.httpbin.org/get',
            'async': 'https://www.httpbin.org/get',
            'html': 'https://www.httpbin.org/html',
            'json': 'https://www.httpbin.org/json',
            'status_200': 'https://www.httpbin.org/status/200',
            'status_404': 'https://www.httpbin.org/status/404',
        }

        # 配置日志
        mylog.info('开始测试统一响应处理模块')

    def tearDown(self) -> None:
        """清理测试环境"""
        mylog.info('测试完成')

    def test_sync_response(self) -> None:
        """测试同步响应处理"""
        mylog.info('\n===== 测试同步响应处理 =====')

        # 发送同步请求
        start_time = time.time()
        raw_response = get(self.test_urls['sync'])
        response_time = time.time() - start_time

        mylog.info(f'同步请求耗时: {response_time:.4f} 秒')

        # 使用工厂创建统一响应对象
        unified_resp = ResponseFactory.create_response(raw_response)

        # 测试基本属性
        self.assertEqual(unified_resp.status, 200)
        self.assertTrue(ResponseFactory.is_success(unified_resp))
        self.assertTrue(self.test_urls['sync'] in unified_resp.url)

        # 测试内容解析
        self.assertIsNotNone(unified_resp.content)
        self.assertIsNotNone(unified_resp.text)

        # 测试JSON解析
        json_data = unified_resp.json
        self.assertIsInstance(json_data, dict)
        self.assertIn('args', json_data)

        mylog.info('同步响应测试通过!')

    def test_async_response(self) -> None:
        """测试异步响应处理"""
        mylog.info('\n===== 测试异步响应处理 =====')

        # 定义异步测试函数
        async def async_test():
            # 发送异步请求
            start_time = time.time()
            raw_response = ahttp_get(self.test_urls['async'])
            response_time = time.time() - start_time

            mylog.info(f'异步请求耗时: {response_time:.4f} 秒')

            # 使用工厂创建统一响应对象
            unified_resp = ResponseFactory.create_response(raw_response)

            # 测试基本属性
            self.assertEqual(unified_resp.status, 200)
            self.assertTrue(ResponseFactory.is_success(unified_resp))
            self.assertTrue(self.test_urls['async'] in unified_resp.url)

            # 测试内容解析
            self.assertIsNotNone(unified_resp.content)
            self.assertIsNotNone(unified_resp.text)

            # 测试JSON解析
            json_data = unified_resp.json
            self.assertIsInstance(json_data, dict)
            self.assertIn('args', json_data)

            mylog.info('异步响应测试通过!')

        # 运行异步测试
        loop = asyncio.get_event_loop()
        loop.run_until_complete(async_test())

    def test_html_parsing(self) -> None:
        """测试HTML解析功能"""
        mylog.info('\n===== 测试HTML解析功能 =====')

        # 获取包含HTML内容的响应
        raw_response = get(self.test_urls['html'])
        unified_resp = ResponseFactory.create_response(raw_response)

        # 测试html属性
        html = unified_resp.html
        self.assertIsNotNone(html)

        # 测试element属性
        element = unified_resp.element
        self.assertIsNotNone(element)

        # 测试soup属性
        soup = unified_resp.soup
        self.assertIsNotNone(soup)

        # 测试dom属性
        dom = unified_resp.dom
        self.assertIsNotNone(dom)

        # 测试query属性
        query = unified_resp.query
        self.assertIsNotNone(query)

        # 测试xpath方法
        title_xpath = '//h1/text()'
        titles = unified_resp.xpath(title_xpath)
        self.assertIsInstance(titles, list)
        self.assertTrue(len(titles) > 0)
        self.assertTrue(len(titles[0]) > 0)
        self.assertEqual(titles[0][0], 'Herman Melville - Moby-Dick')

        # 测试多个xpath选择器
        multiple_xpaths = ['//h1/text()', '//p/text()']
        results = unified_resp.xpath(multiple_xpaths)
        self.assertEqual(len(results), 2)
        self.assertTrue(len(results[0]) > 0)
        self.assertTrue(len(results[1]) > 0)

        mylog.info('HTML解析功能测试通过!')

    def test_text_processing(self) -> None:
        """测试文本处理功能"""
        mylog.info('\n===== 测试文本处理功能 =====')

        # 获取包含HTML内容的响应
        raw_response = get(self.test_urls['html'])
        unified_resp = ResponseFactory.create_response(raw_response)

        # 测试原始文本
        raw_text = unified_resp.text
        self.assertIsNotNone(raw_text)
        self.assertTrue(len(raw_text) > 0)

        # 测试纯净文本(ctext)
        clean_text = unified_resp.ctext
        self.assertIsNotNone(clean_text)
        self.assertTrue(len(clean_text) > 0)
        # 确保ctext不包含HTML标签
        self.assertFalse('<html>' in clean_text.lower())

        # 测试深度清理文本(clean_text)
        deep_clean_text = unified_resp.clean_text
        self.assertIsNotNone(deep_clean_text)
        self.assertTrue(len(deep_clean_text) > 0)

        mylog.info('文本处理功能测试通过!')

    def test_json_parsing(self) -> None:
        """测试JSON解析功能"""
        mylog.info('\n===== 测试JSON解析功能 =====')

        # 获取包含JSON内容的响应
        raw_response = get(self.test_urls['json'])
        unified_resp = ResponseFactory.create_response(raw_response)

        # 测试JSON解析
        json_data = unified_resp.json
        self.assertIsInstance(json_data, dict)
        self.assertIn('slideshow', json_data)

        # 测试复杂JSON结构访问
        slideshow = json_data['slideshow']
        self.assertIn('author', slideshow)
        self.assertEqual(slideshow['author'], 'Yours Truly')

        mylog.info('JSON解析功能测试通过!')

    def test_status_code_handling(self) -> None:
        """测试状态码处理"""
        mylog.info('\n===== 测试状态码处理 =====')

        # 测试成功状态码
        success_resp = get(self.test_urls['status_200'])
        unified_success = ResponseFactory.create_response(success_resp)
        self.assertEqual(unified_success.status, 200)
        self.assertTrue(ResponseFactory.is_success(unified_success))
        self.assertTrue(bool(unified_success))  # 测试布尔值转换

        # 测试失败状态码
        error_resp = get(self.test_urls['status_404'])
        unified_error = ResponseFactory.create_response(error_resp)
        self.assertEqual(unified_error.status, 404)
        self.assertFalse(ResponseFactory.is_success(unified_error))
        self.assertFalse(bool(unified_error))  # 测试布尔值转换

        mylog.info('状态码处理测试通过!')

    def test_session_client_integration(self) -> None:
        """测试与SessionClient的集成"""
        mylog.info('\n===== 测试与SessionClient的集成 =====')

        # 创建会话客户端
        with SessionClient() as session:
            # 发送会话请求
            raw_response = session.get(self.test_urls['sync'])
            unified_resp = ResponseFactory.create_response(raw_response)

            # 验证响应
            self.assertEqual(unified_resp.status, 200)
            self.assertIsNotNone(unified_resp.cookies)
            self.assertIsNotNone(unified_resp.headers)

        mylog.info('与SessionClient集成测试通过!')

    def test_async_loop_integration(self) -> None:
        """测试与AHttpLoop的集成"""
        mylog.info('\n===== 测试与AHttpLoop的集成 =====')

        # 定义异步测试函数
        async def async_test():
            # 创建异步循环客户端
            async with AHttpLoop() as http_loop:
                # 发送异步请求
                raw_response = await http_loop.get(self.test_urls['async'])
                unified_resp = ResponseFactory.create_response(raw_response)

                # 验证响应
                self.assertEqual(unified_resp.status, 200)
                self.assertIsNotNone(unified_resp.cookies)
                self.assertIsNotNone(unified_resp.headers)

        # 运行异步测试
        loop = asyncio.get_event_loop()
        loop.run_until_complete(async_test())

        mylog.info('与AHttpLoop集成测试通过!')

    def test_performance_comparison(self) -> None:
        """测试性能比较"""
        mylog.info('\n===== 测试性能比较 =====')

        # 测试原始响应处理时间
        start_time = time.time()
        raw_response = get(self.test_urls['sync'])
        raw_time = time.time() - start_time

        # 测试统一响应处理时间
        start_time = time.time()
        raw_response = get(self.test_urls['sync'])
        unified_resp = ResponseFactory.create_response(raw_response)
        unified_time = time.time() - start_time

        mylog.info(f'原始响应处理时间: {raw_time:.6f} 秒')
        mylog.info(f'统一响应处理时间: {unified_time:.6f} 秒')

        # 确保统一响应处理时间不会明显长于原始处理
        self.assertLessEqual(unified_time, raw_time * 1.5)

        mylog.info('性能比较测试通过!')

    def test_edge_cases(self) -> None:
        """测试边界情况"""
        mylog.info('\n===== 测试边界情况 =====')

        # 测试空响应
        empty_unified = ResponseFactory.create_response()
        self.assertEqual(empty_unified.status, 999)
        self.assertEqual(empty_unified.text, '')
        self.assertEqual(len(empty_unified), 0)

        # 测试直接提供内容
        content = b'<html><body><h1>Test</h1></body></html>'
        content_unified = ResponseFactory.create_response(content=content)
        self.assertEqual(content_unified.status, 999)  # 无原始响应时状态码为999
        self.assertIn('Test', content_unified.text)

        # 测试无效的XPath
        invalid_xpath = unified_resp = ResponseFactory.create_response(content=content)
        results = invalid_xpath.xpath('//invalid')
        self.assertEqual(results, [[]])

        # 测试空选择器
        empty_xpath = unified_resp = ResponseFactory.create_response(content=content)
        results = empty_xpath.xpath('')
        self.assertEqual(results, [[]])

        mylog.info('边界情况测试通过!')


if __name__ == '__main__':
    """运行测试"""
    mylog.info('启动统一响应处理模块测试...')
    unittest.main()
