# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\PyQt5\source_code_for_pyqt5_tutorials\PyQt579\ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1001, 658)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pb_new = QtWidgets.QPushButton(self.centralWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icon/res/new.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.pb_new.setIcon(icon)
        self.pb_new.setObjectName("pb_new")
        self.horizontalLayout.addWidget(self.pb_new)
        self.pb_home = QtWidgets.QPushButton(self.centralWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icon/res/home.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.pb_home.setIcon(icon1)
        self.pb_home.setObjectName("pb_home")
        self.horizontalLayout.addWidget(self.pb_home)
        self.pb_forward = QtWidgets.QPushButton(self.centralWidget)
        self.pb_forward.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icon/res/forward.ico"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.pb_forward.setIcon(icon2)
        self.pb_forward.setObjectName("pb_forward")
        self.horizontalLayout.addWidget(self.pb_forward)
        self.pb_back = QtWidgets.QPushButton(self.centralWidget)
        self.pb_back.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(":/icon/res/back.ico"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.pb_back.setIcon(icon3)
        self.pb_back.setObjectName("pb_back")
        self.horizontalLayout.addWidget(self.pb_back)
        self.pb_refresh = QtWidgets.QPushButton(self.centralWidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap(":/icon/res/reload.ico"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.pb_refresh.setIcon(icon4)
        self.pb_refresh.setObjectName("pb_refresh")
        self.horizontalLayout.addWidget(self.pb_refresh)
        self.pb_stop = QtWidgets.QPushButton(self.centralWidget)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap(":/icon/res/stop.ico"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.pb_stop.setIcon(icon5)
        self.pb_stop.setObjectName("pb_stop")
        self.horizontalLayout.addWidget(self.pb_stop)
        self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.progressBar = QtWidgets.QProgressBar(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_2.addWidget(self.progressBar)
        self.pb_go = QtWidgets.QPushButton(self.centralWidget)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(":/icon/res/go.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.pb_go.setIcon(icon6)
        self.pb_go.setObjectName("pb_go")
        self.horizontalLayout_2.addWidget(self.pb_go)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(
            _translate("MainWindow", "关注微信公众号：学点编程--简单浏览器"))
        self.pb_new.setText(_translate("MainWindow", "新页面"))
        self.pb_home.setText(_translate("MainWindow", "主页"))
        self.pb_forward.setText(_translate("MainWindow", "前进"))
        self.pb_back.setText(_translate("MainWindow", "后退"))
        self.pb_refresh.setText(_translate("MainWindow", "刷新"))
        self.pb_stop.setText(_translate("MainWindow", "停止"))
        self.pb_go.setText(_translate("MainWindow", "GO"))


import res_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
