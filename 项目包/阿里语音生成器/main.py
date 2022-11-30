# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-11-29 23:53:26
FilePath     : /项目包/阿里语音生成器/main.py
LastEditTime : 2022-11-30 00:02:30
Github       : https://github.com/sandorn/home
==============================================================
'''
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QSplitter

# from pysnooper import snoop
from xt_Alispeech.ex_NSS import NSS_TTS
from xt_String import str_split_limited_list
from xt_Ui import EventLoop, xt_QLineEdit, xt_QMainWindow, xt_QTableView, xt_QTextEdit


class Ui_MainWindow(xt_QMainWindow):

    def __init__(self):
        super().__init__('阿里语音合成器')
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
        self.QTextEdit.textChanged.connect(self.textChanged_event)  # @绑定方法
        self.open_action.triggered.connect(self.TTS_run)  # @绑定方法

    @EventLoop
    def bindTable(self):
        vioce = [
            ('知米_多情感', 'zhimi_emo', '多种情感女声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
            ('知燕_多情感', 'zhiyan_emo', '多种情感女声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
            ('知贝_多情感', 'zhibei_emo', '多种情感童声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
            ('知甜_多情感', 'zhitian_emo', '多种情感女声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
            ('小云', 'xiaoyun', '标准女声', '通用场景', '中文及中英文混合场景', '8K/16K', '否', '否', 'lite版'),
            ('小刚', 'xiaogang', '标准男声', '通用场景', '中文及中英文混合场景', '8K/16K', '否', '否', 'lite版'),
            ('若兮', 'ruoxi', '温柔女声', '通用场景', '中文及中英文混合场景', '8K/16K/24K', '否', '否', '标准版'),
            ('思琪', 'siqi', '温柔女声', '通用场景', '中文及中英文混合场景', '8K/16K/24K', '是', '否', '标准版'),
            ('思佳', 'sijia', '标准女声', '通用场景', '中文及中英文混合场景', '8K/16K/24K', '否', '否', '标准版'),
            ('思诚', 'sicheng', '标准男声', '通用场景', '中文及中英文混合场景', '8K/16K/24K', '是', '否', '标准版'),
            ('艾琪', 'aiqi', '温柔女声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
            ('艾佳', 'aijia', '标准女声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
            ('艾诚', 'aicheng', '标准男声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
            ('艾达', 'aida', '标准男声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
            ('宁儿', 'ninger', '标准女声', '通用场景', '纯中文场景', '8K/16K/24K', '否', '否', '标准版'),
            ('瑞琳', 'ruilin', '标准女声', '通用场景', '纯中文场景', '8K/16K/24K', '否', '否', '标准版'),
            ('思悦', 'siyue', '温柔女声', '客服场景', '中文及中英文混合场景', '8K/16K/24K', '否', '否', '标准版'),
            ('艾雅', 'aiya', '严厉女声', '客服场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
            ('艾夏', 'aixia', '亲和女声', '客服场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
            ('艾美', 'aimei', '甜美女声', '客服场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
            ('艾雨', 'aiyu', '自然女声', '客服场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
            ('艾悦', 'aiyue', '温柔女声', '客服场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
            ('艾婧', 'aijing', '严厉女声', '客服场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
            ('小美', 'xiaomei', '甜美女声', '客服场景', '中文及中英文混合场景', '8K/16K/24K', '否', '否', '标准版'),
            ('艾娜', 'aina', '浙普女声', '客服场景', '纯中文场景', '8K/16K', '是', '否', '标准版'),
            ('伊娜', 'yina', '浙普女声', '客服场景', '纯中文场景', '8K/16K/24K', '否', '否', '标准版'),
            ('思婧', 'sijing', '严厉女声', '客服场景', '纯中文场景', '8K/16K/24K', '是', '否', '标准版'),
            ('思彤', 'sitong', '儿童音', '童声场景', '纯中文场景', '8K/16K/24K', '否', '否', '标准版'),
            ('小北', 'xiaobei', '萝莉女声', '童声场景', '纯中文场景', '8K/16K/24K', '是', '否', '标准版'),
            ('艾彤', 'aitong', '儿童音', '童声场景', '纯中文场景', '8K/16K', '是', '否', '标准版'),
            ('艾薇', 'aiwei', '萝莉女声', '童声场景', '纯中文场景', '8K/16K', '是', '否', '标准版'),
            ('艾宝', 'aibao', '萝莉女声', '童声场景', '纯中文场景', '8K/16K', '是', '否', '标准版'),
            ('Harry', 'harry', '英音男声', '英文场景', '英文场景', '8K/16K', '否', '否', '标准版'),
            ('Abby', 'abby', '美音女声', '英文场景', '英文场景', '8K/16K', '是', '否', '标准版'),
            ('Andy', 'andy', '美音男声', '英文场景', '英文场景', '8K/16K', '否', '否', '标准版'),
            ('Eric', 'eric', '英音男声', '英文场景', '英文场景', '8K/16K', '否', '否', '标准版'),
            ('Emily', 'emily', '英音女声', '英文场景', '英文场景', '8K/16K', '否', '否', '标准版'),
            ('Luna', 'luna', '英音女声', '英文场景', '英文场景', '8K/16K', '是', '否', '标准版'),
            ('Luca', 'luca', '英音男声', '英文场景', '英文场景', '8K/16K', '否', '否', '标准版'),
            ('Wendy', 'wendy', '英音女声', '英文场景', '英文场景', '8K/16K/24K', '否', '否', '标准版'),
            ('William', 'william', '英音男声', '英文场景', '英文场景', '8K/16K/24K', '否', '否', '标准版'),
            ('Olivia', 'olivia', '英音女声', '英文场景', '英文场景', '8K/16K/24K', '否', '否', '标准版'),
            ('姗姗', 'shanshan', '粤语女声', '方言场景', '标准粤文及粤英文混合场景', '8K/16K/24K', '否', '否', '标准版'),
            ('小玥', 'chuangirl', '四川话女声', '方言场景', '中文及中英文混合场景', '8K/16K', '否', '否', '标准版'),
            ('Lydia', 'lydia', '英中双语女声', '英文场景', '英文及英中文混合场景', '8K/16K', '是', '否', '标准版'),
            ('艾硕', 'aishuo', '自然男声', '客服场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
            ('青青', 'qingqing', '中国台湾话女声', '方言场景', '中文场景', '8K/16K', '否', '否', '标准版'),
            ('翠姐', 'cuijie', '东北话女声', '方言场景', '中文场景', '8K/16K', '否', '是', '标准版'),
            ('小泽', 'xiaoze', '湖南重口音男声', '方言场景', '中文场景', '8K/16K', '否', '否', '标准版'),
            ('智香', 'tomoka', '日语女声', '多语种场景', '日文场景', '8K/16K', '是', '否', '标准版'),
            ('智也', 'tomoya', '日语男声', '多语种场景', '日文场景', '8K/16K', '是', '否', '标准版'),
            ('Annie', 'annie', '美语女声', '英文场景', '英文场景', '8K/16K', '是', '否', '标准版'),
            ('佳佳', 'jiajia', '粤语女声', '方言场景', '标准粤文（简体）及粤英文混合场景', '8K/16K', '是', '否', '标准版'),
            ('Indah', 'indah', '印尼语女声', '多语种场景', '纯印尼语场景', '8K/16K', '否', '否', '标准版'),
            ('桃子', 'taozi', '粤语女声', '方言场景', '支持标准粤文（简体）及粤英文混合场景', '8K/16K', '是', '否', '标准版'),
            ('柜姐', 'guijie', '亲切女声', '通用场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
            ('Stella', 'stella', '知性女声', '通用场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
            ('Stanley', 'stanley', '沉稳男声', '通用场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
            ('Kenny', 'kenny', '沉稳男声', '通用场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
            ('Rosa', 'rosa', '自然女声', '通用场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
            ('Farah', 'farah', '马来语女声', '多语种场景', '仅支持纯马来语场景', '8K/16K', '否', '否', '标准版'),
            ('马树', 'mashu', '儿童剧男声', '通用场景', '支持中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
            ('小仙', 'xiaoxian', '亲切女声', '直播场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
            ('悦儿', 'yuer', '儿童剧女声', '通用场景', '仅支持纯中文场景', '8K/16K', '是', '否', '标准版'),
            ('猫小美', 'maoxiaomei', '活力女声', '直播场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
            ('知飞', 'zhifei', '激昂解说', '超高清场景', '支持中文及中英文混合场景', '8K/16K', '是', '否', '精品版'),
            ('知伦', 'zhilun', '悬疑解说', '超高清场景', '支持中文及中英文混合场景', '8K/16K', '是', '否', '精品版'),
            ('艾飞', 'aifei', '激昂解说', '直播场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
            ('亚群', 'yaqun', '卖场广播', '直播场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
            ('巧薇', 'qiaowei', '卖场广播', '直播场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
            ('大虎', 'dahu', '东北话男声', '方言场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
            ('ava', 'ava', '美语女声', '英文场景', '仅支持纯英文场景', '8K/16K', '是', '否', '标准版'),
            ('艾伦', 'ailun', '悬疑解说', '直播场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
            ('杰力豆', 'jielidou', '治愈童声', '童声场景', '仅支持纯中文场景', '8K/16K', '是', '是', '标准版'),
            ('老铁', 'laotie', '东北老铁', '直播场景', '仅支持纯中文场景', '8K/16K', '是', '是', '标准版'),
            ('老妹', 'laomei', '吆喝女声', '直播场景', '仅支持纯中文场景', '8K/16K', '是', '是', '标准版'),
            ('艾侃', 'aikan', '天津话男声', '方言场景', '仅支持纯中文场景', '8K/16K', '是', '是', '标准版'),
            ('Tala', 'tala', '菲律宾语女声', '多语种场景', '仅支持菲律宾语场景', '8K/16K', '否', '否', '标准版'),
            ('Tien', 'tien', '越南语女声', '多语种场景', '仅支持越南语场景', '8K/16K', '否', '否', '标准版'),
            ('Becca', 'becca', '美语客服女声', '美式英语', '支持纯英语场景', '8K/16K', '否', '否', '标准版'),
            ('Kyong', 'Kyong', '韩语女声', '韩语场景', '韩语', '8K/16K', '否', '否', '标准版'),
            ('masha', 'masha', '俄语女声', '俄语场景', '俄语', '8K/16K', '否', '否', '标准版'),
        ]

        res = [[*item] for item in vioce]
        self.tableWidget.appendItems(res)
        self.tableWidget.scrollToTop()
        self.tableWidget.clicked.connect(self.tableClick_event)  # @绑定表格单击方法

    @EventLoop
    def tableClick_event(self, item):
        QModelIndex = self.tableWidget.model.index(item.row(), 1)
        _text = QModelIndex.data()
        self.args_dict.update({'vioce': _text})

    @EventLoop
    def TTS_run(self, *args, **kwargs):
        NSS_TTS(self.text, self.args_dict)

    def textChanged_event(self):
        self.text = str_split_limited_list(self.QTextEdit.toPlainText())


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.QTextEdit.setText('根据北京银保监局近期工作部署要求，盛唐融信迅速响应，立即成立专项整治小组')
    sys.exit(app.exec_())  # 程序关闭时退出进程
