"""The commit tool's author date input: an optional --date DATE passed to git unchanged as
"git commit --date DATE", setting the commit's author date only while its committer date stays
the time the commit is made. Git runs through a logging wrapper put first on PATH, so every
test sees the git commands the tool really ran; the repeat test has the wrapper fail the
commit itself with 128 a set number of times. A call without the option runs exactly the
commands it ran before the option existed, both dates the time of the commit."""

import shlex
import shutil
import time
from datetime import datetime
from pathlib import Path

import pytest

import commit

COMMIT_TOOL = Path(commit.__file__).resolve()
NO_OP_LINE = "Nothing committed — none of the paths changed."
WINDOW = (commit.ATTEMPTS - 1) * commit.PAUSE

FILES = {
    "README.md": b"# A project\n",
    "notes/a.md": b"a\n",
    "milestones/first/requirements.md": b"# First\n",
    "milestones/first/TASKS_TODO.md": b"# TASKS TODO\n",
}
FIRST = ["milestones/first/TASKS_TODO.md", "milestones/first/requirements.md"]
DATE = "2026-09-02T10:11:12+02:00"


@pytest.fixture
def project(repo):
    """A repository whose initial commit holds README.md, a note, and one milestone directory."""
    return repo({}, files=dict(FILES))


@pytest.fixture
def logged(tmp_path, environment):
    """The environment with git replaced on PATH by a wrapper that logs every call, its
    GIT_OPTIONAL_LOCKS value and its whole argument list as one record ended by a record
    separator rather than a newline, since a body argument may hold one, and then runs the real
    git; a subcommand named in failures exits 128 that many times first: logged(failures={"commit": 2})
    -> (the environment, a function returning the logged calls as (optional locks, subcommand,
    arguments) triples)."""

    def build(failures=None):
        failures = {} if failures is None else failures
        real = shutil.which("git", path=environment["PATH"])
        assert real, "git is not on PATH"
        directory = tmp_path / "git-wrapper"
        directory.mkdir()
        log = tmp_path / "git-calls.log"
        lines = [
            "#!/bin/sh",
            "sub=",
            'for word in "$@"; do case "$word" in -*) ;; *) sub="$word"; break ;; esac; done',
            f'{{ printf \'%s\\037%s\' "${{GIT_OPTIONAL_LOCKS:-}}" "$sub"; '
            f'for word in "$@"; do printf \'\\037%s\' "$word"; done; printf \'\\036\'; }} >> {shlex.quote(str(log))}',
        ]
        for subcommand, count in failures.items():
            counter = shlex.quote(str(tmp_path / f"{subcommand}.failures"))
            lines += [
                f'if [ "$sub" = {shlex.quote(subcommand)} ]; then',
                f"  done_count=$(cat {counter} 2>/dev/null || echo 0)",
                f'  if [ "$done_count" -lt {count} ]; then',
                f"    echo $((done_count + 1)) > {counter}",
                "    echo 'fatal: a simulated fatal error' >&2",
                "    exit 128",
                "  fi",
                "fi",
            ]
        lines.append(f'exec {shlex.quote(real)} "$@"')
        wrapper = directory / "git"
        wrapper.write_text("\n".join(lines) + "\n", encoding="utf-8")
        wrapper.chmod(0o755)
        env = dict(environment, PATH=str(directory) + ":" + environment["PATH"])

        def calls():
            if not log.exists():
                return []
            logged_calls = []
            for record in log.read_text(encoding="utf-8").split("\036")[:-1]:
                locks, subcommand, *arguments = record.split("\037")
                logged_calls.append((locks, subcommand, arguments))
            return logged_calls

        def reset():
            if log.exists():
                log.unlink()

        calls.reset = reset
        return env, calls

    return build


def of(calls, name):
    return [call for call in calls if call[1] == name]


def head(git, root, environment):
    return git(root, environment, "rev-parse", "HEAD").strip()


def changes(git, root, environment):
    """The HEAD commit's changes as sorted name-status lines."""
    output = git(root, environment, "show", "--name-status", "--format=", "HEAD")
    return sorted(line for line in output.split("\n") if line)


def staged(git, root, environment):
    output = git(root, environment, "diff", "-z", "--cached", "--name-only")
    return sorted(name for name in output.split("\0") if name)


def message(git, root, environment):
    raw = git(root, environment, "cat-file", "commit", "HEAD")
    return raw.split("\n\n", 1)[1]


def dates(git, root, environment):
    """The HEAD commit's author date as git log's %aI prints it, and its author and committer
    timestamps: -> (author ISO date, author timestamp, committer timestamp)."""
    output = git(root, environment, "log", "-1", "--format=%aI%x1f%at%x1f%ct", "HEAD").strip()
    author_iso, author_time, committer_time = output.split("\x1f")
    return author_iso, int(author_time), int(committer_time)


def assert_landed(result):
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def assert_one_error_line(result):
    assert result.returncode == 1
    assert result.stdout == b""
    lines = result.stderr.decode("utf-8").split("\n")
    assert len(lines) == 2 and lines[1] == ""
    assert lines[0].startswith("Error: ")
    assert b"Traceback" not in result.stderr
    return lines[0]


def deleted(paths):
    return sorted("D\t" + path for path in paths)


def epoch(iso):
    """The Unix timestamp of an ISO 8601 date carrying its offset."""
    return int(datetime.fromisoformat(iso).timestamp())


# --- the author date --------------------------------------------------------------------


def test_the_date_sets_the_author_date_and_the_committer_date_stays_the_time_of_the_commit(run_commit, project, git, environment):
    (project / "README.md").write_bytes(b"# An edited project\n")
    started = int(time.time())
    result = run_commit(project, "--subject", "Dated", "--date", DATE, "--", "README.md")
    finished = int(time.time())
    assert_landed(result)
    author_iso, author_time, committer_time = dates(git, project, environment)
    assert author_iso == DATE
    assert author_time == epoch(DATE)
    assert started <= committer_time <= finished
    assert changes(git, project, environment) == ["M\tREADME.md"]
    assert message(git, project, environment) == "Dated\n"


@pytest.mark.parametrize(
    "date",
    ["2026-09-02T10:11:12+02:00", "2019-01-31T23:59:59-05:30", "2024-02-29T00:00:00+05:45"],
    ids=["east-of-utc", "west-of-utc", "leap-day"],
)
def test_an_iso_author_date_read_back_with_a_i_is_the_date_given(run_commit, project, git, environment, date):
    (project / "README.md").write_bytes(b"# An edited project\n")
    result = run_commit(project, "--subject", "Round trip", "--date", date, "--", "README.md")
    assert_landed(result)
    author_iso, author_time, _ = dates(git, project, environment)
    assert (author_iso, author_time) == (date, epoch(date))


def test_the_date_reaches_git_commit_unchanged_beside_the_subject_and_the_body(run_commit, project, git, environment, logged):
    env, calls = logged()
    (project / "README.md").write_bytes(b"# An edited project\n")
    result = run_commit(project, "--subject", "Dated", "--body", "A body", "--date", DATE, "--", "README.md", env=env)
    assert_landed(result)
    assert calls() == [
        ("0", "status", ["--literal-pathspecs", "status", "--porcelain", "--", "README.md"]),
        ("", "add", ["--literal-pathspecs", "add", "--", "README.md"]),
        ("", "commit", ["--literal-pathspecs", "commit", "-m", "Dated", "-m", "A body", "--date", DATE, "--", "README.md"]),
    ]
    assert message(git, project, environment) == "Dated\n\nA body\n"


def test_a_date_in_a_form_other_than_iso_is_passed_on_unchanged_for_git_to_parse(run_commit, project, git, environment, logged):
    env, calls = logged()
    (project / "README.md").write_bytes(b"# An edited project\n")
    date = "Wed, 2 Sep 2026 10:11:12 +0200"
    result = run_commit(project, "--subject", "Other form", "--date", date, "--", "README.md", env=env)
    assert_landed(result)
    assert of(calls(), "commit")[0][2][-4:] == ["--date", date, "--", "README.md"]
    assert dates(git, project, environment)[0] == DATE


def test_a_dated_removal_lands_as_one_commit_carrying_the_author_date(run_commit, project, git, environment, logged):
    env, calls = logged()
    before = head(git, project, environment)
    body = "First\n\n- a bullet\n- another bullet"
    started = int(time.time())
    result = run_commit(
        project, "--subject", "Milestone-finish: milestones/first/", "--body", body, "--date", DATE,
        "--remove", "milestones/first/", env=env,
    )
    finished = int(time.time())
    assert_landed(result)
    assert git(project, environment, "rev-parse", "HEAD~1").strip() == before
    assert changes(git, project, environment) == deleted(FIRST)
    assert message(git, project, environment) == "Milestone-finish: milestones/first/\n\n" + body + "\n"
    author_iso, _, committer_time = dates(git, project, environment)
    assert author_iso == DATE
    assert started <= committer_time <= finished
    assert of(calls(), "commit")[0][2] == [
        "--literal-pathspecs", "commit", "-m", "Milestone-finish: milestones/first/", "-m", body,
        "--date", DATE, "--", "milestones/first/",
    ]


def test_a_dated_path_file_call_lands_carrying_the_author_date(run_commit, project, git, environment, tmp_path):
    (project / "README.md").write_bytes(b"# An edited project\n")
    (project / "notes" / "a.md").write_bytes(b"a changed\n")
    path_file = tmp_path / "paths.txt"
    path_file.write_bytes(b"README.md\nnotes/a.md\n")
    result = run_commit(project, "--subject", "From a file", "--date", DATE, "--path-file", str(path_file))
    assert_landed(result)
    assert changes(git, project, environment) == ["M\tREADME.md", "M\tnotes/a.md"]
    assert dates(git, project, environment)[0] == DATE


# --- the retry and a later run ----------------------------------------------------------


def test_every_repeated_commit_carries_the_date(run_commit, project, git, environment, logged):
    env, calls = logged(failures={"commit": 3})
    (project / "README.md").write_bytes(b"# An edited project\n")
    result = run_commit(project, "--subject", "Repeated", "--date", DATE, "--", "README.md", env=env)
    assert_landed(result)
    commits = of(calls(), "commit")
    assert len(commits) == 4
    assert all(call[2][-4:] == ["--date", DATE, "--", "README.md"] for call in commits)
    assert dates(git, project, environment)[0] == DATE


def test_a_dated_commit_a_hook_refused_lands_with_its_date_on_the_next_run(run_commit, project, git, environment):
    before = head(git, project, environment)
    hook = project / ".git" / "hooks" / "pre-commit"
    hook.parent.mkdir(exist_ok=True)
    hook.write_text("#!/bin/sh\necho 'the hook refused this commit' >&2\nexit 1\n", encoding="utf-8")
    hook.chmod(0o755)
    (project / "README.md").write_bytes(b"# An edited project\n")
    arguments = ("--subject", "Resumed", "--date", DATE, "--", "README.md")
    result = run_commit(project, *arguments)
    assert result.stderr == b"Error: git commit exited 1: the hook refused this commit\n"
    assert head(git, project, environment) == before
    assert staged(git, project, environment) == ["README.md"]
    hook.unlink()
    assert_landed(run_commit(project, *arguments))
    assert dates(git, project, environment)[0] == DATE


def test_a_dated_call_none_of_whose_paths_changed_is_the_no_op(run_commit, project, git, environment, logged):
    env, calls = logged()
    before = head(git, project, environment)
    result = run_commit(project, "--subject", "Nothing", "--date", DATE, "--", "README.md", env=env)
    assert (result.returncode, result.stdout, result.stderr) == (0, (NO_OP_LINE + "\n").encode("utf-8"), b"")
    assert calls() == [("0", "status", ["--literal-pathspecs", "status", "--porcelain", "--", "README.md"])]
    assert head(git, project, environment) == before


# --- refusals ---------------------------------------------------------------------------


@pytest.mark.parametrize("date", ["", "   "], ids=["empty", "whitespace"])
def test_an_empty_date_is_refused_before_any_git_command(run_commit, project, git, environment, logged, date):
    env, calls = logged()
    before = head(git, project, environment)
    (project / "README.md").write_bytes(b"# An edited project\n")
    result = run_commit(project, "--subject", "Empty date", "--date", date, "--", "README.md", env=env)
    line = assert_one_error_line(result)
    assert "the date given as --date is empty" in line
    assert calls() == []
    assert head(git, project, environment) == before
    assert staged(git, project, environment) == []


def test_a_date_flag_without_its_value_is_a_usage_error(run_commit, project):
    result = run_commit(project, "--subject", "No value", "README.md", "--date")
    assert result.returncode == 2
    assert b"usage: commit.py" in result.stderr and b"expected one argument" in result.stderr


def test_a_date_git_cannot_parse_fails_the_commit_with_git_s_message_and_records_nothing(run_commit, project, git, environment, logged):
    env, calls = logged()
    before = head(git, project, environment)
    (project / "README.md").write_bytes(b"# An edited project\n")
    started = time.monotonic()
    result = run_commit(project, "--subject", "Bad date", "--date", "not a date", "--", "README.md", env=env)
    elapsed = time.monotonic() - started
    line = assert_one_error_line(result)
    assert line.startswith(f"Error: git commit exited 128 on all {commit.ATTEMPTS} attempts: ")
    assert "invalid date format: not a date" in line
    assert WINDOW <= elapsed < WINDOW + 15
    assert len(of(calls(), "commit")) == commit.ATTEMPTS
    assert head(git, project, environment) == before
    assert staged(git, project, environment) == ["README.md"]


# --- help -------------------------------------------------------------------------------


def test_the_help_text_states_the_date(run_commit, project):
    result = run_commit(project, "--help")
    assert result.returncode == 0 and result.stderr == b""
    text = " ".join(result.stdout.decode("utf-8").split())
    assert "[--date DATE]" in text
    assert "git commit --date DATE" in text
    assert "author date only" in text
    assert "committer date staying the time the commit is made" in text


def test_the_module_docstring_states_the_date():
    text = " ".join(commit.__doc__.split())
    assert '[--date DATE]' in text
    assert '"git commit --date DATE"' in text
    assert "It sets the author date only: the committer date stays the time the commit is actually made." in text


# --- every call without the option -----------------------------------------------------


def test_a_call_without_the_option_runs_exactly_the_commands_it_ran_before(run_commit, project, git, environment, logged):
    env, calls = logged()
    (project / "README.md").write_bytes(b"# An edited project\n")
    started = int(time.time())
    result = run_commit(project, "--subject", "Plain", "--body", "A body", "--", "README.md", "notes/a.md", env=env)
    finished = int(time.time())
    assert_landed(result)
    assert calls() == [
        ("0", "status", ["--literal-pathspecs", "status", "--porcelain", "--", "README.md", "notes/a.md"]),
        ("", "add", ["--literal-pathspecs", "add", "--", "README.md", "notes/a.md"]),
        ("", "commit", ["--literal-pathspecs", "commit", "-m", "Plain", "-m", "A body", "--", "README.md", "notes/a.md"]),
    ]
    _, author_time, committer_time = dates(git, project, environment)
    assert started <= author_time <= committer_time <= finished


def test_a_removal_without_the_option_runs_exactly_the_commands_it_ran_before(run_commit, project, git, environment, logged):
    env, calls = logged()
    result = run_commit(project, "--subject", "Removed", "--remove", "milestones/first/", env=env)
    assert_landed(result)
    assert [call[1:] for call in calls()] == [
        ("status", ["--literal-pathspecs", "status", "--porcelain", "--", "milestones/first/"]),
        ("ls-files", ["--literal-pathspecs", "ls-files", "--", "milestones/first/"]),
        ("rm", ["--literal-pathspecs", "rm", "-r", "-q", "--", "milestones/first/"]),
        ("commit", ["--literal-pathspecs", "commit", "-m", "Removed", "--", "milestones/first/"]),
    ]
