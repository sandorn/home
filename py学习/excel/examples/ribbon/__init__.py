"""
PyXLL Examples: Ribbon

Custom ribbon controls can be added using PyXLL without writing and registering
complicated COM controls.

The ribbon is defined by an XML document, configured in the pyxll.cfg file.

Calls in the XML document are dispatched to Python functions. This module
demonstrates some of the possible callbacks for a sample ribbon.

Most callbacks are passed an IRibbonControl object as a paramter. This is
the ribbon control the callback was associated with and has two properties,
Id and Tag. Both can be set as attributes in the XML so the callbacks can
identify which control they are being called for.

If pythoncom is not available (e.g. if the pywin32 extensions are not
installed) the control passed to the callbacks will be None.

For callbacks that should return an image (IPicture), eg 'getImage'
there is function 'pyxll.load_image' that will load an image from
a file and return it as an IPicture for this purpose.
"""
from pyxll import get_config
import logging
import os

_log = logging.getLogger(__name__)

try:
    from win32api import MessageBox
except ImportError:
    _log.warning("*** win32api could not be imported.                ***")
    _log.warning("*** Some of the ribbon examples will not work.     ***")
    _log.warning("*** to fix this, install the pywin32 extensions.   ***")

# the webbrowser module is used in an example to open the log file
try:
    import webbrowser
except ImportError:
    _log.warning("*** webbrowser could not be imported             ***")
    _log.warning("*** the menu examples will not work correctly    ***")

# All message boxes launched from the ribbon are task-modal (meaning that the
# main window is disabled while the message box is active).
# This prevents problems that occur when trying to display two message boxes
# at once (e.g. if one isn't dismissed before another is created).
MB_TASKMODAL = 0x00002000

def open_logfile(control):
    """Opens the PyXLL log file"""
    config = get_config()
    if not config.has_option("LOG", "path") or not config.has_option("LOG", "file"):
        raise Exception("Log file not found")

    path = os.path.join(config.get("LOG", "path"), config.get("LOG", "file"))
    webbrowser.open("file://%s" % path)

def checkbox_initial_state(control):
    """Called when the checkBox is created."""
    return False

def checkbox_on_action(checked, control):
    """Called when the checkBox is checked or unchecked."""
    msg = "Checkbox is now "
    if checked:
        msg += "checked"
    else:
        msg += "unchecked"
    MessageBox(None, msg, "", MB_TASKMODAL)

_combo_boxes = {
    "ComboBox1": ["Item1", "Item2", "Item3", "Item4"],
    "ComboBox2": ["A", "B", "C"],
}

def combo_box_item_count(control):
    """Called when the comboBox is constructed to get the number of items."""
    return len(_combo_boxes[control.Id])

def combo_box_initial_item(control):
    """Called when the comboBox is contructed to get the intially selected item."""
    return _combo_boxes[control.Id][0]

def combo_box_item(idx, control):
    """Called to get the text for the comboBoxes"""
    return _combo_boxes[control.Id][idx]

def combo_box_on_change(item, control):
    """Called when the comboBox selection is changed."""
    MessageBox(None, "%s is now %s" % (control.Id, item), "", MB_TASKMODAL)

def month_selected(item_idx, item_id, control):
    """Called when something is selected from the Months gallery."""
    MessageBox(None, "%s selected" % item_id, "Months", MB_TASKMODAL)

def show_time_zones(control):
    """Called when the Regional Settings button in the gallery is clicked."""
    # This could be a more complex form using another windowing toolkit such as Qt or Wx.
    MessageBox(None, "This is where you would put your timezone options", "Timezones", MB_TASKMODAL)