"""Key registration.

N is a normal application shortcut (always active). The S launcher and the
sketch tool keys are handled by an event filter that is only effective while
a sketch is being edited (see key_filter.py).
"""

import FreeCAD
import FreeCADGui
from PySide import QtCore, QtGui, QtWidgets

from .constants import LOG_TAG, SHORTCUT_N_NAME, SKETCH_LAUNCHER_KEY
from .key_filter import SketchKeyFilter
from .shortcut_bar import ShortcutBar
from .sketch_actions import close_popup, run_sketch_command
from .tool_catalog import sketch_key_bindings
from .view_actions import do_normal_to

# Kept at module level so it is not garbage collected.
_key_filter = None


def do_shortcut_bar():
    try:
        if close_popup():  # S を再度押すとランチャーを閉じる
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


def _make_shortcut(mw, name, key, callback):
    old = mw.findChild(QtGui.QShortcut, name)
    if old:
        old.setEnabled(False)
        old.deleteLater()
    sc = QtGui.QShortcut(QtGui.QKeySequence(key), mw)
    sc.setObjectName(name)
    sc.setContext(QtCore.Qt.ApplicationShortcut)
    sc.activated.connect(callback)
    return sc


def _install_sketch_keys():
    global _key_filter
    app = QtWidgets.QApplication.instance()
    if _key_filter is not None:
        app.removeEventFilter(_key_filter)

    handlers = {SKETCH_LAUNCHER_KEY: do_shortcut_bar}
    for key, cmd_name, label in sketch_key_bindings():
        handlers[key] = lambda c=cmd_name, t=label: run_sketch_command(c, t)
    _key_filter = SketchKeyFilter(handlers)
    app.installEventFilter(_key_filter)


def register_shortcuts(retry=0):
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
        _install_sketch_keys()

        FreeCAD.Console.PrintMessage(
            ">> %s 初期化完了: Navigation / Nキー(正対) / スケッチ中のキー(S/L/R/C/A/D/I/Shift+S/Shift+M) が有効化されました。\n"
            % LOG_TAG
        )
    except Exception as e:
        FreeCAD.Console.PrintError(
            "%s register_shortcuts error: %s\n" % (LOG_TAG, e)
        )
