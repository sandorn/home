import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Controls 1.4 as Controls1
import QtQuick.Layouts 1.1


ApplicationWindow {
    id: _window

    // 窗口标题设置
    title: "SplitView布局"
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

    Controls1.SplitView{
        anchors.fill:parent;
        orientation: Qt.Horizontal;
        Rectangle{
            id:rect1;
            width:100;
            color:"red";
        }
        Rectangle{
            id:rect2;
            Layout.fillWidth: true;
            Layout.minimumWidth: 50;
            color:"blue";
        }
        Rectangle{
            id:rect3;
            width:100;
            color:"green";
        }
    }

}
