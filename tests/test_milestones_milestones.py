"""The milestones tool's milestones query: one line per milestone, live or finished, that changed
PATH through a task commit or whose scope (the directory holding its milestones/ container)
contains PATH or lies under it, each four tab-separated fields (the state, "live" or
"finished"; the finish commit's author date as YYYY-MM-DD, "-" for a live milestone; the path
with its trailing slash; the title, read as the live query reads it for a live milestone and
from the first line of the finish commit's body for a finished one), every live line above
every finished one, the live lines by path and the finished lines newest first by the finish
commit's author timestamp. A finished milestone is a milestone path that is not live and that
a Milestone-finish: <path> subject names, so presence wins over the log and a legacy subject
naming an id is not read. Every test runs on a repository seeded through the conftest factory,
then given finish-shaped commits (the directory removed, the subject naming its path, the body
its title line, a blank line, and its bullets) made through the conftest helper."""

import pytest

ALPHA = "milestones/alpha/"
BETA = "milestones/beta/"
GAMMA = "milestones/gamma/"
API = "packages/api/milestones/rate-limits/"
WEB = "packages/web/milestones/forms/"
TODO = b"# TASKS TODO\n\n"


def milestone_files(directory, title):
    return {
        directory + "requirements.md": f"# {title}\n\n## Goal\n\nThe goal of {title}.\n".encode("utf-8"),
        directory + "TASKS_TODO.md": TODO,
        directory + "open_questions.xml": b"<open-questions/>\n",
    }


def finish(make_commit, repo, directory, title, bullets=("- built it",), date=None, trailer=None):
    """Make the finish-shaped commit for a milestone: its directory removed, the subject naming
    its path, the body its title line, a blank line, and its bullets, with an optional trailer
    paragraph after them."""
    removed = sorted(
        str(path.relative_to(repo)) for path in (repo / directory).rglob("*") if path.is_file()
    )
    body = title + "\n\n" + "\n".join(bullets) + "\n"
    if trailer is not None:
        body += "\n" + trailer + "\n"
    return make_commit(repo, "Milestone-finish: " + directory, removed=removed, body=body, date=date)


def milestones(run_milestones, repo, path="."):
    result = run_milestones(repo, "milestones", path)
    assert result.returncode == 0, result.stderr
    assert result.stderr == b""
    return result.stdout.decode("utf-8")


@pytest.fixture
def three(repo):
    files = {"README.md": b"# A project\n", "src/app.txt": b"one\n"}
    for directory, title in ((ALPHA, "Alpha Work"), (BETA, "Beta Work"), (GAMMA, "Gamma Work")):
        files.update(milestone_files(directory, title))
    return repo({}, files=files)


def test_a_finished_line_is_state_date_path_and_title_tab_separated(three, make_commit, run_milestones):
    finish(make_commit, three, ALPHA, "Alpha Work", date="2026-03-04T22:30:00+01:00")
    lines = milestones(run_milestones, three).splitlines()
    assert lines[-1] == f"finished\t2026-03-04\t{ALPHA}\tAlpha Work"


def test_a_live_line_carries_the_placeholder_date_and_the_heading_title(three, run_milestones):
    assert milestones(run_milestones, three) == (
        f"live\t-\t{ALPHA}\tAlpha Work\nlive\t-\t{BETA}\tBeta Work\nlive\t-\t{GAMMA}\tGamma Work\n"
    )


def test_the_finish_date_is_the_author_date_in_the_authors_own_zone(three, make_commit, run_milestones):
    finish(make_commit, three, BETA, "Beta Work", date="2026-03-04T23:30:00-05:00")
    assert f"finished\t2026-03-04\t{BETA}\tBeta Work\n" in milestones(run_milestones, three)


def test_every_live_line_stands_above_every_finished_one(three, make_commit, run_milestones):
    finish(make_commit, three, BETA, "Beta Work", date="2026-03-01T10:00:00+00:00")
    finish(make_commit, three, GAMMA, "Gamma Work", date="2026-03-02T10:00:00+00:00")
    states = [line.split("\t")[0] for line in milestones(run_milestones, three).splitlines()]
    assert states == ["live", "finished", "finished"]


def test_finished_lines_are_newest_first_by_author_date_whatever_the_commit_order(
    three, make_commit, run_milestones
):
    finish(make_commit, three, ALPHA, "Alpha Work", date="2026-03-05T10:00:00+00:00")
    finish(make_commit, three, BETA, "Beta Work", date="2026-03-01T10:00:00+00:00")
    finish(make_commit, three, GAMMA, "Gamma Work", date="2026-03-03T10:00:00+00:00")
    paths = [line.split("\t")[2] for line in milestones(run_milestones, three).splitlines()]
    assert paths == [ALPHA, GAMMA, BETA]


def test_the_finish_sort_key_is_the_author_timestamp_not_the_printed_day(three, make_commit, run_milestones):
    finish(make_commit, three, ALPHA, "Alpha Work", date="2026-03-05T01:00:00+05:00")
    finish(make_commit, three, BETA, "Beta Work", date="2026-03-04T23:00:00-05:00")
    paths = [line.split("\t")[2] for line in milestones(run_milestones, three).splitlines()]
    assert paths == [GAMMA, BETA, ALPHA]


def test_live_lines_are_ordered_by_path(repo, run_milestones):
    files = {}
    for directory in ("pkg/milestones/zeta/", "milestones/beta/", "milestones/alpha/", "docs/milestones/gamma/"):
        files.update(milestone_files(directory, "Work"))
    seeded = repo({}, files=files)
    paths = [line.split("\t")[2] for line in milestones(run_milestones, seeded).splitlines()]
    assert paths == sorted(paths)
    assert len(paths) == 4


def test_the_finished_title_is_the_first_body_line_with_whitespace_folded(three, make_commit, run_milestones):
    finish(make_commit, three, ALPHA, "  Alpha \t Work  Done ")
    assert milestones(run_milestones, three).splitlines()[-1].split("\t")[3] == "Alpha Work Done"


def test_a_finish_body_that_is_only_a_trailer_gets_the_placeholder_title(three, make_commit, run_milestones):
    removed = [ALPHA + name for name in ("requirements.md", "TASKS_TODO.md", "open_questions.xml")]
    make_commit(
        three,
        "Milestone-finish: " + ALPHA,
        removed=removed,
        body="Co-Authored-By: Someone <someone@example.invalid>\n",
        date="2026-03-01T10:00:00+00:00",
    )
    assert milestones(run_milestones, three).splitlines()[-1] == f"finished\t2026-03-01\t{ALPHA}\t-"


def test_a_subject_only_finish_gets_the_placeholder_title(three, make_commit, run_milestones):
    removed = [ALPHA + name for name in ("requirements.md", "TASKS_TODO.md", "open_questions.xml")]
    make_commit(three, "Milestone-finish: " + ALPHA, removed=removed, date="2026-03-01T10:00:00+00:00")
    assert milestones(run_milestones, three).splitlines()[-1] == f"finished\t2026-03-01\t{ALPHA}\t-"


def test_a_reverted_finish_reads_live(three, make_commit, run_milestones, git, environment):
    commit = finish(make_commit, three, ALPHA, "Alpha Work")
    git(three, environment, "revert", "--no-edit", commit)
    assert (three / ALPHA / "requirements.md").is_file()
    assert milestones(run_milestones, three).splitlines()[0] == f"live\t-\t{ALPHA}\tAlpha Work"
    assert "finished" not in milestones(run_milestones, three)


def test_the_latest_finish_commit_of_a_path_is_its_finish_commit(three, make_commit, run_milestones, git, environment):
    first = finish(make_commit, three, ALPHA, "First Title", date="2026-03-01T10:00:00+00:00")
    git(three, environment, "revert", "--no-edit", first)
    finish(make_commit, three, ALPHA, "Second Title", date="2026-03-09T10:00:00+00:00")
    lines = milestones(run_milestones, three).splitlines()
    assert lines.count(f"finished\t2026-03-09\t{ALPHA}\tSecond Title") == 1
    assert "First Title" not in "\n".join(lines)


@pytest.mark.parametrize(
    "subject",
    [
        "Milestone-finish: milestone_07_alpha",
        "Milestone-finish: milestones/alpha",
        "Milestone-finish: ./milestones/alpha/",
        "Milestone-finish: milestones//alpha/",
        "Milestone-finish: alpha/",
        "Milestone-finished: milestones/alpha/",
        "Finish: milestones/alpha/",
    ],
)
def test_a_subject_naming_no_milestone_path_is_not_a_finish(three, make_commit, run_milestones, subject):
    removed = [ALPHA + name for name in ("requirements.md", "TASKS_TODO.md", "open_questions.xml")]
    make_commit(three, subject, removed=removed, body="Alpha Work\n\n- built it\n")
    assert milestones(run_milestones, three) == f"live\t-\t{BETA}\tBeta Work\nlive\t-\t{GAMMA}\tGamma Work\n"


def test_a_finish_subject_in_a_merge_commit_is_not_read(three, make_commit, run_milestones, git, environment):
    git(three, environment, "checkout", "-q", "-b", "side")
    make_commit(three, "Chore: side work", files={"side.txt": b"side\n"})
    git(three, environment, "checkout", "-q", "-")
    make_commit(three, "Chore: main work", files={"main.txt": b"main\n"})
    git(three, environment, "merge", "-q", "--no-ff", "-m", "Milestone-finish: milestones/delta/", "side")
    assert "milestones/delta/" not in milestones(run_milestones, three)


def test_a_finished_milestone_in_a_package_has_its_packages_scope(repo, make_commit, run_milestones):
    seeded = repo(
        {},
        files={
            **milestone_files(API, "Rate Limits"),
            **milestone_files(WEB, "Forms"),
            "packages/api/src/limit.py": b"a\n",
            "packages/web/src/form.js": b"b\n",
        },
    )
    finish(make_commit, seeded, API, "Rate Limits", date="2026-03-01T10:00:00+00:00")
    assert milestones(run_milestones, seeded, "packages/api/src/limit.py") == (
        f"finished\t2026-03-01\t{API}\tRate Limits\n"
    )
    assert milestones(run_milestones, seeded, "packages/web/src/form.js") == f"live\t-\t{WEB}\tForms\n"


@pytest.fixture
def packages(repo):
    return repo(
        {},
        files={
            **milestone_files(ALPHA, "Root Work"),
            **milestone_files(API, "Rate Limits"),
            **milestone_files(WEB, "Forms"),
            "packages/api/src/limit.py": b"a\n",
            "packages/web/src/form.js": b"b\n",
            "docs/guide.md": b"guide\n",
        },
    )


def test_a_root_milestones_scope_contains_every_path(packages, run_milestones):
    for path in ("packages/api/src/limit.py", "packages/web/", "docs/guide.md", "."):
        assert f"live\t-\t{ALPHA}\tRoot Work\n" in milestones(run_milestones, packages, path)


def test_a_package_milestone_is_listed_for_a_path_inside_its_scope_only(packages, run_milestones):
    assert milestones(run_milestones, packages, "packages/api/src/limit.py") == (
        f"live\t-\t{ALPHA}\tRoot Work\nlive\t-\t{API}\tRate Limits\n"
    )
    assert milestones(run_milestones, packages, "packages/api") == (
        f"live\t-\t{ALPHA}\tRoot Work\nlive\t-\t{API}\tRate Limits\n"
    )
    assert milestones(run_milestones, packages, "docs/guide.md") == f"live\t-\t{ALPHA}\tRoot Work\n"


def test_a_scope_lying_under_path_is_listed(packages, run_milestones):
    assert milestones(run_milestones, packages, "packages") == (
        f"live\t-\t{ALPHA}\tRoot Work\nlive\t-\t{API}\tRate Limits\nlive\t-\t{WEB}\tForms\n"
    )
    assert milestones(run_milestones, packages, ".") == milestones(run_milestones, packages, "packages")


@pytest.mark.parametrize("spelling", ["./packages/api/", "packages//api", "packages/api/./src/../"])
def test_path_is_read_lexically_for_the_scope_test(packages, run_milestones, spelling):
    assert milestones(run_milestones, packages, spelling) == (
        f"live\t-\t{ALPHA}\tRoot Work\nlive\t-\t{API}\tRate Limits\n"
    )


def test_a_task_commit_that_changed_path_lists_its_milestone_outside_its_scope(
    packages, make_commit, run_milestones
):
    make_commit(
        packages,
        "Task-completion: Document The Limits",
        files={API + "TASKS_TODO.md": TODO + b"\n", "docs/guide.md": b"guide with limits\n"},
    )
    assert milestones(run_milestones, packages, "docs/guide.md") == (
        f"live\t-\t{ALPHA}\tRoot Work\nlive\t-\t{API}\tRate Limits\n"
    )
    assert f"\t{WEB}\t" not in milestones(run_milestones, packages, "docs/guide.md")


def test_a_finished_milestone_joined_by_a_task_commit_is_listed(packages, make_commit, run_milestones):
    make_commit(
        packages,
        "Task-completion: Document The Forms",
        files={WEB + "TASKS_TODO.md": TODO + b"\n", "docs/guide.md": b"guide with forms\n"},
    )
    finish(make_commit, packages, WEB, "Forms", date="2026-03-02T10:00:00+00:00")
    assert milestones(run_milestones, packages, "docs/guide.md") == (
        f"live\t-\t{ALPHA}\tRoot Work\nfinished\t2026-03-02\t{WEB}\tForms\n"
    )


def test_a_task_commit_joined_to_a_path_neither_live_nor_finished_lists_nothing(repo, make_commit, run_milestones):
    seeded = repo({}, files={**milestone_files(API, "Rate Limits"), "docs/guide.md": b"guide\n"})
    make_commit(
        seeded,
        "Task-completion: A Task",
        files={"packages/old/milestones/gone/TASKS_TODO.md": TODO, "docs/guide.md": b"two\n"},
    )
    make_commit(seeded, "Chore: drop the old milestone", removed=("packages/old/milestones/gone/TASKS_TODO.md",))
    assert milestones(run_milestones, seeded, "docs/guide.md") == ""


def test_a_present_path_with_no_milestone_prints_nothing(repo, run_milestones):
    seeded = repo({}, files={"README.md": b"# A project\n"})
    result = run_milestones(seeded, "milestones", "README.md")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def test_a_path_changed_only_by_history_is_accepted(three, make_commit, run_milestones):
    make_commit(three, "Chore: drop the app", removed=("src/app.txt",))
    assert milestones(run_milestones, three, "src/app.txt").startswith(f"live\t-\t{ALPHA}\t")


@pytest.mark.parametrize("path", ["milestones/omega/", "src/missing.txt"])
def test_a_path_neither_present_nor_ever_changed_is_refused(three, run_milestones, path):
    result = run_milestones(three, "milestones", path)
    assert result.returncode == 1
    assert result.stdout == b""
    lines = result.stderr.decode("utf-8").splitlines()
    assert len(lines) == 1
    assert lines[0].startswith("Error: ")
    assert path in lines[0]


def test_an_untracked_requirements_file_is_not_listed(three, run_milestones):
    (three / "milestones" / "delta").mkdir()
    (three / "milestones" / "delta" / "requirements.md").write_bytes(b"# Delta\n")
    assert "milestones/delta/" not in milestones(run_milestones, three)
