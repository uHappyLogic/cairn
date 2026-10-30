"""The milestones tool is one self-contained file: it imports no sibling tool and no importlib,
so every rendered tool stays one runnable file and no run imports a sibling, and every host
tree under hosts/ carries a byte-identical copy of it. Its conformance to the shared output
contract is pinned only behaviourally, by its own subprocess tests."""

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOL = REPO_ROOT / "core" / "tools" / "milestones.py"
HOSTS = REPO_ROOT / "hosts"


def imported_modules(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".")[0])
    return imported


def test_the_milestones_tool_imports_no_sibling_tool():
    imported = imported_modules(TOOL)
    assert "open_questions" not in imported
    assert "task_list" not in imported
    assert "requirements" not in imported
    assert "define_milestone" not in imported
    assert "commit" not in imported
    assert "importlib" not in imported


def test_every_host_tree_carries_a_byte_identical_copy():
    trees = sorted(path for path in HOSTS.iterdir() if path.is_dir())
    assert trees
    source = TOOL.read_bytes()
    for tree in trees:
        copies = sorted(tree.glob("**/tools/milestones.py"))
        assert len(copies) == 1, (tree, copies)
        assert copies[0].read_bytes() == source, copies[0]
