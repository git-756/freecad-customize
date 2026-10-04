"""Diagnostics output to the report view."""

import FreeCAD

from .constants import DEBUG_KEYS, LOG_TAG


def debug(msg):
    if DEBUG_KEYS:
        FreeCAD.Console.PrintMessage("%s [debug] %s\n" % (LOG_TAG, msg))
