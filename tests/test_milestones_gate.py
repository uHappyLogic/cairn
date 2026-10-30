"""The milestones tool's gate query: for a MILESTONE_PATH naming a directory directly inside a
milestones/ container, read lexically relative to the workspace root, it prints one bare path
per line, ordered by path, for every other live milestone that is started (its TASKS_TODO.md
modified after the commit adding it, by the path-scoped git log -1 --diff-filter=M test) and
whose scope (the directory holding its milestones/ container) equals the named milestone's
scope, contains it, or lies under it, and exits 0 whether or not it prints. It refuses a
shallow repository (git rev-parse --is-shallow-repository printing true), naming
git fetch --unshallow, and a MILESTONE_PATH with no milestones/ container, each on one Error
line with exit 1 and nothing on stdout. Every test runs on a repository seeded through the
conftest factory, then given commits made through the conftest helper, a milestone being
started by a task-derivation-shaped commit writing its task list."""

import subprocess

import pytest

ROOT = "milestones/root-work/"
ROOT_TOO = "milestones/more-root-work/"
API = "packages/api/milestones/rate-limits/"
API_TOO = "packages/api/milestones/caching/"
API_DEEP = "packages/api/v2/milestones/endpoints/"
WEB = "packages/web/milestones/forms/"
TODO = b"# TASKS TODO\n\n"


def milestone_files(directory):
    return {
        directory + "requirements.md": f"# Work in {directory}\n\n## Goal\n\nThe goal.\n".encode("utf-8"),
        directory + "TASKS_TODO.md": TODO,
        directory + "open_questions.xml": b"<open-questions/>\n",
    }


def seed(repo, *directories):
    files = {"README.md": b"# A project\n"}
    for directory in directories:
        files.update(milestone_files(directory))
    return repo({}, files=files)


def start(make_commit, repo, directory):
    """Start a milestone the way task entry does: one commit writing tasks into its list."""
    tasks = TODO + b"## A Task\n\nDo it.\n\n---\n"
    make_commit(repo, "Task-derivation: " + directory, files={directory + "TASKS_TODO.md": tasks})


def gate(run_milestones, repo, path):
    result = run_milestones(repo, "gate", path)
    assert result.returncode == 0, result.stderr
    assert result.stderr == b""
    return result.stdout.decode("utf-8")


def assert_one_error_line(result):
    assert result.returncode == 1
    assert result.stdout == b""
    text = result.stderr.decode("utf-8")
    assert "Traceback" not in text
    lines = text.splitlines()
    assert len(lines) == 1
    assert lines[0].startswith("Error: ")
    return lines[0]


# --- overlap ------------------------------------------------------------------------------


def test_a_started_milestone_in_the_same_container_holds_the_scope(repo, make_commit, run_milestones):
    seeded = seed(repo, ROOT, ROOT_TOO)
    start(make_commit, seeded, ROOT_TOO)
    assert gate(run_milestones, seeded, ROOT) == ROOT_TOO + "\n"


def test_a_started_milestone_whose_scope_contains_the_named_one_holds_it(repo, make_commit, run_milestones):
    seeded = seed(repo, ROOT, API)
    start(make_commit, seeded, ROOT)
    assert gate(run_milestones, seeded, API) == ROOT + "\n"


def test_a_started_milestone_whose_scope_lies_under_the_named_one_holds_it(repo, make_commit, run_milestones):
    seeded = seed(repo, ROOT, API)
    start(make_commit, seeded, API)
    assert gate(run_milestones, seeded, ROOT) == API + "\n"


def test_overlap_reaches_through_every_level_in_both_directions(repo, make_commit, run_milestones):
    seeded = seed(repo, API, API_DEEP)
    start(make_commit, seeded, API)
    assert gate(run_milestones, seeded, API_DEEP) == API + "\n"
    start(make_commit, seeded, API_DEEP)
    assert gate(run_milestones, seeded, API) == API_DEEP + "\n"


def test_disjoint_packages_hold_nothing_against_each_other(repo, make_commit, run_milestones):
    seeded = seed(repo, API, WEB)
    start(make_commit, seeded, API)
    start(make_commit, seeded, WEB)
    assert gate(run_milestones, seeded, API) == ""
    assert gate(run_milestones, seeded, WEB) == ""


def test_scope_is_compared_by_whole_components_not_by_prefix(repo, make_commit, run_milestones):
    near = "packages/api-extra/milestones/other/"
    seeded = seed(repo, API, near)
    start(make_commit, seeded, near)
    assert gate(run_milestones, seeded, API) == ""


def test_every_holder_is_printed_as_a_bare_path_ordered_by_path(repo, make_commit, run_milestones):
    seeded = seed(repo, ROOT, ROOT_TOO, API, API_TOO, API_DEEP, WEB)
    for directory in (WEB, API_DEEP, ROOT_TOO, API_TOO):
        start(make_commit, seeded, directory)
    assert gate(run_milestones, seeded, API) == "".join(
        line + "\n" for line in sorted([ROOT_TOO, API_TOO, API_DEEP])
    )
    assert gate(run_milestones, seeded, ROOT) == "".join(
        line + "\n" for line in sorted([ROOT_TOO, API_TOO, API_DEEP, WEB])
    )


# --- what holds nothing -------------------------------------------------------------------


def test_a_defined_only_milestone_holds_nothing(repo, make_commit, run_milestones):
    seeded = seed(repo, ROOT, ROOT_TOO, API)
    make_commit(
        seeded,
        "Requirements-review: " + ROOT_TOO,
        files={ROOT_TOO + "requirements.md": b"# Work\n\n## Goal\n\nA revised goal.\n"},
    )
    assert gate(run_milestones, seeded, ROOT) == ""
    assert gate(run_milestones, seeded, API) == ""


def test_the_named_milestone_itself_is_never_printed(repo, make_commit, run_milestones):
    seeded = seed(repo, ROOT, ROOT_TOO)
    start(make_commit, seeded, ROOT)
    assert gate(run_milestones, seeded, ROOT) == ""


def test_a_finished_milestone_whose_directory_is_gone_holds_nothing(repo, make_commit, run_milestones):
    seeded = seed(repo, ROOT, ROOT_TOO)
    start(make_commit, seeded, ROOT_TOO)
    make_commit(
        seeded,
        "Milestone-finish: " + ROOT_TOO,
        removed=tuple(ROOT_TOO + name for name in ("requirements.md", "TASKS_TODO.md", "open_questions.xml")),
        body="Work\n\n- built it\n",
    )
    assert gate(run_milestones, seeded, ROOT) == ""


def test_an_untracked_milestone_directory_holds_nothing(repo, make_commit, run_milestones):
    seeded = seed(repo, ROOT)
    (seeded / "milestones" / "stray").mkdir()
    (seeded / "milestones" / "stray" / "requirements.md").write_bytes(b"# Stray\n")
    (seeded / "milestones" / "stray" / "TASKS_TODO.md").write_bytes(TODO + b"## A Task\n")
    assert gate(run_milestones, seeded, ROOT) == ""


# --- reading MILESTONE_PATH ---------------------------------------------------------------


@pytest.mark.parametrize("spelling", ["./milestones/root-work/", "milestones/root-work", "milestones//root-work/"])
def test_the_named_path_is_read_lexically(repo, make_commit, run_milestones, spelling):
    seeded = seed(repo, ROOT, ROOT_TOO)
    start(make_commit, seeded, ROOT)
    start(make_commit, seeded, ROOT_TOO)
    assert gate(run_milestones, seeded, spelling) == ROOT_TOO + "\n"


def test_the_named_milestone_need_not_be_live(repo, make_commit, run_milestones):
    seeded = seed(repo, ROOT)
    start(make_commit, seeded, ROOT)
    assert gate(run_milestones, seeded, "packages/api/milestones/not-defined-yet/") == ROOT + "\n"


def test_no_live_milestone_prints_nothing_and_exits_0(repo, run_milestones):
    seeded = repo({}, files={"README.md": b"# A project\n"})
    result = run_milestones(seeded, "gate", ROOT)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


# --- refusals -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "path",
    [
        "packages/api/",
        "rate-limits/",
        ".",
        "./",
        "milestones/",
        "milestones",
        "milestones/root-work/nested/",
        "milestones.fixture/root-work/",
        "/abs/milestones/root-work/",
        "../milestones/root-work/",
        "milestones/root-work/../../..",
    ],
)
def test_a_path_with_no_milestones_container_is_refused(repo, make_commit, run_milestones, path):
    seeded = seed(repo, ROOT, ROOT_TOO)
    start(make_commit, seeded, ROOT_TOO)
    line = assert_one_error_line(run_milestones(seeded, "gate", path))
    assert path in line
    assert "milestones/ container" in line


def shallow_clone(source, destination, environment):
    result = subprocess.run(
        ["git", "clone", "-q", "--depth", "1", source.as_uri(), str(destination)],
        env=environment,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8", "replace")
    return destination


def test_a_shallow_repository_is_refused_naming_the_unshallow_fetch(
    repo, make_commit, run_milestones, environment, git, tmp_path
):
    seeded = seed(repo, ROOT, ROOT_TOO)
    start(make_commit, seeded, ROOT_TOO)
    assert gate(run_milestones, seeded, ROOT) == ROOT_TOO + "\n"
    clone = shallow_clone(seeded, tmp_path / "shallow", environment)
    assert git(clone, environment, "rev-parse", "--is-shallow-repository").strip() == "true"
    line = assert_one_error_line(run_milestones(clone, "gate", ROOT))
    assert "shallow" in line
    assert "git fetch --unshallow" in line


def test_a_shallow_repository_is_refused_whatever_the_path(repo, make_commit, run_milestones, environment, tmp_path):
    seeded = seed(repo, ROOT)
    start(make_commit, seeded, ROOT)
    clone = shallow_clone(seeded, tmp_path / "shallow", environment)
    for path in (ROOT, API, "packages/api/"):
        line = assert_one_error_line(run_milestones(clone, "gate", path))
        assert "git fetch --unshallow" in line


def test_a_complete_clone_is_not_refused(repo, make_commit, run_milestones, environment, tmp_path):
    seeded = seed(repo, ROOT, ROOT_TOO)
    start(make_commit, seeded, ROOT_TOO)
    clone = tmp_path / "complete"
    result = subprocess.run(
        ["git", "clone", "-q", seeded.as_uri(), str(clone)],
        env=environment,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8", "replace")
    assert gate(run_milestones, clone, ROOT) == ROOT_TOO + "\n"
