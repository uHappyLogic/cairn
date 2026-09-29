"""The empty open-question document define_milestone.py writes is the one the open-question
tool reads and renders, so the two tools cannot drift apart on its bytes."""

import ast
from pathlib import Path

import open_questions

DEFINE_TOOL = Path(__file__).resolve().parent.parent / "core" / "tools" / "define_milestone.py"


def test_the_written_document_is_the_serializer_empty_document(run_define, workspace):
    root = workspace()
    result = run_define("--title", "First", stdin=b"Ship it.\n", cwd=root)
    assert result.returncode == 0, result.stderr
    directory = root / "milestones" / "milestone_01_first"
    written = (directory / open_questions.DOCUMENT_NAME).read_bytes()
    assert written == open_questions.render_document(open_questions.Document()).encode("utf-8")
    assert open_questions.load_document(str(directory)) == open_questions.Document()


def test_the_open_question_tool_lists_nothing_in_the_new_milestone(run_define, run_tool, workspace):
    root = workspace()
    run_define("--title", "First", stdin=b"Ship it.\n", cwd=root)
    result = run_tool("list", str(root / "milestones" / "milestone_01_first"))
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def test_the_definition_tool_imports_nothing_from_the_open_question_tool():
    tree = ast.parse(DEFINE_TOOL.read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".")[0])
    assert "open_questions" not in imported
