"""The milestones tool's shared contract: its help states the record's two limits (a shallow
clone's truncated log, and the record's start at the first Task-completion: commit), every
failure is one Error line on stderr with exit 1 and nothing on stdout, a malformed invocation
gets argparse's exit 2, no traceback reaches the caller, and a query writes nothing: the
repository's status and HEAD are the same after it as before."""

import os

import pytest

FIRST = "milestones/milestone_07_first/"


@pytest.fixture
def seeded(repo):
    return repo({FIRST: "parallel_first"})


def assert_one_error_line(result):
    assert result.returncode == 1
    assert result.stdout == b""
    text = result.stderr.decode("utf-8")
    assert "Traceback" not in text
    lines = text.splitlines()
    assert len(lines) == 1
    assert lines[0].startswith("Error: ")
    return lines[0]


@pytest.mark.parametrize("args", [("--help",), ("tasks", "--help")])
def test_the_help_states_the_shallow_clone_limit_and_where_the_record_starts(tmp_path, run_milestones, args):
    result = run_milestones(tmp_path, *args)
    assert result.returncode == 0
    text = " ".join(result.stdout.decode("utf-8").split())
    assert "shallow clone" in text
    assert "no check is made" in text
    assert "Task-completion:" in text
    assert "2026-09-02" in text
    assert "milestone_15" in text
    assert "Tasklist-completion:" in text


def test_the_help_names_the_query_and_its_body_flag(tmp_path, run_milestones):
    text = run_milestones(tmp_path, "tasks", "--help").stdout.decode("utf-8")
    assert "PATH" in text
    assert "--with-body" in text


def test_outside_a_git_repository_the_query_fails_on_one_error_line(tmp_path, run_milestones):
    outside = tmp_path / "outside"
    outside.mkdir()
    line = assert_one_error_line(run_milestones(outside, "tasks", "."))
    assert "git log" in line


def test_an_empty_path_is_refused(seeded, run_milestones):
    assert_one_error_line(run_milestones(seeded, "tasks", ""))


def test_a_missing_git_fails_on_one_error_line(seeded, run_milestones, environment, tmp_path):
    empty_bin = tmp_path / "no-git-bin"
    empty_bin.mkdir()
    env = dict(environment, PATH=str(empty_bin))
    line = assert_one_error_line(run_milestones(seeded, "tasks", FIRST, env=env))
    assert "git" in line


@pytest.mark.parametrize("args", [(), ("tasks",), ("unknown", FIRST), ("tasks", FIRST, "--body")])
def test_a_malformed_invocation_exits_2(seeded, run_milestones, args):
    result = run_milestones(seeded, *args)
    assert result.returncode == 2
    assert result.stdout == b""
    assert "Traceback" not in result.stderr.decode("utf-8")


def test_a_query_writes_nothing(seeded, make_commit, run_milestones, git, environment):
    make_commit(seeded, "Task-completion: A Task", files={FIRST + "TASKS_TODO.md": b"a\n"}, body="- done\n")
    (seeded / "untracked.txt").write_bytes(b"x\n")
    before = (
        git(seeded, environment, "status", "--porcelain", "--ignored"),
        git(seeded, environment, "rev-parse", "HEAD"),
        sorted(os.listdir(seeded / ".git")),
    )
    for args in (("tasks", FIRST), ("tasks", FIRST, "--with-body"), ("tasks", "untracked.txt"), ("tasks", "nope")):
        run_milestones(seeded, *args)
    after = (
        git(seeded, environment, "status", "--porcelain", "--ignored"),
        git(seeded, environment, "rev-parse", "HEAD"),
        sorted(os.listdir(seeded / ".git")),
    )
    assert after == before
