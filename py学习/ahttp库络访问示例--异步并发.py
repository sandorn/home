# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-15 10:17:45
FilePath     : /CODE/py学习/asyncio学习/ahttp简单网络访问组件.py
Github       : https://github.com/sandorn/home
==============================================================
https://blog.csdn.net/getcomputerstyle/article/details/103014896
python ahttp：简单、高效、异步requests请求模块
'''
import ahttp

#urls = [f"https://movie.douban.com/top250?start={i*25}" for i in range(10)]
sess = ahttp.Session()

urlslist = [
    'https://www.biqukan.com/76_76572/526754921.html', 'https://www.biqukan.com/76_76572/526753588.html', 'https://www.biqukan.com/76_76572/526752995.html', 'https://www.biqukan.com/76_76572/526728684.html', 'https://www.biqukan.com/76_76572/526722644.html', 'https://www.biqukan.com/76_76572/526722178.html', 'https://www.biqukan.com/76_76572/526721667.html', 'https://www.biqukan.com/76_76572/526721173.html', 'https://www.biqukan.com/76_76572/526638294.html',
    'https://www.biqukan.com/76_76572/526637790.html', 'https://www.biqukan.com/76_76572/526491185.html', 'https://www.biqukan.com/76_76572/526491060.html', 'https://www.biqukan.com/76_76572/526490968.html', 'https://www.biqukan.com/76_76572/526490871.html', 'https://www.biqukan.com/76_76572/526490785.html', 'https://www.biqukan.com/76_76572/526490714.html', 'https://www.biqukan.com/76_76572/526490641.html', 'https://www.biqukan.com/76_76572/526490574.html',
    'https://www.biqukan.com/76_76572/526490494.html', 'https://www.biqukan.com/76_76572/526490419.html', 'https://www.biqukan.com/76_76572/526490344.html', 'https://www.biqukan.com/76_76572/526490278.html', 'https://www.biqukan.com/76_76572/526490233.html', 'https://www.biqukan.com/76_76572/526490158.html', 'https://www.biqukan.com/76_76572/526490114.html', 'https://www.biqukan.com/76_76572/526490061.html', 'https://www.biqukan.com/76_76572/526489994.html',
    'https://www.biqukan.com/76_76572/526489938.html', 'https://www.biqukan.com/76_76572/525386682.html', 'https://www.biqukan.com/76_76572/525386470.html', 'https://www.biqukan.com/76_76572/525386283.html', 'https://www.biqukan.com/76_76572/525386086.html', 'https://www.biqukan.com/76_76572/525385879.html', 'https://www.biqukan.com/76_76572/524870708.html', 'https://www.biqukan.com/76_76572/525385581.html', 'https://www.biqukan.com/76_76572/525385419.html',
    'https://www.biqukan.com/76_76572/525385315.html', 'https://www.biqukan.com/76_76572/525385213.html', 'https://www.biqukan.com/76_76572/525385088.html', 'https://www.biqukan.com/76_76572/525384998.html', 'https://www.biqukan.com/76_76572/525384892.html', 'https://www.biqukan.com/76_76572/525384773.html', 'https://www.biqukan.com/76_76572/525384704.html', 'https://www.biqukan.com/76_76572/525384630.html', 'https://www.biqukan.com/76_76572/525384570.html',
    'https://www.biqukan.com/76_76572/525384470.html', 'https://www.biqukan.com/76_76572/525384404.html', 'https://www.biqukan.com/76_76572/525384325.html', 'https://www.biqukan.com/76_76572/524355584.html', 'https://www.biqukan.com/76_76572/524355500.html', 'https://www.biqukan.com/76_76572/524355323.html', 'https://www.biqukan.com/76_76572/524355192.html', 'https://www.biqukan.com/76_76572/524355134.html', 'https://www.biqukan.com/76_76572/524355009.html',
    'https://www.biqukan.com/76_76572/524354950.html', 'https://www.biqukan.com/76_76572/524354719.html', 'https://www.biqukan.com/76_76572/524354616.html', 'https://www.biqukan.com/76_76572/524354527.html', 'https://www.biqukan.com/76_76572/524354211.html', 'https://www.biqukan.com/76_76572/524353967.html', 'https://www.biqukan.com/76_76572/523499318.html', 'https://www.biqukan.com/76_76572/523499217.html', 'https://www.biqukan.com/76_76572/523499128.html',
    'https://www.biqukan.com/76_76572/523499065.html', 'https://www.biqukan.com/76_76572/523320034.html', 'https://www.biqukan.com/76_76572/523319814.html', 'https://www.biqukan.com/76_76572/523319594.html', 'https://www.biqukan.com/76_76572/523319325.html', 'https://www.biqukan.com/76_76572/523319143.html', 'https://www.biqukan.com/76_76572/523318917.html', 'https://www.biqukan.com/76_76572/523318679.html', 'https://www.biqukan.com/76_76572/523318092.html',
    'https://www.biqukan.com/76_76572/522790776.html', 'https://www.biqukan.com/76_76572/522790572.html', 'https://www.biqukan.com/76_76572/522790509.html', 'https://www.biqukan.com/76_76572/522790409.html', 'https://www.biqukan.com/76_76572/522790303.html', 'https://www.biqukan.com/76_76572/522790171.html', 'https://www.biqukan.com/76_76572/522059621.html', 'https://www.biqukan.com/76_76572/522036693.html', 'https://www.biqukan.com/76_76572/522058567.html',
    'https://www.biqukan.com/76_76572/522058153.html', 'https://www.biqukan.com/76_76572/522057452.html', 'https://www.biqukan.com/76_76572/522056921.html', 'https://www.biqukan.com/76_76572/522056362.html', 'https://www.biqukan.com/76_76572/522055789.html', 'https://www.biqukan.com/76_76572/521786186.html', 'https://www.biqukan.com/76_76572/521785724.html', 'https://www.biqukan.com/76_76572/521785381.html', 'https://www.biqukan.com/76_76572/521784907.html',
    'https://www.biqukan.com/76_76572/521614998.html', 'https://www.biqukan.com/76_76572/521614782.html', 'https://www.biqukan.com/76_76572/521614631.html', 'https://www.biqukan.com/76_76572/521614401.html', 'https://www.biqukan.com/76_76572/521280891.html', 'https://www.biqukan.com/76_76572/521280749.html', 'https://www.biqukan.com/76_76572/521280139.html', 'https://www.biqukan.com/76_76572/521279911.html', 'https://www.biqukan.com/76_76572/521205635.html',
    'https://www.biqukan.com/76_76572/521205583.html', 'https://www.biqukan.com/76_76572/521205348.html', 'https://www.biqukan.com/76_76572/521205254.html', 'https://www.biqukan.com/76_76572/521205160.html', 'https://www.biqukan.com/76_76572/521205105.html', 'https://www.biqukan.com/76_76572/521205047.html', 'https://www.biqukan.com/76_76572/521204986.html', 'https://www.biqukan.com/76_76572/521204904.html', 'https://www.biqukan.com/76_76572/521204830.html',
    'https://www.biqukan.com/76_76572/521204778.html', 'https://www.biqukan.com/76_76572/521204705.html', 'https://www.biqukan.com/76_76572/520693240.html', 'https://www.biqukan.com/76_76572/520692891.html', 'https://www.biqukan.com/76_76572/520692329.html', 'https://www.biqukan.com/76_76572/520691994.html', 'https://www.biqukan.com/76_76572/520691543.html', 'https://www.biqukan.com/76_76572/520691157.html', 'https://www.biqukan.com/76_76572/520690925.html',
    'https://www.biqukan.com/76_76572/520690651.html', 'https://www.biqukan.com/76_76572/520690404.html', 'https://www.biqukan.com/76_76572/520690253.html', 'https://www.biqukan.com/76_76572/520689904.html', 'https://www.biqukan.com/76_76572/520689768.html', 'https://www.biqukan.com/76_76572/520689660.html', 'https://www.biqukan.com/76_76572/520689556.html', 'https://www.biqukan.com/76_76572/520689395.html', 'https://www.biqukan.com/76_76572/520689141.html',
    'https://www.biqukan.com/76_76572/520688988.html', 'https://www.biqukan.com/76_76572/520688658.html', 'https://www.biqukan.com/76_76572/520688518.html', 'https://www.biqukan.com/76_76572/520688391.html', 'https://www.biqukan.com/76_76572/520688119.html', 'https://www.biqukan.com/76_76572/520688002.html', 'https://www.biqukan.com/76_76572/520687929.html', 'https://www.biqukan.com/76_76572/520687837.html', 'https://www.biqukan.com/76_76572/519094324.html',
    'https://www.biqukan.com/76_76572/520687766.html', 'https://www.biqukan.com/76_76572/520687619.html', 'https://www.biqukan.com/76_76572/520687540.html', 'https://www.biqukan.com/76_76572/520687364.html', 'https://www.biqukan.com/76_76572/520687249.html', 'https://www.biqukan.com/76_76572/520687008.html', 'https://www.biqukan.com/76_76572/518907854.html', 'https://www.biqukan.com/76_76572/518907014.html', 'https://www.biqukan.com/76_76572/518906398.html',
    'https://www.biqukan.com/76_76572/518905612.html', 'https://www.biqukan.com/76_76572/518904898.html', 'https://www.biqukan.com/76_76572/518903663.html', 'https://www.biqukan.com/76_76572/518899482.html', 'https://www.biqukan.com/76_76572/518898342.html', 'https://www.biqukan.com/76_76572/518894012.html', 'https://www.biqukan.com/76_76572/518893378.html', 'https://www.biqukan.com/76_76572/518892832.html', 'https://www.biqukan.com/76_76572/518892371.html',
    'https://www.biqukan.com/76_76572/518891965.html', 'https://www.biqukan.com/76_76572/518891532.html', 'https://www.biqukan.com/76_76572/518890958.html', 'https://www.biqukan.com/76_76572/518890421.html', 'https://www.biqukan.com/76_76572/518890040.html', 'https://www.biqukan.com/76_76572/518889558.html', 'https://www.biqukan.com/76_76572/518888821.html', 'https://www.biqukan.com/76_76572/518888057.html', 'https://www.biqukan.com/76_76572/515133588.html',
    'https://www.biqukan.com/76_76572/515132986.html', 'https://www.biqukan.com/76_76572/515132042.html', 'https://www.biqukan.com/76_76572/515131279.html', 'https://www.biqukan.com/76_76572/515126986.html', 'https://www.biqukan.com/76_76572/515125698.html', 'https://www.biqukan.com/76_76572/515125061.html', 'https://www.biqukan.com/76_76572/515124069.html', 'https://www.biqukan.com/76_76572/515123657.html', 'https://www.biqukan.com/76_76572/515123311.html',
    'https://www.biqukan.com/76_76572/515123072.html', 'https://www.biqukan.com/76_76572/515122466.html'
]

tasks = [sess.get(url) for url in urlslist]

resps = ahttp.run(tasks, order=True)  # ahttp.run添加参数order=True顺序返回
for item in resps:
    print(item.url)
# 快速批量采集网络数据
# 173页面，耗时18秒
