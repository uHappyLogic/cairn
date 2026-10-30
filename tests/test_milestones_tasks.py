"""The milestones tool's tasks query, its line and its selection: one line per Task-completion:
commit that changed PATH, four tab-separated fields (%h, the author date as YYYY-MM-DD, the
milestone joined from the commit's root-anchored milestones/*/TASKS_TODO.md, the title after the
marker), newest first by author timestamp sorted after the read, with one fixed placeholder in
the milestone field when the commit's file list holds no matching task list or more than one.
Every test runs on a repository seeded through the conftest factory with two fixture
milestones and one project file, then given commits made through the conftest helper."""

import pytest

FIRST = "milestones/milestone_07_first/"
SECOND = "milestones/milestone_08_second/"
PROJECT_FILE = "src/app.txt"
NO_MILESTONE = "-"


@pytest.fixture
def seeded(repo):
    """The repository both fixture milestones and the project file are seeded into."""
    return repo(
        {FIRST: "parallel_first", SECOND: "parallel_second"},
        files={PROJECT_FILE: b"one\n", "README.md": b"# A project\n"},
    )


def short_hash(git, repo, environment, commit):
    return git(repo, environment, "log", "-1", "--format=%h", commit).strip()


def tasks(run_milestones, repo, *args):
    result = run_milestones(repo, "tasks", *args)
    assert result.returncode == 0, result.stderr
    assert result.stderr == b""
    return result.stdout.decode("utf-8")


def test_a_task_line_is_hash_date_milestone_and_title_tab_separated(
    seeded, make_commit, run_milestones, git, environment
):
    commit = make_commit(
        seeded,
        "Task-completion: Add The Widget",
        files={FIRST + "TASKS_TODO.md": b"# TASKS TODO\n\n", PROJECT_FILE: b"two\n"},
        date="2026-03-04T22:30:00+01:00",
    )
    printed = tasks(run_milestones, seeded, FIRST)
    assert printed == f"{short_hash(git, seeded, environment, commit)}\t2026-03-04\t{FIRST}\tAdd The Widget\n"


def test_the_date_is_the_author_date_in_the_authors_own_zone(seeded, make_commit, run_milestones):
    make_commit(
        seeded,
        "Task-completion: Late Night Task",
        files={FIRST + "TASKS_TODO.md": b"# TASKS TODO\n\n"},
        date="2026-03-04T23:30:00-05:00",
    )
    fields = tasks(run_milestones, seeded, FIRST).rstrip("\n").split("\t")
    assert fields[1] == "2026-03-04"


def test_the_title_keeps_its_own_spacing_and_punctuation(seeded, make_commit, run_milestones):
    make_commit(
        seeded,
        'Task-completion: Read A/B "Quoted"  Title',
        files={FIRST + "TASKS_TODO.md": b"# TASKS TODO\n\n"},
    )
    fields = tasks(run_milestones, seeded, FIRST).rstrip("\n").split("\t")
    assert len(fields) == 4
    assert fields[3] == 'Read A/B "Quoted"  Title'


def test_lines_are_newest_first_by_author_date_whatever_the_commit_order(seeded, make_commit, run_milestones):
    todo = FIRST + "TASKS_TODO.md"
    make_commit(seeded, "Task-completion: Third Authored", files={todo: b"a\n"}, date="2026-01-03T12:00:00+00:00")
    make_commit(seeded, "Task-completion: First Authored", files={todo: b"b\n"}, date="2026-01-01T12:00:00+00:00")
    make_commit(seeded, "Task-completion: Second Authored", files={todo: b"c\n"}, date="2026-01-02T12:00:00+00:00")
    lines = tasks(run_milestones, seeded, FIRST).splitlines()
    assert [line.split("\t")[3] for line in lines] == ["Third Authored", "Second Authored", "First Authored"]
    assert [line.split("\t")[1] for line in lines] == ["2026-01-03", "2026-01-02", "2026-01-01"]


def test_the_sort_key_is_the_author_timestamp(seeded, make_commit, run_milestones):
    # Later Instant is committed first and printed with the earlier day, so neither git's order
    # nor a sort of the printed day would put it first.
    todo = FIRST + "TASKS_TODO.md"
    make_commit(seeded, "Task-completion: Later Instant", files={todo: b"a\n"}, date="2026-01-01T23:00:00-05:00")
    make_commit(seeded, "Task-completion: Earlier Instant", files={todo: b"b\n"}, date="2026-01-02T01:00:00+05:00")
    lines = tasks(run_milestones, seeded, FIRST).splitlines()
    assert [line.split("\t")[3] for line in lines] == ["Later Instant", "Earlier Instant"]


def test_commits_sharing_an_author_timestamp_keep_the_logs_order(seeded, make_commit, run_milestones):
    todo = FIRST + "TASKS_TODO.md"
    same = "2026-01-05T09:00:00+00:00"
    make_commit(seeded, "Task-completion: Made First", files={todo: b"a\n"}, date=same)
    make_commit(seeded, "Task-completion: Made Second", files={todo: b"b\n"}, date=same)
    lines = tasks(run_milestones, seeded, FIRST).splitlines()
    assert [line.split("\t")[3] for line in lines] == ["Made Second", "Made First"]


def test_only_task_completion_subjects_are_listed(seeded, make_commit, run_milestones):
    todo = FIRST + "TASKS_TODO.md"
    make_commit(seeded, "Task-derivation: milestone_07_first", files={todo: b"a\n"})
    make_commit(
        seeded,
        "Tasklist-completion: complete one milestone task",
        files={todo: b"b\n"},
        body="Task-completion: A Legacy Heading",
    )
    make_commit(seeded, "Task-completion: The One Task", files={todo: b"c\n"})
    make_commit(seeded, "Recommendation-answer: Task-completion: Not A Task", files={todo: b"d\n"})
    make_commit(seeded, "task-completion: Wrong Case", files={todo: b"e\n"})
    lines = tasks(run_milestones, seeded, FIRST).splitlines()
    assert [line.split("\t")[3] for line in lines] == ["The One Task"]


def test_only_commits_that_changed_the_path_are_listed(seeded, make_commit, run_milestones):
    make_commit(seeded, "Task-completion: First Milestone Task", files={FIRST + "TASKS_TODO.md": b"a\n"})
    make_commit(seeded, "Task-completion: Second Milestone Task", files={SECOND + "TASKS_TODO.md": b"b\n"})
    assert [line.split("\t")[3] for line in tasks(run_milestones, seeded, FIRST).splitlines()] == [
        "First Milestone Task"
    ]
    assert [line.split("\t")[3] for line in tasks(run_milestones, seeded, SECOND).splitlines()] == [
        "Second Milestone Task"
    ]
    assert [line.split("\t")[3] for line in tasks(run_milestones, seeded, "milestones").splitlines()] == [
        "Second Milestone Task",
        "First Milestone Task",
    ]


def test_a_project_path_joins_each_task_to_its_milestone(seeded, make_commit, run_milestones):
    make_commit(
        seeded,
        "Task-completion: Edit The App",
        files={SECOND + "TASKS_TODO.md": b"a\n", PROJECT_FILE: b"two\n"},
    )
    make_commit(seeded, "Task-completion: Leave The App", files={FIRST + "TASKS_TODO.md": b"b\n"})
    lines = tasks(run_milestones, seeded, PROJECT_FILE).splitlines()
    assert [line.split("\t")[2:] for line in lines] == [[SECOND, "Edit The App"]]


def test_a_deleted_path_still_lists_the_tasks_that_changed_it(seeded, make_commit, run_milestones):
    make_commit(
        seeded,
        "Task-completion: Remove The App",
        files={FIRST + "TASKS_TODO.md": b"a\n"},
        removed=(PROJECT_FILE,),
    )
    lines = tasks(run_milestones, seeded, PROJECT_FILE).splitlines()
    assert [line.split("\t")[2:] for line in lines] == [[FIRST, "Remove The App"]]


def test_a_commit_with_no_task_list_gets_the_placeholder(seeded, make_commit, run_milestones):
    make_commit(seeded, "Task-completion: Hand Made", files={PROJECT_FILE: b"two\n"})
    lines = tasks(run_milestones, seeded, PROJECT_FILE).splitlines()
    assert [line.split("\t")[2:] for line in lines] == [[NO_MILESTONE, "Hand Made"]]


def test_a_commit_with_two_task_lists_gets_the_placeholder(seeded, make_commit, run_milestones):
    make_commit(
        seeded,
        "Task-completion: Two Lists At Once",
        files={FIRST + "TASKS_TODO.md": b"a\n", SECOND + "TASKS_TODO.md": b"b\n"},
    )
    for path in (FIRST, SECOND):
        lines = tasks(run_milestones, seeded, path).splitlines()
        assert [line.split("\t")[2:] for line in lines] == [[NO_MILESTONE, "Two Lists At Once"]]


def test_the_join_pattern_is_anchored_at_the_repository_root(seeded, make_commit, run_milestones):
    make_commit(
        seeded,
        "Task-completion: Also Edits A Fixture List",
        files={
            FIRST + "TASKS_TODO.md": b"a\n",
            "tests/fixtures/milestones/fixture/TASKS_TODO.md": b"b\n",
            "tests/fixtures/sample/TASKS_TODO.md": b"c\n",
            "milestones/milestone_07_first/nested/TASKS_TODO.md": b"d\n",
        },
    )
    lines = tasks(run_milestones, seeded, FIRST).splitlines()
    assert [line.split("\t")[2:] for line in lines] == [[FIRST, "Also Edits A Fixture List"]]


def test_a_nested_or_unanchored_task_list_alone_gets_the_placeholder(seeded, make_commit, run_milestones):
    make_commit(
        seeded,
        "Task-completion: Only A Fixture List",
        files={"tests/fixtures/sample/TASKS_TODO.md": b"c\n"},
    )
    lines = tasks(run_milestones, seeded, "tests").splitlines()
    assert [line.split("\t")[2:] for line in lines] == [[NO_MILESTONE, "Only A Fixture List"]]


def test_a_removed_task_list_still_joins_its_milestone(seeded, make_commit, run_milestones):
    make_commit(seeded, "Task-completion: Drop The List", removed=(FIRST + "TASKS_TODO.md",))
    lines = tasks(run_milestones, seeded, FIRST).splitlines()
    assert [line.split("\t")[2:] for line in lines] == [[FIRST, "Drop The List"]]


def test_a_path_holding_a_glob_character_is_read_literally(seeded, make_commit, run_milestones):
    make_commit(seeded, "Task-completion: Star File", files={"src/a*.txt": b"x\n", FIRST + "TASKS_TODO.md": b"a\n"})
    make_commit(seeded, "Task-completion: Plain File", files={"src/ab.txt": b"y\n", FIRST + "TASKS_TODO.md": b"b\n"})
    lines = tasks(run_milestones, seeded, "src/a*.txt").splitlines()
    assert [line.split("\t")[3] for line in lines] == ["Star File"]


def test_merge_commits_are_never_listed(seeded, make_commit, run_milestones, git, environment):
    git(seeded, environment, "checkout", "-q", "-b", "side")
    make_commit(seeded, "Task-completion: On The Side", files={FIRST + "TASKS_TODO.md": b"a\n"})
    git(seeded, environment, "checkout", "-q", "-")
    make_commit(seeded, "Task-completion: On The Main Line", files={SECOND + "TASKS_TODO.md": b"b\n"})
    git(seeded, environment, "merge", "-q", "--no-ff", "-m", "Task-completion: A Merge", "side")
    lines = tasks(run_milestones, seeded, "milestones").splitlines()
    assert sorted(line.split("\t")[3] for line in lines) == ["On The Main Line", "On The Side"]
