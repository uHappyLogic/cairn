"""Fixtures of the agy suite, the on-demand pytest directory that drives the installed
Antigravity CLI against the plugin copy at ~/.gemini/config/plugins/cairn.

The directory sits outside pyproject.toml's `testpaths`, so `uv run pytest` and the 3.9
floor run never reach it; it runs only when named: `uv run pytest agy_tests`. Before any
test, one up-front check stops the whole run with a non-zero exit and one line when a
prerequisite is missing. The suite drives the copy already installed in the user's real
HOME and writes nothing to it (replacing that copy is the user's own act), runs every agy
process at the account's default model and effort, and lets agy's own print timeout bound
each run.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
BUILT_TREE = REPO_ROOT / "hosts" / "antigravity"
FIXTURE_PROJECT = REPO_ROOT / "tests" / "fixtures" / "agy_project"
PLUGIN_ROOT_TILDE = "~/.gemini/config/plugins/cairn"
PLUGIN_ROOT = Path(os.path.expanduser(PLUGIN_ROOT_TILDE))

# The one fixed bound on a headless run, enforced by agy itself through `--print-timeout`,
# so the suite holds no wall-clock limit of its own.
PRINT_TIMEOUT = "20m"


def _tree_files(root):
    """Every file under root, keyed by its path relative to root."""
    files = {}
    for directory, _, names in os.walk(root):
        for name in names:
            path = Path(directory) / name
            files[path.relative_to(root).as_posix()] = path
    return files


def _agy_on_path():
    if shutil.which("agy") is None:
        return "agy is not resolvable on PATH"
    return None


def _copy_present():
    if not PLUGIN_ROOT.is_dir():
        return (
            f"no plugin copy at {PLUGIN_ROOT_TILDE}; "
            "extract the release or copy the built hosts/antigravity/ tree there"
        )
    return None


def _copy_matches_built_tree():
    built = _tree_files(BUILT_TREE)
    installed = _tree_files(PLUGIN_ROOT)
    for relative in sorted(set(built) | set(installed)):
        if (
            relative not in built
            or relative not in installed
            or built[relative].read_bytes() != installed[relative].read_bytes()
        ):
            return (
                f"the plugin copy at {PLUGIN_ROOT_TILDE} differs from hosts/antigravity/ "
                f"at {relative}; re-extract the release or copy the built tree there"
            )
    return None


# Checked in this order before any test; the first missing one stops the run.
PREREQUISITES = (_agy_on_path, _copy_present, _copy_matches_built_tree)


def pytest_cmdline_main(config):
    """Stop the whole run before any test when a prerequisite is missing: one line naming
    it on stderr, a non-zero exit, no per-test outcome, and never a skip. Returning the exit
    code from this hook ends the run before pytest configures its reporting, so that line
    is the run's only output; when every prerequisite holds, returning None lets pytest
    carry on as usual."""
    for check in PREREQUISITES:
        missing = check()
        if missing is not None:
            sys.stderr.write(f"agy suite prerequisite missing: {missing}\n")
            sys.stderr.flush()
            return 1
    return None


def _git(repository, *args):
    subprocess.run(
        ["git", *args],
        cwd=str(repository),
        stdin=subprocess.DEVNULL,
        capture_output=True,
        check=True,
    )


@pytest.fixture
def seeded_repo(tmp_path):
    """A fresh committed copy of the fixture project for one agy process: seeded_repo() -> Path.
    Each call copies tests/fixtures/agy_project to its own directory under tmp_path, runs
    `git init` there, and makes the initial commit, so every agy process starts from the same
    committed tree and nothing it changes reaches the fixture or another process."""

    count = 0

    def build():
        nonlocal count
        count += 1
        repository = tmp_path / f"project{count}"
        shutil.copytree(FIXTURE_PROJECT, repository)
        _git(repository, "init", "-q")
        _git(repository, "config", "user.name", "Agy Suite")
        _git(repository, "config", "user.email", "agy-suite@example.invalid")
        _git(repository, "config", "commit.gpgsign", "false")
        _git(repository, "add", "-A")
        _git(repository, "commit", "-q", "--no-verify", "-m", "Seed the fixture project")
        return repository

    return build


@pytest.fixture
def run_agy():
    """Run one headless agy process in a seeded repository: run_agy("<prompt>", cwd=repository)
    -> CompletedProcess with decoded stdout and stderr. The line is always
    `agy -p <prompt> --dangerously-skip-permissions --print-timeout <PRINT_TIMEOUT>`, with no
    `--model` and no `--effort` (the account's defaults) and an `--output-format` only when
    one is given. It runs with the user's real HOME, so it drives the installed copy, and
    nothing here bounds it but agy's own print timeout."""

    def run(prompt, *, cwd, output_format=None):
        command = [
            "agy",
            "-p",
            prompt,
            "--dangerously-skip-permissions",
            "--print-timeout",
            PRINT_TIMEOUT,
        ]
        if output_format is not None:
            command += ["--output-format", output_format]
        return subprocess.run(
            command,
            cwd=str(cwd),
            stdin=subprocess.DEVNULL,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

    return run
