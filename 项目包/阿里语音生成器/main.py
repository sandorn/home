# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-11-29 23:53:26
LastEditTime : 2022-12-19 22:57:36
FilePath     : /项目包/阿里语音生成器/main.py
Github       : https://github.com/sandorn/home
==============================================================
'''

from PyQt5.QtCore import Qt, QThread, pyqtSlot
from PyQt5.QtWidgets import QApplication, QSplitter
from xt_Alispeech.cfg import VIOCE
from xt_Alispeech.ex_NSS import TODO_TTS
from xt_String import str_split_limited_list
from xt_Ui import (EventLoop, xt_QLineEdit, xt_QMainWindow, xt_QTableView, xt_QTextEdit)


class Ui_MainWindow(xt_QMainWindow):

    def __init__(self):
        super().__init__('阿里语音合成器', status=True, tool=True)
        self.args_dict = {}  # 存参数
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setupUi()
        self.retranslateUi()
        self.bindTable()

    def setupUi(self):
        self.tableWidget = xt_QTableView(['名称', '参数值', '类型', '适用场景', '支持语言', '采样率', '时间戳', '儿化音', '声音品质'])
        self.FilePath = xt_QLineEdit()
        self.QTextEdit = xt_QTextEdit()
        self.splitter = QSplitter(self)

    def retranslateUi(self):
        self.splitter.addWidget(self.tableWidget)
        self.splitter.setStretchFactor(0, 4)  # 设定比例
        self.splitter.addWidget(self.QTextEdit)
        self.splitter.setStretchFactor(1, 6)  # 设定比例
        self.splitter.setOrientation(Qt.Horizontal)  # Qt.Vertical 垂直  # Qt.Horizontal 水平
        self.setCentralWidget(self.splitter)
        self.QTextEdit.textChanged.connect(self.textChanged_event)  # @绑定方法 triggered

    @EventLoop
    def bindTable(self):
        res = [[*item] for item in VIOCE]
        self.tableWidget.appendItems(res)
        self.tableWidget.scrollToTop()
        self.tableWidget.clicked.connect(self.tableClick_event)  # @绑定表格单击方法

    @EventLoop
    def tableClick_event(self, item):
        QModelIndex = self.tableWidget.model.index(item.row(), 1)
        _voice = QModelIndex.data()
        self.args_dict.update({'voice': _voice})

    @pyqtSlot()
    def on_Run_triggered(self, *args, **kwargs):
        self.args_dict.update({'savefile': False})
        # TODO_TTS(self.text, renovate_args=self.args_dict, merge=True)
        nowthread = QThread()
        nowthread.run = TODO_TTS(self.text, renovate_args=self.args_dict, merge=True)  # type: ignore

    def textChanged_event(self):
        self.text = str_split_limited_list(self.QTextEdit.toPlainText())


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    _text = '''
    北京时间12月18日23:00(卡塔尔当地时间18:00)，2022世界杯决赛展开争夺，阿根廷通过点球大战7-5取胜法国。梅西双响，迪马利亚进球，姆巴佩上演帽子戏法两度追平。点球大战，法国两度射失点球。阿根廷第3次夺得世界杯。
　　阿根廷仅用迪马利亚轮换出场。法国轮换2人，拉比奥特和于帕梅卡诺出战。
　　第23分钟，迪马利亚切入禁区左侧被登贝莱绊倒，梅西射入点球。第36分钟，麦考利斯特反击中斜传，迪马利亚小禁区前低射入网，2-0。
　　法国2分钟连入2球扳平。第80分钟，奥塔门迪禁区内对穆阿尼犯规，姆巴佩射入点球，1-2。第81分钟，图拉姆传球，姆巴佩禁区左侧15码处劲射入网，2-2。
　　进入加时赛。阿根廷第108分钟再次超出，恩佐传球，劳塔罗禁区右侧小角度射门被洛里扑出，梅西近距离补射被孔德在门线内挡出，3-2。法国第118分钟再次扳平，蒙铁尔禁区内手球犯规，姆巴佩射入点球上演帽子戏法，3-3。
　　进入点球大战。首轮，姆巴佩和梅西双双罚入，1-1；次轮，科曼主罚点球被扑出，迪巴拉一蹴而就，1-2；第3轮，楚阿梅尼低射左下角偏出，帕雷德斯射入，1-3；第4轮，穆阿尼和蒙铁尔相继射入，2-4。
    '''
    ui.QTextEdit.setText(_text)
    sys.exit(app.exec())
