import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.1


ApplicationWindow {
    id: _window

    // 窗口标题设置
    title: "布局管理器"
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

    GridLayout{
        
        // 行列数量分别为2
        columns: 2;
        rows:2;
        // 填充父元素，外边距为5
        anchors.fill: parent;
        anchors.margins: 5;
        // 行列子控件之间的距离
        columnSpacing: 5;
        rowSpacing: 5;

        Rectangle{
            color: "red";
            Layout.preferredWidth: 200;
            Layout.preferredHeight: 150;
        }

        ColumnLayout {
            spacing: 0
            Rectangle {
                color: "red";
                Layout.preferredWidth: 200;
                Layout.preferredHeight: 75;
            }
            Rectangle {
                color: "blue";
                Layout.preferredWidth: 200;
                Layout.preferredHeight: 75;
            }
        }

        RowLayout {
            spacing: 0
            Rectangle {
                color: "red";
                Layout.preferredWidth: 100;
                Layout.preferredHeight: 150;
            }
            Rectangle {
                color: "green";
                Layout.preferredWidth: 100;
                Layout.preferredHeight: 150;
            }
        }

        Rectangle{
            color: "yellow";
            Layout.preferredWidth: 200;
            Layout.preferredHeight: 150;
        }
    }

}

