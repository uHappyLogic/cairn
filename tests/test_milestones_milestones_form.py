"""The milestones tool's milestones query in its milestone-path form and under its bound: with
--milestone MILESTONE_PATH in place of PATH, read lexically relative to the workspace root as the
gate query reads its argument and refused on one Error line with exit 1 and nothing on stdout
when it names no directory directly inside a milestones/ container, the query prints exactly the
overview it prints with that milestone's scope (the directory holding its milestones/ container,
"." for the root) as PATH; with --last N it prints every live line and only the N newest finished
lines; and with neither it prints what it always has. Every test runs on a repository seeded
through the conftest factory, then given finish-shaped commits made through the conftest
helper."""

import pytest

ROOT_A = "milestones/alpha/"
ROOT_B = "milestones/beta/"
ROOT_C = "milestones/gamma/"
ROOT_D = "milestones/delta/"
API = "packages/api/milestones/rate-limits/"
API_TOO = "packages/api/milestones/caching/"
WEB = "packages/web/milestones/forms/"
TODO = b"# TASKS TODO\n\n"


def milestone_files(directory, title):
    return {
        directory + "requirements.md": f"# {title}\n\n## Goal\n\nThe goal of {title}.\n".encode("utf-8"),
        directory + "TASKS_TODO.md": TODO,
        directory + "open_questions.xml": b"<open-questions/>\n",
    }


def finish(make_commit, repo, directory, title, date):
    removed = sorted(
        str(path.relative_to(repo)) for path in (repo / directory).rglob("*") if path.is_file()
    )
    body = title + "\n\n- built it\n"
    return make_commit(repo, "Milestone-finish: " + directory, removed=removed, body=body, date=date)


def query(run_milestones, repo, *args):
    result = run_milestones(repo, "milestones", *args)
    assert result.returncode == 0, result.stderr
    assert result.stderr == b""
    return result.stdout.decode("utf-8")


def assert_one_error_line(result, value):
    assert result.returncode == 1
    assert result.stdout == b""
    lines = result.stderr.decode("utf-8").splitlines()
    assert len(lines) == 1
    assert lines[0].startswith("Error: ")
    assert value in lines[0]


@pytest.fixture
def project(repo, make_commit):
    """Four root milestones and three package ones, three root and one package milestone
    finished on distinct days, so live and finished lines stand in both scopes."""
    files = {"README.md": b"# A project\n", "packages/api/src/limit.py": b"a\n", "packages/web/src/form.js": b"b\n"}
    for directory, title in (
        (ROOT_A, "Alpha Work"),
        (ROOT_B, "Beta Work"),
        (ROOT_C, "Gamma Work"),
        (ROOT_D, "Delta Work"),
        (API, "Rate Limits"),
        (API_TOO, "Caching"),
        (WEB, "Forms"),
    ):
        files.update(milestone_files(directory, title))
    seeded = repo({}, files=files)
    finish(make_commit, seeded, ROOT_B, "Beta Work", "2026-03-01T10:00:00+00:00")
    finish(make_commit, seeded, ROOT_C, "Gamma Work", "2026-03-03T10:00:00+00:00")
    finish(make_commit, seeded, ROOT_D, "Delta Work", "2026-03-02T10:00:00+00:00")
    finish(make_commit, seeded, API_TOO, "Caching", "2026-03-04T10:00:00+00:00")
    return seeded


@pytest.mark.parametrize(
    "milestone, scope",
    [
        (ROOT_A, "."),
        (API, "packages/api"),
        (WEB, "packages/web"),
        (API_TOO, "packages/api"),
        ("packages/api/milestones/not-yet/", "packages/api"),
    ],
)
def test_the_milestone_path_form_prints_the_scope_calls_overview(project, run_milestones, milestone, scope):
    expected = query(run_milestones, project, scope)
    assert expected
    assert query(run_milestones, project, "--milestone", milestone) == expected


def test_the_package_form_lists_the_root_and_its_own_scope_only(project, run_milestones):
    assert query(run_milestones, project, "--milestone", API) == (
        f"live\t-\t{ROOT_A}\tAlpha Work\n"
        f"live\t-\t{API}\tRate Limits\n"
        f"finished\t2026-03-04\t{API_TOO}\tCaching\n"
        f"finished\t2026-03-03\t{ROOT_C}\tGamma Work\n"
        f"finished\t2026-03-02\t{ROOT_D}\tDelta Work\n"
        f"finished\t2026-03-01\t{ROOT_B}\tBeta Work\n"
    )


@pytest.mark.parametrize("spelling", ["./packages/api/milestones/rate-limits", "packages//api/milestones/rate-limits/./"])
def test_the_milestone_path_is_read_lexically(project, run_milestones, spelling):
    assert query(run_milestones, project, "--milestone", spelling) == query(run_milestones, project, "packages/api")


@pytest.mark.parametrize(
    "value",
    ["packages/api/", "packages/api/src/limit.py", "milestones/", "/abs/milestones/alpha/", "../milestones/alpha/", "milestones/alpha/extra/"],
)
def test_a_value_naming_no_directory_inside_a_container_is_refused(project, run_milestones, value):
    assert_one_error_line(run_milestones(project, "milestones", "--milestone", value), value)


def test_an_empty_milestone_path_is_refused(project, run_milestones):
    assert_one_error_line(run_milestones(project, "milestones", "--milestone", ""), "MILESTONE_PATH")


@pytest.mark.parametrize("args", [(), (".", "--milestone", ROOT_A), ("--last", "2"), (".", "--last", "-1"), (".", "--last", "x")])
def test_a_malformed_form_exits_2(project, run_milestones, args):
    result = run_milestones(project, "milestones", *args)
    assert result.returncode == 2
    assert result.stdout == b""


@pytest.mark.parametrize("last", [0, 1, 2, 3])
def test_the_bound_keeps_every_live_line_and_the_newest_finished_lines(project, run_milestones, last):
    unbounded = query(run_milestones, project, ".").splitlines(keepends=True)
    live = [line for line in unbounded if line.startswith("live\t")]
    finished = [line for line in unbounded if line.startswith("finished\t")]
    assert len(live) == 3 and len(finished) == 4
    assert query(run_milestones, project, ".", "--last", str(last)) == "".join(live + finished[:last])


def test_the_bound_keeps_the_newest_by_finish_timestamp(project, run_milestones):
    assert query(run_milestones, project, ".", "--last", "2").splitlines()[-2:] == [
        f"finished\t2026-03-04\t{API_TOO}\tCaching",
        f"finished\t2026-03-03\t{ROOT_C}\tGamma Work",
    ]


def test_a_bound_wider_than_the_record_prints_it_whole(project, run_milestones):
    assert query(run_milestones, project, ".", "--last", "10") == query(run_milestones, project, ".")


def test_the_bound_applies_to_the_milestone_path_form(project, run_milestones):
    assert query(run_milestones, project, "--milestone", WEB, "--last", "1") == (
        f"live\t-\t{ROOT_A}\tAlpha Work\n"
        f"live\t-\t{WEB}\tForms\n"
        f"finished\t2026-03-03\t{ROOT_C}\tGamma Work\n"
    )


def test_the_unbounded_print_is_unchanged(project, run_milestones):
    assert query(run_milestones, project, ".") == (
        f"live\t-\t{ROOT_A}\tAlpha Work\n"
        f"live\t-\t{API}\tRate Limits\n"
        f"live\t-\t{WEB}\tForms\n"
        f"finished\t2026-03-04\t{API_TOO}\tCaching\n"
        f"finished\t2026-03-03\t{ROOT_C}\tGamma Work\n"
        f"finished\t2026-03-02\t{ROOT_D}\tDelta Work\n"
        f"finished\t2026-03-01\t{ROOT_B}\tBeta Work\n"
    )


def test_the_record_query_takes_no_bound(project, run_milestones):
    result = run_milestones(project, "record", ".", "--last", "1")
    assert result.returncode == 2
