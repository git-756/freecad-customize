"""Sketch tools and their key bindings (pure; no FreeCAD/Qt dependency)."""

# (名前, FreeCAD内部コマンド名, キー or None)
# キーはスケッチ編集中だけ有効。None はランチャー（Sキー）からのみ選べる。
SKETCH_TOOLS = (
    ("直線", "Sketcher_CreateLine", "L"),
    ("矩形", "Sketcher_CreateRectangle", "R"),
    ("円", "Sketcher_CreateCircle", "C"),
    ("円弧", "Sketcher_CreateArc", "A"),
    ("点", "Sketcher_CreatePoint", "Shift+S"),
    ("トリム", "Sketcher_Trimming", None),
    ("寸法", "Sketcher_Dimension", "D"),
    ("中点", "Sketcher_ConstrainSymmetric", "Shift+M"),
    ("一致", "Sketcher_ConstrainCoincidentUnified", "I"),
)

# FreeCAD のバージョンによってコマンド名が異なるものの代替名（先頭が優先）。
COMMAND_FALLBACKS = {
    "Sketcher_ConstrainCoincidentUnified": ("Sketcher_ConstrainCoincident",),
}


def _label(name: str, key: str | None) -> str:
    return f"{name} ({key})" if key else name


def tools_for_context(is_sketching: bool) -> list[tuple[str, str]]:
    """Return [(label, command_name), ...] for the launcher.

    Tools are only offered while a sketch is being edited.
    """
    if not is_sketching:
        return []
    return [(_label(name, key), cmd) for name, cmd, key in SKETCH_TOOLS]


def sketch_key_bindings() -> list[tuple[str, str, str]]:
    """Return [(key_sequence, command_name, label), ...] active while sketching."""
    return [(key, cmd, _label(name, key)) for name, cmd, key in SKETCH_TOOLS if key]


def command_candidates(cmd_name: str) -> tuple[str, ...]:
    """Command names to try, in order of preference."""
    return (cmd_name, *COMMAND_FALLBACKS.get(cmd_name, ()))
