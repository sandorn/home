"""
PyXLL Examples: Callbacks

The PyXLL Excel Addin is configured to load one or more
python modules when it's loaded.

Moldules can register callbacks with PyXLL that will be
called at various times to inform the user code of
certain events.
"""

from pyxll import xl_on_open,               \
                    xl_on_reload,           \
                    xl_on_close,            \
                    xl_license_notifier,    \
                    xlcAlert,               \
                    xlcCalculateNow

import logging
_log = logging.getLogger(__name__)

@xl_on_open
def on_open(import_info):
    """
    on_open is registered to be called by PyXLL when the addin
    is opened via the xl_on_open decorator.
    This happens each time Excel starts with PyXLL installed.
    """
    # Check to see which modules didn't import correctly.
    for modulename, module, exc_info in import_info:
        if module is None:
            exc_type, exc_value, exc_traceback = exc_info
            _log.error("Error loading '%s' : %s" % (modulename, exc_value))

@xl_on_reload
def on_reload(import_info):
    """
    on_reload is registered to be called by PyXLL whenever a
    reload occurs via the xl_on_reload decorator.
    """
    # Check to see if any modules didn't import correctly.
    errors = 0
    for modulename, module, exc_info in import_info:
        if module is None:
            exc_type, exc_value, exc_traceback = exc_info
            _log.error("Error loading '%s' : %s" % (modulename, exc_value))
            errors += 1

    # Report if everything reloaded OK.
    # If there are errors they will be dealt with by the error_handler.
    if errors == 0:
        xlcAlert("Everything reloaded OK!\n\n(Message from callbacks.py example)")

    # Recalculate all open workbooks.
    xlcCalculateNow()

@xl_on_close
def on_close():
    """
    on_close will get called as Excel is about to close.

    This is a good time to clean up any globals and stop
    any background threads so that the python interpretter
    can be closed down cleanly.
    
    The user may cancel Excel closing after this has been
    called, so your code should make sure that anything
    that's been cleaned up here will get recreated again
    if it's needed.
    """
    _log.info("callbacks.on_close: PyXLL is closing")

@xl_license_notifier
def license_notifier(name, expdate, days_left, is_perpetual):
    """
    license_notifier will be called when PyXLL is starting up, after
    it has read the config and verified the license.
    
    If there is no license name will be None and days_left will be less than 0.
    """
    if days_left >= 0 or is_perpetual:
        _log.info("callbacks.license_notifier: "
                    "This copy of PyXLL is licensed to %s" % name)
        if not is_perpetual:
            _log.info("callbacks.license_notifier: "
                        "%d days left before the license expires (%s)" % (days_left, expdate))
    elif expdate is not None:
        _log.info("callbacks.license_notifier: License key expired on %s" % expdate)
    else:
        _log.info("callbacks.license_notifier: Invalid license key")