"""Sketch-only key handling via an application-wide event filter.

QShortcut cannot be used for these keys: FreeCAD binds the same keys
(S, L, ...) to Sketcher constraint commands, so Qt treats them as ambiguous
and fires neither. The filter accepts ShortcutOverride so that Qt skips its
shortcut matching, then handles the KeyPress itself.
"""

from PySide import QtCore, QtGui

from . import guards, log

_PORTABLE = QtGui.QKeySequence.SequenceFormat.PortableText


def normalize(key):
    """Canonical text for a key sequence, e.g. 'shift+s' -> 'Shift+S'."""
    return QtGui.QKeySequence(key).toString(_PORTABLE)


class SketchKeyFilter(QtCore.QObject):

    def __init__(self, handlers, parent=None):
        """handlers: {key sequence text: callable taking no arguments}"""
        super().__init__(parent)
        self._handlers = {normalize(k): h for k, h in handlers.items()}

    def _active(self):
        return guards.is_sketching() and not guards.is_text_input_focused()

    def eventFilter(self, obj, event):
        etype = event.type()
        if etype not in (QtCore.QEvent.ShortcutOverride, QtCore.QEvent.KeyPress):
            return False
        key = QtGui.QKeySequence(event.keyCombination()).toString(_PORTABLE)
        handler = self._handlers.get(key)
        if handler is None or not self._active():
            return False

        if etype == QtCore.QEvent.ShortcutOverride:
            event.accept()
            return True
        if not event.isAutoRepeat():
            log.debug("key %s handled (focus=%s)" % (key, guards.describe_focus()))
            handler()
        return True
