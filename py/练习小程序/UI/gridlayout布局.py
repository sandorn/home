# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Software :   VSCode
@File     :   gridlayout布局.py
@Time     :   2019/05/06 16:45:29
@Author   :   Even Sand
@Version  :   1.0
@Contact  :   sandorn@163.com
@License  :   (C)Copyright 2009-2019, NewSea
PyQt5：网格布局2(14) - 谁谁谁的专栏 - CSDN博客
https://blog.csdn.net/c3060911030/article/details/51551036
'''

#!/usr/bin/python
# gridlayout2.py
from PyQt5.QtWidgets import QApplication, QLineEdit, QLabel, QGridLayout
from PyQt5 import QtWidgets


class GridLayout(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self)

        self.setWindowTitle('grid layout')

        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')

        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QLineEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)
        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)
        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)

        self.setLayout(grid)
        self.resize(350, 300)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    qb = GridLayout()
    qb.show()
    sys.exit(app.exec_())
