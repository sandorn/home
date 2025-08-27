# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-05-20 13:33:11
LastEditTime : 2025-08-15 08:35:03
FilePath     : /CODE/test/seleniumbase-test1.py
Github       : https://github.com/sandorn/home
==============================================================
"""

# from seleniumbase import SB

# with SB(test=True, uc=True) as sb:
#     sb.open("https://cn.bing.com")
#     sb.type('[title="Search"]', "SeleniumBase GitHub page\n")
#     sb.click('[href*="github.com/seleniumbase/"]')
#     sb.save_screenshot_to_logs()  # ./latest_logs/
#     print(sb.get_page_title())

import html2text

h = html2text.HTML2Text()

# 配置选项
h.ignore_links = True  # 忽略链接
h.ignore_images = True  # 忽略图片
h.body_width = 0  # 不限制行宽
h.ignore_emphasis = False  # 保留强调格式

html_content = """
<h2>产品介绍</h2>
<p>我们的<strong>新产品</strong>具有<em>革命性</em>的特性。</p>
<a href="http://example.com">了解更多</a>
<img src="image.jpg" alt="产品图片">
"""

result = h.handle(html_content)
print(result)