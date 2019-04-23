import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Controls 1.4 as Controls1
import QtQuick.Layouts 1.1


ApplicationWindow {
    id: _window

    // 窗口标题设置
    title: "Test App"
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

    Rectangle{
        id: rec001
        height: 80
        width: 80
        color: "yellow"
        //锚定位在父元素的中间
        anchors.centerIn: parent
    }
    Rectangle{
        id: rec010
        height: 80
        width: 80
        color: "red"
        // right与rec001的left对齐
        anchors.right: rec001.left
        // 右侧外边距
        anchors.rightMargin: 40
        // verticalCenter与rec001的对齐
        anchors.verticalCenter: rec001.verticalCenter
        // verticalCenter偏移量
        anchors.verticalCenterOffset: 0
    }

    Rectangle{
        id: rec011
        height: 80
        width: 80
        color: "green"
        anchors.left: rec001.right
        anchors.leftMargin: 40
        anchors.verticalCenter: rec001.verticalCenter
        anchors.verticalCenterOffset: 0
    }
    Rectangle{
        id: rec100
        height: 80
        width: 80
        color: "cyan"
        anchors.bottomMargin: 40
        anchors.horizontalCenter: rec001.horizontalCenter
        anchors.horizontalCenterOffset: 0
    }
    Rectangle{
        id: rec101
        height: 80
        width: 80
        color: "blue"
        anchors.top: rec001.bottom
        anchors.topMargin: 40
        anchors.horizontalCenter: rec001.horizontalCenter
        anchors.horizontalCenterOffset: 0
    }

}
