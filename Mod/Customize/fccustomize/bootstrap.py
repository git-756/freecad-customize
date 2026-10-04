"""Startup entry point called from InitGui.py."""

import FreeCAD
from PySide import QtCore

from .constants import LOG_TAG
from .navigation import setup_navigation
from .shortcuts import register_shortcuts


def start():
    try:
        setup_navigation()
    except Exception as e:
        FreeCAD.Console.PrintError(
            "%s setup_navigation error: %s\n" % (LOG_TAG, e)
        )

    QtCore.QTimer.singleShot(200, register_shortcuts)
