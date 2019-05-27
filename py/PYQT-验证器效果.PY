'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-22 12:41:37
@LastEditors: Even.Sand
@LastEditTime: 2019-05-24 12:37:23
'''
# 导入，Qapplication，单行文本框，窗口，表单布局
from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, QFormLayout
# 导入文本校验器：整数校验器与浮点数校验器,其他自定义校验器
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QRegExpValidator

from PyQt5.QtCore import QRegExp
import sys


class lineEditDemo(QWidget):
    def __init__(self, parent=None):
        super(lineEditDemo, self).__init__(parent)
        self.setWindowTitle('QLineEdit例子')

        # 实例化表单布局
        flo = QFormLayout()

        # 创建三个文本框
        pIntLineEdit = QLineEdit()
        pDoubleLineEdit = QLineEdit()
        pValidatorLineEdit = QLineEdit()

        # 表单布局添加名称及控件
        flo.addRow('整型', pIntLineEdit)
        flo.addRow('浮点型', pDoubleLineEdit)
        flo.addRow('字母和数字', pValidatorLineEdit)

        # 设置文本框的默认浮现文本
        pIntLineEdit.setPlaceholderText('整型')
        pDoubleLineEdit.setPlaceholderText('浮点型')
        pValidatorLineEdit.setPlaceholderText('字母和数字')

        # 整型 范围 【1-99】

        # 实例化整型验证器，并设置范围为1-99
        pIntvalidator = QIntValidator(self)
        pIntvalidator.setRange(1, 99)

        # 浮点型 范围 【-360,360】，精度 小数点后两位

        # 实例化浮点验证器，设置范围-360到360
        pDoubleValidator = QDoubleValidator()
        pDoubleValidator.setRange(-360, 360)

        pDoubleValidator.setNotation(QDoubleValidator.StandardNotation)
        # 设置精度小数点后两位
        pDoubleValidator.setDecimals(2)

        # 字母和数字

        # 设置文本允许出现的字符内容
        reg = QRegExp('[a-zA-Z0-9]+$')
        # 自定义文本验证器
        pValidator = QRegExpValidator(self)
        # 设置属性
        pValidator.setRegExp(reg)

        # 设置验证器
        pIntLineEdit.setValidator(pIntvalidator)
        pDoubleLineEdit.setValidator(pDoubleValidator)
        pValidatorLineEdit.setValidator(pValidator)

        self.setLayout(flo)


'''
QHBoxLayout类中常用的方法如下
方法	描述
addLayout(self,stretch=0)	在窗口的右边添加布局，使用stretch（伸缩量）进行伸缩，伸缩量默认为0
addWidget(self,QWidget.stretch,Qt.Alignmeny alihnment)	在布局中添加控件
stretch（伸缩量），只适用于QBoxLayout，控件和窗口会随着伸缩量的变大而增大
alignment：指定的对齐方式
addSpacing(self,int)	设置各控件的上下间距，通过该方法可以增加额外的控件
---------------------
作者：jia666666
来源：CSDN
原文：https://blog.csdn.net/jia666666/article/details/81699900
版权声明：本文为博主原创文章，转载请附上博文链接！
'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = lineEditDemo()
    win.show()
    sys.exit(app.exec_())
