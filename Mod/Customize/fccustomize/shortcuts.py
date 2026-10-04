"""N/S key registration and the S-key handler."""

import FreeCAD
import FreeCADGui
from PySide import QtCore, QtGui

from . import guards
from .constants import LOG_TAG, SHORTCUT_N_NAME, SHORTCUT_S_NAME
from .shortcut_bar import ShortcutBar
from .view_actions import do_normal_to


def do_shortcut_bar():
    try:
        if guards.is_text_input_focused():
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

        # Nキーの登録
        old_n = mw.findChild(QtGui.QShortcut, SHORTCUT_N_NAME)
        if old_n:
            old_n.setEnabled(False)
            old_n.deleteLater()
        sc_n = QtGui.QShortcut(QtGui.QKeySequence("N"), mw)
        sc_n.setObjectName(SHORTCUT_N_NAME)
        sc_n.setContext(QtCore.Qt.ApplicationShortcut)
        sc_n.activated.connect(do_normal_to)

        # Sキーの登録
        old_s = mw.findChild(QtGui.QShortcut, SHORTCUT_S_NAME)
        if old_s:
            old_s.setEnabled(False)
            old_s.deleteLater()
        sc_s = QtGui.QShortcut(QtGui.QKeySequence("S"), mw)
        sc_s.setObjectName(SHORTCUT_S_NAME)
        sc_s.setContext(QtCore.Qt.ApplicationShortcut)
        sc_s.activated.connect(do_shortcut_bar)

        FreeCAD.Console.PrintMessage(
            ">> %s 初期化完了: Navigation / Nキー(正対) / Sキー(ツールバー) が有効化されました。\n"
            % LOG_TAG
        )
    except Exception as e:
        FreeCAD.Console.PrintError(
            "%s register_shortcuts error: %s\n" % (LOG_TAG, e)
        )
