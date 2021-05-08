"""
PyXLL Examples: Qt Custom Task Pane

This example shows how a Qt widget can be hosted
in an Excel Custom Task Pane.

Custom Task Panes are Excel controls that can be docked in the
Excel application or be floating windows. These can be used for
creating more advanced UI Python tools within Excel.
"""
from pyxll import create_ctp, CTPDockPositionRight, xl_app
import logging
import sys
import os

_log = logging.getLogger(__name__)
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

# There are several Qt packages available for Python, PySide6, PySide2, PyQt6 and PyQt5.
# PyXLL can work with any of these.
qt_imported = False

try:
    # Try PySide6 first
    from PySide6.QtWidgets import *
    from PySide6.QtGui import QPixmap
    _log.info("Using PySide6")
    qt_imported = True
except ImportError:
    pass

if not qt_imported:
    try:
        # Then PySide2 if PySide6 wasn't found
        from PySide2.QtWidgets import *
        from PySide2.QtGui import QPixmap
        _log.info("Using PySide2")
        qt_imported = True
    except ImportError:
        pass

try:
    # Try PyQt6 if PySide wasn't found
    from PyQt6.QtWidgets import *
    from PyQt6.QtGui import QPixmap
    _log.info("Using PyQt6")
    qt_imported = True
except ImportError:
    pass

if not qt_imported:
    # Finally try PyQt5 if none of the others were found
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import QPixmap
    _log.info("Using PyQt5")
    qt_imported = True

class ExampleQtWiget(QWidget):
    """This is an example Qt Widget for demonstrating how a Qt widget
    can be embedded in Excel as a Custom Task Pane.
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Set the window title and create a layout for the widget
        self.setWindowTitle("Qt Example")
        layout = QVBoxLayout()

        # Load the Qt icon and add the header to the widget
        image_path = os.path.join(os.path.dirname(__file__), "icons", "qt.png")
        image = QLabel()
        image.setPixmap(QPixmap(image_path))
        label = QLabel("Qt Custom Task Pane Example")

        header = QHBoxLayout()
        header.addWidget(image)
        header.addWidget(label)
        header.addStretch()
        layout.addLayout(header)

        layout.addSpacing(30)

        # Step 1, getting the address of the currently selected cell
        label = QLabel("1. Press the button to get the current selection")
        self.address = QLineEdit()
        self.address_btn = QPushButton(">>")
        self.address_btn.setStyleSheet("padding: 5px;")
        self.address_btn.clicked.connect(self.get_selected_cell_address)

        button_and_edit = QHBoxLayout()
        button_and_edit.addWidget(self.address_btn)
        button_and_edit.addWidget(self.address)

        layout.addWidget(label)
        layout.addLayout(button_and_edit)

        layout.addSpacing(30)

        # Step 2, getting the value of the cell
        label = QLabel("2. Press the button to get cell value")
        layout.addWidget(label)

        self.load_btn = QPushButton("Get Cell Value")
        self.load_btn.clicked.connect(self.get_cell_value)
        layout.addWidget(self.load_btn)

        layout.addSpacing(30)

        self.cell_value = QLineEdit()
        layout.addWidget(self.cell_value)

        layout.addSpacing(30)

        # Step 3, setting the value of the cell
        label = QLabel("3. Edit the text above and set it")
        layout.addWidget(label)

        self.save_btn = QPushButton("Set Cell Value")
        self.save_btn.clicked.connect(self.set_cell_value)
        layout.addWidget(self.save_btn)

        # Set dialog layout
        layout.addStretch()
        self.setLayout(layout)

    def get_selected_cell_address(self):
        """Get the address of the currently selected cell."""
        xl = xl_app(com_package="win32com")
        address = xl.Selection.Address
        self.address.setText(address)

    def get_cell_value(self):
        address = self.address.text()
        if not address:
            msg = QMessageBox()
            msg.setText("Select a cell with the button above first.");
            msg.exec_()

        xl = xl_app(com_package="win32com")
        cell = xl.Range(address)
        self.cell_value.setText(str(cell.Value))

    def set_cell_value(self):
        address = self.address.text()
        if not address:
            msg = QMessageBox()
            msg.setText("Select a cell with the button above first.");
            msg.exec_()

        xl = xl_app(com_package="win32com")
        cell = xl.Range(address)
        cell.Value = self.cell_value.text()

def show_qt_ctp():
    """Create a Qt Widget and embed it in Excel as a Custom Task Pane."""

    # Before we can create a Qt widget the Qt App must have been initialized
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    # Create our Qt widget
    widget = ExampleQtWiget()

    # Use PyXLL's 'create_ctp' function to create the custom task pane
    create_ctp(widget, width=400, position=CTPDockPositionRight)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = ExampleQtWiget()
    widget.show()
    app.exec_()
