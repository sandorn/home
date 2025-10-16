from __future__ import annotations

from xthttp.resp import RespFactory
from xtlog import mylog


def run_test(url: str):
    """运行测试"""
    mylog.info('=' * 70)
    mylog.info(f'正在测试网址: {url}')

    try:
        # 导入get函数
        from xthttp.requ import get

        # 获取原始响应
        raw_response = get(url)

        # 创建统一响应对象
        unified_resp = RespFactory.create_response(raw_response)
        unified_resp.raise_for_status()

        mylog.info(f'响应状态: {unified_resp.status}|{unified_resp.index}')
        mylog.info(f'响应URL: {unified_resp.url}')
        mylog.info(f'响应编码: {unified_resp.encoding}')
        # 测试HTML解析功能
        title = unified_resp.xpath('//title/text()')
        mylog.info(f'页面标题: {title[0] if title and title[0] else "未找到"}')
        mylog.info(f'页面内容: {unified_resp.text[:100]}')

        # 增加更多的xpath测试内容
        xpath_result = unified_resp.xpath('//title/text()')
        mylog.info(f'xpath(//title/text()) : {xpath_result}')

        xpath_multi = unified_resp.xpath('//title/text()', '//title/text()')
        mylog.info(f'xpath([//title/text(), //title/text()]) : {xpath_multi}')

        query_result = unified_resp.query('title').text()
        mylog.info(f'query(title).text() : {query_result}')

        # 只有在DOM有效时才执行这个测试
        if unified_resp.dom is not None and hasattr(unified_resp.dom, 'xpath'):
            try:
                dom_result = unified_resp.dom.xpath('//title/text()')
                mylog.info(f'dom.xpath(//title/text()) : {dom_result}')
            except Exception as e:
                mylog.warning(f'direct dom.xpath failed: {e}')
        else:
            mylog.info('dom.xpath: DOM对象不可用')

        mylog.info('测试完成!')
    except Exception as e:
        mylog.error(f'测试失败: {e}')
        import traceback

        mylog.error(f'详细堆栈: {traceback.format_exc()}')


# 选择常用中文网址作为测试目标
test_urls = [
    'https://www.baidu.com',
    'https://www.sina.com.cn',
    'https://cn.bing.com',
]

# 运行测试
for url in test_urls:
    run_test(url)

mylog.info('\n\n所有测试完成!')
