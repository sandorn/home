# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-12 17:13:40
#LastEditTime : 2020-05-20 21:31:10
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''
# package
# __init__.py

__author__ = 'Even.Sand'
__license__ = 'NewSea'

xjLib_VERSION = __version__ = '0.0.2'

__all__ = [
    'EventLoop', "xt_QStatusBar", "xt_QTableWidget", "xt_QPushButton", "main_UI"
]

import os
import sys
from functools import wraps

from PyQt5.QtCore import (QEventLoop, QMetaObject, QSize, Qt, QThread,
                          pyqtSignal, pyqtSlot)
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QDesktopWidget, QHBoxLayout,
                             QHeaderView, QListView, QListWidget, QMainWindow,
                             QProgressBar, QPushButton, QStatusBar,
                             QTableWidget, QTableWidgetItem, QTabWidget,
                             QVBoxLayout, QWidget, qApp)

from xjLib.mystr import qsstools
import qdarkstyle
import random


def EventLoop(function):
    '''定义一个装饰器,确定鼠标显示和控制权'''

    @wraps(function)
    def _run(*args, **kwargs):
        # @忽略用户的输入（鼠标和键盘事件）,显示等待中的鼠标样式
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
        QApplication.setOverrideCursor(Qt.WaitCursor)

        result = function(*args, **kwargs)

        # @交还控制权,恢复鼠标样式
        qApp.processEvents()
        QApplication.restoreOverrideCursor()
        return result

    return _run


class xt_QStatusBar(QStatusBar):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QStatusBar_{id(self)}")


class xt_QProgressBar(QProgressBar):
    step = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QProgressBar_{id(self)}")
        self.step.connect(self.step_by_step)
        # #self.signal.emit(value)  # 传递信号
        # #self.setInvertedAppearance(True) # 逆序
        # #self.setOrientation(Qt.Vertical)  # 垂直

    @EventLoop
    def step_by_step(self, value):
        if type(value) == int and value > self.maximum():
            value = self.maximum()

        if value is None or type(value) == str:  # #传入None或字符，则在原值上+1
            value = self.value() + 1

        self.setValue(int(value))


class xt_QTableWidget(QTableWidget):
    '''ColumnsName按顺序传递，不用='''

    def __init__(self, ColumnsName=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QTableWidget_{id(self)}")
        self.verticalHeader().setFixedWidth(40)
        self.row_name_show = True  # #行名显示标志
        self.column_name_show = True  # #列名显示标志
        #TODO 设置垂直方向的表头标签
        self.setColumnsName(ColumnsName)
        #TODO 设置其他优化
        # self.设置各列分布()
        self.设置末列填充()
        self.表格禁止编辑()
        self.设置整行选中()
        self.多行选择()
        self.自动匹配宽高()
        self.表头排序()
        self.颜色交替()
        self.双向滚动条()

    def 设置各列分布(self):
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def 设置末列填充(self):
        self.horizontalHeader().setStretchLastSection(True)

    def 表格禁止编辑(self):
        self.setEditTriggers(QTableWidget.NoEditTriggers)

    def 禁止点击表头(self):
        self.horizontalHeader().setSectionsClickable(False)

    def 设置整行选中(self):
        self.setSelectionBehavior(QTableWidget.SelectRows)

    def 自动匹配宽高(self):
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def 单行选择(self):
        self.setSelectionMode(QTableWidget.SingleSelection)

    def 多行选择(self):
        # shift键的连续选择
        self.setSelectionMode(QTableWidget.ExtendedSelection)
        '''
        QTableWidget.NoSelection 不能选择
        QTableWidget.SingleSelection 选中单个目标
        QTableWidget.MultiSelection 选中多个目标
        QTableWidget.ExtendedSelection shift键的连续选择
        QTableWidget.ContiguousSelection ctrl键的不连续的多个选择
        '''

    def 表头排序(self):
        self.des_sort = True  # #排序标志
        self.setSortingEnabled(True)

    def 颜色交替(self):
        self.setAlternatingRowColors(True)

    def 双向滚动条(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def addWidget(self, row, column, widget):
        #TODO 在单元格内放置控件
        #comBox=QComboBox()
        #comBox.addItems(['男','女'])
        #comBox.addItem('未知')
        #self.setCellWidget(0,1,comBox)
        self.setCellWidget(row, column, widget)

    def columnsNameShow(self):
        #TODO 水平表头隐藏
        self.column_name_show = not self.column_name_show  # #列名显示标志
        self.horizontalHeader().setVisible(self.column_name_show)
        return self.column_name_show

    def rowsNameShow(self):
        #TODO 竖直表头隐藏
        self.row_name_show = not self.row_name_show  # #行名显示标志
        self.verticalHeader().setVisible(self.row_name_show)
        return self.row_name_show

    def setColumnsName(self, Columnslist):
        #TODO 设置水平表头
        self.setHorizontalHeaderLabels(Columnslist)

    def setColumnName(self, column, ColumnName):
        #TODO 设置单一水平表头
        self.setHorizontalHeaderItem(column, QTableWidgetItem(str(ColumnName)))

    def setRowsName(self, Rowslist):
        #TODO 设置竖直表头
        self.setVerticalHeaderLabels(Rowslist)

    def setRowName(self, row, RowName):
        #TODO 设置单一竖直表头
        self.setVerticalHeaderItem(row, QTableWidgetItem(str(RowName)))

    def setSort(self, sbool=None):
        #TODO 设置单一竖直表头
        if sbool is None:
            self.des_sort = not self.des_sort
        else:
            self.des_sort = sbool

        self.setSortingEnabled(self.des_sort)
        return self.des_sort

    @EventLoop
    def appendItem(self, itemlist):
        # #取消自动排序
        self.setSortingEnabled(False)

        if isinstance(itemlist, list):
            row = self.rowCount()
            self.insertRow(row)

            for column, item in enumerate(itemlist):
                self.setItem(row, column, QTableWidgetItem(str(item)))

            # $滚动到最下面
            self.scrollToBottom()

        # #恢复排序设置
        self.setSort(self.des_sort)

    @EventLoop
    def appendItemList(self, recolist):
        if isinstance(recolist, list) and isinstance(recolist[0], list):
            for record in recolist:
                self.appendItem(record)

    @EventLoop
    def empty(self):
        [self.removeRow(0) for _ in range(self.rowCount())]


class xt_QListWidget(QListWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QListWidget_{id(self)}")
        self.setMovement(QListView.Static)  #设置单元项不可拖动，
        self.setViewMode(QListView.IconMode)  # 图标格式显示
        self.setIconSize(QSize(50, 50))  # 图标大小
        self.setMaximumWidth(405)  # 最大宽度
        self.setSpacing(15)  # 间距大小
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # 垂直滚动条
        self.itemClicked.connect(self.itemClicked_event)  #绑定点击事件
        self.itemDoubleClicked.connect(self.itemDoubleClicked_event)  #绑定双击事件

    def itemClicked_event(self, item):
        self._item_temp = item

    def itemDoubleClicked_event(self, item):
        self._item_temp = item

    '''
    方法	描述
    resize()
    addItem()	在列表中添加QListWidgetItem对象或字符串
    addItems()	添加列表中的每个条目
    insertItem()	在指定地索引处插入条目
    clear()	删除列表的内容
    setCurrentItem()	设置当前所选的条目
    sortItems()	按升序重新排列条目
    QLIstWidget类中常用的信号
    信号	含义
    currentItemChanged	当列表中的条目发生改变时发射此信号
    itemClicked	当点击列表中的条目时发射此信号
    '''


class xt_QTabWidget(QTabWidget):
    '''textlist 按顺序传递，不用='''

    def __init__(self, textlist=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QTabWidget_{id(self)}")
        self.setTabShape(QTabWidget.Triangular)  ## 页签样式
        # self.setTabsClosable(True)  ## 关闭按钮
        self.tabCloseRequested.connect(self.tabCloseRequested_event)
        #创建选项卡控件
        self.tab = {}
        if isinstance(textlist, list):
            for index in range(len(textlist)):
                self.tab[index] = QWidget()
                self.addTab(self.tab[index], textlist[index])

        elif isinstance(int(textlist), int):
            for index in range(int(textlist)):
                self.tab[index] = QWidget()
                self.addTab(self.tab[index], 'TAB_' + str(index))
        else:
            self.addTab(self.tab[0], 'TAB_0')

        self.stylestring = self.styleSheet()
        self.currentChanged.connect(self.currentChanged_event)
        self.tabBarDoubleClicked.connect(self.tabBarDoubleClicked_event)

    def currentChanged_event(self, index):
        # print(f'切换页面为:{index}')
        pass

    def tabCloseRequested_event(self, index):
        self.removeTab(index)

    def tabBarDoubleClicked_event(self, index):
        self.removeTab(index)

    #@动态调整tab页签宽度
    def resizeEvent(self, event):
        # print(self.styleSheet())
        _tabCount = self.count()
        if _tabCount == 0:
            return
        _tabWidth = round(self.width() / _tabCount)
        self.setStyleSheet(self.stylestring +
                           "QTabBar::tab{width:%upx;}" % _tabWidth)

    '''
    方法	描述
    setCurrentWidget()	设置当前可见的界面
    setTabBar()	设置选项卡栏的小控件
    QTabWidget类中的常用信号

    1.void setTabText(int, QString); //设置页面的名字.
    2.void setTabToolTip(QString); //设置页面的提示信息.
    3.void setTabEnabled(bool); //设置页面是否被激活.
    4.void setTabPosition(QTabPosition::South); //设置页面名字的位置.
    5.void setTabsClosable(bool); //设置页面关闭按钮。
    6.int currentIndex(); //返回当前页面的下标，从0开始.
    7.int count(); //返回页面的数量.
    8.void clear(); //清空所有页面.
    9.void removeTab(int); //删除页面.
    10.addTab()	将一个控件添加到Tab控件的选项卡中
    11.insertTab()	将一个Tab控件的选项卡插入到指定的位置
    12.void setMoveable(bool); //设置页面是否可被拖拽移动.
    13.void setCurrentIndex(int); //设置当前显示的页面.

    signals:
    1.void tabCloseRequested(int). //当点击第参数个选项卡的关闭按钮的时候，发出信号
                                    配合setTabsClosable(true)
    2.void tabBarClicked(int). //当点击第参数个选项卡的时候，发出信号.
    3.void currentChanged(int). //当改变第参数个选项卡的时候，发出信号.
    4.void tabBarDoubleClicked(int). //当双击第参数个选项卡的时候，发出信号
    '''


class xt_QPushButton(QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QPushButton_{id(self)}")
        self.clicked.connect(self.clicked_event)

    def clicked_event(self):
        # #print('QPushButton_clicked_event')
        pass

    '''
    事件信号： clicked、pressed、released
    '''


class xt_menu():

    def __init___(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName('xt_QPushButton')
        statusbarAct = QAction('View statusbar', self, checkable=True)
        statusbarAct.setStatusTip('View statusbar')
        statusbarAct.setChecked(True)  # True为默认选中状态
        statusbarAct.triggered.connect(self.toggleMenu)


class xt_QMainWindow(QMainWindow):

    def __init__(self,
                 title="MainWindow",
                 status=True,
                 menu=True,
                 action=True,
                 FramelessWindowHint=True,
                 TranslucentBackground=False,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        # #窗体title,setupUI
        self.setWindowTitle(title)
        self.setupUI()

        if status:
            self.status_progress_init()
        if action:
            self.action_init()
        if menu:
            self.menu_tool_init()
        if TranslucentBackground:
            self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        if FramelessWindowHint:
            self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏边框
        else:
            '''恢复event'''
            self.mousePressEvent = super().mousePressEvent
            self.mouseMoveEvent = super().mouseMoveEvent
            self.mouseReleaseEvent = super().mouseReleaseEvent
        # @用于自动绑定信号和函数
        QMetaObject.connectSlotsByName(self)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        # qsstools.set('./xjLib/xt_ui/blue.qss', self)
        self.show()

    def setupUI(self):
        # #窗体icon,size...
        self.icon_path = os.path.dirname(__file__) + '\ico\\'
        self.setWindowIcon(QIcon(self.icon_path + 'ico.ico'))
        self.setMinimumSize(800, 600)
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        # #居中设置  # setGeometry
        deskSize = QDesktopWidget().screenGeometry()  #获取桌面窗体参数
        windowSize = self.geometry()  #获取窗体本身参数
        self.move(
            int((deskSize.width() - windowSize.width()) / 2),
            int((deskSize.height() - windowSize.height()) / 2))

    #@重写事件，响应拖动
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def status_progress_init(self):
        # #状态栏、进度条
        _statusBar = self.statusBar()
        self.statusBar = xt_QStatusBar()
        self.statusBar.showMessage('Ready to compose')
        self.pbar = xt_QProgressBar()
        _statusBar.addPermanentWidget(self.statusBar, stretch=100)
        _statusBar.addPermanentWidget(self.pbar, stretch=100)

    def action_init(self):
        # #QAction
        # _path = os.path.dirname(__file__) + '/'
        self.open_action = QAction(
            QIcon(self.icon_path + 'open.ico'), 'Open', self)
        self.save_action = QAction(
            QIcon(self.icon_path + 'save.ico'), 'Save', self)
        self.run_action = QAction(
            QIcon(self.icon_path + 'run.ico'), 'Theme', self)
        self.open_action.setObjectName("openObject")
        self.save_action.setObjectName("saveObject")
        self.run_action.setObjectName("runObject")
        # !必须,关键，用于自动绑定信号和函数  on_ObjectName_triggered
        # !配套：QMetaObject.connectSlotsByName(self)
        self.close_action = QAction(
            QIcon(self.icon_path + 'close.ico'), 'Close', self)

        self.open_action.setShortcut('Ctrl+O')
        self.save_action.setShortcut('Ctrl+S')
        self.run_action.setShortcut('Ctrl+R')
        self.close_action.setShortcut('Ctrl+Q')
        self.close_action.setToolTip('Close the window')
        self.close_action.setStatusTip('Close the window')
        self.close_action.triggered.connect(qApp.quit)

    def menu_tool_init(self):
        # #菜单栏
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)  # 全平台一致的效果
        self.file_menu = menubar.addMenu('menu')
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.run_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.close_action)
        # #工具栏
        self.file_toolbar = self.addToolBar('ToolBar')
        self.file_toolbar.setToolButtonStyle(3)  # @同时显示文字和图标
        self.file_toolbar.setFixedHeight(64)
        self.file_toolbar.addAction(self.open_action)
        self.file_toolbar.addSeparator()  # 分隔线
        self.file_toolbar.addAction(self.save_action)
        self.file_toolbar.addSeparator()  # 分隔线
        self.file_toolbar.addAction(self.run_action)
        self.file_toolbar.addSeparator()  # 分隔线
        self.file_toolbar.addAction(self.close_action)
        self.file_toolbar.addSeparator()  # 分隔线
        '''
        工具栏中的按钮事件：actionTriggered
        '''

    @pyqtSlot()
    def on_openObject_triggered(self):
        # #根据名称绑定的函数
        pass

    @pyqtSlot()
    def on_saveObject_triggered(self):
        # #根据名称绑定的函数
        pass

    @pyqtSlot()
    def on_runObject_triggered(self):
        # #根据名称绑定的函数
        qss_list = [
            'd:/CODE/xjLib/xt_ui/blue.qss',
            'd:/CODE/xjLib/xt_ui/css.qss',
            'd:/CODE/xjLib/xt_ui/dark_orange.qss',
            'd:/CODE/xjLib/xt_ui/dark.qss',
            'd:/CODE/xjLib/xt_ui/grey.qss',
            'd:/CODE/xjLib/xt_ui/qdark.qss',
            'd:/CODE/xjLib/xt_ui/white.qss',
        ]
        qsstools.set(random.choice(qss_list), self)

        rrr = qdarkstyle.load_stylesheet_pyqt5()
        print(rrr)
        # self.setStyleSheet()
        pass

    '''
    #@setWindowFlags(Qt.WindowFlags|Qt.WindowFlags)
    PYQT基本窗口类型有如下类型：
    Qt.Qt.Widget#插件默认窗口，有最小化、最大化、关闭按钮
    Qt.Qt.Window#普通窗口，有最小化、最大化、关闭按钮
    Qt.Qt.Dialog#对话框窗口，有问号和关闭按钮
    Qt.Qt.Popup#弹出窗口，窗口无边框化
    Qt.Qt.ToolTip#提示窗口，窗口无边框化，无任务栏窗口
    Qt.Qt.SplashScreen#飞溅屏幕，窗口无边框化，无任务栏窗口
    Qt.Qt.SubWindow#子窗口，窗口无按钮但有标题栏

    自定义外观的顶层窗口标志：
    Qt.Qt.MSWindowsFixedSizeDialogHint#窗口无法调整大小
    Qt.Qt.FramelessWindowHint#窗口无边框化
    Qt.Qt.CustomizeWindowHint#有边框但无标题栏和按钮，不能移动和拖动
    Qt.Qt.WindowTitleHint#添加标题栏和一个关闭按钮
    Qt.Qt.WindowSystemMenuHint#添加系统目录和一个关闭按钮
    Qt.Qt.WindowMaximizeButtonHint#激活最大化和关闭按钮，禁止最小化按钮
    Qt.Qt.WindowMinimizeButtonHint#激活最小化和关闭按钮，禁止最大化按钮
    Qt.Qt.WindowMinMaxButtonsHint#激活最小化、最大化和关闭按钮，
    #相当于Qt.Qt.WindowMaximizeButtonHint|Qt.Qt.WindowMinimizeButtonHint
    Qt.Qt.WindowCloseButtonHint#添加一个关闭按钮
    Qt.Qt.WindowContextHelpButtonHint#添加问号和关闭按钮，像对话框一样
    Qt.Qt.WindowStaysOnTopHint#窗口始终处于顶层位置
    Qt.Qt.WindowStaysOnBottomHint#窗口始终处于底层位置
    Qt.Qt.Tool 有一个小小的关闭按钮
    '''


if __name__ == '__main__':

    class Example(xt_QMainWindow):

        def __init__(self):
            super().__init__()
            self.create_UI()
            self.retranslateUi()

        def create_UI(self):
            self.btn = xt_QPushButton('Start==', self)
            self.btn1 = xt_QPushButton('Start!=', self)
            self.btn3 = xt_QPushButton('<-Start->', self)
            self.table = xt_QTableWidget([], 10, 5)
            self.tabw = xt_QTabWidget(2)
            self.btn.move(40, 80)
            self.btn.clicked.connect(self.tabls)
            self.btn1.clicked.connect(self.tabls2)
            self.btn3.clicked.connect(self.getDatas)

        def retranslateUi(self):
            # #设置窗口布局
            vlayout1 = QVBoxLayout()
            vlayout1.addWidget(self.btn)
            vlayout1.addWidget(self.btn1)
            vlayout1.addWidget(self.btn3)
            vlayout1.addWidget(self.tabw)
            hlayout = QHBoxLayout()
            hlayout.addLayout(vlayout1)
            hlayout.addWidget(self.table)
            # hlayout各控件的比例
            hlayout.setStretchFactor(vlayout1, 1)
            hlayout.setStretchFactor(self.table, 3)
            hlayout.setSpacing(1)  # 设置控件间距
            vlayout = QVBoxLayout()
            vlayout.addLayout(hlayout)
            widget = QWidget()
            widget.setLayout(vlayout)
            self.setCentralWidget(widget)

        def getDatas(self):
            for i in range(50):
                self.pbar.step.emit('adfrgagaew')
                self.pbar.step.emit(None)

            QThread.msleep(200)
            self.pbar.step.emit(0)
            QThread.msleep(200)
            self.pbar.step.emit(60)
            QThread.msleep(200)
            self.pbar.step.emit(120)
            QThread.msleep(200)
            self.pbar.step.emit(30)

        def tabls(self):
            self.table.empty()
            self.table.appendItem(['1', '记录一'])
            self.table.appendItem(['2', '记录2', 2, 3, 4, 5])
            self.table.appendItemList(
                [['3', '记录3'], ['4', '记录4'],
                 ['5', '记录5', 'djahd', 'ihviairh' * 5, 'ohv7384' * 3]])
            r = []
            for i in range(10):
                r.append([i * 10, '记录' * 10 + str(i * 10)])
                # self.table.appendItem([i * 10, '记录' + str(i * 10)])
            # print(r)
            self.table.appendItemList(r)
            self.table.setColumnName(0, '张三')
            self.table.setRowName(0, '张4')
            self.table.setColumnWidth(0, 60)
            self.table.setColumnWidth(1, 200)
            self.table.setColumnWidth(2, 150)
            self.table.setColumnWidth(3, 100)
            self.table.setColumnWidth(3, 80)

        def tabls2(self):
            # self.table.columnsNameShow()
            self.table.setColumnsName(['A', 'B', 'C', 'DD'])
            self.table.setRowsName(['A', 'B', 'C', 'DDDDDDDDDD'])

    app = QApplication(sys.argv)
    ex = Example()
    #ex = xt_QMainWindow()
    sys.exit(app.exec_())
    '''
    import sys, qdarkstyle
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


    styleFile = 'd:/CODE/xjLib/xt_ui/white.qss'
    qssStyle = readQss.all(styleFile)
    app.setStyleSheet(qssStyle)
    '''
