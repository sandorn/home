import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Window(QWidget):

    def __init__(self):
        # 初始化构造用户界面类的基础类，QWidget提供了默认的构造方法
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("劳资是标题")  # 设置窗口名
        self.resize(300, 300)  # 设置窗口大小
        self.move(500, 200)  # 设置窗口位置
        self.show()  #在屏幕上显示一个widget（窗口）


if __name__ == "__main__":
    # 所有应用必须创建一个应用（Application）对象
    app = QApplication(sys.argv)
    test = Window()
    sys.exit(app.exec_())