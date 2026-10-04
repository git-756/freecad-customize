"""FreeCAD 起動時自動設定 (macOS / Windows 共通)
- ナビゲーションスタイル自動適用 (Mac: Gesture / Win: TinkerCAD)
- Onshape風「N」キー正対ショートカット
- Onshape風「S」キーショートカットツールバー (外部アドオン不要)
"""

try:
    from fccustomize import bootstrap

    bootstrap.start()
except Exception as _e:
    import FreeCAD as _FreeCAD

    _FreeCAD.Console.PrintError("[Customize] init error: %s\n" % _e)
