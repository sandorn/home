# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Software :   VSCode
@File     :   pyqt5-记事本-main.py
@Time     :   2019/05/06 17:47:19
@Author   :   Even Sand
@Version  :   1.0
@Contact  :   sandorn@163.com
@License  :   (C)Copyright 2009-2019, NewSea
《快速掌握PyQt5》第二十三章 主窗口QMainWindow - La_vie_est_belle的博客 - CSDN博客
https://blog.csdn.net/La_vie_est_belle/article/details/82819766
'''
import sys
import os
import time
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QMimeData, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QMessageBox,\
                            QFontDialog, QColorDialog, QSplashScreen


class mywindow(QMainWindow):
    is_saved = True
    is_saved_first = True
    path = ''

    def __init__(self):
        super(mywindow, self).__init__()
        _path =os.path.dirname(__file__)+'/'
        self.setWindowIcon(QIcon(_path+'images/book.png'))
        self.file_menu = self.menuBar().addMenu('File')
        self.edit_menu = self.menuBar().addMenu('Edit')
        self.help_menu = self.menuBar().addMenu('Help')

        self.file_toolbar = self.addToolBar('File')
        self.edit_toolbar = self.addToolBar('Edit')
        self.help_toolbar = self.addToolBar('Help')

        self.status_bar = self.statusBar()

        self.new_action = QAction('New', self)
        self.open_action = QAction('Open', self)
        self.save_action = QAction('Save', self)
        self.save_as_action = QAction('Save As', self)
        self.close_action = QAction('Close', self)
        self.cut_action = QAction('Cut', self)
        self.copy_action = QAction('Copy', self)
        self.paste_action = QAction('Paste', self)
        self.font_action = QAction('Font', self)
        self.color_action = QAction('Color', self)
        self.about_action = QAction('Qt', self)

        self.text_edit = QTextEdit(self)

        self.mime_data = QMimeData()
        self.clipboard = QApplication.clipboard()

        self.setCentralWidget(self.text_edit)
        self.resize(450, 600)

        self.menu_init()
        self.toolbar_init()
        self.status_bar_init()
        self.action_init()
        self.text_edit_int()

    def menu_init(self):
        self.file_menu.addAction(self.new_action)
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.save_as_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.close_action)
        self.edit_menu.addAction(self.cut_action)
        self.edit_menu.addAction(self.copy_action)
        self.edit_menu.addAction(self.paste_action)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.font_action)
        self.edit_menu.addAction(self.color_action)
        self.help_menu.addAction(self.about_action)

    def toolbar_init(self):
        self.file_toolbar.addAction(self.new_action)
        self.file_toolbar.addAction(self.open_action)
        self.file_toolbar.addAction(self.save_action)
        self.file_toolbar.addAction(self.save_as_action)
        self.edit_toolbar.addAction(self.cut_action)
        self.edit_toolbar.addAction(self.copy_action)
        self.edit_toolbar.addAction(self.paste_action)
        self.edit_toolbar.addAction(self.font_action)
        self.edit_toolbar.addAction(self.color_action)
        self.edit_toolbar.addSeparator() # 分割线
        self.help_toolbar.addAction(self.close_action)

    def status_bar_init(self):
        self.status_bar.showMessage('Ready to compose')

    def action_init(self):
        _path =os.path.dirname(__file__)+'/'
        self.new_action.setIcon(QIcon(_path+'images/new.ico'))
        self.new_action.setShortcut('Ctrl+N')
        self.new_action.setToolTip('Create a new file')
        self.new_action.setStatusTip('Create a new file')
        self.new_action.triggered.connect(self.new_func)

        self.open_action.setIcon(QIcon(_path+'images/open.ico'))
        self.open_action.setShortcut('Ctrl+O')
        self.open_action.setToolTip('Open an existing file')
        self.open_action.setStatusTip('Open an existing file')
        self.open_action.triggered.connect(self.open_file_func)

        self.save_action.setIcon(QIcon(_path+'images/save.ico'))
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.setToolTip('Save the file')
        self.save_action.setStatusTip('Save the file')
        self.save_action.triggered.connect(lambda: self.save_func(self.text_edit.toHtml()))

        self.save_as_action.setIcon(QIcon(_path+'images/save_as.ico'))
        self.save_as_action.setShortcut('Ctrl+A')
        self.save_as_action.setToolTip('Save the file to a specified location')
        self.save_as_action.setStatusTip('Save the file to a specified location')
        self.save_as_action.triggered.connect(lambda: self.save_as_func(self.text_edit.toHtml()))

        self.close_action.setIcon(QIcon(_path+'images/close.ico'))
        self.close_action.setShortcut('Ctrl+E')
        self.close_action.setToolTip('Close the window')
        self.close_action.setStatusTip('Close the window')
        self.close_action.triggered.connect(self.close_func)

        self.cut_action.setIcon(QIcon(_path+'images/cut.ico'))
        self.cut_action.setShortcut('Ctrl+X')
        self.cut_action.setToolTip('Cut the text to clipboard')
        self.cut_action.setStatusTip('Cut the text')
        self.cut_action.triggered.connect(self.cut_func)

        self.copy_action.setIcon(QIcon(_path+'images/copy.ico'))
        self.copy_action.setShortcut('Ctrl+C')
        self.copy_action.setToolTip('Copy the text')
        self.copy_action.setStatusTip('Copy the text')
        self.copy_action.triggered.connect(self.copy_func)

        self.paste_action.setIcon(QIcon(_path+'images/paste.ico'))
        self.paste_action.setShortcut('Ctrl+V')
        self.paste_action.setToolTip('Paste the text')
        self.paste_action.setStatusTip('Paste the text')
        self.paste_action.triggered.connect(self.paste_func)

        self.font_action.setIcon(QIcon(_path+'images/font.ico'))
        self.font_action.setShortcut('Ctrl+T')
        self.font_action.setToolTip('Change the font')
        self.font_action.setStatusTip('Change the font')
        self.font_action.triggered.connect(self.font_func)

        self.color_action.setIcon(QIcon(_path+'images/color.ico'))
        self.color_action.setShortcut('Ctrl+R')
        self.color_action.setToolTip('Change the color')
        self.color_action.setStatusTip('Change the color')
        self.color_action.triggered.connect(self.color_func)

        self.about_action.setIcon(QIcon(_path+'images/about.ico'))
        self.about_action.setShortcut('Ctrl+Q')
        self.about_action.setToolTip('What is Qt?')
        self.about_action.setStatusTip('What is Qt?')
        self.about_action.triggered.connect(self.about_func)

    def text_edit_int(self):
        self.text_edit.textChanged.connect(self.text_changed_func)

    def text_changed_func(self):
        if self.text_edit.toPlainText():
            self.is_saved = False
        else:
            self.is_saved = True

    def new_func(self):
        if not self.is_saved:
            choice = QMessageBox.question(self, '', 'Do you want to save the text?',
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if choice == QMessageBox.Yes:
                self.save_func()
                self.text_edit.clear()
            elif choice == QMessageBox.No:
                self.text_edit.clear()
            else:
                pass
        else:
            self.text_edit.clear()

    def open_file_func(self):
        if not self.is_saved:
            choice = QMessageBox.question(self, '', 'Do you want to save the text?',
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if choice == QMessageBox.Yes:
                self.save_func()
                file, _ = QFileDialog.getOpenFileName(self, 'Open File', './', 'Files (*.html *.txt *.log)')
                if file:
                    with open(file, 'r') as f:
                        self.text_edit.clear()
                        self.text_edit.setText(f.read())
                        self.is_saved = True
            elif choice == QMessageBox.No:
                file, _ = QFileDialog.getOpenFileName(self, 'Open File', './', 'Files (*.html *.txt *.log)')
                if file:
                    with open(file, 'r') as f:
                        self.text_edit.clear()
                        self.text_edit.setText(f.read())
                        self.is_saved = True
            else:
                pass
        else:
            file, _ = QFileDialog.getOpenFileName(self, 'Open File', './', 'Files (*.html *.txt *.log)')
            if file:
                with open(file, 'r') as f:
                    self.text_edit.clear()
                    self.text_edit.setText(f.read())
                    self.is_saved = True

    def save_func(self, text):
        if self.is_saved_first:
            self.save_as_func(text)
        else:
            with open(self.path, 'w') as f:
                f.write(text)
            self.is_saved = True

    def save_as_func(self, text):
        self.path, _ = QFileDialog.getSaveFileName(self, 'Save File', './', 'Files (*.html *.txt *.log)')
        if self.path:
            with open(self.path, 'w') as f:
                f.write(text)
            self.is_saved = True
            self.is_saved_first = False

    def close_func0(self):
        if not self.is_saved:
            choice = QMessageBox.question(self, 'Save File', 'Do you want to save the text?',
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if choice == QMessageBox.Yes:
                self.save_func(self.text_edit.toHtml())
                self.close()
            elif choice == QMessageBox.No:
                self.close()
            else:
                pass

    def close_func(self):
        self.close()

    def closeEvent(self, QCloseEvent):
        if not self.is_saved:
            choice = QMessageBox.question(self, 'Save File', 'Do you want to save the text?',
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if choice == QMessageBox.Yes:
                self.save_func(self.text_edit.toHtml())
                QCloseEvent.accept()
            elif choice == QMessageBox.No:
                QCloseEvent.accept()
            else:
                QCloseEvent.ignore()

    def cut_func(self):
        self.mime_data.setHtml(self.text_edit.textCursor().selection().toHtml())
        self.clipboard.setMimeData(self.mime_data)
        self.text_edit.textCursor().removeSelectedText()

    def copy_func(self):
        self.mime_data.setHtml(self.text_edit.textCursor().selection().toHtml())
        self.clipboard.setMimeData(self.mime_data)

    def paste_func(self):
        self.text_edit.insertHtml(self.clipboard.mimeData().html())

    def font_func(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.text_edit.setFont(font)

    def color_func(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_edit.setTextColor(color)

    def about_func(self):
        QMessageBox.aboutQt(self, 'About Qt')


def main():
    app = QApplication(sys.argv)
    splash = QSplashScreen()

    _path =os.path.dirname(__file__)+'/'
    splash.setPixmap(QPixmap(_path + 'images/splash.jpg'))
    splash.show()
    splash.showMessage('Welcome to Use This PyQt5-Made Notebook~',
                       Qt.AlignBottom | Qt.AlignCenter, Qt.white)
    time.sleep(2)

    demo = mywindow()
    demo.show()
    splash.finish(demo)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
