# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Software:   VSCode
@File    :   design.py
@Time    :   2019/05/04 13:13:39
@Author  :   Even Sand
@Version :   1.0
@Contact :   sandorn@163.com
@License :   (C)Copyright 2019-2019, NewSea
@Desc    :   None
'''

from PySide2.QtCore import QCoreApplication, QMetaObject
from PySide2.QtWidgets import QListWidget, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow


# 在Qt Designer中自动生成的代码，但需要部分修改
class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)
        # 唤醒窗口
        MainWindow.raise_()
        # 必须要手动创建一个总部件，并把子部件加载于此，否则会出现以下报错：
        # QLayout: Attempting to add QLayout "" to WoHeYunApp "MainWindow", which already has a layout
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.resize(400, 300)

        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(self.centralwidget)
        QMetaObject.connectSlotsByName(self.centralwidget)

        # 窗口自适应部件
        MainWindow.setCentralWidget(self.centralwidget)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Pick a folder"))


def main():
    # 创建新的实例应用
    app = QApplication(sys.argv)
    # 我们将表单设置为WoHeYunApp
    widgets = Ui_MainWindow()
    # 显示我们的表单
    #widgets.show()
    # 退出程序
    app.exec_()


# 如果我们直接运行文件而不是导入它，则执行
if __name__ == '__main__':
    main()
