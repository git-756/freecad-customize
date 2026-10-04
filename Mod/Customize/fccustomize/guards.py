"""Context checks shared by the key handlers."""

import FreeCADGui
from PySide import QtWidgets

# QAbstractSpinBox covers QSpinBox/QDoubleSpinBox and FreeCAD's QuantitySpinBox.
_TEXT_INPUT_TYPES = (
    QtWidgets.QLineEdit,
    QtWidgets.QTextEdit,
    QtWidgets.QPlainTextEdit,
    QtWidgets.QAbstractSpinBox,
    QtWidgets.QComboBox,
)

_SKETCH_TYPE = "Sketcher::SketchObject"


def is_text_input_focused():
    """True if keyboard focus is in a text/number input widget."""
    # The focus widget may be a child of the input (e.g. a spin box's line edit).
    widget = QtWidgets.QApplication.focusWidget()
    while widget is not None:
        if isinstance(widget, _TEXT_INPUT_TYPES):
            return True
        widget = widget.parentWidget()
    return False


def describe_focus():
    """Class name of the widget that has keyboard focus (for diagnostics)."""
    focused = QtWidgets.QApplication.focusWidget()
    return type(focused).__name__ if focused else "None"


def is_sketch_view_provider(vobj):
    """True if the given view provider belongs to a sketch."""
    obj = getattr(vobj, "Object", None)
    return bool(obj and obj.isDerivedFrom(_SKETCH_TYPE))


def is_sketching():
    """True if a sketch is currently being edited."""
    doc = FreeCADGui.ActiveDocument
    if not doc:
        return False
    return is_sketch_view_provider(doc.getInEdit())
