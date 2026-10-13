"""The output and error contract every task-list subcommand shares: silent mutators, one Error
line with exit 1 and both task files byte-for-byte unchanged, argparse's own exit 2 for a
malformed invocation, and never a traceback."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

import task_list

TOOL = Path(task_list.__file__).resolve()

TODO = task_list.TODO_NAME
DONE = task_list.DONE_NAME


def snapshot(target):
    return (target / TODO).read_bytes(), (target / DONE).read_bytes()


def assert_one_error_line(result):
    assert result.returncode == 1
    assert result.stdout == b""
    lines = result.stderr.decode("utf-8").split("\n")
    assert len(lines) == 2 and lines[1] == ""
    assert lines[0].startswith("Error: ")
    assert b"Traceback" not in result.stderr


# --- malformed invocations --------------------------------------------------------------


def test_no_subcommand_is_a_usage_error(run_task_list):
    result = run_task_list()
    assert result.returncode == 2
    assert result.stdout == b""
    assert result.stderr.startswith(b"usage: task_list.py")
    assert b"Traceback" not in result.stderr


def test_unknown_subcommand_is_a_usage_error(run_task_list, tmp_path):
    result = run_task_list("append", str(tmp_path))
    assert result.returncode == 2
    assert result.stdout == b""
    assert b"invalid choice: 'append'" in result.stderr


@pytest.mark.parametrize("subcommand", ["initialize", "insert", "move"])
def test_missing_milestone_dir_is_a_usage_error(run_task_list, subcommand):
    result = run_task_list(subcommand)
    assert result.returncode == 2
    assert result.stdout == b""
    assert b"MILESTONE_DIR" in result.stderr


def test_insert_without_a_position_flag_is_a_usage_error(run_task_list, task_list_dir):
    target = task_list_dir()
    before = snapshot(target)
    result = run_task_list("insert", str(target), "No Position Given", stdin=b"A body.\n")
    assert result.returncode == 2
    assert result.stdout == b""
    assert b"one of the arguments --end --before --after is required" in result.stderr
    assert snapshot(target) == before


@pytest.mark.parametrize(
    "flags",
    [
        ["--end", "--before", "Build The Parser First"],
        ["--before", "Build The Parser First", "--after", "Build The Parser First"],
        ["--end", "--after", "Build The Parser First"],
    ],
)
def test_insert_with_two_position_flags_is_a_usage_error(run_task_list, task_list_dir, flags):
    target = task_list_dir()
    before = snapshot(target)
    result = run_task_list("insert", str(target), "Two Positions Given", *flags, stdin=b"A body.\n")
    assert result.returncode == 2
    assert result.stdout == b""
    assert b"not allowed with argument" in result.stderr
    assert snapshot(target) == before


def test_insert_and_move_without_a_title_are_usage_errors(run_task_list, task_list_dir):
    target = task_list_dir()
    before = snapshot(target)
    for args in (["insert", str(target), "--end"], ["move", str(target)]):
        result = run_task_list(*args, stdin=b"text\n")
        assert result.returncode == 2
        assert result.stdout == b""
        assert b"TASK_TITLE" in result.stderr
    assert snapshot(target) == before


def test_initialize_refuses_a_stray_flag_as_a_usage_error(run_task_list, task_list_dir):
    target = task_list_dir()
    before = snapshot(target)
    result = run_task_list("initialize", str(target), "--force", stdin=b"## A Task\n\nBody.\n\n---\n")
    assert result.returncode == 2
    assert b"unrecognized arguments: --force" in result.stderr
    assert snapshot(target) == before


def test_help_exits_zero_and_lists_the_subcommands(run_task_list):
    result = run_task_list("--help")
    assert result.returncode == 0
    for subcommand in (b"initialize", b"insert", b"move"):
        assert subcommand in result.stdout
    assert b"append" not in result.stdout
    assert result.stderr == b""


# --- failures ---------------------------------------------------------------------------


def test_a_failure_is_exactly_one_error_line_on_stderr(run_task_list, task_list_dir):
    target = task_list_dir()
    before = snapshot(target)
    result = run_task_list("move", str(target), "No Such Task", stdin=b"- a criterion\n")
    assert_one_error_line(result)
    assert snapshot(target) == before


def test_an_operating_system_failure_is_an_error_line_not_a_traceback(run_task_list, tmp_path):
    blocker = tmp_path / "not-a-directory"
    blocker.write_text("")
    for args in (["initialize", str(blocker)], ["insert", str(blocker), "A Task", "--end"], ["move", str(blocker), "A Task"]):
        result = run_task_list(*args, stdin=b"## A Task\n\nBody.\n\n---\n")
        assert_one_error_line(result)
    assert blocker.read_bytes() == b""


@pytest.mark.parametrize("missing", [TODO, DONE])
def test_a_missing_task_file_is_refused_and_nothing_is_written(run_task_list, task_list_dir, missing):
    target = task_list_dir()
    (target / missing).unlink()
    kept = DONE if missing == TODO else TODO
    before = (target / kept).read_bytes()
    result = run_task_list("move", str(target), "Build The Parser First", stdin=b"- a criterion\n")
    assert_one_error_line(result)
    assert b"does not exist" in result.stderr
    assert (target / kept).read_bytes() == before
    assert sorted(path.name for path in target.iterdir()) == [kept]


@pytest.mark.parametrize(
    "args",
    [
        ["initialize"],
        ["insert", "Non UTF Body", "--end"],
        ["move", "Build The Parser First"],
    ],
)
def test_a_non_utf8_stdin_is_refused_with_both_files_unchanged(run_task_list, task_list_dir, args):
    target = task_list_dir()
    before = snapshot(target)
    result = run_task_list(args[0], str(target), *args[1:], stdin=b"## Bad \xff\xfe bytes\n\nBody.\n\n---\n")
    assert_one_error_line(result)
    assert b"is not UTF-8 text" in result.stderr
    assert snapshot(target) == before


def test_a_non_utf8_task_file_is_refused(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n## Bad \xff\n\nBody.\n\n---\n")
    before = snapshot(target)
    result = run_task_list("insert", str(target), "A Task", "--end", stdin=b"Body.\n")
    assert_one_error_line(result)
    assert snapshot(target) == before


@pytest.mark.parametrize(
    "args",
    [
        ["initialize"],
        ["insert", "Typed At A Terminal", "--end"],
        ["move", "Build The Parser First"],
    ],
)
def test_a_terminal_stdin_is_refused_without_blocking(task_list_dir, args):
    pty = pytest.importorskip("pty")
    target = task_list_dir()
    before = snapshot(target)
    master, slave = pty.openpty()
    try:
        result = subprocess.run(
            [sys.executable, "-B", str(TOOL), args[0], str(target), *args[1:]],
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
    assert snapshot(target) == before


# --- success ----------------------------------------------------------------------------


def test_every_mutator_prints_nothing_on_success(run_task_list, task_list_dir):
    target = task_list_dir()
    calls = [
        (["initialize", str(target)], b"## First Task\n\nThe first body.\n\n---\n\n## Second Task\n\nThe second body.\n\n---\n"),
        (["insert", str(target), "Third Task", "--end"], b"The third body.\n"),
        (["insert", str(target), "Zeroth Task", "--before", "First Task"], b"The zeroth body.\n"),
        (["insert", str(target), "Middle Task", "--after", "First Task"], b"The middle body.\n"),
        (["move", str(target), "First Task"], b"- the first criterion\n"),
    ]
    for args, stdin in calls:
        result = run_task_list(*args, stdin=stdin)
        assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def test_a_write_keeps_the_task_file_mode_and_leaves_no_temporary_file(run_task_list, task_list_dir):
    target = task_list_dir()
    os.chmod(target / TODO, 0o640)
    os.chmod(target / DONE, 0o604)
    result = run_task_list("move", str(target), "Build The Parser First", stdin=b"- a criterion\n")
    assert (result.returncode, result.stderr) == (0, b"")
    assert (os.stat(target / TODO).st_mode & 0o777) == 0o640
    assert (os.stat(target / DONE).st_mode & 0o777) == 0o604
    assert sorted(path.name for path in target.iterdir()) == [DONE, TODO]
