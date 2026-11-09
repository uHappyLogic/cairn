"""The milestones tool's shared contract: its help states the record's limits (a shallow clone's
truncated log, with no check made for it, the record's start at the first Task-completion:
commit, and the finish subjects read only in the path form) for the tasks query and the three
history queries, the live query's started test reading the same log, the gate and since queries
the two that refuse a shallow repository, and the trailer rule over every printed body; every failure is one Error line on stderr with exit 1 and nothing on stdout,
a malformed invocation gets argparse's exit 2, no traceback reaches the caller, and a query
writes nothing: the repository's status and HEAD are the same after it as before."""

import os

import pytest

FIRST = "milestones/milestone_07_first/"


@pytest.fixture
def seeded(repo):
    return repo({FIRST: "parallel_first"}, files={FIRST + "requirements.md": b"# Milestone 7: First\n"})


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


@pytest.mark.parametrize("args", [("--help",), ("live", "--help")])
def test_the_help_states_that_the_started_test_reads_a_shallow_clones_log(tmp_path, run_milestones, args):
    result = run_milestones(tmp_path, *args)
    assert result.returncode == 0
    text = " ".join(result.stdout.decode("utf-8").split())
    assert "started test" in text
    assert "shallow clone" in text
    assert 'reads "defined"' in text


@pytest.mark.parametrize("query", ["milestones", "summary", "record", "show"])
def test_each_history_querys_help_states_the_shallow_clone_limit(tmp_path, run_milestones, query):
    result = run_milestones(tmp_path, query, "--help")
    assert result.returncode == 0
    text = " ".join(result.stdout.decode("utf-8").split())
    assert "shallow clone" in text
    assert "no check is made" in text
    assert "finish" in text
    assert "Milestone-finish:" in text
    assert "Task-completion:" in text


def test_the_top_level_help_states_the_finish_subject_limit_and_names_every_query(tmp_path, run_milestones):
    text = " ".join(run_milestones(tmp_path, "--help").stdout.decode("utf-8").split())
    assert "Milestone-finish: subjects naming a milestone path" in text
    for query in ("live", "gate", "tasks", "milestones", "summary", "record", "since", "show"):
        assert query in text


def test_the_top_level_help_states_that_gate_and_since_check_for_a_shallow_clone(tmp_path, run_milestones):
    text = " ".join(run_milestones(tmp_path, "--help").stdout.decode("utf-8").split())
    assert "two queries check, gate and since, each refusing a shallow repository" in text
    assert "alone checks" not in text


def test_the_gate_help_names_its_scope_rule_and_both_refusals(tmp_path, run_milestones):
    result = run_milestones(tmp_path, "gate", "--help")
    assert result.returncode == 0
    text = " ".join(result.stdout.decode("utf-8").split())
    assert "MILESTONE_PATH" in text
    assert "one bare path per line" in text
    assert "started" in text
    assert "equals MILESTONE_PATH's scope, contains it, or lies under it" in text
    assert "exits 0 whether or not it prints" in text
    assert "git rev-parse --is-shallow-repository" in text
    assert "git fetch --unshallow" in text
    assert "no milestones/ container is refused" in text


@pytest.mark.parametrize(
    "args", [("tasks", "--help"), ("summary", "--help"), ("record", "--help")]
)
def test_the_help_of_each_body_printer_states_the_trailer_rule(tmp_path, run_milestones, args):
    text = " ".join(run_milestones(tmp_path, *args).stdout.decode("utf-8").split())
    assert "trailing paragraph whose every line is a trailer" in text
    assert "Token: value" in text


def test_the_history_helps_name_their_line_shapes(tmp_path, run_milestones):
    milestones = " ".join(run_milestones(tmp_path, "milestones", "--help").stdout.decode("utf-8").split())
    assert '"live" or "finished"' in milestones
    assert "YYYY-MM-DD" in milestones
    assert "Every live line stands above every finished one" in milestones
    summary = " ".join(run_milestones(tmp_path, "summary", "--help").stdout.decode("utf-8").split())
    assert '"live"' in summary and "## Goal" in summary
    record = " ".join(run_milestones(tmp_path, "record", "--help").stdout.decode("utf-8").split())
    assert "column 0" in record and "four spaces" in record and "no bar" in record


def test_the_live_help_names_the_discovery_pattern_and_the_line(tmp_path, run_milestones):
    text = " ".join(run_milestones(tmp_path, "live", "--help").stdout.decode("utf-8").split())
    assert "**/milestones/*/requirements.md" in text
    assert "started" in text and "defined" in text
    assert "--diff-filter=M" in text


def test_the_help_names_the_query_and_its_body_flag(tmp_path, run_milestones):
    text = run_milestones(tmp_path, "tasks", "--help").stdout.decode("utf-8")
    assert "PATH" in text
    assert "--with-body" in text


def test_outside_a_git_repository_the_query_fails_on_one_error_line(tmp_path, run_milestones):
    outside = tmp_path / "outside"
    outside.mkdir()
    line = assert_one_error_line(run_milestones(outside, "tasks", "."))
    assert "git log" in line


def test_outside_a_git_repository_live_fails_on_one_error_line(tmp_path, run_milestones):
    outside = tmp_path / "outside"
    outside.mkdir()
    line = assert_one_error_line(run_milestones(outside, "live"))
    assert "git ls-files" in line


@pytest.mark.parametrize("query", ["gate", "since"])
def test_outside_a_git_repository_gate_and_since_fail_on_one_error_line(tmp_path, run_milestones, query):
    outside = tmp_path / "outside"
    outside.mkdir()
    line = assert_one_error_line(run_milestones(outside, query, FIRST))
    assert "git rev-parse" in line


@pytest.mark.parametrize("args", [("milestones", "."), ("summary", FIRST), ("record", "."), ("show", FIRST)])
def test_outside_a_git_repository_a_history_query_fails_on_one_error_line(tmp_path, run_milestones, args):
    outside = tmp_path / "outside"
    outside.mkdir()
    line = assert_one_error_line(run_milestones(outside, *args))
    assert "git" in line


@pytest.mark.parametrize("query", ["live", "gate", "tasks", "milestones", "summary", "record", "since", "show"])
def test_an_empty_path_is_refused(seeded, run_milestones, query):
    assert_one_error_line(run_milestones(seeded, query, ""))


def test_a_missing_git_fails_on_one_error_line(seeded, run_milestones, environment, tmp_path):
    empty_bin = tmp_path / "no-git-bin"
    empty_bin.mkdir()
    env = dict(environment, PATH=str(empty_bin))
    line = assert_one_error_line(run_milestones(seeded, "tasks", FIRST, env=env))
    assert "git" in line
    line = assert_one_error_line(run_milestones(seeded, "live", env=env))
    assert "git" in line
    for args in (("live", FIRST), ("gate", FIRST), ("milestones", "."), ("summary", FIRST), ("record", "."), ("since", FIRST), ("show", FIRST)):
        line = assert_one_error_line(run_milestones(seeded, *args, env=env))
        assert "git" in line


@pytest.mark.skipif(hasattr(os, "geteuid") and os.geteuid() == 0, reason="root reads a file whatever its mode")
def test_an_unreadable_live_requirements_file_fails_on_one_error_line(seeded, run_milestones):
    requirements = seeded / FIRST / "requirements.md"
    requirements.chmod(0)
    try:
        for args in (("milestones", "."), ("summary", FIRST), ("record", "."), ("show", FIRST)):
            line = assert_one_error_line(run_milestones(seeded, *args))
            assert "requirements.md" in line
    finally:
        requirements.chmod(0o644)


@pytest.mark.parametrize(
    "args",
    [
        (),
        ("tasks",),
        ("unknown", FIRST),
        ("tasks", FIRST, "--body"),
        ("live", FIRST, FIRST),
        ("live", "--with-body"),
        ("live", FIRST, "--with-body"),
        ("gate",),
        ("gate", FIRST, FIRST),
        ("gate", FIRST, "--with-body"),
        ("milestones",),
        ("milestones", FIRST, FIRST),
        ("milestones", FIRST, "--with-body"),
        ("summary",),
        ("summary", FIRST, FIRST),
        ("summary", FIRST, "--with-body"),
        ("record",),
        ("record", FIRST, FIRST),
        ("record", FIRST, "--with-body"),
        ("since",),
        ("since", FIRST, FIRST),
        ("since", FIRST, "--with-body"),
        ("show",),
        ("show", FIRST, "requirements.md"),
        ("show", FIRST, "--with-body"),
    ],
)
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
    for args in (
        ("tasks", FIRST),
        ("tasks", FIRST, "--with-body"),
        ("tasks", "untracked.txt"),
        ("tasks", "nope"),
        ("live",),
        ("live", FIRST),
        ("live", "nope/"),
        ("gate", FIRST),
        ("gate", "nope/"),
        ("gate", "milestones/nope/"),
        ("milestones", "."),
        ("milestones", "nope"),
        ("summary", FIRST),
        ("summary", "nope/"),
        ("record", "."),
        ("record", FIRST),
        ("since", FIRST),
        ("since", FIRST, "--milestones"),
        ("since", "nope/"),
        ("show", FIRST),
        ("show", "nope/"),
    ):
        run_milestones(seeded, *args)
    after = (
        git(seeded, environment, "status", "--porcelain", "--ignored"),
        git(seeded, environment, "rev-parse", "HEAD"),
        sorted(os.listdir(seeded / ".git")),
    )
    assert after == before
