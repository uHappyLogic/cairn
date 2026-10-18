"""The fold tool is one self-contained file: it imports no sibling tool and no importlib, so
every rendered tool stays one runnable file and no run imports a sibling. Its conformance to
the shared output contract is pinned only behaviourally, by its own subprocess tests."""

import ast
from pathlib import Path

TOOL = Path(__file__).resolve().parent.parent / "core" / "tools" / "requirements.py"


def imported_modules(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".")[0])
    return imported


def test_the_fold_tool_imports_no_sibling_tool():
    imported = imported_modules(TOOL)
    assert "open_questions" not in imported
    assert "task_list" not in imported
    assert "define_milestone" not in imported
    assert "importlib" not in imported
