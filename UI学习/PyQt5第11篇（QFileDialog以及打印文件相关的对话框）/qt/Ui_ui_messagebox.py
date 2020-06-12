# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yangff\Desktop\PyQt5\11\qt\ui_messagebox.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        Dialog.setSizeGripEnabled(True)
        self.pushButton_about = QtWidgets.QPushButton(Dialog)
        self.pushButton_about.setGeometry(QtCore.QRect(70, 170, 75, 23))
        self.pushButton_about.setObjectName("pushButton_about")
        self.pushButton_question = QtWidgets.QPushButton(Dialog)
        self.pushButton_question.setGeometry(QtCore.QRect(240, 170, 75, 23))
        self.pushButton_question.setObjectName("pushButton_question")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 50, 201, 41))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "关注微信公众号：学点编程吧"))
        self.pushButton_about.setText(_translate("Dialog", "关于Qt"))
        self.pushButton_question.setText(_translate("Dialog", "询问"))
        self.label.setText(_translate("Dialog", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

