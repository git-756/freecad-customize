"""Tool lists for the S-key shortcut bar (pure; no FreeCAD/Qt dependency)."""

# [(ラベル, FreeCAD内部コマンド名), ...]
SKETCH_TOOLS = (
    ("直線 (L)", "Sketcher_CreateLine"),
    ("矩形 (R)", "Sketcher_CreateRectangle"),
    ("円 (C)", "Sketcher_CreateCircle"),
    ("円弧 (A)", "Sketcher_CreateArc"),
    ("トリム (M)", "Sketcher_Trimming"),
    ("寸法 (D)", "Sketcher_Dimension"),
)

PART_TOOLS = (
    ("スケッチ", "PartDesign_NewSketch"),
    ("パッド (Extrude)", "PartDesign_Pad"),
    ("ポケット (Cut)", "PartDesign_Pocket"),
    ("フィレット", "PartDesign_Fillet"),
    ("面取り", "PartDesign_Chamfer"),
    ("穴あけ (Hole)", "PartDesign_Hole"),
)


def tools_for_context(is_sketching: bool) -> list[tuple[str, str]]:
    """Return [(label, command_name), ...] for the current editing context."""
    return list(SKETCH_TOOLS if is_sketching else PART_TOOLS)
