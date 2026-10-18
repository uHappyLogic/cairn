"""The output and error contract the fold tool shares with its siblings: a silent mutator, one
Error line with exit 1 and requirements.md byte-for-byte unchanged, argparse's own exit 2 for
a malformed invocation, a terminal stdin refused without blocking, and never a traceback."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

import requirements

TOOL = Path(requirements.__file__).resolve()

NAME = requirements.REQUIREMENTS_NAME
SECTION = "Prose decision"
DECISION = b"A decision folded by the contract tests.\n"


def assert_one_error_line(result):
    assert result.returncode == 1
    assert result.stdout == b""
    lines = result.stderr.decode("utf-8").split("\n")
    assert len(lines) == 2 and lines[1] == ""
    assert lines[0].startswith("Error: ")
    assert b"Traceback" not in result.stderr


def assert_usage_error(result):
    assert result.returncode == 2
    assert result.stdout == b""
    assert b"usage: requirements.py" in result.stderr
    assert b"Traceback" not in result.stderr


# --- malformed invocations --------------------------------------------------------------


def test_no_subcommand_is_a_usage_error(run_requirements):
    result = run_requirements()
    assert_usage_error(result)
    assert result.stderr.startswith(b"usage: requirements.py")


def test_unknown_subcommand_is_a_usage_error(run_requirements, requirements_dir):
    target = requirements_dir()
    before = (target / NAME).read_bytes()
    result = run_requirements("append", str(target), "--section", SECTION, stdin=DECISION)
    assert_usage_error(result)
    assert b"invalid choice: 'append'" in result.stderr
    assert (target / NAME).read_bytes() == before


def test_a_missing_milestone_dir_is_a_usage_error(run_requirements):
    result = run_requirements("fold", "--section", SECTION, stdin=DECISION)
    assert_usage_error(result)
    assert b"MILESTONE_DIR" in result.stderr


def test_a_missing_section_flag_is_a_usage_error_with_the_file_unchanged(run_requirements, requirements_dir):
    target = requirements_dir()
    before = (target / NAME).read_bytes()
    result = run_requirements("fold", str(target), stdin=DECISION)
    assert_usage_error(result)
    assert b"the following arguments are required: --section" in result.stderr
    assert (target / NAME).read_bytes() == before


def test_a_section_flag_without_its_heading_is_a_usage_error(run_requirements, requirements_dir):
    target = requirements_dir()
    before = (target / NAME).read_bytes()
    result = run_requirements("fold", str(target), "--section", stdin=DECISION)
    assert_usage_error(result)
    assert b"expected one argument" in result.stderr
    assert (target / NAME).read_bytes() == before


def test_a_stray_argument_is_a_usage_error(run_requirements, requirements_dir):
    target = requirements_dir()
    before = (target / NAME).read_bytes()
    result = run_requirements("fold", str(target), "--section", SECTION, "--force", stdin=DECISION)
    assert_usage_error(result)
    assert b"unrecognized arguments: --force" in result.stderr
    assert (target / NAME).read_bytes() == before


def test_help_exits_zero_and_lists_the_fold_subcommand(run_requirements):
    result = run_requirements("--help")
    assert result.returncode == 0
    assert b"fold" in result.stdout
    assert result.stderr == b""


def test_fold_help_names_its_required_section_flag(run_requirements):
    result = run_requirements("fold", "--help")
    assert result.returncode == 0
    assert b"MILESTONE_DIR" in result.stdout
    assert b"--section HEADING" in result.stdout
    assert result.stderr == b""


# --- failures ---------------------------------------------------------------------------


def test_a_failure_is_exactly_one_error_line_with_the_file_unchanged(run_requirements, requirements_dir):
    target = requirements_dir(b"# Milestone 1: No decisions\n\n## Goal\n\nShip it.\n")
    before = (target / NAME).read_bytes()
    result = run_requirements("fold", str(target), "--section", SECTION, stdin=DECISION)
    assert_one_error_line(result)
    assert (target / NAME).read_bytes() == before


def test_a_missing_requirements_file_is_refused_and_nothing_is_created(run_requirements, tmp_path):
    target = tmp_path / "milestone"
    target.mkdir()
    result = run_requirements("fold", str(target), "--section", SECTION, stdin=DECISION)
    assert_one_error_line(result)
    assert b"does not exist" in result.stderr
    assert list(target.iterdir()) == []


def test_an_operating_system_failure_is_an_error_line_not_a_traceback(run_requirements, tmp_path):
    blocker = tmp_path / "not-a-directory"
    blocker.write_bytes(b"")
    result = run_requirements("fold", str(blocker), "--section", SECTION, stdin=DECISION)
    assert_one_error_line(result)
    assert blocker.read_bytes() == b""


def test_a_non_utf8_requirements_file_is_refused(run_requirements, requirements_dir):
    target = requirements_dir(b"# Milestone 1: Bad \xff bytes\n\n## Decisions\n")
    before = (target / NAME).read_bytes()
    result = run_requirements("fold", str(target), "--section", SECTION, stdin=DECISION)
    assert_one_error_line(result)
    assert b"is not UTF-8 text" in result.stderr
    assert (target / NAME).read_bytes() == before


def test_a_non_utf8_stdin_is_refused_with_the_file_unchanged(run_requirements, requirements_dir):
    target = requirements_dir()
    before = (target / NAME).read_bytes()
    result = run_requirements("fold", str(target), "--section", SECTION, stdin=b"Bad \xff\xfe bytes.\n")
    assert_one_error_line(result)
    assert b"is not UTF-8 text" in result.stderr
    assert (target / NAME).read_bytes() == before


def test_a_terminal_stdin_is_refused_without_blocking(requirements_dir):
    pty = pytest.importorskip("pty")
    target = requirements_dir()
    before = (target / NAME).read_bytes()
    master, slave = pty.openpty()
    try:
        result = subprocess.run(
            [sys.executable, "-B", str(TOOL), "fold", str(target), "--section", SECTION],
            stdin=slave,
            capture_output=True,
            check=False,
            timeout=30,
        )
    finally:
        os.close(slave)
        os.close(master)
    assert_one_error_line(result)
    assert b"must be piped on standard input (as a quoted heredoc or a redirected file), not typed at a terminal" in result.stderr
    assert (target / NAME).read_bytes() == before


# --- success ----------------------------------------------------------------------------


def test_the_fold_prints_nothing_on_success(run_requirements, requirements_dir):
    target = requirements_dir()
    for section in (SECTION, "A Subsection Created By The Fold"):
        result = run_requirements("fold", str(target), "--section", section, stdin=DECISION)
        assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def test_a_write_keeps_the_file_mode_and_leaves_no_temporary_file(run_requirements, requirements_dir):
    target = requirements_dir()
    os.chmod(target / NAME, 0o640)
    result = run_requirements("fold", str(target), "--section", SECTION, stdin=DECISION)
    assert (result.returncode, result.stderr) == (0, b"")
    assert (os.stat(target / NAME).st_mode & 0o777) == 0o640
    assert sorted(path.name for path in target.iterdir()) == [NAME]
