"""The milestones tool's one trailer rule over every body it prints: tasks --with-body, summary,
and record each trim a body's outer blank lines and then drop a trailing paragraph whose every
line is a trailer, "Token: value" with a token of letters, digits, and hyphens, so a pre-flip
task body that is only an attribution trailer prints as a commit with no body. A paragraph
that is not the last, or a last one holding any line that is not a trailer, is printed as it
stands. Every test runs on a repository seeded through the conftest factory, then given task and
finish-shaped commits made through the conftest helper."""

import pytest

FIRST = "milestones/milestone_07_first/"
TODO = FIRST + "TASKS_TODO.md"
ATTRIBUTION = "Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
SESSION = "Claude-Session: https://claude.ai/code/session_0123"


@pytest.fixture
def seeded(repo):
    return repo({FIRST: "parallel_first"}, files={FIRST + "requirements.md": b"# First\n\n## Goal\n\nG.\n"})


def bodies(run_milestones, repo):
    result = run_milestones(repo, "tasks", FIRST, "--with-body")
    assert result.returncode == 0, result.stderr
    return result.stdout.decode("utf-8")


def beneath(printed):
    return [line[4:] for line in printed.splitlines() if line.startswith("    ")]


@pytest.mark.parametrize(
    "body",
    [
        ATTRIBUTION + "\n",
        "\n" + ATTRIBUTION + "\n" + SESSION + "\n\n",
        "Signed-off-by: A Person <a@example.invalid>\n",
        "Token-2: value\nX: y\n",
    ],
)
def test_a_body_that_is_only_a_trailer_block_prints_as_no_body(seeded, make_commit, run_milestones, body):
    make_commit(seeded, "Task-completion: Pre-Flip Task", files={TODO: b"a\n"}, body=body)
    printed = bodies(run_milestones, seeded)
    assert printed.count("\n") == 1
    assert printed.endswith("\tPre-Flip Task\n")


def test_a_trailing_trailer_paragraph_is_dropped_after_the_bar(seeded, make_commit, run_milestones):
    make_commit(
        seeded,
        "Task-completion: Barred Task",
        files={TODO: b"a\n"},
        body="- the first criterion\n- the second criterion\n\n\n" + ATTRIBUTION + "\n" + SESSION + "\n",
    )
    assert beneath(bodies(run_milestones, seeded)) == ["- the first criterion", "- the second criterion"]


def test_a_trailer_paragraph_that_is_not_the_last_is_kept(seeded, make_commit, run_milestones):
    make_commit(
        seeded,
        "Task-completion: Middle Trailer",
        files={TODO: b"a\n"},
        body=ATTRIBUTION + "\n\n- the bar\n",
    )
    assert beneath(bodies(run_milestones, seeded)) == [ATTRIBUTION, "", "- the bar"]


@pytest.mark.parametrize(
    "last",
    [
        ATTRIBUTION + "\nand a line that is no trailer",
        "- a bullet: with a colon",
        "Token:value with no space",
        "Two words: value",
        "Token: ",
        "  Indented-Token: value",
        "-Token: value",
    ],
)
def test_a_last_paragraph_holding_any_line_that_is_no_trailer_is_kept(seeded, make_commit, run_milestones, last):
    make_commit(seeded, "Task-completion: Kept", files={TODO: b"a\n"}, body="- the bar\n\n" + last + "\n")
    assert beneath(bodies(run_milestones, seeded)) == ["- the bar", ""] + [
        line.rstrip("\n") for line in last.split("\n")
    ]


def test_only_one_trailing_trailer_paragraph_is_dropped(seeded, make_commit, run_milestones):
    make_commit(
        seeded,
        "Task-completion: Two Blocks",
        files={TODO: b"a\n"},
        body="- the bar\n\nNote: kept\n\n" + ATTRIBUTION + "\n",
    )
    assert beneath(bodies(run_milestones, seeded)) == ["- the bar", "", "Note: kept"]


def test_summary_and_record_drop_a_finish_bodys_trailer_paragraph(seeded, make_commit, run_milestones):
    removed = [FIRST + name for name in ("requirements.md", "TASKS_TODO.md", "open_questions.xml")]
    make_commit(
        seeded,
        "Milestone-finish: " + FIRST,
        removed=[path for path in removed if (seeded / path).exists()],
        body="First\n\n- built the first\n\n" + ATTRIBUTION + "\n" + SESSION + "\n",
        date="2026-03-01T10:00:00+00:00",
    )
    summary = run_milestones(seeded, "summary", FIRST)
    assert summary.returncode == 0, summary.stderr
    assert summary.stdout.decode("utf-8") == "2026-03-01\nFirst\n\n- built the first\n"
    record = run_milestones(seeded, "record", ".")
    assert record.returncode == 0, record.stderr
    assert record.stdout.decode("utf-8") == f"finished\t2026-03-01\t{FIRST}\tFirst\n    - built the first\n"
