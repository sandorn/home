# !/usr/bin/env python
"""
==============================================================
Description  : 异步HTTP请求模块综合测试程序
Develop      : VSCode
Author       : sandorn sandorn@live.cn
LastEditTime : 2025-10-16 17:00:00
Github       : https://github.com/sandorn/xthttp

本文件演示了异步HTTP请求模块的主要功能和用法
参照demo_requ.py的测试模式构建
==============================================================
"""

from __future__ import annotations

import asyncio

from xthttp.ahttp import AsyncHttpClient, ahttp_get, ahttp_get_all, ahttp_post, ahttp_post_all
from xtlog import mylog

# 定义测试URL集合
test_urls = [
    'https://httpbin.org/get',  # 正常GET请求
    'https://httpbin.org/post',  # 正常POST请求
    'https://httpbin.org/json',  # JSON响应
    'https://httpbin.org/html',  # HTML响应
    'https://httpbin.org/status/200',  # 200状态码
    'https://httpbin.org/status/404',  # 404错误
    'https://httpbin.org/status/500',  # 500错误
    'https://httpbin.org/redirect/1',  # 重定向
    'https://httpbin.org/delay/1',  # 延迟响应
]

# 无效URL测试集合
invalid_urls = [
    'http:/www.example.com',  # 缺少双斜杠
    'ftp://www.example.com',  # 不支持的协议
    'www.example.com',  # 缺少协议
    '://example.com',  # 空协议
    'https://',  # 空主机名
    'https://..com',  # 无效主机名
    '这不是一个URL',  # 完全无效的字符串
    5555,  # 非字符串类型
]

# POST请求测试数据
post_data = {'key1': 'value1', 'key2': 'value2', 'json_data': {'nested': 'object'}}


def test_basic_requests():
    """测试基本请求功能"""
    mylog.info('\n=== 基本请求功能测试 ===')

    # GET请求测试
    mylog.info('1. GET请求测试...')
    response = ahttp_get(test_urls[0])
    mylog.info(f'GET请求结果: {type(response).__name__} - {response}')

    # POST请求测试
    mylog.info('2. POST请求测试...')
    response = ahttp_post(test_urls[1], data=post_data)
    mylog.info(f'POST请求结果: {type(response).__name__} - {response}')

    # JSON响应测试
    mylog.info('3. JSON响应测试...')
    response = ahttp_get(test_urls[2])
    mylog.info(f'JSON请求结果: {type(response).__name__} - {response}')

    # HTML响应测试
    mylog.info('4. HTML响应测试...')
    response = ahttp_get(test_urls[3])
    mylog.info(f'HTML请求结果: {type(response).__name__} - {response}')


def test_error_handling():
    """测试错误处理机制"""
    mylog.info('\n=== 错误处理机制测试 ===')

    # 404错误测试
    mylog.info('1. 404错误测试...')
    response = ahttp_get(test_urls[5])
    mylog.info(f'404请求结果: {type(response).__name__} - {response}')

    # 500错误测试
    mylog.info('2. 500错误测试...')
    response = ahttp_get(test_urls[6])
    mylog.info(f'500请求结果: {type(response).__name__} - {response}')

    # 重定向测试
    mylog.info('3. 重定向测试...')
    response = ahttp_get(test_urls[7])
    mylog.info(f'重定向请求结果: {type(response).__name__} - {response}')


def test_invalid_urls():
    """测试无效URL处理"""
    mylog.info('\n=== 无效URL处理测试 ===')

    for i, invalid_url in enumerate(invalid_urls[:3]):  # 只测试前3个，避免输出过多
        mylog.info(f'{i + 1}. 测试无效URL: {invalid_url}')
        response = ahttp_get(invalid_url)
        mylog.info(f'无效URL请求结果: {type(response).__name__} - {response}')


def test_custom_headers():
    """测试自定义请求头"""
    mylog.info('\n=== 自定义请求头测试 ===')

    custom_headers = {'User-Agent': 'Custom-Agent/1.0', 'X-Custom-Header': 'custom-value', 'Accept': 'application/json'}

    response = ahttp_get(test_urls[0], headers=custom_headers)
    mylog.info(f'自定义请求头结果: {type(response).__name__} - {response}')


def test_timeout_handling():
    """测试超时处理"""
    mylog.info('\n=== 超时处理测试 ===')

    # 使用一个可能导致超时的URL，设置较短的超时时间
    timeout_url = 'https://httpbin.org/delay/5'

    response = ahttp_get(timeout_url, timeout=2)  # 2秒超时
    mylog.info(f'超时测试结果: {type(response).__name__} - {response}')


def test_retry_mechanism():
    """测试重试机制"""
    mylog.info('\n=== 重试机制测试 ===')

    # 测试不稳定的URL（可能会失败但会重试）
    unstable_urls = [
        'https://httpbin.org/status/500',  # 服务器错误
        'https://httpbin.org/status/503',  # 服务不可用
    ]

    for i, url in enumerate(unstable_urls):
        mylog.info(f'{i + 1}. 测试重试机制URL: {url}')
        response = ahttp_get(url)
        mylog.info(f'重试测试结果: {type(response).__name__} - {response}')


async def test_async_client_basic():
    """测试异步客户端基本功能"""
    mylog.info('\n=== 异步客户端基本功能测试 ===')

    client = AsyncHttpClient(max_concurrent=5)

    # 单个请求测试
    mylog.info('1. 单个请求测试...')
    response = await client.request('get', test_urls[0])
    mylog.info(f'单个请求结果: {type(response).__name__} - {response}')

    # POST请求测试
    mylog.info('2. POST请求测试...')
    response = await client.request('post', test_urls[1], data=post_data)
    mylog.info(f'POST请求结果: {type(response).__name__} - {response}')


async def test_async_client_batch():
    """测试异步客户端批量请求"""
    mylog.info('\n=== 异步客户端批量请求测试 ===')

    client = AsyncHttpClient(max_concurrent=3)

    # 批量GET请求测试
    mylog.info('1. 批量GET请求测试...')
    urls_to_test = test_urls[:4]  # 测试前4个URL
    results = await client.batch_request('get', urls_to_test)

    for i, result in enumerate(results):
        mylog.info(f'批量请求{i + 1}结果: {type(result).__name__} - {result}')

    # 批量POST请求测试
    mylog.info('2. 批量POST请求测试...')
    post_urls = [test_urls[1]] * 3  # 3个相同的POST URL
    results = await client.batch_request('post', post_urls, data=post_data)

    for i, result in enumerate(results):
        mylog.info(f'批量POST请求{i + 1}结果: {type(result).__name__} - {result}')


async def test_async_client_multi():
    """测试异步客户端共享会话请求"""
    mylog.info('\n=== 异步客户端共享会话请求测试 ===')

    client = AsyncHttpClient(max_concurrent=3)

    # 共享会话GET请求测试
    mylog.info('1. 共享会话GET请求测试...')
    urls_to_test = test_urls[:4]  # 测试前4个URL
    results = await client.multi_request('get', urls_to_test)

    for i, result in enumerate(results):
        mylog.info(f'共享会话请求{i + 1}结果: {type(result).__name__} - {result}')


async def test_async_client_error_handling():
    """测试异步客户端错误处理"""
    mylog.info('\n=== 异步客户端错误处理测试 ===')

    client = AsyncHttpClient(max_concurrent=3)

    # 混合URL测试（包含正常和错误URL）
    mixed_urls = [
        test_urls[0],  # 正常URL
        test_urls[5],  # 404错误
        test_urls[6],  # 500错误
        invalid_urls[0],  # 无效URL
        test_urls[1],  # 正常URL
    ]

    mylog.info('1. 混合URL批量请求测试...')
    results = await client.batch_request('get', mixed_urls)

    for i, (url, result) in enumerate(zip(mixed_urls, results, strict=False)):
        mylog.info(f'混合URL{i + 1}[{url}]结果: {type(result).__name__} - {result}')


def test_batch_functions():
    """测试批量请求便捷函数"""
    mylog.info('\n=== 批量请求便捷函数测试 ===')

    # 批量GET请求测试
    mylog.info('1. ahttp_get_all批量GET请求测试...')
    urls_to_test = test_urls[:3]  # 测试前3个URL
    results = ahttp_get_all(urls_to_test)

    for i, result in enumerate(results):
        mylog.info(f'批量GET{i + 1}结果: {type(result).__name__} - {result}')

    # 批量POST请求测试
    mylog.info('2. ahttp_post_all批量POST请求测试...')
    post_urls = [test_urls[1]] * 2  # 2个相同的POST URL
    results = ahttp_post_all(post_urls, data=post_data)

    for i, result in enumerate(results):
        mylog.info(f'批量POST{i + 1}结果: {type(result).__name__} - {result}')

    # 共享会话批量请求测试
    mylog.info('3. 共享会话批量请求测试...')
    results = ahttp_get_all(urls_to_test, force_sequential=True)

    for i, result in enumerate(results):
        mylog.info(f'共享会话批量{i + 1}结果: {type(result).__name__} - {result}')


def run_comprehensive_tests():
    """运行综合测试"""
    mylog.info('=' * 60)
    mylog.info('异步HTTP请求工具模块综合测试开始')
    mylog.info('=' * 60)

    # 运行同步测试
    test_basic_requests()
    test_error_handling()
    test_invalid_urls()
    test_custom_headers()
    test_timeout_handling()
    test_retry_mechanism()
    test_batch_functions()

    # 运行异步测试
    async def run_async_tests():
        await test_async_client_basic()
        await test_async_client_batch()
        await test_async_client_multi()
        await test_async_client_error_handling()

    asyncio.run(run_async_tests())

    mylog.info('=' * 60)
    mylog.info('异步HTTP请求工具模块综合测试完成')
    mylog.info('=' * 60)


if __name__ == '__main__':
    run_comprehensive_tests()
