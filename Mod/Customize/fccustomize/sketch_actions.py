"""Actions bound to the sketch-only keys."""

import FreeCAD
import FreeCADGui

from .constants import LOG_TAG


def run_sketch_command(cmd_name):
    try:
        FreeCADGui.runCommand(cmd_name)
    except Exception as e:
        FreeCAD.Console.PrintError(
            f"{LOG_TAG} Command failed: {cmd_name} ({e})\n"
        )
