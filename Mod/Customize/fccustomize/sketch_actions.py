"""Actions bound to the sketch-only keys."""

import FreeCAD
import FreeCADGui

from . import guards
from .constants import LOG_TAG


def run_sketch_command(cmd_name):
    """Run a FreeCAD command if a sketch is being edited and no input has focus."""
    try:
        if guards.is_text_input_focused() or not guards.is_sketching():
            return
        FreeCADGui.runCommand(cmd_name)
    except Exception as e:
        FreeCAD.Console.PrintError(
            f"{LOG_TAG} Command failed: {cmd_name} ({e})\n"
        )
