# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:57
LastEditTime : 2023-10-20 10:21:02
FilePath     : /CODE/项目包/阿里语音生成器/main.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from PyQt6.QtCore import Qt, QThread, pyqtSlot
from PyQt6.QtWidgets import QApplication, QSplitter
from xt_alispeech.cfg import VIOCE
from xt_alispeech.ex_NSS import TODO_TTS
from xt_pyqt import EventLoop, QMessageBox, xt_QLineEdit, xt_QMainWindow, xt_QSpinBox, xt_QTableView, xt_QTextEdit


class Ui_MainWindow(xt_QMainWindow):
    def __init__(self):
        super().__init__("阿里语音合成器", status=True, tool=True)
        self.args_dict = {}  # 存参数
        self.setWindowOpacity(1.0)  # 设置窗口透明度
        self.setupUi()
        self.retranslateUi()
        self.bindTable()

    def setupUi(self):
        self.tableWidget = xt_QTableView(["名称", "参数值", "类型", "适用场景", "支持语言", "采样率", "时间戳", "儿化音", "声音品质"])
        self.FilePath = xt_QLineEdit()
        self.QTextEdit = xt_QTextEdit()
        self.splitter = QSplitter(self)

        self.QSpinBox = xt_QSpinBox(self)
        self.QSpinBox.setRange(0, 100)
        self.QSpinBox.setValue(50)
        self.QSpinBox.setPrefix("volume: ")
        self.file_toolbar.addWidget(self.QSpinBox)

        self.QSpinBox1 = xt_QSpinBox(self)
        self.QSpinBox1.setRange(-500, 500)
        self.QSpinBox1.setValue(0)
        self.QSpinBox1.setPrefix("speech_rate: ")
        self.QSpinBox1.setSuffix("")  #  后缀
        self.file_toolbar.addWidget(self.QSpinBox1)

        self.QSpinBox2 = xt_QSpinBox(self)
        self.QSpinBox2.setRange(-500, 500)
        self.QSpinBox2.setValue(0)
        self.QSpinBox2.setPrefix("pitch_rate: ")
        self.QSpinBox2.setSuffix("")  #  后缀
        self.file_toolbar.addWidget(self.QSpinBox2)

    def retranslateUi(self):
        self.splitter.addWidget(self.tableWidget)
        self.splitter.setStretchFactor(0, 4)  # 设定比例
        self.splitter.addWidget(self.QTextEdit)
        self.splitter.setStretchFactor(1, 6)  # 设定比例
        self.splitter.setOrientation(Qt.Horizontal)
        # Qt.Vertical 垂直  # Qt.Horizontal 水平
        self.setCentralWidget(self.splitter)
        self.QTextEdit.textChanged.connect(self.textChanged_event)

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
        self.args_dict.update({"voice": _voice})

    @EventLoop
    @pyqtSlot()
    def on_Run_triggered(self):
        self.args_dict.update({"volume": self.QSpinBox.value()})
        self.args_dict.update({"speech_rate": self.QSpinBox1.value()})
        self.args_dict.update({"pitch_rate": self.QSpinBox2.value()})
        nowthread = QThread()
        nowthread.run = TODO_TTS(self.text, readonly=False, merge=True, **self.args_dict)  # type: ignore #

        QApplication.restoreOverrideCursor()  # 恢复鼠标样式
        QApplication.processEvents()  # 交还控制权
        QMessageBox.information(self, "提示", "合成完成！", QMessageBox.Yes)

    def textChanged_event(self):
        self.text = self.QTextEdit.toPlainText()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    _text = """
    立志做有理想、敢担当、能吃苦、肯奋斗的新时代好青年。
    青年强，则国家强。当代中国青年生逢其时，施展才干的舞台无比广阔，实现梦想的前景无比光明。广大青年坚定不移听党话、跟党走，怀抱梦想又脚踏实地，敢想敢为又善作善成，立志做有理想、敢担当、能吃苦、肯奋斗的新时代好青年，让青春在全面建设社会主义现代化国家的火热实践中绽放绚丽之花。
    未来属于青年，希望寄予青年。广大青年要牢记嘱托，坚定理想信念，筑牢精神之基，厚植爱国情怀，矢志不渝跟党走，以实现中华民族伟大复兴为己任，增强做中国人的志气、骨气、底气，不负时代，不负韶华，不负党和人民的殷切期望。
    """
    ui.QTextEdit.setText(_text)
    sys.exit(app.exec())  # app.exec_()
