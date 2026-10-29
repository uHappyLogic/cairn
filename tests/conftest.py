"""Shared fixtures for the suite of the four tools under core/tools/, and for the tests that run
a fixed shell call extracted from the rendered Claude Code tree in a temporary git repository.

Each tool is importable by its module name (`open_questions`, `define_milestone`,
`task_list`, `requirements`) through the `pythonpath = ["core/tools"]` line in
pyproject.toml and driven end-to-end as a subprocess under the interpreter running the
suite, so every exit status, stdout, and stderr the tests see is exactly what a caller sees.
"""

import os
import shlex
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
TASK_LIST_TOOL = REPO_ROOT / "core" / "tools" / "task_list.py"
REQUIREMENTS_TOOL = REPO_ROOT / "core" / "tools" / "requirements.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
CLAUDE_TREE = REPO_ROOT / "hosts" / "claude"
CLAUDE_PLUGIN_ROOT_VARIABLE = "CLAUDE_PLUGIN_ROOT"


@pytest.fixture
def run_tool():
    """Run the tool as a subprocess: run_tool("add", str(dir), "Short Title", stdin=b"...")."""

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


@pytest.fixture
def run_task_list():
    """Run the task-list tool as a subprocess: run_task_list("move", str(dir), "Task Title",
    stdin=b"- criterion"). Standard input is always piped (empty when stdin is None), so the
    child never inherits a terminal."""

    def run(*args, stdin=None):
        return subprocess.run(
            [sys.executable, "-B", str(TASK_LIST_TOOL), *args],
            input=b"" if stdin is None else stdin,
            capture_output=True,
            check=False,
        )

    return run


@pytest.fixture
def task_list_dir(tmp_path):
    """A fresh milestone directory holding the two task files: by default copies of the golden
    task-file fixtures, or the given bytes (task_list_dir(todo=b"# TASKS TODO\\n\\n")) -> Path."""

    def build(todo=None, done=None, name="milestone"):
        destination = tmp_path / name
        destination.mkdir()
        todo_bytes = (FIXTURES / "task_list_todo.md").read_bytes() if todo is None else todo
        done_bytes = (FIXTURES / "task_list_done.md").read_bytes() if done is None else done
        (destination / "TASKS_TODO.md").write_bytes(todo_bytes)
        (destination / "TASKS_DONE.md").write_bytes(done_bytes)
        return destination

    return build


@pytest.fixture
def run_requirements():
    """Run the fold tool as a subprocess: run_requirements("fold", str(dir), "--section",
    "A Heading", stdin=b"The decision."). Standard input is always piped (empty when stdin is
    None), so the child never inherits a terminal."""

    def run(*args, stdin=None):
        return subprocess.run(
            [sys.executable, "-B", str(REQUIREMENTS_TOOL), *args],
            input=b"" if stdin is None else stdin,
            capture_output=True,
            check=False,
        )

    return run


@pytest.fixture
def requirements_dir(tmp_path):
    """A fresh milestone directory holding requirements.md: by default a copy of the golden
    requirements fixture, or the given bytes (requirements_dir(b"## Decisions\\n")) -> Path."""

    def build(requirements=None, name="milestone"):
        destination = tmp_path / name
        destination.mkdir()
        data = (FIXTURES / "requirements.md").read_bytes() if requirements is None else requirements
        (destination / "requirements.md").write_bytes(data)
        return destination

    return build


# --- git repositories for the fixed shell calls ---------------------------------------------


def run_git(repo, env, *args):
    """Run one git command in the repository under the given environment, asserting it exited
    0, and return its stdout as text."""
    result = subprocess.run(["git", *args], cwd=str(repo), env=env, capture_output=True, check=False)
    assert result.returncode == 0, result.stderr.decode("utf-8", "replace")
    return result.stdout.decode("utf-8")


def run_bash(cwd, env, call):
    """Run a fixed shell call under `bash -c` from the given directory with no standard input:
    -> (exit status, stdout, stderr), the two streams as text."""
    result = subprocess.run(
        ["bash", "-c", call], cwd=str(cwd), env=env, stdin=subprocess.DEVNULL, capture_output=True, check=False
    )
    return result.returncode, result.stdout.decode("utf-8"), result.stderr.decode("utf-8")


@pytest.fixture
def environment(tmp_path):
    """The environment a fixed call runs under: the Claude Code tree's plugin-root variable
    exported to the tree root, `python3` resolving to the interpreter running the suite (so each
    pytest run drives the rendered tools under its own interpreter), no bytecode written into the
    tree, and git isolated from every global or system configuration with a fixed identity."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    wrapper = bin_dir / "python3"
    wrapper.write_text(f'#!/bin/sh\nexec {shlex.quote(sys.executable)} "$@"\n', encoding="utf-8")
    wrapper.chmod(0o755)
    home = tmp_path / "home"
    home.mkdir()
    env = dict(os.environ)
    env.update(
        {
            CLAUDE_PLUGIN_ROOT_VARIABLE: str(CLAUDE_TREE),
            "PATH": str(bin_dir) + os.pathsep + env.get("PATH", ""),
            "PYTHONDONTWRITEBYTECODE": "1",
            "HOME": str(home),
            "XDG_CONFIG_HOME": str(home / ".config"),
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_AUTHOR_NAME": "Cairn Test",
            "GIT_AUTHOR_EMAIL": "test@example.invalid",
            "GIT_COMMITTER_NAME": "Cairn Test",
            "GIT_COMMITTER_EMAIL": "test@example.invalid",
        }
    )
    return env


@pytest.fixture
def git():
    """Run one git command: git(repo, environment, "log", "-1") -> its stdout as text, the
    command asserted to have exited 0."""
    return run_git


@pytest.fixture
def run_call():
    """Run a fixed shell call under bash: run_call(repo, environment, call) -> (exit status,
    stdout, stderr)."""
    return run_bash


@pytest.fixture
def repo(tmp_path, environment):
    """A fresh git repository under tmp_path whose one commit holds copies of the named fixture
    milestones and the given files: repo({"milestones/milestone_07_slug/": "sweep"},
    files={"README.md": b"..."}) -> the repository Path, each fixture directory copied to the
    path it is keyed by and each file written with its bytes."""

    def build(milestones, files=None):
        files = {} if files is None else files
        root = tmp_path / "repo"
        root.mkdir()
        for destination, name in milestones.items():
            shutil.copytree(FIXTURES / name, root / destination)
        for path, data in files.items():
            (root / path).parent.mkdir(parents=True, exist_ok=True)
            (root / path).write_bytes(data)
        run_git(root, environment, "init", "-q")
        run_git(root, environment, "add", "--", *milestones, *files)
        run_git(root, environment, "commit", "-q", "-m", "Initial commit")
        return root

    return build
