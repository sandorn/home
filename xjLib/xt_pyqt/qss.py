# !/usr/bin/env python
"""
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-15 23:56:43
#LastEditTime : 2020-06-17 16:20:16
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
"""

QStatusBarstyle = """
    QStatusBar{background-color:LightGray;color:Navy;font:bold 10pt 'Sarasa Term SC'}
"""

QProgressBarstyle = """
    QProgressBar{border: 1px solid grey;text-align: center;font:bold 10pt 'Sarasa Term SC'}
"""
# #QProgressBar{border:1px solid grey;border-radius: 5px;text-align: center;font:bold 8pt 微软雅黑;}
# #QProgressBar::chunk{background-color: #CD96CD;width: 10px;margin: 0.5px;}# 斑马线,色条

QToolBarstyle = """
    QToolBar{spacing: 8px;font:bold 11pt 'Sarasa Term SC';}
    QToolButton{font:bold 10pt 'Sarasa Term SC';background-color:transparent;margin:0px 0px;border-bottom:1px solid #DBDBDB;}
    QToolButton::hover{background-color: #2dabf9;}
"""

QMenuBarstyle = """
    QMenuBar{spacing: 8px;font:bold 11pt 'Sarasa Term SC';}
    QMenu{font:bold 10pt 'Sarasa Term SC';background-color:white;border:1px solid white;}
    QMenu::item{background-color: transparent;padding:8px 32px;margin:0px 8px;border-bottom:1px solid #DBDBDB;}
    QMenu::item:selected{background-color: #2dabf9;}
"""

QTableWidgetstyle = """
    QTableWidget{color:green;border:1px solid gray;selection-background-color:gray;font:10pt 微软雅黑;}
    QHeaderView::section:vertical {background-color:lightblue;font:bold 10pt 微软雅黑;}
    QHeaderView::section:horizontal {background-color:lightblue;font:bold 10pt 微软雅黑;}
    QTableCornerButton::section{background-color:lightblue;}
"""

QListWidgetstyle = """
    QListWidget{color:green;border:1px solid gray;selection-background-color:gray;font:10pt 微软雅黑;}
    QListWidget::Item{padding-top:-2px; padding-bottom:-1px;}
    QListWidget::Item:hover{background:skyblue;padding-top:0px; padding-bottom:0px;}
    QListWidget::item:selected{background:lightgray; color:red; }
    QListWidget::item:selected:active{border-width:0px;background:lightgreen;}
    QListWidget::item:selected:!active{border-width:0px;background:lightgreen;}
"""

QTabWidgetstyle = """
    QTabWidget{font:10pt 微软雅黑;}
    QTabWidget::pane{border-width:1px;border-color:rgb(48, 104, 151);border-style: outset;background-color: rgb(132, 171, 208);background: transparent;}
    QTabWidget::tab-bar{border-width:0px;}
    QTabBar::tab{border-bottom-color: #C2C7CB; border-top-left-radius: 0px;border-top-right-radius: 0px;min-height:25px;font:10pt 微软雅黑; padding: 0px;}
    QTabBar::tab:selected{color:blue;}
    QTabBar::tab:!selected{color:black;}
    QTabBar::tab:hover:!selected{color:red;}
    QTabBar::scroller{width:25;border:0;padding:0px;}
    QTabBarQToolButton{background-color:rgb(132,171,208);border-width:0;background-image:url(:/images/tab/rightbtn.png);}
"""

QPushButtonstyle = """
    QPushButton{background-color:rgb(248,242,220);color:black;border-radius:10px;border:2px groove gray;border-style:outset;font:bold 11pt 'Sarasa Term SC';}
    QPushButton:hover{background-color:rgb(22,36,92);color:white;}
    QPushButton:pressed{background-color:rgb(163,159,147);border-style:inset;}
"""

QLineEditstyle = """
    QLineEdit{width:100% ;height:20%; border:2px groove gray;border-radius:10px;padding:2px 4px;background:lightBlue;color:Indigo; font:11pt 微软雅黑;}
    QLineEdit:hover{border-width: 1px; border-radius: 4px; font-size:12px; color: black; border:1px solid rgb(70, 200, 50);}
"""

QLabelstyle = """
    QLabel{color:rgb(100,100,250);font:bold 10pt  'Sarasa Term SC';}
"""
QTextEditstyle = """
    QTextEdit{width:100% ;height:20%; border:2px groove gray;border-radius:10px;padding:2px 4px;background:lightBlue;color:Indigo;font:12pt 'Sarasa Term SC';}
"""
QSplitterstyle = """
    QSplitter::handle{background:lightgray;}
"""

allstyles = QStatusBarstyle + QProgressBarstyle + QToolBarstyle + QMenuBarstyle + QTableWidgetstyle + QListWidgetstyle + QTabWidgetstyle + QPushButtonstyle + QLineEditstyle + QLabelstyle + QTextEditstyle + QSplitterstyle

if __name__ == '__main__':
    pass
    from qdarkstyle.utils.scss import _dict_to_scss, create_custom_qss_from_dict

    temp = {
        'QPushButton': {'background-color': 'rgb(248,242,220)', 'color': 'black', 'border-radius': '10px', 'border': '2px groove gray', 'border-style': 'outset', 'font': "bold 11pt 'Sarasa Term SC'"},
        'QPushButton:hover': {'background-color': 'rgb(22,36,92)', 'color': 'white'},
        'QPushButton:pressed': {'background-color': 'rgb(163,159,147)', 'border-style': 'inset'},
    }
    style = _dict_to_scss(temp)

    print(style, QPushButtonstyle)

    qss = create_custom_qss_from_dict(
        'mytest',
        'd:/',
        {
            'color_background_light': '#FFFF99',
            'color_background_normal': '#006600',
            'color_background_dark': '#99CC99',
            'color_foreground_light': '#99CCFF',
            'color_foreground_normal': '#333366',
            'color_foreground_dark': '#003366',
            'color_selection_light': '#CCCCFF',
            'color_selection_normal': '#999999',
            'color_selection_dark': '#660033',
            'border_radius': '0px',
        },
    )
    print(qss)
"""
    import sys, qdarkstyle
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


    styleFile = 'd:/CODE/xjLib/xt_ui/white.qss'
    qssStyle = readQss.all(styleFile)
    app.setStyleSheet(qssStyle)
"""
