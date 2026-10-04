"""Actions bound to the sketch-only keys and the launcher."""

import FreeCAD
import FreeCADGui
from PySide import QtWidgets

from . import log
from .constants import LOG_TAG
from .tool_catalog import command_candidates

STATUS_MESSAGE_MS = 2000


def resolve_command(cmd_name):
    """Pick the first candidate command name registered in this FreeCAD."""
    available = set(FreeCADGui.listCommands())
    for name in command_candidates(cmd_name):
        if name in available:
            return name
    return cmd_name


def close_popup():
    """Close the open popup (the launcher). Return True if there was one."""
    popup = QtWidgets.QApplication.activePopupWidget()
    if popup is None:
        return False
    popup.close()
    return True


def _show_status(text):
    mw = FreeCADGui.getMainWindow()
    if mw:
        mw.statusBar().showMessage(text, STATUS_MESSAGE_MS)


def run_sketch_command(cmd_name, label=None):
    try:
        close_popup()
        resolved = resolve_command(cmd_name)
        if resolved != cmd_name:
            log.debug("command %s -> %s" % (cmd_name, resolved))
        if label:
            _show_status(label)
        FreeCADGui.runCommand(resolved)
    except Exception as e:
        FreeCAD.Console.PrintError(
            f"{LOG_TAG} Command failed: {cmd_name} ({e})\n"
        )
