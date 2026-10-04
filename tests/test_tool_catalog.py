from fccustomize.tool_catalog import (
    SKETCH_TOOLS,
    command_candidates,
    sketch_key_bindings,
    tools_for_context,
)


def test_sketching_returns_sketcher_tools_with_key_labels():
    tools = dict((cmd, label) for label, cmd in tools_for_context(True))
    assert list(tools) == [
        "Sketcher_CreateLine",
        "Sketcher_CreateRectangle",
        "Sketcher_CreateCircle",
        "Sketcher_CreateArc",
        "Sketcher_CreatePoint",
        "Sketcher_Trimming",
        "Sketcher_Dimension",
        "Sketcher_ConstrainSymmetric",
        "Sketcher_ConstrainCoincidentUnified",
    ]
    assert tools["Sketcher_CreateLine"] == "直線 (L)"
    assert tools["Sketcher_CreatePoint"] == "点 (Shift+S)"
    # キーなしのツールはラベルにキー表記を付けない
    assert tools["Sketcher_Trimming"] == "トリム"


def test_not_sketching_returns_no_tools():
    assert tools_for_context(False) == []


def test_key_bindings():
    assert {k: c for k, c, _ in sketch_key_bindings()} == {
        "L": "Sketcher_CreateLine",
        "R": "Sketcher_CreateRectangle",
        "C": "Sketcher_CreateCircle",
        "A": "Sketcher_CreateArc",
        "Shift+S": "Sketcher_CreatePoint",
        "D": "Sketcher_Dimension",
        "Shift+M": "Sketcher_ConstrainSymmetric",
        "I": "Sketcher_ConstrainCoincidentUnified",
    }


def test_binding_labels_include_the_key():
    labels = {k: label for k, _, label in sketch_key_bindings()}
    assert labels["L"] == "直線 (L)"
    assert labels["Shift+M"] == "中点 (Shift+M)"


def test_command_candidates_prefer_the_primary_name():
    assert command_candidates("Sketcher_CreateLine") == ("Sketcher_CreateLine",)
    assert command_candidates("Sketcher_ConstrainCoincidentUnified") == (
        "Sketcher_ConstrainCoincidentUnified",
        "Sketcher_ConstrainCoincident",
    )


def test_keys_and_commands_are_unique_and_not_the_launcher_key():
    bindings = sketch_key_bindings()
    keys = [k for k, _, _ in bindings]
    commands = [cmd for _, cmd, _ in SKETCH_TOOLS]
    assert len(keys) == len(set(keys))
    assert len(commands) == len(set(commands))
    assert "S" not in keys  # S はランチャー用


def test_returned_list_is_a_copy():
    tools = tools_for_context(True)
    tools.clear()
    assert tools_for_context(True)
