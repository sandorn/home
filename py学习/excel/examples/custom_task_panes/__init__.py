"""
PyXLL Examples: Qt Custom Task Pane

These examples show how Excel Custom Task Panes can be created
by PyXLL to host widgets created using Python's main UI toolkits.

The supported Python UI Toolkits are:

- Tkinter
- Qt5 (PySide2 and PyQt5)
- WxWindows

Tkinter is usually installed as a standard library with Python
but the other UI toolkits will need to be installed using pip
or conda for the examples to work.

Custom Task Panes are Excel controls that can be docked in the
Excel application or be floating windows. These can be used for
creating more advanced UI Python tools within Excel.
"""
from pyxll import xl_menu

def _check_pywin32():
    try:
        import win32com
    except ImportError:
        raise RuntimeError("""

pywin32 needs to be installed for this example.
Install either using pip or conda and try again.

""")

def show_tk_ctp():
    _check_pywin32()
    try:
        from . import tk_ctp
        tk_ctp.show_tk_ctp()
    except ImportError:
        raise RuntimeError("""

Tkinter needs to be installed for this example.
Install either using pip or conda and try again.

""")

def show_qt_ctp():
    _check_pywin32()
    try:
        from . import qt_ctp
        qt_ctp.show_qt_ctp()
    except ImportError:
        raise RuntimeError("""

Either PyQt5 or PySide2 needs to be installed for this example.
Install either using pip or conda and try again.

""")

def show_wx_ctp():
    _check_pywin32()
    try:
        from . import wx_ctp
        wx_ctp.show_wx_ctp()
    except ImportError:
        raise RuntimeError("""

wxPython to be installed for this example.
Install either using pip or conda and try again.

""")

#
# Ribbon actions for the example ribbon toolbar
#

def tk_ctp_ribbon_action(control):
    show_tk_ctp()

def qt_ctp_ribbon_action(control):
    show_qt_ctp()

def wx_ctp_ribbon_action(control):
    show_wx_ctp()

#
# Menu functions for the 'Add-ins' tab
#

@xl_menu("Tk", sub_menu="Custom Task Panes")
def tk_ctp_menu():
    show_tk_ctp()

@xl_menu("Qt", sub_menu="Custom Task Panes")
def qt_ctp_menu():
    show_qt_ctp()

@xl_menu("Wx", sub_menu="Custom Task Panes")
def wx_ctp_menu():
    show_wx_ctp()