"""The milestones tool's record query: for each milestone the milestones query lists for PATH,
in its order, that query's line verbatim at column 0, then beneath it every line indented by
four spaces: first the summary's last part (a finished milestone's bullets, a live one's goal
body; the summary's first line, title line, and the blank line after the title dropped), then
one tasks line, verbatim and with no bar, for each task commit that changed PATH and joins that
milestone. No blank line or separator stands between milestones, so the next column-0 line is
the next milestone; a milestone listed only because its scope overlaps PATH prints its line and
summary alone; and "record ." prints every milestone "milestones ." lists. Every test runs on a
repository seeded through the conftest factory, then given task and finish-shaped commits made
through the conftest helper."""

import pytest

ALPHA = "milestones/alpha/"
BETA = "milestones/beta/"
API = "packages/api/milestones/rate-limits/"
WEB = "packages/web/milestones/forms/"
TODO = b"# TASKS TODO\n\n"
INDENT = "    "


def milestone_files(directory, title, goal="The goal."):
    return {
        directory + "requirements.md": f"# {title}\n\n## Goal\n\n{goal}\n\n## Decisions\n".encode("utf-8"),
        directory + "TASKS_TODO.md": TODO,
        directory + "open_questions.xml": b"<open-questions/>\n",
    }


def finish(make_commit, repo, directory, body, date):
    removed = sorted(str(path.relative_to(repo)) for path in (repo / directory).rglob("*") if path.is_file())
    return make_commit(repo, "Milestone-finish: " + directory, removed=removed, body=body, date=date)


def query(run_milestones, repo, *args):
    result = run_milestones(repo, *args)
    assert result.returncode == 0, result.stderr
    assert result.stderr == b""
    return result.stdout.decode("utf-8")


@pytest.fixture
def worked(repo, make_commit):
    """Two root milestones and one project file: alpha finished with two tasks behind it, one of
    them barred and trailered, and beta live with one task, which also changed the file."""
    seeded = repo(
        {},
        files={
            **milestone_files(ALPHA, "Alpha Work"),
            **milestone_files(BETA, "Beta Work", goal="Build the beta,\nin two lines.\n\nAnd a paragraph."),
            "src/app.txt": b"one\n",
            "src/other.txt": b"one\n",
        },
    )
    make_commit(
        seeded,
        "Task-completion: First Alpha Task",
        files={ALPHA + "TASKS_TODO.md": TODO + b"\n", "src/app.txt": b"two\n"},
        body="- the bar\n\nCo-Authored-By: Someone <someone@example.invalid>\n",
        date="2026-03-01T10:00:00+00:00",
    )
    make_commit(
        seeded,
        "Task-completion: Second Alpha Task",
        files={ALPHA + "TASKS_TODO.md": TODO + b"\n\n", "src/other.txt": b"two\n"},
        body="- another bar\n",
        date="2026-03-02T10:00:00+00:00",
    )
    finish(
        make_commit,
        seeded,
        ALPHA,
        "Alpha Work\n\n- built the alpha\n- documented it\n\nCo-Authored-By: Someone <someone@example.invalid>\n",
        "2026-03-03T10:00:00+00:00",
    )
    make_commit(
        seeded,
        "Task-completion: A Beta Task",
        files={BETA + "TASKS_TODO.md": TODO + b"\n", "src/app.txt": b"three\n"},
        body="- the beta bar\n",
        date="2026-03-04T10:00:00+00:00",
    )
    return seeded


def test_each_milestone_opens_with_its_milestones_line_and_nests_its_summary_and_tasks(worked, run_milestones):
    tasks = query(run_milestones, worked, "tasks", ".").splitlines(keepends=True)
    assert query(run_milestones, worked, "record", ".") == (
        f"live\t-\t{BETA}\tBeta Work\n"
        f"{INDENT}Build the beta,\n"
        f"{INDENT}in two lines.\n"
        f"{INDENT}\n"
        f"{INDENT}And a paragraph.\n"
        f"{INDENT}{tasks[0]}"
        f"finished\t2026-03-03\t{ALPHA}\tAlpha Work\n"
        f"{INDENT}- built the alpha\n"
        f"{INDENT}- documented it\n"
        f"{INDENT}{tasks[1]}"
        f"{INDENT}{tasks[2]}"
    )
    assert [line.split("\t")[3] for line in tasks] == ["A Beta Task\n", "Second Alpha Task\n", "First Alpha Task\n"]


def test_every_column_zero_line_is_a_milestones_line_verbatim(worked, run_milestones):
    printed = query(run_milestones, worked, "record", ".").splitlines(keepends=True)
    headers = [line for line in printed if not line.startswith(INDENT)]
    assert "".join(headers) == query(run_milestones, worked, "milestones", ".")
    assert all(line.strip() or line == INDENT + "\n" for line in printed)
    assert "\n\n" not in "".join(printed)


def test_task_lines_carry_no_bar(worked, run_milestones):
    printed = query(run_milestones, worked, "record", ".")
    assert "the bar" not in printed
    assert "another bar" not in printed
    assert "Co-Authored-By" not in printed


def test_only_the_tasks_that_changed_path_are_printed(worked, run_milestones):
    tasks = query(run_milestones, worked, "tasks", "src/app.txt").splitlines(keepends=True)
    assert [line.split("\t")[3] for line in tasks] == ["A Beta Task\n", "First Alpha Task\n"]
    assert query(run_milestones, worked, "record", "src/app.txt") == (
        f"live\t-\t{BETA}\tBeta Work\n"
        f"{INDENT}Build the beta,\n"
        f"{INDENT}in two lines.\n"
        f"{INDENT}\n"
        f"{INDENT}And a paragraph.\n"
        f"{INDENT}{tasks[0]}"
        f"finished\t2026-03-03\t{ALPHA}\tAlpha Work\n"
        f"{INDENT}- built the alpha\n"
        f"{INDENT}- documented it\n"
        f"{INDENT}{tasks[1]}"
    )


def test_a_milestone_listed_by_scope_alone_prints_its_line_and_summary_alone(worked, run_milestones):
    (worked / "src" / "new.txt").write_bytes(b"untracked\n")
    assert query(run_milestones, worked, "record", "src/new.txt") == (
        f"live\t-\t{BETA}\tBeta Work\n"
        f"{INDENT}Build the beta,\n"
        f"{INDENT}in two lines.\n"
        f"{INDENT}\n"
        f"{INDENT}And a paragraph.\n"
        f"finished\t2026-03-03\t{ALPHA}\tAlpha Work\n"
        f"{INDENT}- built the alpha\n"
        f"{INDENT}- documented it\n"
    )


def test_a_finish_body_without_its_blank_line_still_drops_only_the_title(repo, make_commit, run_milestones):
    seeded = repo({}, files=milestone_files(ALPHA, "Alpha Work"))
    finish(make_commit, seeded, ALPHA, "Alpha Work\n- built\n", "2026-03-01T10:00:00+00:00")
    assert query(run_milestones, seeded, "record", ".") == (
        f"finished\t2026-03-01\t{ALPHA}\tAlpha Work\n{INDENT}- built\n"
    )


def test_a_finish_with_no_bullets_and_a_goalless_live_milestone_print_their_lines_alone(
    repo, make_commit, run_milestones
):
    seeded = repo(
        {},
        files={
            **milestone_files(ALPHA, "Alpha Work"),
            BETA + "requirements.md": b"# Beta Work\n",
        },
    )
    finish(make_commit, seeded, ALPHA, "Alpha Work\n", "2026-03-01T10:00:00+00:00")
    assert query(run_milestones, seeded, "record", ".") == (
        f"live\t-\t{BETA}\tBeta Work\nfinished\t2026-03-01\t{ALPHA}\tAlpha Work\n"
    )


def test_a_task_that_changed_path_nests_under_the_milestone_it_joins_outside_paths_scope(
    repo, make_commit, run_milestones
):
    seeded = repo({}, files={**milestone_files(API, "Rate Limits"), **milestone_files(WEB, "Forms")})
    make_commit(
        seeded,
        "Task-completion: Limit The Forms",
        files={API + "TASKS_TODO.md": TODO + b"\n", WEB + "requirements.md": b"# Forms\n\n## Goal\n\nLimited.\n"},
    )
    task = query(run_milestones, seeded, "tasks", WEB)
    assert task.endswith(f"\t{API}\tLimit The Forms\n")
    assert query(run_milestones, seeded, "record", WEB) == (
        f"live\t-\t{API}\tRate Limits\n"
        f"{INDENT}The goal.\n"
        f"{INDENT}{task}"
        f"live\t-\t{WEB}\tForms\n"
        f"{INDENT}Limited.\n"
    )


def test_record_dot_prints_every_milestone_milestones_dot_lists(repo, make_commit, run_milestones):
    files = {"docs/guide.md": b"guide\n"}
    for directory, title in ((ALPHA, "Root"), (API, "Rate Limits"), (WEB, "Forms")):
        files.update(milestone_files(directory, title))
    seeded = repo({}, files=files)
    finish(make_commit, seeded, WEB, "Forms\n\n- formed\n", "2026-03-01T10:00:00+00:00")
    listed = query(run_milestones, seeded, "milestones", ".")
    assert len(listed.splitlines()) == 3
    headers = [line for line in query(run_milestones, seeded, "record", ".").splitlines(keepends=True) if line[0] != " "]
    assert "".join(headers) == listed


def test_a_path_neither_present_nor_ever_changed_is_refused(worked, run_milestones):
    result = run_milestones(worked, "record", "src/missing.txt")
    assert result.returncode == 1
    assert result.stdout == b""
    lines = result.stderr.decode("utf-8").splitlines()
    assert len(lines) == 1
    assert lines[0].startswith("Error: ")
    assert "src/missing.txt" in lines[0]


def test_an_empty_path_is_refused(worked, run_milestones):
    result = run_milestones(worked, "record", "")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.decode("utf-8").startswith("Error: ")
