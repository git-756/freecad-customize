"""View actions bound to keys."""

import FreeCAD
import FreeCADGui

from . import guards
from .constants import LOG_TAG


def do_normal_to():
    """N key: align the view to the sketch / selection / front."""
    try:
        if guards.is_text_input_focused():
            return

        doc = FreeCADGui.ActiveDocument
        if not doc or not doc.ActiveView:
            return

        if guards.is_sketching():
            try:
                FreeCADGui.runCommand("Sketcher_ViewSketch")
                return
            except Exception:
                pass

        if FreeCADGui.Selection.getSelectionEx():
            try:
                FreeCADGui.runCommand("Std_AlignToSelection")
                return
            except Exception:
                pass

        FreeCADGui.runCommand("Std_ViewFront")
    except Exception as e:
        FreeCAD.Console.PrintError("%s N key error: %s\n" % (LOG_TAG, e))
