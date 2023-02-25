# -*- coding: utf-8 -*-
import os
import sys

# from PySide2.QtWidgets import QApplication, QFileDialog, QMainWindow
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow


# 创建APP类，并继承UI的类
class WoHeYunApp(QMainWindow):
    # 初始化构造函数
    def __init__(self):
        # 继承： super指父类（子类，实例）.构造函数
        super(WoHeYunApp, self).__init__()
        self.setupUi(self)
        # 把UI中的控件连接函数功能（事件）
        self.pushButton.clicked.connect(self.browse_folder)

    # 功能函数
    def browse_folder(self):
        # 清除列表内容
        self.listWidget.clear()
        # 创建文件夹选择对话框
        directory = QFileDialog.getExistingDirectory(self, "Pick a folder")
        # 如果有范围的选择路径则搜索该路径下所有存在的文件，并将其名字加载都列表中
        if directory:
            for file_name in os.listdir(directory):
                self.listWidget.addItem(file_name)


# 创建实例
def main():
    # 创建新的实例应用
    app = QApplication(sys.argv)
    # 我们将表单设置为WoHeYunApp
    widgets = WoHeYunApp()
    # 显示我们的表单
    widgets.show()
    # 退出程序
    app.exec_()


# 如果我们直接运行文件而不是导入它，则执行
if __name__ == '__main__':
    main()
