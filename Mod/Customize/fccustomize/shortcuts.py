"""Key registration.

N is always active. The S launcher and the sketch tool keys are only enabled
while a sketch is being edited (toggled by a document observer).
"""

import FreeCAD
import FreeCADGui
from PySide import QtCore, QtGui

from . import guards, log
from .constants import (
    LOG_TAG,
    SHORTCUT_N_NAME,
    SHORTCUT_S_NAME,
    SKETCH_KEY_NAME_PREFIX,
    SKETCH_LAUNCHER_KEY,
)
from .shortcut_bar import ShortcutBar
from .sketch_actions import run_sketch_command
from .tool_catalog import sketch_key_bindings
from .view_actions import do_normal_to

# Kept at module level so they are not garbage collected.
_sketch_shortcuts = []
_observer = None


def do_shortcut_bar():
    try:
        focus, sketching = guards.describe_focus(), guards.is_sketching()
        log.debug("key S focus=%s sketching=%s" % (focus, sketching))
        if guards.is_text_input_focused() or not sketching:
            log.debug("  ignored")
            return

        mw = FreeCADGui.getMainWindow()
        bar = ShortcutBar(mw)

        # マウスカーソル位置に表示
        cursor_pos = QtGui.QCursor.pos()
        bar.adjustSize()
        bar.move(cursor_pos.x() - 10, cursor_pos.y() - 10)
        bar.show()
    except Exception as e:
        FreeCAD.Console.PrintError("%s S key error: %s\n" % (LOG_TAG, e))


def _make_shortcut(mw, name, key, callback, enabled=True):
    old = mw.findChild(QtGui.QShortcut, name)
    if old:
        old.setEnabled(False)
        old.deleteLater()
    sc = QtGui.QShortcut(QtGui.QKeySequence(key), mw)
    sc.setObjectName(name)
    sc.setContext(QtCore.Qt.ApplicationShortcut)
    sc.activated.connect(callback)
    sc.activatedAmbiguously.connect(lambda: log.debug("AMBIGUOUS key %s" % key))
    sc.setEnabled(enabled)
    return sc


def _set_sketch_keys_enabled(enabled):
    log.debug("sketch keys enabled=%s" % enabled)
    for sc in _sketch_shortcuts:
        sc.setEnabled(enabled)


class _SketchEditObserver:
    """Enable the sketch keys on entering a sketch, disable on leaving."""

    def slotInEdit(self, vobj):
        try:
            _set_sketch_keys_enabled(guards.is_sketch_view_provider(vobj))
        except Exception as e:
            FreeCAD.Console.PrintError(
                "%s slotInEdit error: %s\n" % (LOG_TAG, e)
            )

    def slotResetEdit(self, vobj):
        _set_sketch_keys_enabled(False)


def register_shortcuts(retry=0):
    global _observer
    try:
        mw = FreeCADGui.getMainWindow()
        if not mw:
            if retry < 50:
                QtCore.QTimer.singleShot(
                    100, lambda: register_shortcuts(retry + 1)
                )
            else:
                FreeCAD.Console.PrintError(
                    "%s MainWindow not available.\n" % LOG_TAG
                )
            return

        # Nキー（常時有効）
        _make_shortcut(mw, SHORTCUT_N_NAME, "N", do_normal_to)

        # スケッチ中のみ有効なキー: ランチャー(S) と各ツール
        _sketch_shortcuts.clear()
        _sketch_shortcuts.append(
            _make_shortcut(
                mw, SHORTCUT_S_NAME, SKETCH_LAUNCHER_KEY, do_shortcut_bar,
                enabled=False,
            )
        )
        for key, cmd_name in sketch_key_bindings():
            _sketch_shortcuts.append(
                _make_shortcut(
                    mw,
                    SKETCH_KEY_NAME_PREFIX + cmd_name,
                    key,
                    lambda c=cmd_name: run_sketch_command(c),
                    enabled=False,
                )
            )

        if _observer is None:
            _observer = _SketchEditObserver()
            FreeCADGui.addDocumentObserver(_observer)
        _set_sketch_keys_enabled(guards.is_sketching())

        FreeCAD.Console.PrintMessage(
            ">> %s 初期化完了: Navigation / Nキー(正対) / スケッチ中のキー(S/L/R/C/A/D/Shift+S/Shift+M) が有効化されました。\n"
            % LOG_TAG
        )
    except Exception as e:
        FreeCAD.Console.PrintError(
            "%s register_shortcuts error: %s\n" % (LOG_TAG, e)
        )
