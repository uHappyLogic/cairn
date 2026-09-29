"""Shared fixtures for the suite of the two tools under core/tools/.

Each tool is importable by its module name (`open_questions`, `define_milestone`) through the
`pythonpath = ["core/tools"]` line in pyproject.toml and driven end-to-end as a subprocess
under the interpreter running the suite, so every exit status, stdout, and stderr the tests
see is exactly what a caller sees.
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
DEFINE_TOOL = REPO_ROOT / "core" / "tools" / "define_milestone.py"
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


@pytest.fixture
def run_define():
    """Run the definition tool as a subprocess from a workspace directory:
    run_define("--title", "A title", stdin=b"The goal.", cwd=workspace). Standard input is
    always piped (empty when stdin is None), so the child never inherits a terminal."""

    def run(*args, stdin=None, cwd):
        return subprocess.run(
            [sys.executable, "-B", str(DEFINE_TOOL), *args],
            input=b"" if stdin is None else stdin,
            capture_output=True,
            check=False,
            cwd=str(cwd),
        )

    return run


@pytest.fixture
def workspace(tmp_path):
    """A fresh workspace directory under tmp_path holding a milestones root laid out as asked:
    workspace("milestone_01_first", files=("milestone_50_file",)) -> the workspace Path, whose
    milestones/ holds each named directory and each named empty file. root=False leaves the
    milestones root out altogether."""

    def build(*directories, files=(), root=True):
        path = tmp_path / "workspace"
        path.mkdir()
        if root:
            milestones = path / "milestones"
            milestones.mkdir()
            for name in directories:
                (milestones / name).mkdir()
            for name in files:
                (milestones / name).write_bytes(b"")
        return path

    return build
