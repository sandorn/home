# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, \
    QPushButton, QLineEdit, QLabel, QToolTip, QComboBox, QTextEdit


class MyBeautifulClass(QMainWindow):
    def __init__(self):
        super(MyBeautifulClass, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(1000, 800)
        self.setWindowTitle('Demo of PyQt5 QThread')
        self.btn_1 = QPushButton('start', self)
        self.btn_1.setGeometry(100, 100, 100, 50)
        self.btn_1.clicked.connect(self.slot_btn_1)
        self.linEdit_2 = QLineEdit(self)
        self.linEdit_2.setGeometry(100, 400, 300, 50)

    def slot_btn_1(self):
        self.mbt = MyBeautifulThread()
        self.mbt.trigger.connect(self.slot_thread)
        self.mbt.start()

    def say_love(self):
        print('say love')

    def slot_thread(self, msg_1, msg_2):
        self.linEdit_2.setText(msg_1 + msg_2)


class MyBeautifulThread(QThread):
    trigger = pyqtSignal(str, str)

    def __init__(self):
        super(MyBeautifulThread, self).__init__()

    def run(self):
        w = MyBeautifulClass()
        w.say_love()
        self.trigger.emit('Lo', 've')


def main():
    app = QApplication(sys.argv)
    w = MyBeautifulClass()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
