"""Popup tool bar shown by the S key."""

import FreeCAD
import FreeCADGui
from PySide import QtCore, QtGui, QtWidgets

from . import guards
from .constants import LOG_TAG
from .tool_catalog import tools_for_context


class ShortcutBar(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(
            parent,
            QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint,
        )
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                border: 1px solid #555555;
                border-radius: 6px;
            }
            QToolButton {
                background-color: #383838;
                color: #ffffff;
                border: 1px solid #4a4a4a;
                border-radius: 4px;
                padding: 6px;
                font-size: 11px;
                font-weight: bold;
                min-width: 44px;
                min-height: 28px;
            }
            QToolButton:hover {
                background-color: #007acc;
                border-color: #0098ff;
            }
        """)
        self._grid = QtWidgets.QGridLayout(self)
        self._grid.setContentsMargins(6, 6, 6, 6)
        self._grid.setSpacing(4)
        self._populate_tools()

    def _populate_tools(self):
        # コンテキストに応じたツールリスト [(ラベル, FreeCAD内部コマンド名), ...]
        tools = tools_for_context(guards.is_sketching())

        cols = 3
        for i, (label, cmd_name) in enumerate(tools):
            btn = QtWidgets.QToolButton(self)
            btn.setText(label)
            # FreeCAD標準コマンドのアイコンがあれば取得して設定
            fc_cmd = FreeCADGui.Command.get(cmd_name)
            if fc_cmd and hasattr(fc_cmd, "getIcon"):
                icon_path = fc_cmd.getIcon()
                if icon_path:
                    btn.setIcon(QtGui.QIcon(icon_path))
                    btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

            btn.clicked.connect(
                lambda _, c=cmd_name: self._run_command_and_close(c)
            )
            self._grid.addWidget(btn, i // cols, i % cols)

    def _run_command_and_close(self, cmd_name):
        self.close()
        try:
            FreeCADGui.runCommand(cmd_name)
        except Exception as e:
            FreeCAD.Console.PrintError(
                f"{LOG_TAG} Command failed: {cmd_name} ({e})\n"
            )
