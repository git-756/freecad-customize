"""Actions bound to the sketch-only keys."""

import FreeCAD
import FreeCADGui

from . import guards, log
from .constants import LOG_TAG


def run_sketch_command(cmd_name):
    """Run a FreeCAD command if a sketch is being edited and no input has focus."""
    try:
        focus, sketching = guards.describe_focus(), guards.is_sketching()
        log.debug("key -> %s focus=%s sketching=%s" % (cmd_name, focus, sketching))
        if guards.is_text_input_focused() or not sketching:
            log.debug("  ignored")
            return
        FreeCADGui.runCommand(cmd_name)
    except Exception as e:
        FreeCAD.Console.PrintError(
            f"{LOG_TAG} Command failed: {cmd_name} ({e})\n"
        )
