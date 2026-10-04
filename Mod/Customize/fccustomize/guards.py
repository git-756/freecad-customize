"""Context checks shared by the key handlers."""

import FreeCADGui
from PySide import QtWidgets

_TEXT_INPUT_TYPES = (
    QtWidgets.QLineEdit,
    QtWidgets.QTextEdit,
    QtWidgets.QPlainTextEdit,
    QtWidgets.QSpinBox,
    QtWidgets.QDoubleSpinBox,
)


def is_text_input_focused():
    """True if keyboard focus is in a text/number input widget."""
    focused = QtWidgets.QApplication.focusWidget()
    return isinstance(focused, _TEXT_INPUT_TYPES)


def is_sketching():
    """True if a sketch is currently being edited."""
    doc = FreeCADGui.ActiveDocument
    if not doc:
        return False
    edit_obj = doc.getInEdit()
    return bool(
        edit_obj and edit_obj.Object.isDerivedFrom("Sketcher::SketchObject")
    )
