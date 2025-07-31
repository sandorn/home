# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-05-20 13:33:11
LastEditTime : 2025-07-17 10:22:08
FilePath     : /CODE/test/seleniumbase-test1.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from seleniumbase import SB

with SB(test=True, uc=True) as sb:
    sb.open("https://cn.bing.com")
    sb.type('[title="Search"]', "SeleniumBase GitHub page\n")
    sb.click('[href*="github.com/seleniumbase/"]')
    sb.save_screenshot_to_logs()  # ./latest_logs/
    print(sb.get_page_title())
