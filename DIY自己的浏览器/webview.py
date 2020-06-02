# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Software:   VSCode
@File    :   webview.py
@Time    :   2019/05/05 18:10:28
@Author  :   Even Sand
@Version :   1.0
@Contact :   sandorn@163.com
@License :   (C)Copyright 2019-2019, NewSea
@Desc    :   None
PyQt5系列教程（81）：DIY自己的浏览器-3
http://www.xdbcb8.com/archives/1581.html
'''

import sys
from PyQt5.QtCore import pyqtSlot, QUrl, QEvent, Qt, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication, QTabWidget, QMessageBox, QWidget, QVBoxLayout, QCompleter
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from Ui_ui import Ui_MainWindow


class NewWebView(QWebEngineView):

    def __init__(self, tabWidget):
        super().__init__()
        self.tabWidget = tabWidget

    def createWindow(self, WebWindowType):
        new_webview = NewWebView(self.tabWidget)
        self.tabWidget.newTab(new_webview)
        return new_webview


class WebView(QMainWindow, Ui_MainWindow):
    """Class documentation goes here."""

    def __init__(self, parent=None):
        """
        Constructor
        @param parent reference to the parent widget
        @type QWidget
        """
        super(WebView, self).__init__(parent)
        self.setupUi(self)
        self.initUi()

    def initUi(self):

        self.progressBar.hide()
        self.showMaximized()
        # self.tabWidget.setTabShape(QTabWidget.Triangular)
        # self.tabWidget.setDocumentMode(True)
        # self.tabWidget.setMovable(True)
        # self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.tabWidget.currentChanged.connect(self.tabChange)
        self.view = NewWebView(self)
        self.view.load(QUrl("https://www.baidu.com"))
        self.newTab(self.view)
        self.lineEdit.installEventFilter(self)
        self.lineEdit.setMouseTracking(True)
        settings = QWebEngineSettings.defaultSettings()
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        # settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.getModel()

    def getModel(self):
        self.m_model = QStandardItemModel(0, 1, self)
        m_completer = QCompleter(self.m_model, self)
        self.lineEdit.setCompleter(m_completer)
        m_completer.activated[str].connect(self.onUrlChoosed)

    def newTab(self, view):
        self.pb_forward.setEnabled(False)
        self.pb_back.setEnabled(False)
        view.titleChanged.connect(self.webTitle)  # 重点学习
        view.iconChanged.connect(self.webIcon)
        view.loadProgress.connect(self.webProgress)
        view.loadFinished.connect(self.webProgressEnd)
        view.urlChanged.connect(self.webHistory)
        view.page().linkHovered.connect(self.showUrl)
        currentUrl = self.getUrl(view)

        self.lineEdit.setText(currentUrl)
        self.tabWidget.addTab(view, "新标签页")
        self.tabWidget.setCurrentWidget(view)

    def getUrl(self, webview):
        url = webview.url().toString()
        return url

    def closeTab(self, index):
        if self.tabWidget.count() > 1:
            self.tabWidget.widget(index).deleteLater()
            self.tabWidget.removeTab(index)
        elif self.tabWidget.count() == 1:
            self.tabWidget.removeTab(0)
            self.on_pb_new_clicked()

    def tabChange(self, index):

        currentView = self.tabWidget.widget(index)
        if currentView:
            currentViewUrl = self.getUrl(currentView)
            self.lineEdit.setText(currentViewUrl)

    def closeEvent(self, event):
        tabNum = self.tabWidget.count()
        closeInfo = "你打开了{}个标签页，现在确认关闭？".format(tabNum)
        if tabNum > 1:
            r = QMessageBox.question(self, "关闭浏览器", closeInfo,
                                     QMessageBox.Ok | QMessageBox.Cancel,
                                     QMessageBox.Cancel)
            if r == QMessageBox.Ok:
                event.accept()
            elif r == QMessageBox.Cancel:
                event.ignore()
        else:
            event.accept()

    def eventFilter(self, object, event):
        if object == self.lineEdit:
            if event.type() == QEvent.MouseButtonRelease:
                self.lineEdit.selectAll()
            elif event.type() == QEvent.KeyPress:
                if event.key() == Qt.Key_Return:
                    self.on_pb_go_clicked()
        return QObject.eventFilter(self, object, event)

    def webTitle(self, title):
        index = self.tabWidget.currentIndex()
        if len(title) > 16:
            title = title[0:17]
        self.tabWidget.setTabText(index, title)

    def webIcon(self, icon):
        index = self.tabWidget.currentIndex()
        self.tabWidget.setTabIcon(index, icon)

    def webProgress(self, progress):
        self.progressBar.show()
        self.progressBar.setValue(progress)

    def webProgressEnd(self, isFinished):
        if isFinished:
            self.progressBar.setValue(100)
            self.progressBar.hide()
            self.progressBar.setValue(0)

    def webHistory(self, url):
        self.lineEdit.setText(url.toString())
        index = self.tabWidget.currentIndex()
        currentView = self.tabWidget.currentWidget()
        history = currentView.history()
        if history.count() > 1:
            if history.currentItemIndex() == history.count() - 1:
                self.pb_back.setEnabled(True)
                self.pb_forward.setEnabled(False)
            elif history.currentItemIndex() == 0:
                self.pb_back.setEnabled(False)
                self.pb_forward.setEnabled(True)
            else:
                self.pb_back.setEnabled(True)
                self.pb_forward.setEnabled(True)

    def showUrl(self, url):
        self.statusBar.showMessage(url)

    def onUrlChoosed(self, url):
        self.lineEdit.setText(url)

    @pyqtSlot(str)
    def on_lineEdit_textChanged(self, text):

        urlGroup = text.split(".")

        if len(urlGroup) == 3 and urlGroup[-1]:
            return
        elif len(urlGroup) == 3 and not (urlGroup[-1]):
            wwwList = ["com", "cn", "net", "org", "gov", "cc"]
            self.m_model.removeRows(0, self.m_model.rowCount())
            for i in range(0, len(wwwList)):
                self.m_model.insertRow(0)
                self.m_model.setData(
                    self.m_model.index(0, 0), text + wwwList[i])

    @pyqtSlot()
    def on_pb_new_clicked(self):
        """
        Slot documentation goes here.
        """
        newView = NewWebView(self)
        self.newTab(newView)
        newView.load(QUrl(""))

    @pyqtSlot()
    def on_pb_forward_clicked(self):
        """
        Slot documentation goes here.
        """
        self.tabWidget.currentWidget().forward()

    @pyqtSlot()
    def on_pb_back_clicked(self):
        """
        Slot documentation goes here.
        """
        self.tabWidget.currentWidget().back()

    @pyqtSlot()
    def on_pb_refresh_clicked(self):
        """
        Slot documentation goes here.
        """
        self.tabWidget.currentWidget().reload()

    @pyqtSlot()
    def on_pb_stop_clicked(self):
        """
        Slot documentation goes here.
        """
        self.tabWidget.currentWidget().stop()

    @pyqtSlot()
    def on_pb_go_clicked(self):
        """
        Slot documentation goes here.
        """
        url = self.lineEdit.text()
        if url[0:7] == "http://" or url[0:8] == "https://":
            qurl = QUrl(url)
        else:
            qurl = QUrl("http://" + url)
        self.tabWidget.currentWidget().load(qurl)

    @pyqtSlot()
    def on_pb_home_clicked(self):
        """
        Slot documentation goes here.
        """
        homeurl = QUrl("http://www.xdbcb8.com")
        if self.tabWidget.currentWidget().title() == "about:blank":
            self.tabWidget.currentWidget().load(homeurl)
        else:
            newView = NewWebView(self)
            self.newTab(newView)
            newView.load(homeurl)

    def __del__(self):
        self.view.deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wv = WebView()
    wv.show()
    sys.exit(app.exec_())
