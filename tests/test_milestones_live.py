"""The milestones tool's live query: one line per live milestone, ordered by path, each three
tab-separated fields (the milestone path with its trailing slash, "started" or "defined" by the
path-scoped git log -1 --diff-filter=M test on its TASKS_TODO.md, and the title from the first
"# " heading of its requirements.md, any legacy "Milestone <N>: " prefix stripped, "-" when it
has none), a live milestone being the directory of a tracked file matching the discovery
pattern **/milestones/*/requirements.md that is present in the working tree. Given no argument
the query prints every live milestone, and nothing, exiting 0, when no milestone is live; its
MILESTONE_PATH filter is pinned in test_milestones_live_filter.py. Every test runs on a
repository seeded through the conftest factory, then given commits made through the conftest
helper."""

import pytest

ALPHA = "milestones/alpha/"
BETA = "milestones/beta/"
REQUIREMENTS = b"# Alpha Work\n\n## Goal\n\nBuild the alpha.\n"
TODO = b"# TASKS TODO\n\n"


def milestone_files(directory, title="Alpha Work", todo=True):
    files = {directory + "requirements.md": f"# {title}\n\n## Goal\n\nThe goal.\n".encode("utf-8")}
    if todo:
        files[directory + "TASKS_TODO.md"] = TODO
    return files


def live(run_milestones, repo):
    result = run_milestones(repo, "live")
    assert result.returncode == 0, result.stderr
    assert result.stderr == b""
    return result.stdout.decode("utf-8")


def test_a_line_is_path_state_and_title_tab_separated(repo, run_milestones):
    seeded = repo({}, files={ALPHA + "requirements.md": REQUIREMENTS, ALPHA + "TASKS_TODO.md": TODO})
    assert live(run_milestones, seeded) == f"{ALPHA}\tdefined\tAlpha Work\n"


def test_a_task_list_modified_after_the_commit_adding_it_reads_started(repo, make_commit, run_milestones):
    seeded = repo({}, files={**milestone_files(ALPHA), **milestone_files(BETA, "Beta Work")})
    make_commit(seeded, "Task-derivation: milestones/alpha/", files={ALPHA + "TASKS_TODO.md": TODO + b"## A Task\n"})
    assert live(run_milestones, seeded) == f"{ALPHA}\tstarted\tAlpha Work\n{BETA}\tdefined\tBeta Work\n"


def test_a_milestone_added_by_a_later_commit_still_reads_defined(repo, make_commit, run_milestones):
    seeded = repo({}, files={"README.md": b"# A project\n"})
    make_commit(seeded, "Milestone-definition: milestones/alpha/", files=milestone_files(ALPHA))
    assert live(run_milestones, seeded) == f"{ALPHA}\tdefined\tAlpha Work\n"


def test_a_commit_changing_only_other_files_starts_nothing(repo, make_commit, run_milestones):
    seeded = repo({}, files={**milestone_files(ALPHA), **milestone_files(BETA, "Beta Work")})
    make_commit(
        seeded,
        "Requirements-review: milestones/alpha/",
        files={ALPHA + "requirements.md": REQUIREMENTS + b"\n## Decisions\n", "src/app.txt": b"one\n"},
    )
    make_commit(seeded, "Task-derivation: milestones/beta/", files={BETA + "TASKS_TODO.md": TODO + b"## B Task\n"})
    assert live(run_milestones, seeded) == f"{ALPHA}\tdefined\tAlpha Work\n{BETA}\tstarted\tBeta Work\n"


def test_a_milestone_with_no_task_list_reads_defined(repo, run_milestones):
    seeded = repo({}, files=milestone_files(ALPHA, todo=False))
    assert live(run_milestones, seeded) == f"{ALPHA}\tdefined\tAlpha Work\n"


@pytest.mark.parametrize(
    "directory",
    [
        "milestones/alpha/",
        "pkg/milestones/alpha/",
        "packages/api/milestones/rate limits/",
        "a/milestones/b/milestones/c/",
    ],
)
def test_the_discovery_pattern_matches_a_container_at_any_depth(repo, run_milestones, directory):
    seeded = repo({}, files=milestone_files(directory))
    assert live(run_milestones, seeded) == f"{directory}\tdefined\tAlpha Work\n"


@pytest.mark.parametrize(
    "name",
    [
        "milestones/requirements.md",
        "milestones/alpha/nested/requirements.md",
        "milestones.fixture/alpha/requirements.md",
        "my-milestones/alpha/requirements.md",
        "Milestones/alpha/requirements.md",
        "milestones/alpha/requirements.md.bak",
        "milestones/alpha/README.md",
    ],
)
def test_a_path_outside_the_discovery_pattern_is_not_a_milestone(repo, run_milestones, name):
    seeded = repo({}, files={name: REQUIREMENTS})
    assert live(run_milestones, seeded) == ""


def test_lines_are_ordered_by_path(repo, run_milestones):
    directories = ["pkg/milestones/zeta/", "milestones/beta/", "milestones/alpha/", "docs/milestones/gamma/"]
    files = {}
    for directory in directories:
        files.update(milestone_files(directory))
    seeded = repo({}, files=files)
    printed = [line.split("\t")[0] for line in live(run_milestones, seeded).splitlines()]
    assert printed == sorted(directories)


def test_an_untracked_requirements_file_is_not_live(repo, run_milestones):
    seeded = repo({}, files=milestone_files(ALPHA))
    (seeded / "milestones" / "beta").mkdir()
    (seeded / "milestones" / "beta" / "requirements.md").write_bytes(b"# Beta Work\n")
    assert live(run_milestones, seeded) == f"{ALPHA}\tdefined\tAlpha Work\n"


def test_a_tracked_requirements_file_missing_from_the_working_tree_is_not_live(repo, run_milestones):
    seeded = repo({}, files={**milestone_files(ALPHA), **milestone_files(BETA, "Beta Work")})
    (seeded / "milestones" / "beta" / "requirements.md").unlink()
    assert live(run_milestones, seeded) == f"{ALPHA}\tdefined\tAlpha Work\n"


def test_a_removed_milestone_is_not_live_though_its_task_commits_remain(repo, make_commit, run_milestones):
    seeded = repo({}, files={**milestone_files(ALPHA), **milestone_files(BETA, "Beta Work")})
    make_commit(seeded, "Task-completion: A Task", files={BETA + "TASKS_TODO.md": TODO + b"\n"})
    make_commit(
        seeded, "Milestone-finish: milestones/beta/", removed=(BETA + "requirements.md", BETA + "TASKS_TODO.md")
    )
    assert live(run_milestones, seeded) == f"{ALPHA}\tdefined\tAlpha Work\n"
    tasks = run_milestones(seeded, "tasks", BETA)
    assert tasks.returncode == 0, tasks.stderr


@pytest.mark.parametrize(
    "heading, title",
    [
        ("# Milestone 54: Milestones addressed by path", "Milestones addressed by path"),
        ("# Milestone 7: Golden sweep fixture", "Golden sweep fixture"),
        ("# Milestones addressed by path", "Milestones addressed by path"),
        ("# Milestone planning", "Milestone planning"),
        ("# Spaced \t title  here ", "Spaced title here"),
        ("# ", "-"),
        ("## Goal", "-"),
    ],
)
def test_the_title_is_the_first_heading_with_any_legacy_prefix_stripped(repo, run_milestones, heading, title):
    seeded = repo({}, files={ALPHA + "requirements.md": f"{heading}\n\n## Goal\n\nThe goal.\n".encode("utf-8")})
    assert live(run_milestones, seeded) == f"{ALPHA}\tdefined\t{title}\n"


def test_the_title_comes_from_the_first_top_level_heading_of_the_working_tree_file(repo, run_milestones):
    seeded = repo({}, files={ALPHA + "requirements.md": b"Preamble line\n\n## Goal\n\n# First Title\n\n# Second\n"})
    assert live(run_milestones, seeded) == f"{ALPHA}\tdefined\tFirst Title\n"
    (seeded / "milestones" / "alpha" / "requirements.md").write_bytes(b"# Edited Title\n")
    assert live(run_milestones, seeded) == f"{ALPHA}\tdefined\tEdited Title\n"


def test_a_requirements_file_with_no_heading_gets_the_placeholder_title(repo, run_milestones):
    seeded = repo({}, files={ALPHA + "requirements.md": b"No heading at all.\n"})
    assert live(run_milestones, seeded) == f"{ALPHA}\tdefined\t-\n"


def test_no_live_milestone_prints_nothing(repo, run_milestones):
    seeded = repo({}, files={"README.md": b"# A project\n", "milestones/answer_decision_principles.md": b"# P\n"})
    result = run_milestones(seeded, "live")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
