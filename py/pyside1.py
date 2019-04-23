import sys

try:
    from PySide import QtGui
    from PySide import QtCore
except ImportError:
    from PySide2 import QtWidgets as QtGui
    from PySide2 import QtCore

app = QtGui.QApplication(sys.argv)

hello = QtGui.QPushButton("Hello world!")
hello.resize(100, 30)

hello.show()

sys.exit(app.exec_())
