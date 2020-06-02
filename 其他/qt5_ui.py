# -*- coding: utf-8 -*-
"""
  ZetCode PyQt5 教程
  在这个例子中, 我们用PyQt5创建了一个简单的窗口。

  作者: Jan Bodnar
  网站: zetcode.com
 最后一次编辑: January 2015
"""

import sys
from PySide2.QtWidgets import QApplication, QWidget
#重点和秘诀就在这里，大家注意看
#from PyQt5.uic import loadUi

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    #loadUi('test.ui', w)  #看到没，瞪大眼睛看
    w.setWindowTitle('Simple')
    w.show()

sys.exit(app.exec_())
