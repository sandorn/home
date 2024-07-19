# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-06-17 13:40:58
LastEditTime : 2024-06-17 13:41:02
FilePath     : /CODE/xjLib/xt_Ui/windowspy.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os
import random

import qdarkstyle
from PyQt6.QtCore import QMetaObject, QSize, Qt, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QProgressBar, QStatusBar
from xt_file import qsstools
from xt_pyqt import event_loop
from xt_pyqt.part import xt_QLabel


class xt_QStatusBar(QStatusBar):
    """
    addPermanentWidget():永久信息窗口 - 不会被一般消息覆盖
    addWidget();//正常信息窗口 - 会被showMessage()的消息覆盖
    addPermanentWidget()	在状态栏中永久添加小控件对象
    removeWidget()	从状态栏中移除指定的小控件
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QStatusBar_{id(self)}")
        self.setSizeGripEnabled(False)  # 是否显示右边的大小控制点


class xt_QProgressBar(QProgressBar):
    step = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QProgressBar_{id(self)}")
        self.step.connect(self.step_by_step)
        # 主UI界面 self.signal.emit(value)  # 传递信号
        # #self.setInvertedAppearance(True) # 逆序
        # #self.setOrientation(Qt.Vertical)  # 垂直

    @event_loop
    def step_by_step(self, value):
        if isinstance(value, int) and value > self.maximum():
            value = self.maximum()

        if value is None or isinstance(value, str):  # #传入None或字符,则在原值上+1
            value = self.value() + 1

        self.setValue(int(value))


class xt_QMainWindow(QMainWindow):
    def __init__(self, title="MainWindow", action=True, tool=True, menu=True, status=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.basepath = os.path.dirname(__file__)
        # #窗体title,setupUI
        self.title = title
        self.setWindowTitle(title)
        self.setupUI()

        self.action_init() if action else ""
        self.tool_init() if tool else ""
        self.menu_init() if menu else ""
        self.status_progress_init() if status else ""

        QMetaObject.connectSlotsByName(self)  # @ 自动绑定信号和函数
        # !关键,用于自动绑定信号和函数  on_ObjectName_triggered
        """继承仍需声明,可能与控件生成顺序有关
        事件action:on_objectName_triggered
        按钮button:on_objectName_clicked
        不确定必须使用@PyQt5.QtCore.pyqtSlot()修饰要调用的函数
        手工绑定:connect(self.func)；解除绑定:disconnect()"""
        self.show()

    def setupUI(self):
        # #窗体icon,size...
        self.setWindowIcon(QIcon(f"{self.basepath}/ico/ico.ico"))
        availableGeometry = self.screen().availableGeometry()
        screen_width, screen_height = availableGeometry.width(), availableGeometry.height()
        self.resize(int(screen_width * 0.618), int(screen_height * 0.618))
        self.move(availableGeometry.center() - self.rect().center())
        qss = qdarkstyle.load_stylesheet_pyqt6() + "* {font: 10pt '微软雅黑';outline: none;}"
        self.setStyleSheet(qss)

    def action_init(self):  # #QAction
        self.Run_action = QAction(QIcon(f"{self.basepath}/ico/Execute.png"), "&Execute", self)
        self.Do_action = QAction(QIcon(f"{self.basepath}/ico/Performing.png"), "&Performing", self)
        self.Theme_action = QAction(QIcon(f"{self.basepath}/ico/color.ico"), "&Theme", self)
        self.Run_action.setObjectName("Run")
        self.Do_action.setObjectName("Do")
        self.Theme_action.setObjectName("Theme")
        self.Close_action = QAction(QIcon(f"{self.basepath}/ico/close.ico"), "&Quit", self)
        self.Run_action.setShortcut("Ctrl+E")
        self.Do_action.setShortcut("Ctrl+P")
        self.Theme_action.setShortcut("Ctrl+T")
        self.Close_action.setShortcut("Ctrl+Q")
        # self.Close_action.setToolTip('Close the window')
        # self.Close_action.setStatusTip('Close the window')
        self.Close_action.triggered.connect(QApplication.quit)

    def tool_init(self):  # #工具栏
        self.file_toolbar = self.addToolBar("")
        self.file_toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        """
        Qt.ToolButtonIconOnly：仅显示图标，没有文本。
        Qt.ToolButtonTextOnly：仅显示文本，没有图标。
        Qt.ToolButtonTextBesideIcon：图标和文本并排显示。
        Qt.ToolButtonTextUnderIcon：图标在上方，文本在下方显示。
        """
        self.file_toolbar.addAction(self.Run_action)
        self.file_toolbar.addSeparator()  # 分隔线
        self.file_toolbar.addAction(self.Do_action)
        self.file_toolbar.addSeparator()  # 分隔线
        self.file_toolbar.addAction(self.Theme_action)
        self.file_toolbar.addSeparator()  # 分隔线
        self.file_toolbar.addAction(self.Close_action)
        self.file_toolbar.addSeparator()  # 分隔线
        self.file_toolbar.setMovable(False)
        self.file_toolbar.setFloatable(False)
        self.file_toolbar.setIconSize(QSize(36, 36))
        self.file_toolbar.setStyleSheet("QToolBar{spacing:16px;}")
        self.file_toolbar.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)  # ActionsContextMenu

    def menu_init(self):  # #菜单栏
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)  # 全平台一致的效果
        self.file_menu = menubar.addMenu("菜单")
        self.file_menu.addAction(self.Run_action)
        self.file_menu.addAction(self.Do_action)
        self.file_menu.addAction(self.Theme_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.Close_action)

    def status_progress_init(self):  # #状态栏、进度条
        self.status1 = xt_QStatusBar()
        self.status2 = xt_QLabel()
        self.status3 = xt_QLabel()
        self.pbar = xt_QProgressBar()
        _statusBar = self.statusBar()
        _statusBar.setSizeGripEnabled(False)
        _statusBar.addWidget(self.status1, stretch=1)
        _statusBar.addWidget(self.status2, stretch=1)
        _statusBar.addWidget(self.status3, stretch=1)
        _statusBar.addWidget(self.pbar, stretch=1)
        self.status1.showMessage("Ready to compose")

    @pyqtSlot()
    def on_Run_triggered(self):
        # print('on_Run_triggered')
        ...

    @pyqtSlot()
    def on_Do_triggered(self):
        # print('on_Do_triggered')
        ...

    def on_Theme_triggered(self):
        # print('on_Theme_triggered')
        qss_list = [f"{self.basepath}/qss/blue.qss", f"{self.basepath}/qss/css.qss", f"{self.basepath}/qss/dark_orange.qss", f"{self.basepath}/qss/dark.qss", f"{self.basepath}/qss/grey.qss", f"{self.basepath}/qss/qdark.qss"]
        file_name = random.choice(qss_list)
        self.setWindowTitle(f"{self.title}--" + file_name.split("/")[-1].split(".")[0])
        qsstools.set(file_name, self)


if __name__ == "__main__":
    import sys

    from PyQt6.QtWidgets import QApplication, QMainWindow, QProgressBar, QStatusBar
    # from PyQt6.QtWidgets import  QHBoxLayout, QVBoxLayout, QWidget

    app = QApplication(sys.argv)
    win = xt_QMainWindow()
    # tab = xt_QFileDialog()  # ['A', 'B', 'C', 'D'])
    # hlayout = QHBoxLayout()
    # hlayout.addWidget(tab)
    # vlayout = QVBoxLayout()
    # vlayout.addLayout(hlayout)
    # widget = QWidget()
    # widget.setLayout(vlayout)
    # win.setCentralWidget(widget)
    sys.exit(app.exec())
