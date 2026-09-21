"""Shared fixtures for the open_questions.py suite.

The tool is imported as `open_questions` through the `pythonpath = ["core/tools"]` line in
pyproject.toml and driven end-to-end as a subprocess under the interpreter running the
suite, so every exit status, stdout, and stderr the tests see is exactly what a caller sees.
"""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

# The host build renders every file under core/ into every host tree, so importing the tool
# from core/tools/ must leave no __pycache__ behind there.
sys.dont_write_bytecode = True

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOL = REPO_ROOT / "core" / "tools" / "open_questions.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture
def run_tool():
    """Run the tool as a subprocess: run_tool("create", str(dir), stdin=b"...")."""

    def run(*args, stdin=None):
        return subprocess.run(
            [sys.executable, "-B", str(TOOL), *args],
            input=stdin,
            capture_output=True,
            check=False,
        )

    return run


@pytest.fixture
def milestone_dir(tmp_path):
    """A fresh copy of a named fixture directory: milestone_dir("annotated") -> Path."""

    def copy(name):
        destination = tmp_path / name
        shutil.copytree(FIXTURES / name, destination)
        return destination

    return copy
