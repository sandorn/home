# -*- coding: utf-8 -*-

"""
Module implementing Dialog_msgbox.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication
import sys

from Ui_ui_messagebox import Ui_Dialog


class Dialog_msgbox(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Dialog_msgbox, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot()
    def on_pushButton_about_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        QMessageBox.aboutQt(self, '关于Qt')
    
    @pyqtSlot()
    def on_pushButton_question_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        reply = QMessageBox.question(self, '询问', '这是选择题哦?默认值是No',QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No )
        if reply == QMessageBox.Yes:
            self.label.setText('你选择了Yes')
        elif reply == QMessageBox.No:
            self.label.setText('你选择了No') 
        else:
            self.label.setText('你选择了Cancel') 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Dialog = Dialog_msgbox()
    Dialog.show()
    sys.exit(app.exec_())
