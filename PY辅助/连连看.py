# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : [Python] 用python做一个游戏辅助脚本，完整思路 - 蜗牛噢 - 博客园
https://www.cnblogs.com/reader/p/10111777.html
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-07-25 09:28:00
#FilePath     : /PY辅助/连连看.py
#LastEditTime : 2020-07-25 09:52:16
#Github       : https://github.com/sandorn/home
#==============================================================
'''

import win32gui
import time
from PIL import ImageGrab, Image
import numpy as np
import operator
from pymouse import PyMouse


class GameAssist:
    def __init__(self, wdname):
        """初始化"""

        # 取得窗口句柄
        self.hwnd = win32gui.FindWindow(0, wdname)
        if not self.hwnd:
            print("窗口找不到，请确认窗口句柄名称：【%s】" % wdname)
            exit()

        # 窗口显示最前面
        win32gui.SetForegroundWindow(self.hwnd)

        # 小图标编号矩阵
        self.im2num_arr = []

        # 主截图的左上角坐标和右下角坐标
        self.scree_left_and_right_point = (299, 251, 768, 564)
        # 小图标宽高
        self.im_width = 39

        # PyMouse对象，鼠标点击
        self.mouse = PyMouse()

    def screenshot(self):
        """屏幕截图"""

        # 1、用grab函数截图，参数为左上角和右下角左标
        # image = ImageGrab.grab((417, 257, 885, 569))
        image = ImageGrab.grab(self.scree_left_and_right_point)

        # 2、分切小图
        # exit()
        image_list = {}
        offset = self.im_width  # 39

        # 8行12列
        for x in range(8):
            image_list[x] = {}
            for y in range(12):
                # print("show",x, y)
                # exit()
                top = x * offset
                left = y * offset
                right = (y + 1) * offset
                bottom = (x + 1) * offset

                # 用crop函数切割成小图标，参数为图标的左上角和右下角左边
                im = image.crop((left, top, right, bottom))
                # 将切割好的图标存入对应的位置
                image_list[x][y] = im

        return image_list

    def image2num(self, image_list):
        """将图标矩阵转换成数字矩阵"""

        # 1、创建全零矩阵和空的一维数组
        arr = np.zeros((10, 14), dtype=np.int32)  # 以数字代替图片
        image_type_list = []

        # 2、识别出不同的图片，将图片矩阵转换成数字矩阵
        for i in range(len(image_list)):
            for j in range(len(image_list[0])):
                im = image_list[i][j]

                # 验证当前图标是否已存入
                index = self.getIndex(im, image_type_list)

                # 不存在image_type_list
                if index < 0:
                    image_type_list.append(im)
                    arr[i + 1][j + 1] = len(image_type_list)
                else:
                    arr[i + 1][j + 1] = index + 1

        print("图标数：", len(image_type_list))

        self.im2num_arr = arr
        return arr

    # 检查数组中是否有图标,如果有则返回索引下表
    def getIndex(self, im, im_list):
        for i in range(len(im_list)):
            if self.isMatch(im, im_list[i]):
                return i

        return -1

    # 汉明距离判断两个图标是否一样
    def isMatch(self, im1, im2):

        # 缩小图标，转成灰度
        image1 = im1.resize((20, 20), Image.ANTIALIAS).convert("L")
        image2 = im2.resize((20, 20), Image.ANTIALIAS).convert("L")

        # 将灰度图标转成01串,即系二进制数据
        pixels1 = list(image1.getdata())
        pixels2 = list(image2.getdata())

        avg1 = sum(pixels1) / len(pixels1)
        avg2 = sum(pixels2) / len(pixels2)
        hash1 = "".join(map(lambda p: "1" if p > avg1 else "0", pixels1))
        hash2 = "".join(map(lambda p: "1" if p > avg2 else "0", pixels2))

        # 统计两个01串不同数字的个数
        match = sum(map(operator.ne, hash1, hash2))

        # 阀值设为10
        return match < 10

    # 判断矩阵是否全为0
    def isAllZero(self, arr):
        for i in range(1, 9):
            for j in range(1, 13):
                if arr[i][j] != 0:
                    return False
        return True

    # 是否为同行或同列且可连
    def isReachable(self, x1, y1, x2, y2):
        # 1、先判断值是否相同
        if self.im2num_arr[x1][y1] != self.im2num_arr[x2][y2]:
            return False

        # 1、分别获取两个坐标同行或同列可连的坐标数组
        list1 = self.getDirectConnectList(x1, y1)
        list2 = self.getDirectConnectList(x2, y2)
        # print(x1, y1, list1)
        # print(x2, y2, list2)

        # exit()

        # 2、比较坐标数组中是否可连
        for x1, y1 in list1:
            for x2, y2 in list2:
                if self.isDirectConnect(x1, y1, x2, y2):
                    return True
        return False

    # 获取同行或同列可连的坐标数组
    def getDirectConnectList(self, x, y):

        plist = []
        for px in range(0, 10):
            for py in range(0, 14):
                # 获取同行或同列且为0的坐标
                if self.im2num_arr[px][py] == 0 and self.isDirectConnect(x, y, px, py):
                    plist.append([px, py])

        return plist

    # 是否为同行或同列且可连
    def isDirectConnect(self, x1, y1, x2, y2):
        # 1、位置完全相同
        if x1 == x2 and y1 == y2:
            return False

        # 2、行列都不同的
        if x1 != x2 and y1 != y2:
            return False

        # 3、同行
        if x1 == x2 and self.isRowConnect(x1, y1, y2):
            return True

        # 4、同列
        if y1 == y2 and self.isColConnect(y1, x1, x2):
            return True

        return False

    # 判断同行是否可连
    def isRowConnect(self, x, y1, y2):
        minY = min(y1, y2)
        maxY = max(y1, y2)

        # 相邻直接可连
        if maxY - minY == 1:
            return True

        # 判断两个坐标之间是否全为0
        for y0 in range(minY + 1, maxY):
            if self.im2num_arr[x][y0] != 0:
                return False
        return True

    # 判断同列是否可连
    def isColConnect(self, y, x1, x2):
        minX = min(x1, x2)
        maxX = max(x1, x2)

        # 相邻直接可连
        if maxX - minX == 1:
            return True

        # 判断两个坐标之间是否全为0
        for x0 in range(minX + 1, maxX):
            if self.im2num_arr[x0][y] != 0:
                return False
        return True

    # 点击事件并设置数组为0
    def clickAndSetZero(self, x1, y1, x2, y2):
        # print("click", x1, y1, x2, y2)

        # (299, 251, 768, 564)
        # 原理：左上角图标中点 + 偏移量
        p1_x = int(self.scree_left_and_right_point[0] + (y1 - 1) * self.im_width + (self.im_width / 2))
        p1_y = int(self.scree_left_and_right_point[1] + (x1 - 1) * self.im_width + (self.im_width / 2))

        p2_x = int(self.scree_left_and_right_point[0] + (y2 - 1) * self.im_width + (self.im_width / 2))
        p2_y = int(self.scree_left_and_right_point[1] + (x2 - 1) * self.im_width + (self.im_width / 2))

        time.sleep(0.2)
        self.mouse.click(p1_x, p1_y)
        time.sleep(0.2)
        self.mouse.click(p2_x, p2_y)

        # 设置矩阵值为0
        self.im2num_arr[x1][y1] = 0
        self.im2num_arr[x2][y2] = 0

        print("消除：(%d, %d) (%d, %d)" % (x1, y1, x2, y2))
        # exit()

    # 程序入口、控制中心
    def start(self):

        # 1、先截取游戏区域大图，然后分切每个小图
        image_list = self.screenshot()

        # 2、识别小图标，收集编号
        self.image2num(image_list)

        print(self.im2num_arr)

        # 3、遍历查找可以相连的坐标
        while not self.isAllZero(self.im2num_arr):
            for x1 in range(1, 9):
                for y1 in range(1, 13):
                    if self.im2num_arr[x1][y1] == 0:
                        continue

                    for x2 in range(1, 9):
                        for y2 in range(1, 13):
                            # 跳过为0 或者同一个
                            if self.im2num_arr[x2][y2] == 0 or (x1 == x2 and y1 == y2):
                                continue
                            if self.isReachable(x1, y1, x2, y2):
                                self.clickAndSetZero(x1, y1, x2, y2)


if __name__ == "__main__":
    # wdname 为连连看窗口的名称，必须写完整
    wdname = u'宠物连连看经典版2,宠物连连看经典版2小游戏,4399小游戏 www.4399.com - Google Chrome'

    demo = GameAssist(wdname)
    demo.start()
