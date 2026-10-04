"""FreeCAD 起動時自動設定スクリプト (macOS / Windows 共通)
- ナビゲーションスタイル自動適用 (Mac: Gesture / Win: TinkerCAD)
- Onshape互換「N」キー正対ショートカット
- Onshape互換「S」キーショートカットツールバー (外部アドオン不要)
"""


def _onshape_workflow_main():
    import sys
    import FreeCAD
    import FreeCADGui
    from PySide import QtCore, QtGui, QtWidgets

    SHORTCUT_N_NAME = "OnshapeNShortcut"
    SHORTCUT_S_NAME = "OnshapeSShortcut"

    # =========================================================
    # 1. ナビゲーション設定
    # =========================================================
    def setup_navigation():
        view_param = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/View")
        nav_style = (
            "Gui::GestureNavigationStyle"
            if sys.platform == "darwin"
            else "Gui::TinkerCADNavigationStyle"
        )
        view_param.SetString("NavigationStyle", nav_style)
        view_param.SetBool("ZoomAtCursor", True)
        view_param.SetBool("InvertZoom", False)
        view_param.SetBool("UseAnimation", True)

    # =========================================================
    # 2. Nキー: 最短正対処理
    # =========================================================
    def do_normal_to():
        try:
            focused = QtWidgets.QApplication.focusWidget()
            if isinstance(
                focused,
                (
                    QtWidgets.QLineEdit,
                    QtWidgets.QTextEdit,
                    QtWidgets.QPlainTextEdit,
                    QtWidgets.QSpinBox,
                    QtWidgets.QDoubleSpinBox,
                ),
            ):
                return

            doc = FreeCADGui.ActiveDocument
            if not doc or not doc.ActiveView:
                return

            edit_obj = doc.getInEdit()
            if edit_obj and edit_obj.Object.isDerivedFrom(
                "Sketcher::SketchObject"
            ):
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
            FreeCAD.Console.PrintError("[OnshapeWorkflow] N key error: %s\n" % e)

    # =========================================================
    # 3. Sキー: Onshape風 ショートカットツールバー
    # =========================================================
    class OnshapeShortcutBar(QtWidgets.QWidget):

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
            self.layout = QtWidgets.QGridLayout(self)
            self.layout.setContentsMargins(6, 6, 6, 6)
            self.layout.setSpacing(4)
            self._populate_tools()

        def _populate_tools(self):
            doc = FreeCADGui.ActiveDocument
            is_sketching = False
            if doc:
                edit_obj = doc.getInEdit()
                if edit_obj and edit_obj.Object.isDerivedFrom(
                    "Sketcher::SketchObject"
                ):
                    is_sketching = True

            # コンテキストに応じたツールリスト [(ラベル, FreeCAD内部コマンド名), ...]
            if is_sketching:
                tools = [
                    ("直線 (L)", "Sketcher_CreateLine"),
                    ("矩形 (R)", "Sketcher_CreateRectangle"),
                    ("円 (C)", "Sketcher_CreateCircle"),
                    ("円弧 (A)", "Sketcher_CreateArc"),
                    ("トリム (M)", "Sketcher_Trimming"),
                    ("寸法 (D)", "Sketcher_Dimension"),
                ]
            else:
                tools = [
                    ("スケッチ", "PartDesign_NewSketch"),
                    ("パッド (Extrude)", "PartDesign_Pad"),
                    ("ポケット (Cut)", "PartDesign_Pocket"),
                    ("フィレット", "PartDesign_Fillet"),
                    ("面取り", "PartDesign_Chamfer"),
                    ("穴あけ (Hole)", "PartDesign_Hole"),
                ]

            cols = 3
            for i, (label, cmd_name) in enumerate(tools):
                btn = QtWidgets.QToolButton(self)
                btn.setText(label)
                # FreeCAD標準コマンドのアイコンがあれば取得して設定
                cmd = FreeCADGui.runCommand  # noqa
                fc_cmd = FreeCADGui.Command.get(cmd_name)
                if fc_cmd and hasattr(fc_cmd, "getIcon"):
                    icon_path = fc_cmd.getIcon()
                    if icon_path:
                        btn.setIcon(QtGui.QIcon(icon_path))
                        btn.setToolButtonStyle(
                            QtCore.Qt.ToolButtonTextBesideIcon
                        )

                btn.clicked.connect(
                    lambda _, c=cmd_name: self._run_command_and_close(c)
                )
                self.layout.addWidget(btn, i // cols, i % cols)

        def _run_command_and_close(self, cmd_name):
            self.close()
            try:
                FreeCADGui.runCommand(cmd_name)
            except Exception as e:
                FreeCAD.Console.PrintError(
                    f"[OnshapeWorkflow] Command failed: {cmd_name} ({e})\n"
                )

    def do_shortcut_bar():
        try:
            focused = QtWidgets.QApplication.focusWidget()
            if isinstance(
                focused,
                (
                    QtWidgets.QLineEdit,
                    QtWidgets.QTextEdit,
                    QtWidgets.QPlainTextEdit,
                    QtWidgets.QSpinBox,
                    QtWidgets.QDoubleSpinBox,
                ),
            ):
                return

            mw = FreeCADGui.getMainWindow()
            bar = OnshapeShortcutBar(mw)

            # マウスカーソル位置に表示
            cursor_pos = QtGui.QCursor.pos()
            bar.adjustSize()
            bar.move(cursor_pos.x() - 10, cursor_pos.y() - 10)
            bar.show()
        except Exception as e:
            FreeCAD.Console.PrintError("[OnshapeWorkflow] S key error: %s\n" % e)

    # =========================================================
    # 4. ショートカット登録 (Nキー & Sキー)
    # =========================================================
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
                        "[OnshapeWorkflow] MainWindow not available.\n"
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
                ">> [OnshapeWorkflow] 初期化完了: Navigation / Nキー(正対) / Sキー(ツールバー) が有効化されました。\n"
            )
        except Exception as e:
            FreeCAD.Console.PrintError(
                "[OnshapeWorkflow] register_shortcuts error: %s\n" % e
            )

    try:
        setup_navigation()
    except Exception as e:
        FreeCAD.Console.PrintError(
            "[OnshapeWorkflow] setup_navigation error: %s\n" % e
        )

    QtCore.QTimer.singleShot(200, register_shortcuts)


try:
    _onshape_workflow_main()
except Exception as _e:
    import FreeCAD as _FreeCAD

    _FreeCAD.Console.PrintError("[OnshapeWorkflow] init error: %s\n" % _e)