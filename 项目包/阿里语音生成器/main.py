# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-11-29 23:53:26
LastEditTime : 2022-12-21 23:18:41
FilePath     : /项目包/阿里语音生成器/main.py
Github       : https://github.com/sandorn/home
==============================================================
'''
from PyQt5.QtCore import Qt, QThread, pyqtSlot
from PyQt5.QtWidgets import QApplication, QSplitter
from xt_Alispeech.cfg import VIOCE
from xt_Alispeech.ex_NSS import TODO_TTS
from xt_Ui import (EventLoop, xt_QLineEdit, xt_QMainWindow, xt_QTableView,
                   xt_QTextEdit)


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
        self.text = self.QTextEdit.toPlainText()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    _text = '''
   立志做有理想、敢担当、能吃苦、肯奋斗的新时代好青年
——广大青年认真学习贯彻党的二十大精神
2022年10月27日08:26   来源：人民网－人民日报

“青年强，则国家强。当代中国青年生逢其时，施展才干的舞台无比广阔，实现梦想的前景无比光明。”习近平总书记在党的二十大报告中勉励广大青年坚定不移听党话、跟党走，怀抱梦想又脚踏实地，敢想敢为又善作善成，立志做有理想、敢担当、能吃苦、肯奋斗的新时代好青年，让青春在全面建设社会主义现代化国家的火热实践中绽放绚丽之花。

未来属于青年，希望寄予青年。认真学习贯彻党的二十大精神，广大青年纷纷表示，一定牢记习近平总书记嘱托，坚定理想信念，筑牢精神之基，厚植爱国情怀，矢志不渝跟党走，以实现中华民族伟大复兴为己任，增强做中国人的志气、骨气、底气，不负时代，不负韶华，不负党和人民的殷切期望。

在海南省陵水海域，全球首座10万吨级深水半潜式生产储油平台“深海一号”钻机轰鸣，作业忙碌。甲板上，气田开发生产团队工艺工程师刘昱亮正和同事们一起调试设备。过去5年来，这支青年人占比七成以上的团队先后攻克一系列行业技术难题。展望未来，刘昱亮和团队成员充满信心：“我们将围绕党的二十大报告提出的‘加大油气资源勘探开发和增储上产力度’部署要求，为保障国家能源安全作出新的贡献。”

这几天，南京大学现代工程与应用科学学院教授李喆，正带领课题组探讨针对动脉粥样硬化疾病的新型纳米治疗方法。李喆在国外获得博士学位后，于2015年回国。今年5月，习近平总书记给南京大学的留学归国青年学者回信，勉励他们“在坚持立德树人、推动科技自立自强上再创佳绩，在坚定文化自信、讲好中国故事上争做表率”。李喆深感重任在肩，调整课题方向专攻生物医学应用研究。铭记习近平总书记殷切期望，李喆表示：“生逢伟大时代，肩负光荣使命，我将努力为国家培养更多人才，在科学研究中不断突破创新。”

西藏自治区林芝市巴宜区委组织部干部黄海芬，最近正和同事深入基层收集记录红色故事，为巴宜区筹办红色研学主题教育展馆准备素材。5年前，广东姑娘黄海芬大学毕业后放弃舒适的工作，怀揣梦想奔赴雪域高原。学习领会党的二十大精神，黄海芬更加坚定了自己的选择：“西藏是我施展才干的广阔舞台，我将铸牢中华民族共同体意识，为民族团结进步事业多作贡献。”

深秋的可可西里，昆仑负雪，大地苍茫。今年33岁的三江源国家公园长江源园区可可西里管理处索南达杰保护站副站长龙周才加，已在这片土地上守护藏羚羊10多年。“如今在可可西里保护站，80后、90后青年已成为骨干和主力。在党的二十大精神指引下，我们将携手奋斗，守护好‘中华水塔’，保护好青藏高原生态环境。”

在长沙机场改扩建工程T3航站楼项目现场，对着施工样板，中国建筑五局总承包公司项目质量总监邹彬为工友们讲解如何确保工序质量标准。这位95后党员曾获第四十三届世界技能大赛砌筑项目优胜奖。“这些年，培育新型产业工人方面出台了很多好政策，给了青年技能人才越来越大的施展平台。”学习领会党的二十大精神，邹彬感受颇深，“一定珍惜这个伟大时代，做新时代的奋斗者，带领更多青年走技能成才、技能报国之路。”

哈尔滨电气集团有限公司首席技师、高技能专家孙柏慧从一名学徒工干起，迄今已带领团队完成一系列技术革新，主导完成科研、攻关、发明专利等40余项。“党的二十大报告充分回应包括青年在内的广大干部群众对美好生活的向往，为我们青年建功立业提供了广阔舞台。”今年32岁的孙柏慧说，作为一名产业技术工人，将潜心钻研业务、练就过硬本领，努力在新征程中书写精彩人生。

这几天，西安交通大学各班陆续举办学习党的二十大精神主题班会。上世纪50年代，一批交大人响应党的号召从上海迁至西安，用高昂情怀和满腔热血铸就了“胸怀大局、无私奉献、弘扬传统、艰苦创业”的“西迁精神”。如今，参观交大西迁博物馆、学习西迁精神，成为西安交大学子的必修课。“学习贯彻党的二十大精神，我们要把青年工作作为战略性工作来抓，用习近平新时代中国特色社会主义思想武装青年，用党的初心使命感召青年，做青年朋友的知心人、青年工作的热心人、青年群众的引路人。”从事班主任工作12年的西安交大机械工程学院青年教授雷亚国表示，将进一步激励交大学子当好“西迁精神”新传人，到祖国建设最需要的地方建功立业。
    '''
    ui.QTextEdit.setText(_text)
    sys.exit(app.exec())
