'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-22 12:14:12
@LastEditors: Even.Sand
@LastEditTime: 2019-05-22 12:17:27
'''
from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, QFormLayout
import sys


class lineEditDemo(QWidget):
    def __init__(self, parent=None):
        super(lineEditDemo, self).__init__(parent)
        self.setWindowTitle('QLineEdit例子')

        # 实例化表单布局
        flo = QFormLayout()

        # 创建4个文本输入框
        PNormalLineEdit = QLineEdit()
        pNoEchoLineEdit = QLineEdit()
        pPasswordListEdit = QLineEdit()
        pPasswordEchoOnEditLineEdit = QLineEdit()

        # 添加到表单布局中
        # flo.addRow(文本名称（可以自定义），文本框)
        flo.addRow('Normal', PNormalLineEdit)
        flo.addRow('NoEcho', pNoEchoLineEdit)
        flo.addRow('Password', pPasswordListEdit)
        flo.addRow('PasswordEchoOnEdit', pPasswordEchoOnEditLineEdit)

        # 设置setPlaceholderText()文本框浮现的文字
        PNormalLineEdit.setPlaceholderText('Normal')
        pNoEchoLineEdit.setPlaceholderText('NoEcho')
        pPasswordListEdit.setPlaceholderText('Password')
        pPasswordEchoOnEditLineEdit.setPlaceholderText('PasswordEchoOnEdit')

        # setEchoMode()：设置显示效果

        # QLineEdit.Normal：正常显示所输入的字符，此为默认选项
        PNormalLineEdit.setEchoMode(QLineEdit.Normal)
        # QLineEdit.NoEcho：不显示任何输入的字符，常用于密码类型的输入，且长度保密
        pNoEchoLineEdit.setEchoMode(QLineEdit.NoEcho)
        # QLineEdit.Password：显示与平台相关的密码掩饰字符，而不是实际输入的字符
        pPasswordListEdit.setEchoMode(QLineEdit.Password)
        # QLineEdit.PasswordEchoOnEdit：在编辑时显示字符，负责显示密码类型的输入
        pPasswordEchoOnEditLineEdit.setEchoMode(QLineEdit.PasswordEchoOnEdit)

        # 设置窗口的布局
        self.setLayout(flo)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = lineEditDemo()
    win.show()
    sys.exit(app.exec_())
