"""The milestones tool's summary query: one three-part print for both states, told apart by its
first line alone. For a finished milestone the first line is the finish commit's author date as
YYYY-MM-DD, followed by that commit's body (title line, blank line, bullets) with its outer
blank lines trimmed and a trailing trailer paragraph dropped; for a live milestone the first
line is the fixed word "live", followed by its title from the requirements.md heading, a blank
line, and the whole "## Goal" section body, verbatim with its outer blank lines trimmed, read
from the working tree. MILESTONE_PATH is the path exactly as the milestones query prints it,
and one naming neither a live nor a finished milestone is refused on one Error line. Every
test runs on a repository seeded through the conftest factory, then given finish-shaped
commits made through the conftest helper."""

import pytest

ALPHA = "milestones/alpha/"
BETA = "milestones/beta/"
REQUIREMENTS = (
    b"# Milestone 7: Alpha Work\n"
    b"\n"
    b"## Goal\n"
    b"\n"
    b"\n"
    b"Build the alpha, in two\n"
    b"paragraphs.\n"
    b"\n"
    b"### A goal subsection\n"
    b"\n"
    b"  - an indented line\t\n"
    b"\n"
    b"## Relevant starting state\n"
    b"\n"
    b"Not the goal.\n"
)


def milestone_files(directory, requirements=REQUIREMENTS):
    return {
        directory + "requirements.md": requirements,
        directory + "TASKS_TODO.md": b"# TASKS TODO\n\n",
        directory + "open_questions.xml": b"<open-questions/>\n",
    }


def removed_files(directory):
    return [directory + name for name in ("requirements.md", "TASKS_TODO.md", "open_questions.xml")]


@pytest.fixture
def seeded(repo):
    return repo({}, files={**milestone_files(ALPHA), **milestone_files(BETA, b"# Beta Work\n\n## Goal\n\nB.\n")})


def summary(run_milestones, repo, path):
    result = run_milestones(repo, "summary", path)
    assert result.returncode == 0, result.stderr
    assert result.stderr == b""
    return result.stdout.decode("utf-8")


def assert_refused(result, path):
    assert result.returncode == 1
    assert result.stdout == b""
    text = result.stderr.decode("utf-8")
    assert "Traceback" not in text
    lines = text.splitlines()
    assert len(lines) == 1
    assert lines[0].startswith("Error: ")
    assert path in lines[0]


def test_a_finished_summary_is_the_finish_date_then_the_body(seeded, make_commit, run_milestones):
    make_commit(
        seeded,
        "Milestone-finish: " + ALPHA,
        removed=removed_files(ALPHA),
        body="Alpha Work\n\n- built the alpha\n- documented it, with `code`\n",
        date="2026-03-04T22:30:00+01:00",
    )
    assert summary(run_milestones, seeded, ALPHA) == (
        "2026-03-04\nAlpha Work\n\n- built the alpha\n- documented it, with `code`\n"
    )


def test_the_finish_date_is_the_author_date_in_the_authors_own_zone(seeded, make_commit, run_milestones):
    make_commit(
        seeded,
        "Milestone-finish: " + ALPHA,
        removed=removed_files(ALPHA),
        body="Alpha Work\n\n- built\n",
        date="2026-03-04T23:30:00-05:00",
    )
    assert summary(run_milestones, seeded, ALPHA).splitlines()[0] == "2026-03-04"


def test_the_finish_bodys_outer_blank_lines_are_trimmed_and_its_trailer_dropped(seeded, make_commit, run_milestones):
    make_commit(
        seeded,
        "Milestone-finish: " + ALPHA,
        removed=removed_files(ALPHA),
        body=(
            "\n  \nAlpha Work\n\n- first  \n\n  - nested\n\n"
            "Co-Authored-By: Someone <someone@example.invalid>\nClaude-Session: https://example.invalid/s\n\n"
        ),
        date="2026-03-05T10:00:00+00:00",
    )
    assert summary(run_milestones, seeded, ALPHA) == "2026-03-05\nAlpha Work\n\n- first  \n\n  - nested\n"


def test_a_finish_with_no_body_prints_its_date_alone(seeded, make_commit, run_milestones):
    make_commit(
        seeded, "Milestone-finish: " + ALPHA, removed=removed_files(ALPHA), date="2026-03-06T10:00:00+00:00"
    )
    assert summary(run_milestones, seeded, ALPHA) == "2026-03-06\n"


def test_a_live_summary_is_the_word_live_the_title_and_the_goal_body(seeded, run_milestones):
    assert summary(run_milestones, seeded, ALPHA) == (
        "live\n"
        "Alpha Work\n"
        "\n"
        "Build the alpha, in two\n"
        "paragraphs.\n"
        "\n"
        "### A goal subsection\n"
        "\n"
        "  - an indented line\t\n"
    )


def test_the_live_summary_is_read_from_the_working_tree(seeded, run_milestones):
    (seeded / ALPHA / "requirements.md").write_bytes(b"# Revised Title\n\n## Goal\n\nThe revised goal.\n")
    assert summary(run_milestones, seeded, ALPHA) == "live\nRevised Title\n\nThe revised goal.\n"


@pytest.mark.parametrize(
    "requirements, printed",
    [
        (b"# Title Only\n", "live\nTitle Only\n"),
        (b"# Empty Goal\n\n## Goal\n\n\n## Decisions\n\n- x\n", "live\nEmpty Goal\n"),
        (b"## Goal\n\nNo heading above.\n", "live\n-\n\nNo heading above.\n"),
        (b"# T\n\n## Goals\n\nNot the section.\n", "live\nT\n"),
        (b"# T\n\n## Goal\n\nUp to the end.\n# Next\n\nAfter.\n", "live\nT\n\nUp to the end.\n"),
        (b"# T\r\n\r\n## Goal\r\n\r\nCRLF goal.\r\n", "live\nT\n\nCRLF goal.\n"),
    ],
)
def test_the_goal_body_runs_to_the_next_top_or_second_level_heading(repo, run_milestones, requirements, printed):
    seeded = repo({}, files=milestone_files(ALPHA, requirements))
    assert summary(run_milestones, seeded, ALPHA) == printed


def test_a_live_milestone_is_not_told_from_a_defined_or_started_one(seeded, make_commit, run_milestones):
    before = summary(run_milestones, seeded, ALPHA)
    make_commit(seeded, "Task-derivation: " + ALPHA, files={ALPHA + "TASKS_TODO.md": b"# TASKS TODO\n\n## A\n"})
    assert summary(run_milestones, seeded, ALPHA) == before


def test_a_reverted_finish_summarizes_as_live(seeded, make_commit, run_milestones, git, environment):
    commit = make_commit(
        seeded, "Milestone-finish: " + ALPHA, removed=removed_files(ALPHA), body="Alpha Work\n\n- built\n"
    )
    git(seeded, environment, "revert", "--no-edit", commit)
    assert summary(run_milestones, seeded, ALPHA).startswith("live\nAlpha Work\n\n")


def test_a_package_milestone_is_summarized(repo, make_commit, run_milestones):
    directory = "packages/api/milestones/rate-limits/"
    seeded = repo({}, files=milestone_files(directory))
    make_commit(
        seeded,
        "Milestone-finish: " + directory,
        removed=removed_files(directory),
        body="Rate Limits\n\n- limited\n",
        date="2026-03-07T10:00:00+00:00",
    )
    assert summary(run_milestones, seeded, directory) == "2026-03-07\nRate Limits\n\n- limited\n"


@pytest.mark.parametrize(
    "path",
    ["milestones/alpha", "./milestones/alpha/", "milestones/omega/", "milestones/", "milestones/alpha/requirements.md"],
)
def test_a_path_naming_no_milestone_is_refused(seeded, run_milestones, path):
    assert_refused(run_milestones(seeded, "summary", path), path)


def test_a_milestone_finished_under_a_legacy_id_subject_is_refused(seeded, make_commit, run_milestones):
    make_commit(seeded, "Milestone-finish: milestone_07_alpha", removed=removed_files(ALPHA), body="Alpha\n\n- x\n")
    assert_refused(run_milestones(seeded, "summary", ALPHA), ALPHA)


def test_a_requirements_file_outside_a_container_is_not_a_live_milestone(repo, run_milestones):
    seeded = repo({}, files=milestone_files("plans/alpha/"))
    assert_refused(run_milestones(seeded, "summary", "plans/alpha/"), "plans/alpha/")


def test_an_empty_milestone_path_is_refused(seeded, run_milestones):
    result = run_milestones(seeded, "summary", "")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.decode("utf-8").startswith("Error: ")
