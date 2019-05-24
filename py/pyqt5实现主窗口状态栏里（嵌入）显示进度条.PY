'''
@Descripttion:
python3.x+pyqt5实现主窗口状态栏里（嵌入）显示进度条 - higher80的博客 - CSDN博客
https://blog.csdn.net/higher80/article/details/82703532
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-23 16:27:43
@LastEditors: Even.Sand
@LastEditTime: 2019-05-23 17:02:46
'''
from PyQt5.QtWidgets import QMainWindow, QProgressBar, QApplication, QLabel, \
    QStatusBar, QPushButton
from PyQt5.QtWidgets import QMainWindow, QProgressBar, QApplication, QLabel
import sys


class SampleBar(QMainWindow):
    def __init__(self, parent=None):
        super(SampleBar, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setMinimumSize(800, 600)
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('准备中...' * 20)
        self.pbar = QProgressBar()
        self.label = QLabel("进度： ")
        self.status_bar.addPermanentWidget(self.label)
        self.status_bar.addPermanentWidget(self.pbar)
        #self.progressBar.setGeometry(0, 0, 100, 5)
        self.pbar.setRange(0, 500)  # 设置进度条的范围
        self.pbar.setValue(100)
        self.show()


class SampleBar2(QMainWindow):

    def __init__(self, parent=None):
        super(SampleBar2, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setMinimumSize(800, 600)
        # File Menus & Status Bar:
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet('QStatusBar::item {border: none;}')
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('准备2')
        self.pbar = QProgressBar()
        self.label = QLabel()
        self.label.setText("进度2： ")
        #self.label2 = QLabel("label2： ")
        #self.statusBar.addWidget(self.label2, stretch=0)
        self.statusBar.addPermanentWidget(self.label, stretch=0)  # #关键，在状态栏中永久添加给定的窗口小控件对象
        self.statusBar.addPermanentWidget(self.pbar, stretch=0)  # #这两句的stretch是设置拉伸因子 stretch !=0  会挡住statusBar.showMessage
        # This is simply to show the bar
        # self.progressBar.setGeometry(0, 0, 100, 5)
        self.pbar.setRange(0, 500)  # 设置进度条的范围
        self.pbar.setValue(20)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main1 = SampleBar2()
    #main2 = SampleBar2()
    sys.exit(app.exec_())
