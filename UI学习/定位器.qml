import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.1


ApplicationWindow {
    id: _window

    // 窗口标题设置
    title: "定位器"
    width: 400
    height: 400

    // Window默认不可见，需要进行设置为可见
    visible: true

    menuBar: MenuBar {
        Menu {
            title: "File"
            Action {
            text: "New"
            shortcut: "Ctrl+N"
            }
            Action {
                text: "Open"
                shortcut: "Ctrl+O"
            }
        }
        Menu {
            title: "Help"
            Action {
                text: "About App"
                shortcut: "F1"
            }
        }
    }

    header: ToolBar {
        // 横向
        RowLayout {
            ToolButton {
                // 设置提示文字
                ToolTip.visible: hovered
                ToolTip.text: qsTr("Create new File")
                // 设置命令图标
                icon.name: "New"
                icon.source: "../img/new.png"
            }
            ToolButton {
                ToolTip.visible: hovered
                ToolTip.text: qsTr("Open File")
                icon.name: "Open"
                icon.source: "../img/open.png"
            }
        }
    }

    Grid {
        columns: 3
        spacing: 5
        Rectangle { color: "red"; width: 50; height: 50 }

        Row {
            spacing: 0
            Rectangle { color: "green"; width: 50; height: 50 }
            Rectangle { color: "gray"; width:50; height: 50 }
        }

        Column {
            spacing: 0
            Rectangle { color: "yellow"; width: 50; height: 50 }
            Rectangle { color: "black"; width: 50; height: 50 }
            Rectangle { color: "blue"; width:50; height: 50 }
        }

        Rectangle { color: "brown"; width: 50; height: 50 }
        
        Flow {
            width: 200
            spacing: 5

            Repeater {
                model: 7
                Rectangle {
                    width: 50
                    height: 50
                    color: 'green'
                }
            }
        }
    }
}
