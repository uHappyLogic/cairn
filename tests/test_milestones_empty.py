"""The milestones tool's tasks query on an empty result: when no task commit changed PATH it
prints nothing and exits 0 for a PATH present in the working tree or changed by any commit, and
refuses with one Error line naming PATH as given and exit 1 for a PATH that is neither. Every
test runs on a repository seeded through the conftest factory."""

import pytest

FIRST = "milestones/milestone_07_first/"


@pytest.fixture
def seeded(repo):
    return repo({FIRST: "parallel_first"}, files={"src/app.txt": b"one\n"})


def assert_empty(result):
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def assert_refused(result, path):
    assert result.returncode == 1
    assert result.stdout == b""
    lines = result.stderr.decode("utf-8").splitlines()
    assert len(lines) == 1
    assert lines[0].startswith("Error: ")
    assert path in lines[0]
    assert "Traceback" not in result.stderr.decode("utf-8")


def test_a_milestone_with_no_completed_task_prints_nothing(seeded, run_milestones):
    assert_empty(run_milestones(seeded, "tasks", FIRST))
    assert_empty(run_milestones(seeded, "tasks", FIRST, "--with-body"))


def test_a_milestone_whose_only_commits_are_not_task_commits_prints_nothing(seeded, make_commit, run_milestones):
    make_commit(seeded, "Task-derivation: milestone_07_first", files={FIRST + "TASKS_TODO.md": b"a\n"})
    make_commit(
        seeded,
        "Tasklist-completion: complete one milestone task",
        files={FIRST + "TASKS_TODO.md": b"b\n"},
        body="Legacy Heading",
    )
    assert_empty(run_milestones(seeded, "tasks", FIRST, "--with-body"))


def test_a_path_present_only_in_the_working_tree_prints_nothing(seeded, run_milestones):
    (seeded / "untracked").mkdir()
    (seeded / "untracked" / "new.txt").write_bytes(b"new\n")
    assert_empty(run_milestones(seeded, "tasks", "untracked/new.txt"))
    assert_empty(run_milestones(seeded, "tasks", "untracked"))


def test_a_path_changed_only_by_history_prints_nothing(seeded, make_commit, run_milestones):
    make_commit(seeded, "Chore: drop the app", removed=("src/app.txt",))
    assert not (seeded / "src" / "app.txt").exists()
    assert_empty(run_milestones(seeded, "tasks", "src/app.txt"))


def test_a_removed_milestone_directory_whose_task_commits_remain_is_listed(seeded, make_commit, run_milestones):
    make_commit(seeded, "Task-completion: The Only Task", files={FIRST + "TASKS_TODO.md": b"a\n"})
    make_commit(seeded, "Milestone-finish: milestone_07_first", removed=(FIRST + "TASKS_TODO.md",))
    result = run_milestones(seeded, "tasks", FIRST)
    assert result.returncode == 0, result.stderr
    assert result.stdout.decode("utf-8").endswith("\tThe Only Task\n")


def test_a_path_neither_present_nor_ever_changed_is_refused(seeded, run_milestones):
    path = "milestones/milestone_99_mistyped/"
    assert_refused(run_milestones(seeded, "tasks", path), path)
    assert_refused(run_milestones(seeded, "tasks", path, "--with-body"), path)
