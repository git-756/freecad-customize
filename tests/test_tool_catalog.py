from fccustomize.tool_catalog import tools_for_context


def test_sketching_returns_sketcher_tools():
    tools = tools_for_context(True)
    assert [cmd for _, cmd in tools] == [
        "Sketcher_CreateLine",
        "Sketcher_CreateRectangle",
        "Sketcher_CreateCircle",
        "Sketcher_CreateArc",
        "Sketcher_Trimming",
        "Sketcher_Dimension",
    ]


def test_not_sketching_returns_part_design_tools():
    tools = tools_for_context(False)
    assert [cmd for _, cmd in tools] == [
        "PartDesign_NewSketch",
        "PartDesign_Pad",
        "PartDesign_Pocket",
        "PartDesign_Fillet",
        "PartDesign_Chamfer",
        "PartDesign_Hole",
    ]


def test_entries_are_well_formed():
    for is_sketching in (True, False):
        tools = tools_for_context(is_sketching)
        assert tools
        for label, cmd in tools:
            assert label
            assert cmd
        commands = [cmd for _, cmd in tools]
        assert len(commands) == len(set(commands))


def test_returned_list_is_a_copy():
    tools = tools_for_context(True)
    tools.clear()
    assert tools_for_context(True)
