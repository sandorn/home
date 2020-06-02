# cidi.py
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

if __name__ == '__main__':

    app = QGuiApplication([])
    engine = QQmlApplicationEngine()
    engine.load(QUrl('定位器.qml'))  #QML文件的相对路径
    engine.load(QUrl('布局管理器.qml'))  #QML文件的相对路径
    engine.load(QUrl('Anchor(锚布局).qml'))  #QML文件的相对路径
    engine.load(QUrl('SplitView布局.qml'))  #QML文件的相对路径

    app.exec_()
