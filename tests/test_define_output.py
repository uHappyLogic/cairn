"""define_milestone.py output and exit contract: two unlabeled stdout lines and the four files
on success, one Error line on stderr with exit 1 and empty stdout on every failure,
argparse's own exit 2, and never a traceback."""

import io
import os
import sys

import pytest

import define_milestone

GOAL = b"Ship it.\n"
FILES = ["TASKS_DONE.md", "TASKS_TODO.md", "open_questions.xml", "requirements.md"]


def current_umask():
    umask = os.umask(0)
    os.umask(umask)
    return umask


def test_success_prints_exactly_the_subject_and_the_directory(run_define, workspace):
    root = workspace("milestone_36_previous")
    result = run_define("--title", "Mechanical milestone definition", stdin=GOAL, cwd=root)
    assert result.returncode == 0
    assert result.stderr == b""
    assert result.stdout == (
        b"Milestone-definition: milestone_37_mechanical-milestone-definition\n"
        b"milestones/milestone_37_mechanical-milestone-definition/\n"
    )


def test_success_writes_exactly_the_four_files(run_define, workspace):
    root = workspace()
    result = run_define("--title", "First steps", stdin=b"Make the first step.\n", cwd=root)
    assert result.returncode == 0, result.stderr
    directory = root / "milestones" / "milestone_01_first-steps"
    assert sorted(path.name for path in directory.iterdir()) == FILES
    assert (directory / "open_questions.xml").read_bytes() == b"<open-questions/>\n"
    assert (directory / "requirements.md").read_bytes() == (
        b"# Milestone 1: First steps\n"
        b"\n"
        b"## Goal\n"
        b"\n"
        b"Make the first step.\n"
        b"\n"
        b"## Relevant starting state\n"
        b"\n"
        b"## Decisions\n"
        b"\n"
        b"## Out of Scope\n"
        b"\n"
    )
    assert (directory / "TASKS_TODO.md").read_bytes() == b"# TASKS TODO\n\n"
    assert (directory / "TASKS_DONE.md").read_bytes() == b"# TASKS DONE\n\n"


def test_the_files_take_the_default_mode(run_define, workspace):
    root = workspace()
    run_define("--title", "First", stdin=GOAL, cwd=root)
    expected = 0o666 & ~current_umask()
    for path in (root / "milestones" / "milestone_01_first").iterdir():
        assert os.stat(path).st_mode & 0o777 == expected


def test_the_goal_is_kept_byte_for_byte_with_only_its_ends_trimmed(run_define, workspace):
    root = workspace()
    goal = "  \n\n\tLine one with `code` and *emphasis*.\n\n## Not a heading guard\n\n- item\n  indented café\r\n\n\n"
    result = run_define("--title", "Goal kept", stdin=goal.encode("utf-8"), cwd=root)
    assert result.returncode == 0, result.stderr
    requirements = (root / "milestones" / "milestone_01_goal-kept" / "requirements.md").read_bytes().decode("utf-8")
    expected_goal = "Line one with `code` and *emphasis*.\n\n## Not a heading guard\n\n- item\n  indented café"
    assert requirements == REQUIREMENTS.format(title="Goal kept", goal=expected_goal)


REQUIREMENTS = (
    "# Milestone 1: {title}\n\n## Goal\n\n{goal}\n\n## Relevant starting state\n\n## Decisions\n\n## Out of Scope\n\n"
)


def test_a_heredoc_final_newline_adds_no_blank_line(run_define, workspace):
    root = workspace()
    run_define("--title", "Heredoc", stdin=b"One line goal.\n", cwd=root)
    requirements = (root / "milestones" / "milestone_01_heredoc" / "requirements.md").read_text(encoding="utf-8")
    assert "One line goal.\n\n## Relevant starting state\n" in requirements


@pytest.mark.parametrize("goal", [b"", b"   ", b"\n\n\t \n"])
def test_an_empty_goal_is_refused(run_define, workspace, goal):
    root = workspace()
    result = run_define("--title", "First", stdin=goal, cwd=root)
    assert (result.returncode, result.stdout) == (1, b"")
    assert result.stderr == b"Error: the goal text on standard input is empty\n"
    assert list((root / "milestones").iterdir()) == []


def test_a_non_utf8_goal_is_refused(run_define, workspace):
    root = workspace()
    result = run_define("--title", "First", stdin=b"caf\xe9\n", cwd=root)
    assert (result.returncode, result.stdout) == (1, b"")
    assert result.stderr == b"Error: the goal text on standard input is not UTF-8 text\n"
    assert list((root / "milestones").iterdir()) == []


class Terminal(io.TextIOWrapper):
    def isatty(self):
        return True


@pytest.mark.parametrize(
    ("stdin", "reason"),
    [
        (None, "Error: the goal text must be supplied on standard input, which is closed\n"),
        (
            Terminal(io.BytesIO(b"typed")),
            "Error: the goal text must be piped on standard input (as a quoted heredoc or a redirected file), "
            "not typed at a terminal\n",
        ),
    ],
)
def test_a_closed_or_terminal_stdin_is_refused(workspace, monkeypatch, capsys, stdin, reason):
    root = workspace()
    monkeypatch.chdir(root)
    monkeypatch.setattr(sys, "stdin", stdin)
    assert define_milestone.main(["--title", "First"]) == 1
    captured = capsys.readouterr()
    assert (captured.out, captured.err) == ("", reason)
    assert list((root / "milestones").iterdir()) == []


def test_a_closed_stream_object_is_refused(workspace, monkeypatch, capsys):
    root = workspace()
    stream = io.TextIOWrapper(io.BytesIO(GOAL))
    stream.close()
    monkeypatch.chdir(root)
    monkeypatch.setattr(sys, "stdin", stream)
    assert define_milestone.main(["--title", "First"]) == 1
    assert capsys.readouterr().err.endswith("which is closed\n")


def test_a_missing_title_is_a_usage_error(run_define, workspace):
    root = workspace()
    result = run_define(stdin=GOAL, cwd=root)
    assert result.returncode == 2
    assert result.stdout == b""
    assert result.stderr.startswith(b"usage: define_milestone.py")
    assert b"--title" in result.stderr
    assert list((root / "milestones").iterdir()) == []


def test_an_unknown_argument_is_a_usage_error(run_define, workspace):
    root = workspace()
    result = run_define("--title", "First", "--root", "elsewhere", stdin=GOAL, cwd=root)
    assert result.returncode == 2
    assert result.stdout == b""
    assert b"unrecognized arguments" in result.stderr
    assert list((root / "milestones").iterdir()) == []


def test_help_exits_zero(run_define, workspace):
    result = run_define("--help", cwd=workspace())
    assert result.returncode == 0
    assert result.stdout.startswith(b"usage: define_milestone.py")
    assert b"--title" in result.stdout
    assert result.stderr == b""


FAILURES = {
    "missing root": dict(layout={"root": False}, title="First", stdin=GOAL),
    "empty title": dict(layout={}, title=" \n ", stdin=GOAL),
    "slugless title": dict(layout={}, title="?!", stdin=GOAL),
    "empty goal": dict(layout={}, title="First", stdin=b" \n"),
    "non-utf8 goal": dict(layout={}, title="First", stdin=b"\xff"),
    "conflict": dict(layout={"files": ("milestone_01_first",)}, title="First", stdin=GOAL),
}


@pytest.mark.parametrize("case", sorted(FAILURES))
def test_every_failure_is_exactly_one_error_line_and_empty_stdout(run_define, workspace, case):
    setup = FAILURES[case]
    root = workspace(**setup["layout"])
    result = run_define("--title", setup["title"], stdin=setup["stdin"], cwd=root)
    assert result.returncode == 1
    assert result.stdout == b""
    lines = result.stderr.decode("utf-8").split("\n")
    assert len(lines) == 2 and lines[1] == ""
    assert lines[0].startswith("Error: ")
    assert b"Traceback" not in result.stderr


def test_an_unexpected_exception_is_one_folded_error_line(workspace, monkeypatch, capsys):
    def explode(title):
        raise RuntimeError("first line\nsecond line")

    root = workspace()
    monkeypatch.chdir(root)
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(GOAL)))
    monkeypatch.setattr(define_milestone, "derive_slug", explode)
    assert define_milestone.main(["--title", "First"]) == 1
    captured = capsys.readouterr()
    assert (captured.out, captured.err) == ("", "Error: RuntimeError: first line second line\n")


def test_an_operating_system_failure_is_an_error_line_not_a_traceback(workspace, monkeypatch, capsys):
    def unreadable(root):
        raise PermissionError(13, "Permission denied", root)

    root = workspace()
    monkeypatch.chdir(root)
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(GOAL)))
    monkeypatch.setattr(define_milestone, "next_number", unreadable)
    assert define_milestone.main(["--title", "First"]) == 1
    captured = capsys.readouterr()
    assert (captured.out, captured.err) == ("", "Error: Permission denied: milestones\n")


def test_an_operating_system_failure_without_a_filename_is_its_message(workspace, monkeypatch, capsys):
    def broken(root):
        raise OSError("device gone")

    root = workspace()
    monkeypatch.chdir(root)
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(GOAL)))
    monkeypatch.setattr(define_milestone, "next_number", broken)
    assert define_milestone.main(["--title", "First"]) == 1
    assert capsys.readouterr().err == "Error: device gone\n"


def test_main_returns_zero_and_prints_the_two_lines(workspace, monkeypatch, capsys):
    root = workspace()
    monkeypatch.chdir(root)
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(GOAL)))
    assert define_milestone.main(["--title", "First"]) == 0
    captured = capsys.readouterr()
    assert captured.out == "Milestone-definition: milestone_01_first\nmilestones/milestone_01_first/\n"
    assert captured.err == ""
