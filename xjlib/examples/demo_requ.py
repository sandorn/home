# !/usr/bin/env python
"""
==============================================================
Description  : HTTP请求工具模块示例代码
Develop      : VSCode
Author       : sandorn sandorn@live.cn
LastEditTime : 2025-10-15 22:00:00
Github       : https://github.com/sandorn/xthttp

本文件演示了HTTP请求工具模块的主要功能和用法
==============================================================
"""

from __future__ import annotations

from xthttp.requ import SessionClient, delete, get, head, options, patch, post, put
from xtlog import mylog

# 定义测试URL - 包含正常URL和错误URL
test_urls = [
    'https://httpbin.org/get',  # 正常GET请求
    'https://httpbin.org/post',  # 正常POST请求
    'https://httpbin.org/put',  # 正常PUT请求
    'https://httpbin.org/delete',  # 正常DELETE请求
    'https://httpbin.org/patch',  # 正常PATCH请求
    'https://httpbin.org/status/404',  # 404错误
    'https://httpbin.org/status/500',  # 500错误
    'https://httpbin.org/redirect/2',  # 重定向
]

# 无效URL - 用于测试URL验证功能
invalid_urls = [
    'http:/www.example.com',  # 缺少双斜杠
    'ftp://www.example.com',  # 不支持的协议
    'www.example.com',  # 缺少协议
    '://example.com',  # 空协议
    'https://',  # 空主机名
    '这不是一个URL',  # 完全无效的字符串
]

# POST测试数据
post_data = {'username': 'test_user', 'password': 'test_password', 'email': 'test@example.com'}

# JSON测试数据
json_data = {'title': 'Test Post', 'body': 'This is a test post body', 'userId': 1}


def test_basic_requests():
    """测试基本HTTP请求方法"""
    mylog.info('=== 基本HTTP请求方法测试 ===')

    # GET请求测试
    mylog.info('1. GET请求测试...')
    response = get(test_urls[0])
    mylog.info(f'GET请求成功: {response.url}')
    mylog.info(f'状态码: {response.status_code}')
    mylog.info(f'响应大小: {len(response.content)} bytes')

    # POST请求测试
    mylog.info('2. POST请求测试...')
    response = post(test_urls[1], data=post_data)
    mylog.info(f'POST请求成功: {response.url}')
    mylog.info(f'状态码: {response.status_code}')
    mylog.info(f'响应大小: {len(response.content)} bytes')

    # PUT请求测试
    mylog.info('3. PUT请求测试...')
    response = put(test_urls[2], json=json_data)
    mylog.info(f'PUT请求成功: {response.url}')
    mylog.info(f'状态码: {response.status_code}')

    # DELETE请求测试
    mylog.info('4. DELETE请求测试...')
    response = delete(test_urls[3])
    mylog.info(f'DELETE请求成功: {response.url}')
    mylog.info(f'状态码: {response.status_code}')

    # PATCH请求测试
    mylog.info('5. PATCH请求测试...')
    response = patch(test_urls[4], json={'title': 'Updated Title'})
    mylog.info(f'PATCH请求成功: {response.url}')
    mylog.info(f'状态码: {response.status_code}')

    # HEAD请求测试
    mylog.info('6. HEAD请求测试...')
    response = head(test_urls[0])
    mylog.info(f'HEAD请求成功: {response.url}')
    mylog.info(f'状态码: {response.status_code}')
    mylog.info(f'响应头: {dict(response.headers)}')

    # OPTIONS请求测试
    mylog.info('7. OPTIONS请求测试...')
    response = options(test_urls[0])
    mylog.info(f'OPTIONS请求成功: {response.url}')
    mylog.info(f'状态码: {response.status_code}')


def test_error_handling():
    """测试错误处理机制"""
    mylog.info('\n=== 错误处理机制测试 ===')

    # 404错误测试
    mylog.info('1. 404错误测试...')
    response = get(test_urls[5])
    mylog.info(f'404请求结果: {type(response).__name__} - {response}')

    # 500错误测试
    mylog.info('2. 500错误测试...')
    response = get(test_urls[6])
    mylog.info(f'500请求结果: {type(response).__name__} - {response}')

    # 重定向测试
    mylog.info('3. 重定向测试...')
    response = get(test_urls[7])
    mylog.info(f'重定向请求结果: {type(response).__name__} - {response}')


def test_invalid_urls():
    """测试无效URL处理"""
    mylog.info('\n=== 无效URL处理测试 ===')

    for i, invalid_url in enumerate(invalid_urls[:3]):  # 只测试前3个，避免输出过多
        mylog.info(f'{i + 1}. 测试无效URL: {invalid_url}')
        response = get(invalid_url)
        mylog.info(f'无效URL请求结果: {type(response).__name__} - {response}')


def test_custom_headers():
    """测试自定义请求头"""
    mylog.info('\n=== 自定义请求头测试 ===')

    custom_headers = {'User-Agent': 'Custom-Agent/1.0', 'X-Custom-Header': 'custom-value', 'Accept': 'application/json'}

    response = get(test_urls[0], headers=custom_headers)
    mylog.info(f'自定义请求头结果: {type(response).__name__} - {response}')


def test_timeout_handling():
    """测试超时处理"""
    mylog.info('\n=== 超时处理测试 ===')

    # 使用一个可能导致超时的URL，设置较短的超时时间
    timeout_url = 'https://httpbin.org/delay/5'

    response = get(timeout_url, timeout=2)  # 2秒超时
    mylog.info(f'超时测试结果: {type(response).__name__} - {response}')


def test_session_client():
    """测试SessionClient会话管理"""
    mylog.info('\n=== SessionClient会话管理测试 ===')

    with SessionClient() as client:
        # 测试链式调用语法
        mylog.info('1. 链式调用语法测试...')
        response = client.get(test_urls[0])
        mylog.info(f'链式GET请求结果: {type(response).__name__} - {response}')

        # 测试索引语法
        mylog.info('2. 索引语法测试...')
        response = client['post'](test_urls[1], data=post_data)
        mylog.info(f'索引POST请求结果: {type(response).__name__} - {response}')

        # 测试Cookie持久化
        mylog.info('3. Cookie持久化测试...')
        # 设置自定义Cookie
        client.update_cookies({'test_cookie': 'test_value'})
        response = client.get('https://httpbin.org/cookies/set?test=value')
        mylog.info(f'Cookie设置请求结果: {type(response).__name__} - {response}')

        # 验证Cookie是否被保存
        response2 = client.get('https://httpbin.org/cookies')
        mylog.info(f'Cookie验证结果: {type(response2).__name__} - {response2}')

        # 测试请求头持久化
        mylog.info('4. 请求头持久化测试...')
        custom_headers = {'X-Session-Header': 'session-value'}
        client.update_headers(custom_headers)

        response1 = client.get(test_urls[0])
        response2 = client.get(test_urls[1])

        mylog.info(f'第一个请求结果: {type(response1).__name__} - {response1}')
        mylog.info(f'第二个请求结果: {type(response2).__name__} - {response2}')


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
        response = get(url)
        mylog.info(f'重试测试结果: {type(response).__name__} - {response}')


def run_comprehensive_tests():
    """运行综合测试"""
    mylog.info('开始HTTP请求工具模块综合测试')
    mylog.info('=' * 60)

    # 运行各个测试模块
    test_basic_requests()
    test_error_handling()
    test_invalid_urls()
    test_custom_headers()
    test_timeout_handling()
    test_session_client()
    test_retry_mechanism()

    mylog.info('=' * 60)
    mylog.info('HTTP请求工具模块综合测试完成')


if __name__ == '__main__':
    run_comprehensive_tests()
