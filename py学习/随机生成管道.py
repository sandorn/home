# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-05-11 10:41:47
LastEditTime : 2024-05-13 09:23:06
FilePath     : /CODE/py学习/随机生成管道.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_random_pipe(num_points, radius):
    # 计算角度
    theta = np.linspace(0, 2 * np.pi, num_points)

    # 计算管道上的点
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = np.zeros(num_points)

    # 创建一个3D图形对象
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 绘制管道
    ax.plot(x, y, z, color='b')

    # 设置图形范围
    ax.set_xlim(-radius, radius)
    ax.set_ylim(-radius, radius)
    ax.set_zlim(-radius, radius)

    # 设置图形标题
    ax.set_title('Random 3D Pipe')

    # 显示图形
    plt.show()

num_points = 50
radius = 1
generate_random_pipe(num_points, radius)
