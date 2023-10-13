# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-09-28 16:21:52
FilePath     : /CODE/xjLib/xt_Ui/__init__.py
Github       : https://github.com/sandorn/home
==============================================================
"""
import os
import random
from functools import wraps

import qdarkstyle
from PyQt5.QtCore import QEventLoop, QSize, Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QCursor, QIcon, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QCheckBox,
    QComboBox,
    QDesktopWidget,
    QDoubleSpinBox,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListView,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSpinBox,
    QStatusBar,
    QTableView,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextBrowser,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
)
from xt_File import qsstools


def EventLoop(function):
    """定义一个装饰器,确定鼠标显示和控制权"""

    @wraps(function)
    def warp(*args, **kwargs):
        QApplication.processEvents(
            QEventLoop.ExcludeUserInputEvents)  # 忽略用户的输入（鼠标和键盘）
        QApplication.setOverrideCursor(Qt.WaitCursor)  # 显示等待中的鼠标样式

        result = function(*args, **kwargs)

        QApplication.restoreOverrideCursor()  # 恢复鼠标样式
        QApplication.processEvents()  # 交还控制权

        return result

    return warp


class xt_QStatusBar(QStatusBar):
    """
    addPermanentWidget():永久信息窗口 - 不会被一般消息覆盖
    addWidget();//正常信息窗口 - 会被showMessage()的消息覆盖
    方法   描述
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

    @EventLoop
    def step_by_step(self, value):
        if isinstance(value, int) and value > self.maximum():
            value = self.maximum()

        if value is None or isinstance(value, str):  # #传入None或字符,则在原值上+1
            value = self.value() + 1

        self.setValue(int(value))


class xt_QTabWidget(QTabWidget):
    """
    方法	描述
    setCurrentWidget()	设置当前可见的界面
    setTabBar()	设置选项卡栏的小控件
    QTabWidget类中的常用信号

    1.void setTabText(int, QString); //设置页面的名字.
    2.void setTabToolTip(QString); //设置页面的提示信息.
    3.void setTabEnabled(bool); //设置页面是否被激活.
    4.void setTabPosition(QTabPosition::South); //设置页面名字的位置.
    5.void setTabsClosable(bool); //设置页面关闭按钮。
    6.int currentIndex(); //返回当前页面的下标,从0开始.
    7.int count(); //返回页面的数量.
    8.void clear(); //清空所有页面.
    9.void removeTab(int); //删除页面.
    10.addTab()	将一个控件添加到Tab控件的选项卡中
    11.insertTab()	将一个Tab控件的选项卡插入到指定的位置
    12.void setMoveable(bool); //设置页面是否可被拖拽移动.
    13.void setCurrentIndex(int); //设置当前显示的页面.

    signals:
    1.void tabCloseRequested(int). //当点击第参数个选项卡的关闭按钮的时候,发出信号
                                    配合setTabsClosable(true)
    2.void tabBarClicked(int). //当点击第参数个选项卡的时候,发出信号.
    3.void currentChanged(int). //当改变第参数个选项卡的时候,发出信号.
    4.void tabBarDoubleClicked(int). //当双击第参数个选项卡的时候,发出信号
    """

    def __init__(self, textlist, *args, **kwargs):
        # #textlist tabname list 或者 页签数量
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QTabWidget_{id(self)}")
        # self.setTabShape(QTabWidget.Triangular)  ## 页签样式
        # self.setTabsClosable(True)  ## 关闭按钮
        # 创建选项卡控件
        self.tab = {}
        self.lay = {}
        if isinstance(textlist, list):
            for index in range(len(textlist)):
                self.tab[index] = QWidget()
                self.addTab(self.tab[index], textlist[index])
        elif isinstance(int(textlist), int):  # 可以输入数值
            for index in range(int(textlist)):
                self.tab[index] = QWidget()
                self.addTab(self.tab[index], f"TAB_{str(index)}")
        else:
            self.addTab(self.tab[0], "TAB_0")

        for index in range(self.count()):
            self.lay[index] = QHBoxLayout()
            self.tab[index].setLayout(self.lay[index])
            # self.lay[index].addWidget(label, 0, 0)

        self.stylestring = self.styleSheet()
        self.currentChanged.connect(self.currentChanged_event)
        self.tabCloseRequested.connect(self.tabCloseRequested_event)
        self.tabBarDoubleClicked.connect(self.tabBarDoubleClicked_event)

    def currentChanged_event(self, index):
        # print(f'QTabWidget_currentChanged_event,切换页面为:{index}')
        pass

    def tabCloseRequested_event(self, index):
        self.removeTab(index)

    def tabBarDoubleClicked_event(self, index):
        self.removeTab(index)

    # @动态调整tab页签宽度
    def resizeEvent(self, event):
        # print(self.styleSheet())
        _tabCount = self.count()
        if _tabCount == 0:
            return
        _tabWidth = round(self.width() / _tabCount)
        self.setStyleSheet(self.stylestring +
                           "QTabBar::tab{width:%upx;}" % _tabWidth)


class xt_QTableView(QTableView):
    """
    QTableView可用的模式
    QTableView控件可以绑定一个模型数据用来更新控件上的内容
    名称	含义
    currentIndex().row()
    QStringListModel	储存一组字符串
    QstandardItemModel	存储任意层次结构的数据
    QDirModel	对文件系统进行封装
    QSqlQueryModel	对SQL的查询结果集进行封装
    QSqlTableModel	对SQL中的表格进行封装
    QSqlRelationalTableModel	对带有foreign key的SQL表格进行封装
    QSortFilterProxyModel	对模型中的数据进行排序或过滤
    事件:
    void	clicked ( const QModelIndex & index )
    void	pressed ( const QModelIndex & index )
    """

    def __init__(self, ColumnsName=None, *args, **kwargs):
        if ColumnsName is None:
            ColumnsName = []
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QTableView_{id(self)}")
        self.model = QStandardItemModel(0, len(ColumnsName))  # type: ignore
        self.ColumnsName = ColumnsName
        self.setColumnsName(ColumnsName)
        self.setModel(self.model)
        self.设置自适应列宽()
        self.设置尾列填充()
        self.设置列宽适应内容()
        self.表格禁止编辑()
        self.设置整行选中()
        self.单行选择()
        self.双向滚动条()
        self.clicked.connect(self.clicked_event)

        self.setContextMenuPolicy(Qt.CustomContextMenu)  # 配合右键菜单
        self.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self):  # 创建右键菜单
        self.contextMenu = QMenu(self)
        self.contextMenu.addAction("Add")
        self.contextMenu.addSeparator()
        self.contextMenu.addAction("Del")
        # self.actionA = self.contextMenu.exec_(self.mapToGlobal(pos))  # 1
        self.contextMenu.popup(QCursor.pos())  # 2菜单显示的位置
        # self.actionA.triggered.connect(self.actionHandler)
        self.contextMenu.triggered[QAction].connect(self.processtrigger)
        self.contextMenu.move(self.pos())  # 3
        self.contextMenu.show()

    def processtrigger(self, QAction):
        print("QTableView_contextMenu_triggered", QAction, QAction.text())

    def 设置自适应列宽(self):
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def 设置尾列填充(self):
        self.horizontalHeader().setStretchLastSection(True)

    def 设置列宽适应内容(self, index=0):
        # #设置要根据内容使用宽度的列
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents)

    def 设置整行选中(self):
        self.setSelectionBehavior(QTableView.SelectRows)

    def 表格禁止编辑(self):
        self.setEditTriggers(QTableWidget.NoEditTriggers)

    def 禁止点击表头(self):
        self.horizontalHeader().setSectionsClickable(False)

    def 单行选择(self):
        self.setSelectionMode(QTableView.SingleSelection)

    def 颜色交替(self):
        self.setAlternatingRowColors(True)

    def 双向滚动条(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def setColumnsName(self, Columnslist):
        # TODO 设置水平表头
        self.model.setHorizontalHeaderLabels(Columnslist)

    @EventLoop
    def appendItem(self, item=None):
        if item is None:
            item = []
        # #取消自动排序
        self.setSortingEnabled(False)

        if isinstance(item, list):
            self.model.appendRow(
                [QStandardItem(str(_c_item)) for _c_item in item])

            # $滚动到最下面
            self.scrollToBottom()

        # #恢复排序设置
        self.setSort(self.des_sort)  # type: ignore

    @EventLoop
    def appendItems(self, items=None):
        if items is None:
            items = []
        self.setUpdatesEnabled(False)  # 暂停界面刷新
        if isinstance(items, list) and isinstance(items[0], list):
            for item in items:
                self.model.appendRow(
                    [QStandardItem(str(_c_item)) for _c_item in item])

        # $滚动到最下面
        self.scrollToBottom()
        self.setUpdatesEnabled(True)  # 恢复界面刷新

    @EventLoop
    def empty(self):
        [self.model.removeRow(0) for _ in range(self.model.rowCount())]

    def clean(self):
        self.model.clear()
        self.setColumnsName(self.ColumnsName)

    def clicked_event(self, item):
        # print('QTableView_clicked_event', item, item.data(), item.row())
        pass


class xt_QTableWidget(QTableWidget):
    """
    QTableWidget类中的常用方法
    方法	描述
    setROwCount(int row)	设置QTableWidget表格控件的行数
    setColumnCount(int col)	设置QTableWidget表格控件的列数
    setHorizontalHeaderLabels()	设置QTableWidget表格控件的水平标签
    setVerticalHeaderLabels()	设置QTableWidget表格控件的垂直标签
    setItem(int ,int ,QTableWidgetItem)	在QTableWidget表格控件的每个选项的单元控件内添加控件
    horizontalHeader()	获得QTableWidget表格控件的表格头,以便执行隐藏
    rowCount()	获得QTableWidget表格控件的行数
    columnCount()	获得QTableWidget表格控件的列数
    setEditTriggers(EditTriggers triggers)	设置表格是否可以编辑,设置表格的枚举值
    setSelectionBehavior	设置表格的选择行为
    setTextAlignment()	设置单元格内文本的对齐方式
    setSpan(int row,int column,int rowSpanCount,int columnSpanCount)	合并单元格,要改变单元格的第row行,column列,要合并rowSpancount行数和columnSpanCount列数
    row:要改变的行数
    column:要改变的列数
    rowSpanCount:需要合并的行数
    columnSpanCount:需要合并的列数
    setShowGrid()	在默认情况下表格的显示是有网格的,可以设置True或False用于是否显示,默认True
    setColumnWidth(int column,int width)	设置单元格行的宽度
    setRowHeight(int row,int height)	设置单元格列的高度
    编辑规则的枚举值类型
    选项	值	描述
    QAbstractItemView.NoEditTriggers0No	0	不能对表格内容进行修改
    QAbstractItemView.CurrentChanged1Editing	1	任何时候都能对单元格进行修改
    QAbstractItemView.DoubleClicked2Editing	2	双击单元格
    QAbstractItemView.SelectedClicked4Editing	4	单击已经选中的内容
    QAbstractItemView.EditKeyPressed8Editing	8	当修改键按下时修改单元格
    QAbstractItemView.AnyKeyPressed16Editing	16	按任意键修改单元格
    QAbstractItemView.AllEditTriggers31Editing	31	包括以上所有条件
    表格选择行为的枚举值
    选择	值	描述
    QAbstractItemView.SelectItems0Selecting	0	选中单个单元格
    QAbstractItemView.SelectRows1Selecting	1	选中一行
    QAbstractItemView.SelectColumns2Selecting	2	选中一列
    单元格文本水平对齐方式
    选项	描述
    Qt.AlignLeft	将单元格内的内容沿单元格的左边缘对齐
    Qt.AlignRight	将单元格内的内容沿单元格的右边缘对齐
    Qt.AlignHCenter	在可用空间中,居中显示在水平方向上
    Qt.AlignJustify	将文本在可用空间内对齐,默认从左到右
    单元格文本垂直对齐方式
    选项	描述
    Qt.AlignTop	与顶部对齐
    Qt.AlignBottom	与底部对齐
    Qt.AlignVCenter	在可用空间中,居中显示在垂直方向上
    Qt.AlignBaseline	与基线对齐
    如果要设置水平和垂直方向对齐方式,比如在表格空间内上下,左右居中对齐,那么只要使用Qt,AlignHCenter和Qt,AlignVCenter即可


        # res = [[self.titles[index], self.urls[index]] for index in range(len(self.titles))]
        # self.tableWidget.appendItems(res)
        # self.tableWidget.scrollToTop()
    """

    def __init__(self, ColumnsName, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QTableWidget_{id(self)}")
        self.row_name_show = True  # #行名显示标志
        self.column_name_show = True  # #列名显示标志
        # TODO 设置垂直方向的表头标签
        self.setColumnCount(len(ColumnsName))
        self.setColumnsName(ColumnsName)
        # TODO 设置其他优化
        self.设置自适应列宽()
        self.设置尾列填充()
        self.设置列宽适应内容()
        self.表格禁止编辑()
        self.设置整行选中()
        self.多行选择()
        self.自动匹配宽高()
        self.表头排序()
        self.颜色交替()
        self.双向滚动条()
        self.itemClicked.connect(self.itemClicked_event)

        self.setContextMenuPolicy(Qt.CustomContextMenu)  # 配合右键菜单
        self.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self):  # 创建右键菜单
        self.contextMenu = QMenu(self)
        self.contextMenu.addAction("Add")
        self.contextMenu.addSeparator()
        self.contextMenu.addAction("Del")
        # self.actionA = self.contextMenu.exec_(self.mapToGlobal(pos))  # 1
        self.contextMenu.popup(QCursor.pos())  # 2菜单显示的位置
        # self.actionA.triggered.connect(self.actionHandler)
        self.contextMenu.triggered[QAction].connect(self.processtrigger)
        # self.contextMenu.move(self.pos())  # 3
        self.contextMenu.show()

    def processtrigger(self, QAction):
        print("QTableWidget_contextMenu_triggered", QAction, QAction.text())

    def 设置自适应列宽(self):
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def 设置尾列填充(self):
        self.horizontalHeader().setStretchLastSection(True)

    def 设置列宽适应内容(self, index=0):
        # #设置要根据内容使用宽度的列
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents)

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
        """
        QTableWidget.NoSelection 不能选择
        QTableWidget.SingleSelection 选中单个目标
        QTableWidget.MultiSelection 选中多个目标
        QTableWidget.ExtendedSelection shift键的连续选择
        QTableWidget.ContiguousSelection ctrl键的不连续的多个选择
        """

    def 表头排序(self):
        self.des_sort = True  # #排序标志
        self.setSortingEnabled(True)

    def 颜色交替(self):
        self.setAlternatingRowColors(True)

    def 双向滚动条(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def addWidget(self, row, column, widget):
        # TODO 在单元格内放置控件
        # comBox=QComboBox()
        # comBox.addItems(['男','女'])
        # comBox.addItem('未知')
        # self.setCellWidget(0,1,comBox)
        self.setCellWidget(row, column, widget)

    def columnsNameShow(self):
        # TODO 水平表头隐藏
        self.column_name_show = not self.column_name_show  # #列名显示标志
        self.horizontalHeader().setVisible(self.column_name_show)
        return self.column_name_show

    def rowsNameShow(self):
        # TODO 竖直表头隐藏
        self.row_name_show = not self.row_name_show  # #行名显示标志
        self.verticalHeader().setVisible(self.row_name_show)
        return self.row_name_show

    def setColumnName(self, column, ColumnName):
        # TODO 设置单一水平表头
        self.setHorizontalHeaderItem(column, QTableWidgetItem(str(ColumnName)))

    def setColumnsName(self, Columnslist):
        # TODO 设置水平表头
        # self.setHorizontalHeaderLabels(Columnslist)
        for column, ColumnName in enumerate(Columnslist):
            self.setColumnName(column, ColumnName)

    def setRowsName(self, Rowslist):
        # TODO 设置竖直表头
        self.setVerticalHeaderLabels(Rowslist)

    def setRowName(self, row, RowName):
        # TODO 设置单一竖直表头
        self.setVerticalHeaderItem(row, QTableWidgetItem(str(RowName)))

    def setSort(self, sbool=None):
        # TODO 设置单一竖直表头
        self.des_sort = not self.des_sort if sbool is None else sbool
        self.setSortingEnabled(self.des_sort)
        return self.des_sort

    @EventLoop
    def appendItem(self, item=None):
        if item is None:
            item = []
        # #取消自动排序
        self.setSortingEnabled(False)

        if isinstance(item, list):
            row = self.rowCount()
            self.insertRow(row)

            for column, _c_item in enumerate(item):
                self.setItem(row, column, QTableWidgetItem(str(_c_item)))

            # $滚动到最下面
            self.scrollToBottom()

        # #恢复排序设置
        self.setSort(self.des_sort)

    @EventLoop
    def appendItems(self, items=None):
        if items is None:
            items = []
        self.setUpdatesEnabled(False)  # 暂停界面刷新
        if isinstance(items, list) and isinstance(items[0], list):
            for item in items:
                row = self.rowCount()
                self.insertRow(row)

                for column, _c_item in enumerate(item):
                    self.setItem(row, column, QTableWidgetItem(str(_c_item)))

        # $滚动到最下面
        self.scrollToBottom()
        # self.scrollToTop()
        self.setUpdatesEnabled(True)  # 恢复界面刷新

    @EventLoop
    def empty(self):
        [self.removeRow(0) for _ in range(self.rowCount())]

    def clean(self):
        self.setRowCount(0)
        self.clearContents()
        # super().clean()

    def itemClicked_event(self, item):
        # print('QTableWidget_itemClicked_event', item, item.text(), item.row())
        # self.currentIndex().row()
        pass


class xt_QListWidget(QListWidget):
    """
    方法	描述
    resize()
    addItem()	在列表中添加QListWidgetItem对象或字符串
    addItems()	添加列表中的每个条目
    insertItem()	在指定地索引处插入条目
    clear()	删除列表的内容
    setCurrentItem()	设置当前所选的条目
    sortItems()	按升序重新排列条目
    setMaximumWidth(405)  # 最大宽度

    QLIstWidget类中常用的信号
    信号	含义
    currentItemChanged	当列表中的条目发生改变时发射此信号
    itemClicked	当点击列表中的条目时发射此信号

    QListWidget自身的信号包括如下:

    currentItemChanged(QListWidgetItem current, QListWidgetItem previous)信号
    当列表部件中的当前项发生变化时发射,带两个参数,分别表示当前选择项和在此之前的选择项。

    currentRowChanged(int currentRow)信号
    当列表部件中的当前项发生变化时发射,带一个参数,currentRow表示当前项行号,如果没有当前项,其值为-1。

    currentTextChanged(str currentText)
    当列表部件中的当前项发生变化时发射,带一个参数,currentText为当前项对应文本。

    itemActivated(QListWidgetItem item)
    当项激活时发射,项激活是指鼠标单击或双击项,具体依赖于系统配置。项激活还可以是在windows环境下在项上按下回车键,在Mac操作系统下按下Command+O键。

    itemChanged(QListWidgetItem item)
    当项的文本发生改变时发射该信号,项文本无论是否真正改变都会发射。

    itemClicked(QListWidgetItem item)
    当部件中的项被鼠标单击时发射该信号。

    itemDoubleClicked(QListWidgetItem item)
    当部件中的项被鼠标双击时发射该信号。

    itemEntered(QListWidgetItem item)
    当部件中的项接收到鼠标光标时发射该信号,发射该信号需设置mouseTracking属性为True,如果未设置该属性,则只有鼠标移动到项时按下按键时才触发。

    itemPressed(QListWidgetItem item)
    当鼠标在部件中的项上按下时触发。

    itemSelectionChanged()
    当列表部件中进行了选择操作后触发,无论选中项是否改变。
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QListWidget_{id(self)}")
        self.setMovement(QListView.Static)  # 设置单元项不可拖动
        # 图标格式显示 QListView.IconMode | QListWidget.ListMode
        self.setViewMode(QListView.ListMode)
        # self.setIconSize(QSize(50, 50))  # 图标大小
        self.setSpacing(6)  # 间距大小
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # 垂直滚动条

        self.itemClicked.connect(self.itemClicked_event)  # 绑定点击事件
        self.currentRowChanged.connect(self.currentRowChanged_event)  # 绑定点击事件

        self.setContextMenuPolicy(Qt.CustomContextMenu)  # 配合右键菜单
        self.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self):  # 创建右键菜单
        self.contextMenu = QMenu(self)
        self.contextMenu.addAction("Add")
        self.contextMenu.addSeparator()
        self.contextMenu.addAction("Del")
        self.contextMenu.popup(QCursor.pos())  # 菜单显示的位置
        self.contextMenu.triggered[QAction].connect(self.processtrigger)
        self.contextMenu.move(self.pos())  # 3
        self.contextMenu.show()

    def processtrigger(self, QAction):
        print("QListWidget_contextMenu_triggered", QAction, QAction.text())

    def clean(self):
        self.clear()

    @EventLoop
    def empty(self):
        [self.takeItem(0) for _ in range(self.count())]

    @EventLoop
    def getall(self):
        widgetres = []
        # 获取listwidget中条目数
        count = self.count()
        # 遍历listwidget中的内容
        for index in range(count):
            _item = self.item(index)
            assert isinstance(_item, QListWidgetItem)
            widgetres.append(_item.text())

        return widgetres

    def itemClicked_event(self, item):
        # print('QListWidget_itemClicked_event')
        # self.currentRow() == self.currentIndex().row()
        ...

    def currentRowChanged_event(self, row):
        # item = self.item(row)
        # print('QListWidget_currentRowChanged_event')
        # self.currentRow() == self.currentIndex().row()
        ...


class xt_QTreeWidget(QTreeWidget):
    """
    QTreeWidget类中的常用方法
    方法	描述
    setColumnWidth(int column,int width)	将指定列的宽度设置为给定的值
    Column:指定的列
    width:指定的宽度
    insertTopLevelItems()	在视图的顶层索引中引入项目的列表
    expandAll()	展开所有节点的树形节点
    invisibleRootItem()	返回树形控件中不可见的根选项(Root Item)
    selectionItems()	返回所有选定的非隐藏项目的列表内
    #@QTreeWidgetItem类中常用的方法
    addChild()	将子项追加到子列表中
    setText()	设置显示的节点文本
    text()	返回显示的节点文本
    setCheckState(column.state)	设置指定列的选中状态:Qt.Checked:节点选中;Qt.Unchecked:节点没有选中
    setIcon(column,icon)	在指定的列中显示图标
    事件
    clicked,doubleClicked,itemDoubleClicked
    """

    def __init__(self, ColumnsName, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QTreeWidget_{id(self)}")
        self.setColumnCount(len(ColumnsName))  # 设置列数
        self.setHeaderLabels(ColumnsName)  # 设置头部信息对应列的标识符
        self.多行选择()
        self.设置自适应列宽()
        self.columns = dict(enumerate(ColumnsName))
        # 设置root为self.tree的子树,故root是根节点
        self.root = QTreeWidgetItem(self)
        self.root.setText(0, "root")  # 设置根节点的名称
        self.addTopLevelItem(self.root)

        self.clicked.connect(self.clicked_event)
        self.itemDoubleClicked.connect(self.itemDoubleClicked_event)

        self.setContextMenuPolicy(Qt.CustomContextMenu)  # 配合右键菜单
        self.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self):  # 创建右键菜单
        self.contextMenu = QMenu(self)
        self.contextMenu.addAction("Add")
        self.contextMenu.addSeparator()
        self.contextMenu.addAction("Del")
        # self.actionA = self.contextMenu.exec_(self.mapToGlobal(pos))  # 1
        self.contextMenu.popup(QCursor.pos())  # 2菜单显示的位置
        # self.actionA.triggered.connect(self.actionHandler)
        self.contextMenu.triggered[QAction].connect(self.processtrigger)
        # self.contextMenu.move(self.pos())  # 3
        self.contextMenu.show()

    def processtrigger(self, QAction):
        print("QTableWidget_contextMenu_triggered", QAction, QAction.text())

    def 多行选择(self):
        # shift键的连续选择
        self.setSelectionMode(QTreeWidget.ExtendedSelection)

    def 设置自适应列宽(self):
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)

    def 设置平均列宽(self):
        self.header().setSectionResizeMode(QHeaderView.Stretch)

    def addItem(self, name_list=None, parent=None):
        if name_list is None:
            name_list = []
        if parent is None:
            child = QTreeWidgetItem(self.root)
        else:
            child = QTreeWidgetItem(parent)

        for index in self.columns.keys():
            _text = name_list[index] if index < len(name_list) else ""
            child.setText(index, _text)

    def clicked_event(self, qmodelindex):
        """PyQt5.QtCore.QModelIndex对象"""
        # print('QTreeWidget_clicked_event', qmodelindex, qmodelindex.data())
        # item = self.currentItem() # 当前节点
        # print([item.text(index) for index in range(self.columnCount())])
        pass

    def itemDoubleClicked_event(self, item, columnindex):
        """QTreeWidgetItem对象,列号"""
        # print('itemDoubleClicked_event', item.text(columnindex), columnindex, [item.text(index) for index in range(self.columnCount())])
        pass


class xt_QLabel(QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QLabel_{id(self)}")


class xt_QTextBrowser(QTextBrowser):
    """
    cursor =  self.textCursor();
    cursor.movePosition(self.textCursor().End);
    self.setTextCursor(cursor);

    textCursor()  #光标的位置
    setText() 解析html格式文本
    setPlainText() 不解析html格式文本
    setHtml() # 设置文档
    setSource() #设置链接  QUrl
    setDocumentTitle('dsds') # 设置文档标题
    QTextBrowser同时 具有以下插槽: home() :返回主文档, backward() #返回上一文档,forward()前进

    _temp = '<font size="5">' + _text.replace("\n","<br>") + '</font>'

    SourceChanged.connect(self.update) # 发出一个SourceChanged(QUrl)信号
        self.anchorClicked.connect(self.__on_anchor_clicked)

    def __on_anchor_clicked(self, url: QUrl):
        fp = url.toString()
        os.startfile(fp)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QTextBrowser_{id(self)}")
        self.setReadOnly(True)
        self.fontsize = 16
        self.setFontPointSize(self.fontsize)  # 设置字号
        self.ensureCursorVisible()  # 游标可用
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 设置垂直滚动条按需可见
        # Qt.ScrollBarAlwaysOff  #禁用垂直滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 设置水平滚动条按需可见
        self.setOpenLinks(True)  # 打开文档内部链接 默认为True
        self.setOpenExternalLinks(
            True)  # 打开外部链接,默认false,openlinks设置false时 该选项无效
        self.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard
                                     | Qt.LinksAccessibleByMouse
                                     | Qt.TextBrowserInteraction
                                     | Qt.TextSelectableByKeyboard
                                     | Qt.TextSelectableByMouse)

    def event(self, event):
        if event.type() == event.Wheel:
            scrollbar = self.verticalScrollBar()
            current_value = scrollbar.value()
            maximum_value = scrollbar.maximum()
            minimum_value = scrollbar.minimum()

            if current_value == maximum_value:
                QThread.msleep(200)
                self.scroll_to_bottom_event()
                return True  # 拦截滚动事件，不再传递给滚动条

            elif current_value == minimum_value:
                QThread.msleep(200)
                self.scroll_to_top_event()
                return True  # 拦截滚动事件，不再传递给滚动条

        return super().event(event)

    def scroll_to_bottom_event(self):
        # 在滚动到底部时触发的函数
        # print("滚动到底部")
        ...

    def scroll_to_top_event(self):
        # 在滚动到底部时触发的函数
        # print("滚动到顶部")
        ...

    def decrease_text_size(self):
        self.fontsize -= 1
        self.setFontSize(self.fontsize)

    def increase_text_size(self):
        self.fontsize += 1
        self.setFontSize(self.fontsize)

    def setFontSize(self, size):
        cursor = self.textCursor()
        char_format = cursor.charFormat()
        char_format.setFontPointSize(size)
        cursor.setCharFormat(char_format)
        self.setTextCursor(cursor)

        _text = self.toPlainText().strip()
        if not cursor.selectedText().strip():
            self.clear()
            self.setText(_text)
        self.repaint()  # 强制刷新


class xt_QTextEdit(QTextEdit):
    # QTextEdit详细操作-凌的博客  http://www.jiuaitu.com/python/407.html
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QTextEdit_{id(self)}")
        self.textChanged.connect(self.textChanged_event)

    def textChanged_event(self):
        print("textChanged", self.toPlainText())
        ...


class xt_QLineEdit(QLineEdit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QLineEdit_{id(self)}")
        self.textChanged.connect(self.textChanged_event)
        self.textEdited.connect(self.textEdited_event)
        self.returnPressed.connect(self.returnPressed_event)

    def textChanged_event(self, text):
        print("xt_QLineEdit textChanged:", text)

    def textEdited_event(self):
        print("xt_QLineEdit textEdited", self.text())

    def returnPressed_event(self):
        # 文本框回车，执行的操作
        print("xt_QLineEdit returnPressed:", self.text())


class xt_QPushButton(QPushButton):
    """
    setText()设置按钮字符
    text()获取按钮字符
    按钮字符开头用 & + 字母 ,设置快捷键:alt+字母
    事件信号: clicked、pressed、released
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QPushButton_{id(self)}")
        self.clicked.connect(self.clicked_event)

    def clicked_event(self):
        # print('QPushButton_clicked_event', self.text())
        ...


class xt_QCheckBox(QCheckBox):
    """
    setChecked()	设置复选框的状态,设置为True表示选中,False表示取消选中的复选框
    setText()	设置复选框的显示文本
    text()	返回复选框的显示文本
    isChecked()	检查复选框是否被选中,选中就返回True,否则返回False
    setTriState()	设置复选框为一个三态复选框
    setCheckState()	三态复选框的状态设置,具体设置可以见下表
    checkState() 获取三态复选框状态 Qt.Checked | Qt.Unchecked | Qt.PartiallyChecked

    名称	值	含义
    Qt.Checked	2	组件没有被选中(默认)
    Qt.PartiallyChecked	1	组件被半选中
    Qt.Unchecked	0	组件被选中

    stateChanged 状态改变事件
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QCheckBox_{id(self)}")
        self.setChecked(True)
        self.stateChanged.connect(self.stateChangedEvent)

    def stateChangedEvent(self, state):
        print(state)
        if state == Qt.Checked:
            print("选中")


class xt_QComboBox(QComboBox):
    """
    QComboBox类中的常用方法如表
    方法	描述
    addItem()	添加一个下拉选项
    addItems()	从列表中添加下拉选项
    Clear()	删除下拉选项集合中的所有选项
    count()	返回下拉选项集合中的数目
    currentText()	返回选中选项的文本
    itemText(i)	获取索引为i的item的选项文本
    currentIndex()	返回选中项的索引
    setItemText(int index,text)	改变序列号为index的文本
    QComboBox类中的常用信号
    信号	含义
    Activated	当用户选中一个下拉选项时发射该信号
    currentIndexChanged	当下拉选项的索引发生改变时发射该信号
    highlighted	当选中一个已经选中的下拉选项时,发射该信号
    """

    def __init__(self, itemlist=None, *args, **kwargs):
        if itemlist is None:
            itemlist = []
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QComboBox_{id(self)}")

        if isinstance(itemlist, list) and len(itemlist) > 0:
            self.addItems(itemlist)

        self.currentIndexChanged.connect(self.currentIndexChanged_event)

    def currentIndexChanged_event(self, index):
        # print('currentIndexChanged_event', index, self.currentText())
        pass


class xt_QSpinBox(QSpinBox):
    """
    如果使用prefix(),suffix()和specialValueText()感觉还是不爽,那么你可以继承QSpinBox并重新实现valueFromText()和textFromValue()

    def valueFromText(self, str):
        import QRegExp
        regExp = QRegExp("(\\d+)(\\s*[xx]\\s*\\d+)?")
        if regExp.exactMatch(str):
            return int(regExp.cap(1))
        else:
            return 0

    def textFromValue(self, num):
        return "{0} x {1}".format(num, num)
    """
    """
    QSpinBox类中的常用方法
    方法	描述
    setMinimum()	设置计数器的下界
    setMaximum()	设置计数器的上界
    setRange()	设置计数器的最大值,最小值,步长值
    setValue()	设置计数器的当前值
    Value()	返回计数器的当前值
    singleStep()	设置计数器的步长值
    信号	含义
    当值发生改变时,会发射两个valueChanged()信号,其中一个提供int类型,另一个则是QString类型,该QString提供了prefix()和suffix()。当前值可以用value()来读取,setValue()来设置。
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # QSpinBox旨在处理整数和离散值(例如:月份名称)

        self.setObjectName(f"xt_QSpinBox_{id(self)}")
        # 范围
        self.setRange(20, 200)
        # 步长
        self.setSingleStep(10)
        #  当前值 self.setValue(150)
        #  前缀
        self.setPrefix("缩放: ")
        #  后缀
        self.setSuffix(" %")
        # 特殊显示文本
        self.setSpecialValueText("Automatic")
        #  开启循环
        self.setWrapping(True)

        self.valueChanged.connect(self.valueChanged_event)

    def valueChanged_event(self, value):
        """传入 int value,与self.value()相等"""
        # print('currentIndexChanged_event', value, self.text())
        pass


class xt_QDoubleSpinBox(QDoubleSpinBox):
    """
    QDoubleSpinBox则用于处理浮点值
    信号	含义
    当值发生改变时,会发射两个valueChanged()信号,其中一个提供int类型,另一个则是QString类型,该QString提供了prefix()和suffix()。当前值可以用value()来读取,setValue()来设置。
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QDoubleSpinBox _{id(self)}")
        # 范围
        self.setRange(20, 200)
        # 步长
        self.setSingleStep(0.005)
        # 精度
        self.setDecimals(3)
        #  当前值 self.setValue(150)
        #  前缀
        self.setPrefix("缩放: ")
        #  后缀
        self.setSuffix(" %")
        # 特殊显示文本
        self.setSpecialValueText("Automatic")
        #  开启循环
        self.setWrapping(True)

        self.valueChanged.connect(self.valueChanged_event)

    def valueChanged_event(self, value):
        # print('currentIndexChanged_event', value, self.text())
        pass


class xt_QInputDialog(QInputDialog):
    """
    def getItem(self):
            items = ['装载机','平地机','推土机','挖掘机','自卸车'] #这里设置成列表或元组都可以
            item, ok = QInputDialog.getItem(self,'选择项目','请选择您的需求',items,0,False)
            if ok and item:
                self.lineEdit_item.setText(item)

        def getInt(self):
            # num,ok = QInputDialog.getDouble(self,'双精度','输入您得数字')
            num, ok = QInputDialog.getInt(self,'获取整数','输入您的数字(-10～10)',0,-10,10,1)
            if ok:
                self.lineEdit_int.setText(str(num))

        def getStr(self):
            str, ok = QInputDialog.getText(self,'获取字符串','请输入您的文本',QLineEdit.Normal,'字符串',)
            if ok:
                self.lineEdit_str.setText(str)
    QInputDialog.getText(QWidget, str, str, QLineEdit.EchoMode echo=QLineEdit.Normal, str text=QString())
    几个参数依次是:父组件；对话框标题；对话框提示信息；对话框中QLineEdit控件的输入模式；默认值。其中,对话框中QLineEdit控件的输入模式有4种,详情如下表:

    常量	值	内容
    QLineEdit.Normal	0	正常显示输入的字符,默认选项。
    QLineEdit.NoEcho	1	不显示任何输入,常用于密码类型,其密码长度都需要保密的时候。
    QLineEdit.Password	2	显示平台相关的密码掩码字符,而不是实际的字符输入。
    QLineEdit.PasswordEchoOnEdit	3	在编辑的时候显示字符,负责显示密码类型。

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QInputDialog_{id(self)}")


class xt_QMessageBOx(QMessageBox):
    """
    方法
    information,question,warning,critical,about

    QMessageDialog.question(父组件,’对话框标题‘,’对话框内容‘,按键一|按键二,默认按键)。关于对话框只有一个按键ok,不需要用户指定按键,所以只需要给定前三项参数即可。在示例中,我们使用了Yes和No两个按键,实际上pyqt中案件类型不止这两种。

    类型	作用
    QMessage.Yes	是
    QMessage.No	否
    QMessage.Ok	确认
    QMessage.Cancel	取消
    QMessage.About	关于
    QMessage.Retry	重试
    QMessage.Ignore	忽略
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QMessageBOx_{id(self)}")


class xt_QFileDialog(QFileDialog):
    """
    QFileDialog是用于打开和保存文件的对话框,常用的方法如下:

    方法	内容
    getOpenFileName()	返回所选文件的名称,并打开该文件(单个文件)
    getOpenFileNames()	返回所选文件的名称,并打开该文件(多个文件)
    getSaveFileName()	以用户选择的名称给文件命名
    setFileMode()
    可以选择文件类型,枚举常量是:
    QFileDialog.AnyFile 任何文件
    QFileDialog.ExistingFile 已存在的文件
    QFileDialog.Directory 文件目录
    QFileDialog.ExistingFiles 因存在的多个文件
    setFilter	设置过滤器,只显示过滤器允许的文件类型
    getOpenFileName()方法的各参数释义如下:(父组件,标题,对话框打开时默认显示的目录,扩展名过滤器)。
    当扩展名过滤器需要显示多种文件类型时,各类型之间需要用两个分号隔开。
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"xt_QFileDialog_{id(self)}")


class xt_QMainWindow(QMainWindow):

    def __init__(
        self,
        title="MainWindow",
        action=True,
        tool=False,
        menu=False,
        status=False,
        TBackground=False,
        FWindowHint=False,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        # #窗体title,setupUI
        self.title = title
        self.setWindowTitle(title)
        self.setupUI()
        self.center()

        if action:
            self.action_init()
        if tool:
            self.tool_init()
        if menu:
            self.menu_init()
        if status:
            self.status_progress_init()
        if TBackground:
            self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
            self.setWindowOpacity(1.0)  # 设置窗口透明度
            self.setAutoFillBackground(False)

        if FWindowHint:
            self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏边框
        else:
            """恢复event"""
            self.mousePressEvent = super().mousePressEvent  # type: ignore
            self.mouseMoveEvent = super().mouseMoveEvent  # type: ignore
            self.mouseReleaseEvent = super().mouseReleaseEvent  # type: ignore

        # QMetaObject.connectSlotsByName(self)  # @用于自动绑定信号和函数
        """
        继承仍需声明,可能与控件生成顺序有关
        事件action:on_objectName_triggered
        按钮button:on_objectName_clicked
        必须使用@PyQt5.QtCore.pyqtSlot()修饰要调用的函数
        手工绑定:connect(self.func)；解除绑定:disconnect()
        """
        qss = ("""* {font: 11pt 'Sarasa Term SC';outline: none;}""" +
               qdarkstyle.load_stylesheet_pyqt5())
        self.setStyleSheet(qss)
        self.show()

    def setupUI(self):
        # #窗体icon,size...
        self.basepath = os.path.dirname(__file__)
        self.setWindowIcon(QIcon(f"{self.basepath}\ico\ico.ico"))
        # @将窗口大小调整为可用屏幕空间的百分比
        self.resize(QDesktopWidget().availableGeometry(self).size() * 0.618)
        # self.setGeometry(300, 300, 1024, 768)
        # def paintEvent(self, event):
        #     '''窗口大小变化后再次居中'''
        #     self.center()

    def center(self):
        screen = QDesktopWidget().screenGeometry()  # 获取桌面尺寸
        size = self.geometry()  # 获取窗体尺寸
        x = int((screen.width() - size.width()) / 2)
        y = int((screen.height() - size.height()) / 2)
        self.move(x, y)

    def mousePressEvent(self, event):  # @重写事件,响应拖动
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

    def action_init(self):  # #QAction
        self.Run_action = QAction(QIcon(f"{self.basepath}\ico\Execute.png"),
                                  "&Execute", self)
        self.Do_action = QAction(QIcon(f"{self.basepath}\ico\Performing.png"),
                                 "&Performing", self)
        self.Theme_action = QAction(QIcon(f"{self.basepath}\ico\color.ico"),
                                    "&Theme", self)
        self.Run_action.setObjectName("Run")
        self.Do_action.setObjectName("Do")
        self.Theme_action.setObjectName("Theme")
        # !必须,关键,用于自动绑定信号和函数  on_ObjectName_triggered
        # !配套:QMetaObject.connectSlotsByName(self)
        self.Close_action = QAction(QIcon(f"{self.basepath}\ico\close.ico"),
                                    "&Quit", self)
        self.Run_action.setShortcut("Ctrl+E")
        self.Do_action.setShortcut("Ctrl+P")
        self.Theme_action.setShortcut("Ctrl+T")
        self.Close_action.setShortcut("Ctrl+Q")
        # self.Close_action.setToolTip('Close the window')
        # self.Close_action.setStatusTip('Close the window')
        self.Close_action.triggered.connect(QApplication.quit)

    def tool_init(self):  # #工具栏
        self.file_toolbar = self.addToolBar("")
        self.file_toolbar.setToolButtonStyle(3)
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
        self.file_toolbar.setContextMenuPolicy(
            Qt.CustomContextMenu)  # ActionsContextMenu

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

    @pyqtSlot()
    def on_Theme_triggered(self):
        # print('on_Theme_triggered')
        qss_list = [
            f"{self.basepath}\qss\\blue.qss",
            f"{self.basepath}\qss\css.qss",
            f"{self.basepath}\qss\dark_orange.qss",
            f"{self.basepath}\qss\dark.qss",
            f"{self.basepath}\qss\grey.qss",
            f"{self.basepath}\qss\qdark.qss",
            f"{self.basepath}\qss\white.qss",
        ]
        file_name = random.choice(qss_list)
        self.setWindowTitle(f"{self.title}--" +
                            file_name.split("/")[-1].split(".")[0])
        qsstools.set(file_name, self)

    """
        #@setWindowFlags(Qt.WindowFlags|Qt.WindowFlags)
        PYQT基本窗口类型有如下类型:
        Qt.Qt.Widget#插件默认窗口,有最小化、最大化、关闭按钮
        Qt.Qt.Window#普通窗口,有最小化、最大化、关闭按钮
        Qt.Qt.Dialog#对话框窗口,有问号和关闭按钮
        Qt.Qt.Popup#弹出窗口,窗口无边框化
        Qt.Qt.ToolTip#提示窗口,窗口无边框化,无任务栏窗口
        Qt.Qt.SplashScreen#飞溅屏幕,窗口无边框化,无任务栏窗口
        Qt.Qt.SubWindow#子窗口,窗口无按钮但有标题栏

        自定义外观的顶层窗口标志:
        Qt.Qt.MSWindowsFixedSizeDialogHint#窗口无法调整大小
        Qt.Qt.FramelessWindowHint#窗口无边框化
        Qt.Qt.CustomizeWindowHint#有边框但无标题栏和按钮,不能移动和拖动
        Qt.Qt.WindowTitleHint#添加标题栏和一个关闭按钮
        Qt.Qt.WindowSystemMenuHint#添加系统目录和一个关闭按钮
        Qt.Qt.WindowMaximizeButtonHint#激活最大化和关闭按钮,禁止最小化按钮
        Qt.Qt.WindowMinimizeButtonHint#激活最小化和关闭按钮,禁止最大化按钮
        Qt.Qt.WindowMinMaxButtonsHint#激活最小化、最大化和关闭按钮,
        #相当于Qt.Qt.WindowMaximizeButtonHint|Qt.Qt.WindowMinimizeButtonHint
        Qt.Qt.WindowCloseButtonHint#添加一个关闭按钮
        Qt.Qt.WindowContextHelpButtonHint#添加问号和关闭按钮,像对话框一样
        Qt.Qt.WindowStaysOnTopHint#窗口始终处于顶层位置
        Qt.Qt.WindowStaysOnBottomHint#窗口始终处于底层位置
        Qt.Qt.Tool 有一个小小的关闭按钮
    """
