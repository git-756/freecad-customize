"""Navigation style settings (Mac: Gesture / others: TinkerCAD)."""

import sys

import FreeCAD


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
