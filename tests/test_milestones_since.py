"""The milestones tool's since query: for a MILESTONE_PATH read and refused as the gate query
reads and refuses it, its first line is the anchor, the latest commit other than a merge that
changed the milestone's requirements.md and whose subject opens with Starting-state:, whatever
follows the marker, and beneath it one line per later commit (reachable from HEAD and not from
the anchor) that changed a path inside the milestone's scope but outside its own directory, each
line three tab-separated fields (the abbreviated hash, the author date, the subject), newest
first by author timestamp, the milestone's own task commits excluded by the tasks query's join;
with no anchor it prints nothing at all. The broad form leaves out a commit whose every changed
path lies inside the directory of another live milestone that reads defined now, counts every
commit of a started or finished sibling and any commit touching a path outside such a directory,
and lists the milestone's own Goal-revision: commits; --milestones lists only other milestones'
task and finish commits. Both forms refuse a shallow repository before any log read, naming
git fetch --unshallow. Every test runs on a repository seeded through the conftest factory, then
given commits made through the conftest helper."""

import subprocess

import pytest

ROOT = "milestones/root-work/"
SIBLING = "milestones/sibling-work/"
API = "packages/api/milestones/rate-limits/"
API_TOO = "packages/api/milestones/caching/"
WEB = "packages/web/milestones/forms/"
TODO = b"# TASKS TODO\n\n"
FILES = ("requirements.md", "TASKS_TODO.md", "open_questions.xml")


def milestone_files(directory):
    return {
        directory + "requirements.md": f"# Work in {directory}\n\n## Goal\n\nThe goal.\n".encode("utf-8"),
        directory + "TASKS_TODO.md": TODO,
        directory + "open_questions.xml": b"<open-questions/>\n",
    }


def seed(repo, *directories):
    files = {"README.md": b"# A project\n", "src/app.txt": b"app\n", "packages/api/src/api.txt": b"api\n"}
    for directory in directories:
        files.update(milestone_files(directory))
    return repo({}, files=files)


class History:
    """Commits made in order with strictly increasing author dates, each returning its line as
    the since query prints it."""

    def __init__(self, repo, make_commit, git, environment):
        self.repo = repo
        self.make_commit = make_commit
        self.git = git
        self.environment = environment
        self.day = 0

    def commit(self, subject, files=None, removed=(), body=None):
        self.day += 1
        date = f"2026-03-{self.day:02d}"
        full = self.make_commit(
            self.repo, subject, files=files, removed=removed, body=body, date=date + "T10:00:00+00:00"
        )
        short = self.git(self.repo, self.environment, "log", "-1", "--format=%h", full).strip()
        return f"{short}\t{date}\t{subject}\n"

    def starting_state(self, directory, subject=None, text=b"facts"):
        return self.commit(
            subject or "Starting-state: " + directory,
            files={directory + "requirements.md": b"# Work\n\n## Goal\n\nThe goal.\n\n## Relevant starting state\n\n" + text + b"\n"},
        )

    def start(self, directory):
        return self.commit(
            "Task-derivation: " + directory, files={directory + "TASKS_TODO.md": TODO + b"## A Task\n\nDo it.\n\n---\n"}
        )

    def complete(self, directory, title, work):
        files = {directory + "TASKS_TODO.md": TODO}
        files.update(work)
        return self.commit("Task-completion: " + title, files=files, body="- done")

    def finish(self, directory):
        return self.commit(
            "Milestone-finish: " + directory,
            removed=tuple(directory + name for name in FILES),
            body="Work\n\n- built it",
        )


@pytest.fixture
def history(make_commit, git, environment):
    def build(repo):
        return History(repo, make_commit, git, environment)

    return build


def since(run_milestones, repo, path, *flags):
    result = run_milestones(repo, "since", path, *flags)
    assert result.returncode == 0, result.stderr
    assert result.stderr == b""
    return result.stdout.decode("utf-8")


def both(run_milestones, repo, path):
    return since(run_milestones, repo, path), since(run_milestones, repo, path, "--milestones")


def assert_one_error_line(result):
    assert result.returncode == 1
    assert result.stdout == b""
    text = result.stderr.decode("utf-8")
    assert "Traceback" not in text
    lines = text.splitlines()
    assert len(lines) == 1
    assert lines[0].startswith("Error: ")
    return lines[0]


# --- the anchor ---------------------------------------------------------------------------


def test_the_anchor_under_the_path_form_is_the_first_line(repo, history, run_milestones):
    seeded = seed(repo, ROOT)
    made = history(seeded)
    anchor = made.starting_state(ROOT)
    assert both(run_milestones, seeded, ROOT) == (anchor, anchor)


def test_the_anchor_under_the_bare_directory_name_subject_is_found_the_same_way(repo, history, run_milestones):
    seeded = seed(repo, ROOT)
    made = history(seeded)
    anchor = made.starting_state(ROOT, subject="Starting-state: root-work")
    work = made.commit("Fix the app", files={"src/app.txt": b"fixed\n"})
    assert since(run_milestones, seeded, ROOT) == anchor + work


def test_the_latest_starting_state_commit_is_the_anchor(repo, history, run_milestones):
    seeded = seed(repo, ROOT)
    made = history(seeded)
    made.starting_state(ROOT, subject="Starting-state: root-work")
    made.commit("Fix the app", files={"src/app.txt": b"fixed\n"})
    anchor = made.starting_state(ROOT, text=b"refreshed facts")
    assert both(run_milestones, seeded, ROOT) == (anchor, anchor)


def test_a_line_is_hash_date_and_subject_tab_separated(repo, history, run_milestones, git, environment):
    seeded = seed(repo, ROOT)
    history(seeded).starting_state(ROOT)
    short = git(seeded, environment, "log", "-1", "--format=%h").strip()
    assert since(run_milestones, seeded, ROOT) == f"{short}\t2026-03-01\tStarting-state: {ROOT}\n"


def test_another_milestones_starting_state_is_not_this_ones_anchor(repo, history, run_milestones):
    seeded = seed(repo, ROOT, SIBLING)
    history(seeded).starting_state(SIBLING)
    assert both(run_milestones, seeded, ROOT) == ("", "")


def test_a_commit_changing_the_requirements_under_another_subject_is_no_anchor(repo, history, run_milestones):
    seeded = seed(repo, ROOT)
    history(seeded).commit("Requirements-review: " + ROOT, files={ROOT + "requirements.md": b"# Work\n"})
    assert both(run_milestones, seeded, ROOT) == ("", "")


def test_no_anchor_prints_nothing_in_either_form_whatever_follows(repo, history, run_milestones):
    seeded = seed(repo, ROOT, SIBLING)
    made = history(seeded)
    made.commit("Fix the app", files={"src/app.txt": b"fixed\n"})
    made.start(SIBLING)
    made.complete(SIBLING, "Sibling Task", {"src/app.txt": b"sibling\n"})
    for flags in ((), ("--milestones",)):
        result = run_milestones(seeded, "since", ROOT, *flags)
        assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def test_the_anchor_alone_when_only_the_milestones_own_directory_changed(repo, history, run_milestones):
    seeded = seed(repo, ROOT)
    made = history(seeded)
    anchor = made.starting_state(ROOT)
    made.commit("Requirements-review: " + ROOT, files={ROOT + "open_questions.xml": b"<open-questions>\n</open-questions>\n"})
    made.start(ROOT)
    assert both(run_milestones, seeded, ROOT) == (anchor, anchor)


def test_commits_before_the_anchor_are_not_listed(repo, history, run_milestones):
    seeded = seed(repo, ROOT, SIBLING)
    made = history(seeded)
    made.commit("Fix the app", files={"src/app.txt": b"fixed\n"})
    made.start(SIBLING)
    made.complete(SIBLING, "Sibling Task", {"src/app.txt": b"sibling\n"})
    anchor = made.starting_state(ROOT)
    assert both(run_milestones, seeded, ROOT) == (anchor, anchor)


# --- what counts beneath the anchor -------------------------------------------------------


def test_work_in_the_scope_counts_in_the_broad_form_only(repo, history, run_milestones):
    seeded = seed(repo, ROOT)
    made = history(seeded)
    anchor = made.starting_state(ROOT)
    work = made.commit("Fix the app", files={"src/app.txt": b"fixed\n"})
    assert both(run_milestones, seeded, ROOT) == (anchor + work, anchor)


def test_a_commit_outside_the_scope_is_not_listed(repo, history, run_milestones):
    seeded = seed(repo, API, WEB)
    made = history(seeded)
    anchor = made.starting_state(API)
    made.commit("Fix the web", files={"packages/web/src/web.txt": b"web\n"})
    made.start(WEB)
    made.complete(WEB, "Web Task", {"packages/web/src/web.txt": b"done\n"})
    made.finish(WEB)
    work = made.commit("Fix the api", files={"packages/api/src/api.txt": b"fixed\n"})
    assert both(run_milestones, seeded, API) == (anchor + work, anchor)


def test_the_milestones_own_task_commits_are_excluded_by_the_join(repo, history, run_milestones):
    seeded = seed(repo, ROOT)
    made = history(seeded)
    anchor = made.starting_state(ROOT)
    made.start(ROOT)
    made.complete(ROOT, "Own Task", {"src/app.txt": b"own work\n", "docs/notes.md": b"notes\n"})
    assert both(run_milestones, seeded, ROOT) == (anchor, anchor)


def test_another_milestones_task_and_finish_commits_count_in_both_forms(repo, history, run_milestones):
    seeded = seed(repo, ROOT, SIBLING)
    made = history(seeded)
    anchor = made.starting_state(ROOT)
    made.start(SIBLING)
    task = made.complete(SIBLING, "Sibling Task", {"src/app.txt": b"sibling\n"})
    finish = made.finish(SIBLING)
    broad, narrow = both(run_milestones, seeded, ROOT)
    assert narrow == anchor + finish + task
    assert broad.startswith(anchor)
    assert finish in broad and task in broad


def test_a_task_commit_of_a_milestone_outside_the_scope_counts_when_it_reaches_the_scope(
    repo, history, run_milestones
):
    seeded = seed(repo, API, WEB)
    made = history(seeded)
    anchor = made.starting_state(API)
    made.start(WEB)
    task = made.complete(WEB, "Web Task Reaching the API", {"packages/api/src/api.txt": b"from web\n"})
    assert both(run_milestones, seeded, API) == (anchor + task, anchor + task)


def test_a_defined_siblings_own_directory_commits_are_left_out(repo, history, run_milestones):
    seeded = seed(repo, ROOT, SIBLING)
    made = history(seeded)
    anchor = made.starting_state(ROOT)
    made.starting_state(SIBLING)
    made.commit("Requirements-review: " + SIBLING, files={SIBLING + "open_questions.xml": b"<open-questions>\n</open-questions>\n"})
    assert both(run_milestones, seeded, ROOT) == (anchor, anchor)


def test_a_defined_siblings_commit_touching_a_path_outside_its_directory_counts_in_full(
    repo, history, run_milestones
):
    seeded = seed(repo, ROOT, SIBLING)
    made = history(seeded)
    anchor = made.starting_state(ROOT)
    mixed = made.commit(
        "Requirements-review: " + SIBLING,
        files={SIBLING + "requirements.md": b"# Sibling\n", "src/app.txt": b"touched\n"},
    )
    assert both(run_milestones, seeded, ROOT) == (anchor + mixed, anchor)


def test_a_started_siblings_own_directory_commits_count_in_the_broad_form(repo, history, run_milestones):
    seeded = seed(repo, ROOT, SIBLING)
    made = history(seeded)
    anchor = made.starting_state(ROOT)
    review = made.commit(
        "Requirements-review: " + SIBLING, files={SIBLING + "open_questions.xml": b"<open-questions>\n</open-questions>\n"}
    )
    start = made.start(SIBLING)
    assert both(run_milestones, seeded, ROOT) == (anchor + start + review, anchor)


def test_a_finished_siblings_preparation_commits_count_in_the_broad_form(repo, history, run_milestones):
    seeded = seed(repo, ROOT, SIBLING)
    made = history(seeded)
    anchor = made.starting_state(ROOT)
    preparation = made.starting_state(SIBLING)
    finish = made.finish(SIBLING)
    assert both(run_milestones, seeded, ROOT) == (anchor + finish + preparation, anchor + finish)


def test_a_sibling_whose_scope_lies_under_the_milestones_reads_the_same_way(repo, history, run_milestones):
    seeded = seed(repo, ROOT, API, API_TOO)
    made = history(seeded)
    anchor = made.starting_state(ROOT)
    made.starting_state(API)
    started = made.start(API_TOO)
    assert both(run_milestones, seeded, ROOT) == (anchor + started, anchor)


# --- goal revisions -----------------------------------------------------------------------


@pytest.mark.parametrize("subject", ["Goal-revision: " + ROOT, "Goal-revision: root-work"])
def test_the_milestones_own_goal_revision_is_listed_in_the_broad_form_only(repo, history, run_milestones, subject):
    seeded = seed(repo, ROOT)
    made = history(seeded)
    anchor = made.starting_state(ROOT)
    revision = made.commit(
        subject,
        files={ROOT + "requirements.md": b"# Work\n\n## Goal\n\nA revised goal.\n", ROOT + "open_questions.xml": b"<x/>\n"},
    )
    assert both(run_milestones, seeded, ROOT) == (anchor + revision, anchor)


def test_a_goal_revision_before_the_anchor_is_not_listed(repo, history, run_milestones):
    seeded = seed(repo, ROOT)
    made = history(seeded)
    made.commit("Goal-revision: " + ROOT, files={ROOT + "requirements.md": b"# Work\n\n## Goal\n\nRevised.\n"})
    anchor = made.starting_state(ROOT)
    assert both(run_milestones, seeded, ROOT) == (anchor, anchor)


def test_a_defined_siblings_goal_revision_is_not_listed(repo, history, run_milestones):
    seeded = seed(repo, ROOT, SIBLING)
    made = history(seeded)
    anchor = made.starting_state(ROOT)
    made.commit("Goal-revision: " + SIBLING, files={SIBLING + "requirements.md": b"# Sibling\n\n## Goal\n\nRevised.\n"})
    assert both(run_milestones, seeded, ROOT) == (anchor, anchor)


# --- the two forms together ---------------------------------------------------------------


def test_the_broad_form_lists_every_line_the_milestones_form_lists(repo, history, run_milestones):
    seeded = seed(repo, ROOT, SIBLING, API, WEB)
    made = history(seeded)
    anchor = made.starting_state(ROOT)
    made.starting_state(API)
    made.start(SIBLING)
    made.complete(SIBLING, "Sibling Task", {"src/app.txt": b"sibling\n"})
    made.commit("Fix the app", files={"src/app.txt": b"fixed\n"})
    made.commit("Goal-revision: " + ROOT, files={ROOT + "requirements.md": b"# Work\n\n## Goal\n\nRevised.\n"})
    made.start(WEB)
    made.complete(WEB, "Web Task", {"packages/web/src/web.txt": b"web\n"})
    made.finish(SIBLING)
    made.finish(WEB)
    broad, narrow = both(run_milestones, seeded, ROOT)
    assert broad.splitlines()[0] == narrow.splitlines()[0] == anchor.rstrip("\n")
    assert set(narrow.splitlines()) <= set(broad.splitlines())
    assert len(narrow.splitlines()) == 5
    assert len(broad.splitlines()) == 9


def test_the_lines_beneath_the_anchor_are_newest_first_by_author_timestamp(repo, make_commit, run_milestones, git, environment):
    seeded = seed(repo, ROOT)
    make_commit(
        seeded,
        "Starting-state: " + ROOT,
        files={ROOT + "requirements.md": b"# Work\n\nfacts\n"},
        date="2026-01-01T10:00:00+00:00",
    )
    make_commit(seeded, "Late work", files={"src/app.txt": b"late\n"}, date="2026-05-01T10:00:00+00:00")
    make_commit(seeded, "Early work", files={"src/other.txt": b"early\n"}, date="2026-02-01T10:00:00+00:00")
    make_commit(seeded, "Middle work", files={"src/third.txt": b"mid\n"}, date="2026-03-01T10:00:00+00:00")
    subjects = [line.split("\t")[2] for line in since(run_milestones, seeded, ROOT).splitlines()]
    assert subjects == ["Starting-state: " + ROOT, "Late work", "Middle work", "Early work"]


def test_a_merged_branchs_commits_count_and_the_merge_does_not(repo, history, run_milestones, git, environment):
    seeded = seed(repo, ROOT)
    made = history(seeded)
    git(seeded, environment, "branch", "side")
    git(seeded, environment, "checkout", "-q", "side")
    side = made.commit("Side work", files={"src/side.txt": b"side\n"})
    git(seeded, environment, "checkout", "-q", "-")
    anchor = made.starting_state(ROOT)
    git(seeded, environment, "merge", "-q", "--no-ff", "--no-edit", "side")
    assert both(run_milestones, seeded, ROOT) == (anchor + side, anchor)


# --- reading MILESTONE_PATH ---------------------------------------------------------------


@pytest.mark.parametrize("spelling", ["./milestones/root-work/", "milestones/root-work", "milestones//root-work/"])
def test_the_named_path_is_read_lexically(repo, history, run_milestones, spelling):
    seeded = seed(repo, ROOT)
    made = history(seeded)
    anchor = made.starting_state(ROOT)
    work = made.commit("Fix the app", files={"src/app.txt": b"fixed\n"})
    assert since(run_milestones, seeded, spelling) == anchor + work


def test_a_finished_milestone_is_read_from_its_history(repo, history, run_milestones):
    seeded = seed(repo, ROOT)
    made = history(seeded)
    anchor = made.starting_state(ROOT)
    work = made.commit("Fix the app", files={"src/app.txt": b"fixed\n"})
    made.finish(ROOT)
    assert since(run_milestones, seeded, ROOT) == anchor + work


@pytest.mark.parametrize(
    "path",
    [
        "packages/api/",
        "rate-limits/",
        ".",
        "milestones/",
        "milestones/root-work/nested/",
        "milestones.fixture/root-work/",
        "/abs/milestones/root-work/",
        "../milestones/root-work/",
    ],
)
@pytest.mark.parametrize("flags", [(), ("--milestones",)])
def test_a_path_with_no_milestones_container_is_refused(repo, history, run_milestones, path, flags):
    seeded = seed(repo, ROOT)
    history(seeded).starting_state(ROOT)
    line = assert_one_error_line(run_milestones(seeded, "since", path, *flags))
    assert path in line
    assert "milestones/ container" in line


def test_an_empty_path_is_refused(repo, run_milestones):
    seeded = seed(repo, ROOT)
    assert_one_error_line(run_milestones(seeded, "since", ""))


# --- the shallow refusal ------------------------------------------------------------------


def clone(source, destination, environment, *flags):
    result = subprocess.run(
        ["git", "clone", "-q", *flags, source.as_uri(), str(destination)],
        env=environment,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8", "replace")
    return destination


@pytest.mark.parametrize("flags", [(), ("--milestones",)])
def test_a_shallow_repository_is_refused_in_both_forms(repo, history, run_milestones, environment, git, tmp_path, flags):
    seeded = seed(repo, ROOT)
    made = history(seeded)
    made.starting_state(ROOT)
    made.commit("Fix the app", files={"src/app.txt": b"fixed\n"})
    shallow = clone(seeded, tmp_path / "shallow", environment, "--depth", "1")
    assert git(shallow, environment, "rev-parse", "--is-shallow-repository").strip() == "true"
    for path in (ROOT, "packages/api/", ""):
        line = assert_one_error_line(run_milestones(shallow, "since", path, *flags))
        assert "shallow" in line
        assert "git fetch --unshallow" in line


def test_a_complete_clone_is_not_refused(repo, history, run_milestones, environment, tmp_path):
    seeded = seed(repo, ROOT)
    made = history(seeded)
    anchor = made.starting_state(ROOT)
    work = made.commit("Fix the app", files={"src/app.txt": b"fixed\n"})
    complete = clone(seeded, tmp_path / "complete", environment)
    assert since(run_milestones, complete, ROOT) == anchor + work


# --- help ---------------------------------------------------------------------------------


def test_the_since_help_names_its_lines_its_forms_and_its_refusals(tmp_path, run_milestones):
    result = run_milestones(tmp_path, "since", "--help")
    assert result.returncode == 0
    text = " ".join(result.stdout.decode("utf-8").split())
    assert "MILESTONE_PATH" in text and "--milestones" in text
    assert "Starting-state:" in text and "Goal-revision:" in text
    assert "Task-completion:" in text and "Milestone-finish:" in text
    assert '"defined"' in text
    assert "git rev-parse --is-shallow-repository" in text
    assert "git fetch --unshallow" in text
    assert "no milestones/ container is refused" in text
    assert "two queries check for a shallow clone, gate and since" in text


def test_the_top_level_help_names_gate_and_since_as_the_two_queries_that_check(tmp_path, run_milestones):
    text = " ".join(run_milestones(tmp_path, "--help").stdout.decode("utf-8").split())
    assert "since" in text
    assert "two queries check, gate and since, each refusing a shallow repository" in text
