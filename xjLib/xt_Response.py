# !/usr/bin/env python3
"""
==============================================================
模块名称     : xt_response.py
功能描述     : 网页响应封装模块 - 提供统一的HTTP响应处理、解析和数据提取功能
开发工具     : VSCode
作者         : Even.Sand
联系方式     : sandorn@163.com
创建时间     : 2022-12-22 17:35:56
最后修改时间 : 2025-09-19 17:30:00
文件路径     : /xjLib/xt_response.py
Github       : https://github.com/sandorn/home

【核心功能】
- BaseResponse: 基础响应类,提供通用的响应处理功能
- HtmlResponse: 扩展响应类,提供HTML解析和数据提取功能
- ACResponse: 异步响应类,专门处理aiohttp库的异步响应
- 支持多种解析方式: XPath、DOM、PyQuery、lxml等
- JSON数据解析与提取
- Unicode文本规范化和清理
- 自动编码检测与处理

【主要特性】
- 统一的响应对象接口,兼容requests和aiohttp等库
- 模块化设计,分离基础功能和扩展功能
- 健壮的错误处理和数据转换机制
- 丰富的文本处理功能,支持Unicode规范化
- 完善的类型注解,提升代码可读性和IDE支持
- 多级缓存机制,提高解析性能

【使用示例】
    >>> from xt_requests import get
    >>> response = get('https://example.com')
    >>> print(response.status)  # 获取状态码
    200
    >>> print(response.text[:100])  # 获取前100个字符的文本内容
    >>> title = response.xpath('//title/text()')[0][0]  # 使用XPath提取标题

【参数说明】
    - response: 原始HTTP响应对象(如requests.Response, aiohttp.ClientResponse)
    - content: 响应内容(字符串或字节流),可选
    - index: 响应对象的唯一标识符,可选

【注意事项】
    - 需要安装可选依赖: lxml, pyquery, requests_html, beautifulsoup4, chardet
    - 对于aiohttp响应,推荐使用ACResponse类
    - 编码检测依赖于chardet库,对于特殊编码内容可能需要手动指定编码
    - 部分功能需要安装相应依赖库才能使用
==============================================================
"""

from __future__ import annotations

# 导入统一响应处理模块
from xt_response_unified import UnifiedResponse

# 保持向后兼容性，重新导出原始类名
BaseResponse = UnifiedResponse
HtmlResponse = UnifiedResponse
ACResponse = UnifiedResponse

# 为保持向后兼容性，保留原来的htmlResponse名称
htmlResponse = HtmlResponse  # noqa

# 为了避免代码重复，现在所有功能都已在统一响应模块中实现
# 此处仅保留向后兼容的接口定义


if __name__ == '__main__':
    from xt_requests import get

    # 选择常用中文网址作为测试目标
    chinese_urls = [
        'https://www.baidu.com',  # 百度 - 中文搜索引擎
        'https://www.sina.com.cn',  # 新浪 - 综合门户网站
        'https://www.163.com',  # 网易 - 综合门户网站
        'https://www.zhihu.com',  # 知乎 - 问答社区
        'https://news.qq.com',  # 腾讯新闻 - 新闻网站
        'https://www.ctrip.com',  # 携程 - 旅游网站
        'https://www.jd.com',  # 京东 - 电商网站
    ]

    def test_base_attributes(response):
        """测试基础响应属性"""
        mylog.info('=' * 60)
        mylog.info(f'测试URL: {response.url} | 状态码: {response.status} | 编码: {response.encoding} | 响应对象类型: {type(response).__name__} | __repr__: {response!r}')
        mylog.info('请求头示例(前5个):')
        for _, (key, value) in enumerate(list(response.headers.items())[:1]):
            mylog.info(f'  {key}: {value}')
        mylog.info(f'Cookie数量: {len(response.cookies)}')
        if response.cookies:
            mylog.info(f'Cookie示例: {response.cookies.items()}')

    def test_html_parsing(response):
        """测试HTML解析功能"""
        mylog.info('-' * 50)
        # 测试标题解析
        title_xpath = '//title/text()'
        title_css = 'title'

        # 使用不同的解析方式获取标题
        mylog.info('页面标题解析:')
        try:
            dom_title = response.dom.xpath(title_xpath)[0] if response.dom.xpath(title_xpath) else 'N/A'
            mylog.info(f'  dom.xpath: {dom_title}')
        except Exception as e:
            mylog.error(f'  dom.xpath 解析失败: {e!s}')

        try:
            query_title = response.query(title_css).text() if response.query(title_css) else 'N/A'
            mylog.info(f'  query: {query_title}')
        except Exception as e:
            mylog.error(f'  query 解析失败: {e!s}')

        try:
            element_title = response.element.xpath(title_xpath)[0] if response.element.xpath(title_xpath) else 'N/A'
            mylog.info(f'  element.xpath: {element_title}')
        except Exception as e:
            mylog.error(f'  element.xpath 解析失败: {e!s}')

        try:
            html_title = response.html.xpath(title_xpath)[0] if response.html.xpath(title_xpath) else 'N/A'
            mylog.info(f'  html.xpath: {html_title}')
        except Exception as e:
            mylog.error(f'  html.xpath 解析失败: {e!s}')

        try:
            html_title = response.soup.select(title_css)[0].text if response.soup.select(title_css) else 'N/A'
            mylog.info(f'  soup.select: {html_title}')
        except Exception as e:
            mylog.error(f'  soup.select 解析失败: {e!s}')
        # 测试自定义xpath方法
        try:
            custom_xpath_title = response.xpath(title_xpath)[0][0] if response.xpath(title_xpath) else 'N/A'
            mylog.info(f'  自定义xpath方法: {custom_xpath_title}')
        except Exception as e:
            mylog.error(f'  自定义xpath方法 解析失败: {e!s}')

    def test_text_processing(response):
        """测试文本处理功能"""
        mylog.info('-' * 50)
        mylog.info('文本处理测试:')

        # 获取页面文本样本
        sample_text = response.text[:200] + '...' if len(response.text) > 200 else response.text
        mylog.info(f'原始文本样本: {sample_text}')

        # 测试clean_text
        clean_sample = response.clean_text[:200] + '...' if len(response.clean_text) > 200 else response.clean_text
        mylog.info(f'清理后文本样本: {clean_sample}')
        mylog.info(f'清理后文本样本2: {response.ctext[:200]}')

    def test_json_parsing(response):
        """测试JSON解析功能"""
        mylog.info('\n' + '-' * 50)
        mylog.info('\nJSON解析测试:')
        try:
            json_data = response.json
            if isinstance(json_data, dict) and json_data:
                mylog.info(f'JSON数据类型: {type(json_data)}')
                mylog.info(f'JSON键数量: {len(json_data)}')
                # 显示前5个键值对
                json_preview = dict(list(json_data.items())[:5])
                mylog.info(f'JSON数据预览: {json_preview}')
            else:
                mylog.info('响应内容不包含有效JSON数据')
        except Exception as e:
            mylog.error(f'JSON解析失败: {e!s}')

    def run_comprehensive_test(urls_to_test=None, max_urls=3):
        """运行全面测试,测试常用中文网站的响应处理"""
        if urls_to_test is None:
            urls_to_test = chinese_urls  # 默认测试前3个网址

        mylog.info('=' * 70)
        mylog.info('响应类综合测试 - 常用中文网站')

        for url in urls_to_test[:max_urls]:
            try:
                mylog.info('=' * 70)
                mylog.info(f'正在测试网站: {url}')

                # 获取响应
                response = get(url)

                # 测试基础属性
                # test_base_attributes(response)

                # 测试HTML解析
                test_html_parsing(response)

                # 测试文本处理
                # test_text_processing(response)

                # 测试JSON解析 (如果适用)
                # test_json_parsing(response)

            except Exception as e:
                mylog.error(f'测试失败: {e!s}')
        mylog.info('=' * 70)
        mylog.info('综合测试完成')

    # 导入日志模块
    from xtlog import mylog

    # 运行测试
    run_comprehensive_test(max_urls=2)

    # 提示用户使用新的统一响应模块
    mylog.info('\n\n注意: 该模块已迁移至新的统一响应处理框架!')
    mylog.info('建议在新项目中使用: from xt_response_unified import ResponseFactory, UnifiedResponse')
    mylog.info('ResponseFactory.create_response() 可以自动处理同步和异步响应对象')
