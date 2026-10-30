"""The milestones tool's tasks query with its body flag: each task line stays at column 0 in its
unflagged shape, and every line of the commit's body is printed beneath it indented by four
spaces, as git log indents a message, with the body's outer blank lines trimmed and nothing
else changed but the trailing trailer paragraph test_milestones_trailers.py pins; a commit
with no body is its task line alone. Every test runs on a repository
seeded through the conftest factory and given commits made through the conftest helper, whose
messages git keeps verbatim."""

import pytest

FIRST = "milestones/milestone_07_first/"
TODO = FIRST + "TASKS_TODO.md"
BODY_FLAG = "--with-body"


@pytest.fixture
def seeded(repo):
    return repo({FIRST: "parallel_first"})


def tasks(run_milestones, repo, *args):
    result = run_milestones(repo, "tasks", *args)
    assert result.returncode == 0, result.stderr
    assert result.stderr == b""
    return result.stdout.decode("utf-8")


def task_line(git, repo, environment, commit, title, date):
    short = git(repo, environment, "log", "-1", "--format=%h", commit).strip()
    return f"{short}\t{date}\t{FIRST}\t{title}\n"


def test_each_body_line_is_indented_by_four_spaces_beneath_its_task_line(
    seeded, make_commit, run_milestones, git, environment
):
    commit = make_commit(
        seeded,
        "Task-completion: Bulleted Bar",
        files={TODO: b"a\n"},
        body="- the first criterion\n- the second criterion, with `code`\n",
        date="2026-02-01T10:00:00+00:00",
    )
    assert tasks(run_milestones, seeded, FIRST, BODY_FLAG) == (
        task_line(git, seeded, environment, commit, "Bulleted Bar", "2026-02-01")
        + "    - the first criterion\n"
        + "    - the second criterion, with `code`\n"
    )


def test_the_task_line_is_the_same_with_and_without_the_flag(seeded, make_commit, run_milestones):
    make_commit(seeded, "Task-completion: Same Line", files={TODO: b"a\n"}, body="- a criterion\n")
    without = tasks(run_milestones, seeded, FIRST)
    with_body = tasks(run_milestones, seeded, FIRST, BODY_FLAG)
    assert with_body.splitlines()[0] + "\n" == without
    assert "a criterion" not in without


def test_the_bodys_outer_blank_lines_are_trimmed_and_nothing_else_changes(
    seeded, make_commit, run_milestones, git, environment
):
    commit = make_commit(
        seeded,
        "Task-completion: Padded Bar",
        files={TODO: b"a\n"},
        body="  \n\n- first  \n\n  - nested\n\t- tabbed\n\n \n\n",
        date="2026-02-02T10:00:00+00:00",
    )
    assert tasks(run_milestones, seeded, FIRST, BODY_FLAG) == (
        task_line(git, seeded, environment, commit, "Padded Bar", "2026-02-02")
        + "    - first  \n"
        + "    \n"
        + "      - nested\n"
        + "    \t- tabbed\n"
    )


def test_a_commit_with_no_body_is_its_task_line_alone(seeded, make_commit, run_milestones, git, environment):
    older = make_commit(
        seeded,
        "Task-completion: Bar In The Body",
        files={TODO: b"a\n"},
        body="- verified\n",
        date="2026-02-03T10:00:00+00:00",
    )
    newer = make_commit(
        seeded, "Task-completion: Subject Only", files={TODO: b"b\n"}, date="2026-02-04T10:00:00+00:00"
    )
    assert tasks(run_milestones, seeded, FIRST, BODY_FLAG) == (
        task_line(git, seeded, environment, newer, "Subject Only", "2026-02-04")
        + task_line(git, seeded, environment, older, "Bar In The Body", "2026-02-03")
        + "    - verified\n"
    )


def test_a_whitespace_only_body_prints_nothing_beneath_its_line(seeded, make_commit, run_milestones):
    make_commit(seeded, "Task-completion: Blank Body", files={TODO: b"a\n"}, body=" \n\n  \n")
    printed = tasks(run_milestones, seeded, FIRST, BODY_FLAG)
    assert printed.count("\n") == 1
    assert printed.endswith("\tBlank Body\n")


def test_every_body_line_is_indented_so_every_column_zero_line_is_a_task(seeded, make_commit, run_milestones):
    make_commit(
        seeded,
        "Task-completion: Tricky Body",
        files={TODO: b"a\n"},
        body="abc1234\t2026-01-01\tmilestones/x/\tLooks Like A Task\n\n## A heading\n---\n",
        date="2026-02-05T10:00:00+00:00",
    )
    make_commit(
        seeded,
        "Task-completion: Next Task",
        files={TODO: b"b\n"},
        body="- plain\n",
        date="2026-02-06T10:00:00+00:00",
    )
    lines = tasks(run_milestones, seeded, FIRST, BODY_FLAG).splitlines()
    column_zero = [line for line in lines if not line.startswith("    ")]
    assert [line.split("\t")[3] for line in column_zero] == ["Next Task", "Tricky Body"]
    assert lines[3:] == [
        "    abc1234\t2026-01-01\tmilestones/x/\tLooks Like A Task",
        "    ",
        "    ## A heading",
        "    ---",
    ]
