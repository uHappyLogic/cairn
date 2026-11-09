"""The milestones tool's show query: one milestone's requirements.md printed whole and verbatim,
from the working tree when the milestone is live and, when it is finished, as the file stood at
its finish commit's parent, read with git show. The query takes MILESTONE_PATH alone, with no
FILE argument, its help saying the question document and the task list are served by no query,
and a path naming neither a live nor a finished milestone is refused on one Error line, as the
summary query refuses it. Every test runs on a repository seeded through the conftest factory,
then given finish-shaped commits made through the conftest helper."""

import pytest

ALPHA = "milestones/alpha/"
BETA = "milestones/beta/"
REQUIREMENTS = (
    b"# Alpha Work\n"
    b"\n"
    b"## Goal\n"
    b"\n"
    b"Build the alpha.\n"
    b"\n"
    b"## Relevant starting state\n"
    b"\n"
    b"  - an indented line\t\n"
    b"\n"
    b"## Decisions\n"
    b"\n"
    b"### The alpha\n"
    b"\n"
    b"- **Shape.** Round, with `code` and \xc3\xa9.\n"
    b"\n"
    b"## Out of Scope\n"
)
FINAL = REQUIREMENTS.replace(b"Round", b"Square")


def milestone_files(directory, requirements=REQUIREMENTS, questions=True):
    files = {
        directory + "requirements.md": requirements,
        directory + "TASKS_TODO.md": b"# TASKS TODO\n\n",
    }
    if questions:
        files[directory + "open_questions.xml"] = b"<open-questions/>\n"
    return files


@pytest.fixture
def seeded(repo):
    return repo({}, files={**milestone_files(ALPHA), **milestone_files(BETA, b"# Beta Work\n\n## Goal\n\nB.\n")})


def finish(make_commit, repository, directory, questions=True, date="2026-03-04T10:00:00+00:00"):
    removed = [directory + "requirements.md", directory + "TASKS_TODO.md"]
    if questions:
        removed.append(directory + "open_questions.xml")
    return make_commit(
        repository,
        "Milestone-finish: " + directory,
        removed=removed,
        body="Alpha Work\n\n- built the alpha\n",
        date=date,
    )


def show(run_milestones, repository, path):
    result = run_milestones(repository, "show", path)
    assert result.returncode == 0, result.stderr
    assert result.stderr == b""
    return result.stdout


def assert_refused(result, path):
    assert result.returncode == 1
    assert result.stdout == b""
    text = result.stderr.decode("utf-8")
    assert "Traceback" not in text
    lines = text.splitlines()
    assert len(lines) == 1
    assert lines[0].startswith("Error: ")
    assert path in lines[0]


def test_a_live_milestone_prints_its_requirements_whole_and_verbatim(seeded, run_milestones):
    assert show(run_milestones, seeded, ALPHA) == REQUIREMENTS


def test_a_live_milestone_is_read_from_the_working_tree(seeded, run_milestones):
    edited = b"# Revised\r\n\r\nno trailing newline"
    (seeded / ALPHA / "requirements.md").write_bytes(edited)
    assert show(run_milestones, seeded, ALPHA) == edited


def test_a_finished_milestone_prints_the_file_at_its_finish_commits_parent(seeded, make_commit, run_milestones):
    make_commit(seeded, "Recommendation-answer: Shape", files={ALPHA + "requirements.md": FINAL})
    finish(make_commit, seeded, ALPHA)
    assert not (seeded / ALPHA / "requirements.md").exists()
    assert show(run_milestones, seeded, ALPHA) == FINAL


def test_a_finished_milestone_whose_parent_holds_no_question_document_is_shown(repo, make_commit, run_milestones):
    seeded = repo({}, files=milestone_files(ALPHA, questions=False))
    finish(make_commit, seeded, ALPHA, questions=False)
    assert show(run_milestones, seeded, ALPHA) == REQUIREMENTS


def test_the_latest_finish_commit_is_the_one_read(seeded, make_commit, run_milestones, git, environment):
    first = finish(make_commit, seeded, ALPHA)
    git(seeded, environment, "revert", "--no-edit", first)
    make_commit(seeded, "Recommendation-answer: Shape", files={ALPHA + "requirements.md": FINAL})
    finish(make_commit, seeded, ALPHA, date="2026-03-05T10:00:00+00:00")
    assert show(run_milestones, seeded, ALPHA) == FINAL


def test_a_reverted_finish_shows_the_live_file(seeded, make_commit, run_milestones, git, environment):
    commit = finish(make_commit, seeded, ALPHA)
    git(seeded, environment, "revert", "--no-edit", commit)
    (seeded / ALPHA / "requirements.md").write_bytes(FINAL)
    assert show(run_milestones, seeded, ALPHA) == FINAL


def test_a_finished_package_milestone_is_shown(repo, make_commit, run_milestones):
    directory = "packages/api/milestones/rate-limits/"
    seeded = repo({}, files=milestone_files(directory))
    finish(make_commit, seeded, directory)
    assert show(run_milestones, seeded, directory) == REQUIREMENTS


def test_showing_a_finished_milestone_writes_nothing(seeded, make_commit, run_milestones, git, environment):
    finish(make_commit, seeded, ALPHA)
    before = (git(seeded, environment, "status", "--porcelain", "--ignored"), git(seeded, environment, "rev-parse", "HEAD"))
    show(run_milestones, seeded, ALPHA)
    after = (git(seeded, environment, "status", "--porcelain", "--ignored"), git(seeded, environment, "rev-parse", "HEAD"))
    assert after == before


@pytest.mark.parametrize(
    "path",
    ["milestones/alpha", "./milestones/alpha/", "milestones/omega/", "milestones/", "milestones/alpha/requirements.md"],
)
def test_a_path_naming_no_milestone_is_refused(seeded, run_milestones, path):
    assert_refused(run_milestones(seeded, "show", path), path)


def test_the_refusal_matches_the_summary_querys(seeded, run_milestones):
    shown = run_milestones(seeded, "show", "milestones/omega/")
    summarized = run_milestones(seeded, "summary", "milestones/omega/")
    assert shown.returncode == summarized.returncode == 1
    assert shown.stderr == summarized.stderr


def test_a_milestone_finished_under_a_legacy_id_subject_is_refused(seeded, make_commit, run_milestones):
    make_commit(
        seeded,
        "Milestone-finish: milestone_07_alpha",
        removed=[ALPHA + "requirements.md", ALPHA + "TASKS_TODO.md", ALPHA + "open_questions.xml"],
        body="Alpha\n\n- x\n",
    )
    assert_refused(run_milestones(seeded, "show", ALPHA), ALPHA)


def test_an_empty_milestone_path_is_refused(seeded, run_milestones):
    result = run_milestones(seeded, "show", "")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.decode("utf-8").startswith("Error: ")


def test_a_file_argument_is_refused_by_argparse(seeded, run_milestones):
    result = run_milestones(seeded, "show", ALPHA, "open_questions.xml")
    assert result.returncode == 2
    assert result.stdout == b""


def test_the_help_states_the_two_sources_and_the_files_no_query_serves(tmp_path, run_milestones):
    result = run_milestones(tmp_path, "show", "--help")
    assert result.returncode == 0
    text = " ".join(result.stdout.decode("utf-8").split())
    assert "MILESTONE_PATH" in text
    assert "requirements.md" in text
    assert "working tree" in text
    assert "finish commit's parent" in text
    assert "no FILE argument" in text
    assert "the question document and the task list are served by no query" in text
