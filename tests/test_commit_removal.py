"""The commit tool's removal input: each path given as a repeatable --remove is removed by
"git rm -r -q -- PATH", one more git write inside the retry schedule, before the other named
paths are staged, and one commit with the removals and those paths as its pathspec records
them together and nothing else. Git runs through a logging wrapper put first on PATH, so every
test sees the git commands the tool really ran; the lock tests hold a real index.lock, and the
repeat test has the wrapper fail the removal itself with 128 a set number of times. A call
without the option runs exactly the commands it ran before the option existed."""

import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

import commit

COMMIT_TOOL = Path(commit.__file__).resolve()
NO_OP_LINE = "Nothing committed — none of the paths changed."
WINDOW = (commit.ATTEMPTS - 1) * commit.PAUSE

FILES = {
    "README.md": b"# A project\n",
    "notes/a.md": b"a\n",
    "notes/b.md": b"b\n",
    "milestones/first/requirements.md": b"# First\n",
    "milestones/first/TASKS_TODO.md": b"# TASKS TODO\n",
    "milestones/firstly/requirements.md": b"# Firstly\n",
    "milestones/second/requirements.md": b"# Second\n",
}
FIRST = ["milestones/first/TASKS_TODO.md", "milestones/first/requirements.md"]


@pytest.fixture
def project(repo):
    """A repository whose initial commit holds README.md, two notes, and three milestone
    directories, one of them sharing the first's name as a prefix."""
    return repo({}, files=dict(FILES))


@pytest.fixture
def logged(tmp_path, environment):
    """The environment with git replaced on PATH by a wrapper that logs every call, its
    GIT_OPTIONAL_LOCKS value and its whole argument list, and then runs the real git; a
    subcommand named in failures exits 128 that many times first: logged(failures={"rm": 2})
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
            f'for word in "$@"; do printf \'\\037%s\' "$word"; done; printf \'\\n\'; }} >> {shlex.quote(str(log))}',
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
            for line in log.read_text(encoding="utf-8").splitlines():
                locks, subcommand, *arguments = line.split("\037")
                logged_calls.append((locks, subcommand, arguments))
            return logged_calls

        def reset():
            if log.exists():
                log.unlink()

        calls.reset = reset
        return env, calls

    return build


def subcommands(calls):
    return [call[1] for call in calls]


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


def status(git, root, environment):
    return sorted(git(root, environment, "status", "--porcelain").splitlines())


def message(git, root, environment):
    raw = git(root, environment, "cat-file", "commit", "HEAD")
    return raw.split("\n\n", 1)[1]


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


# --- the removal ------------------------------------------------------------------------


@pytest.mark.parametrize("removal", ["milestones/first", "milestones/first/"], ids=["bare", "trailing-slash"])
def test_a_removal_alone_lands_as_one_commit_that_removes_the_directory(run_commit, project, git, environment, removal):
    before = head(git, project, environment)
    body = "First\n\n- a bullet\n- another bullet"
    result = run_commit(project, "--subject", "Milestone-finish: milestones/first/", "--body", body, "--remove", removal)
    assert_landed(result)
    assert git(project, environment, "rev-parse", "HEAD~1").strip() == before
    assert changes(git, project, environment) == deleted(FIRST)
    assert message(git, project, environment) == "Milestone-finish: milestones/first/\n\n" + body + "\n"
    assert not (project / "milestones" / "first").exists()
    assert (project / "milestones" / "firstly" / "requirements.md").read_bytes() == b"# Firstly\n"
    assert (project / "milestones" / "second" / "requirements.md").read_bytes() == b"# Second\n"
    assert status(git, project, environment) == []


def test_the_removal_and_the_named_paths_land_in_one_commit_and_nothing_else(run_commit, project, git, environment):
    before = head(git, project, environment)
    (project / "README.md").write_bytes(b"# An edited project\n")
    (project / "notes" / "a.md").write_bytes(b"a changed, never named\n")
    (project / "notes" / "b.md").write_bytes(b"b changed and staged\n")
    git(project, environment, "add", "--", "notes/b.md")
    (project / "untracked.txt").write_bytes(b"left alone\n")
    result = run_commit(project, "--subject", "Together", "--remove", "milestones/first/", "--", "README.md")
    assert_landed(result)
    assert git(project, environment, "rev-parse", "HEAD~1").strip() == before
    assert changes(git, project, environment) == sorted(deleted(FIRST) + ["M\tREADME.md"])
    assert staged(git, project, environment) == ["notes/b.md"]
    assert status(git, project, environment) == sorted([" M notes/a.md", "M  notes/b.md", "?? untracked.txt"])


def test_the_removal_runs_before_the_stage_and_the_commit_names_the_paths_and_the_removal(run_commit, project, git, environment, logged):
    env, calls = logged()
    (project / "README.md").write_bytes(b"# An edited project\n")
    result = run_commit(project, "--subject", "Ordered", "--remove", "milestones/first/", "--", "README.md", env=env)
    assert_landed(result)
    logged_calls = calls()
    assert subcommands(logged_calls) == ["status", "ls-files", "rm", "add", "commit"]
    assert [locks for locks, _, _ in logged_calls[:2]] == ["0", "0"]
    assert of(logged_calls, "status")[0][2] == ["--literal-pathspecs", "status", "--porcelain", "--", "README.md", "milestones/first/"]
    assert of(logged_calls, "rm")[0][2] == ["--literal-pathspecs", "rm", "-r", "-q", "--", "milestones/first/"]
    assert of(logged_calls, "add")[0][2] == ["--literal-pathspecs", "add", "--", "README.md"]
    assert of(logged_calls, "commit")[0][2] == ["--literal-pathspecs", "commit", "-m", "Ordered", "--", "README.md", "milestones/first/"]


def test_a_removal_alone_stages_nothing_else(run_commit, project, git, environment, logged):
    env, calls = logged()
    result = run_commit(project, "--subject", "Alone", "--remove", "milestones/first/", env=env)
    assert_landed(result)
    assert subcommands(calls()) == ["status", "ls-files", "rm", "commit"]
    assert of(calls(), "commit")[0][2][-2:] == ["--", "milestones/first/"]


def test_each_repeated_removal_is_its_own_rm_in_the_order_given_and_one_commit_records_them_all(run_commit, project, git, environment, logged):
    env, calls = logged()
    result = run_commit(
        project, "--subject", "Two removals", "--remove", "milestones/second", "--remove", "milestones/first/", env=env
    )
    assert_landed(result)
    assert [call[2][-1] for call in of(calls(), "rm")] == ["milestones/second", "milestones/first/"]
    assert len(of(calls(), "commit")) == 1
    assert changes(git, project, environment) == deleted(FIRST + ["milestones/second/requirements.md"])
    assert (project / "milestones" / "firstly").is_dir()


def test_a_removal_beside_a_path_file_lands_in_one_commit(run_commit, project, git, environment, tmp_path):
    (project / "README.md").write_bytes(b"# An edited project\n")
    (project / "notes" / "a.md").write_bytes(b"a changed\n")
    path_file = tmp_path / "paths.txt"
    path_file.write_bytes(b"README.md\nnotes/a.md\n")
    result = run_commit(project, "--subject", "From a file", "--path-file", str(path_file), "--remove", "milestones/first/")
    assert_landed(result)
    assert changes(git, project, environment) == sorted(deleted(FIRST) + ["M\tREADME.md", "M\tnotes/a.md"])


def test_untracked_files_under_a_removed_path_stay_in_place_and_out_of_the_commit(run_commit, project, git, environment):
    stray = project / "milestones" / "first" / "scratch.txt"
    stray.write_bytes(b"never tracked\n")
    result = run_commit(project, "--subject", "Untracked left", "--remove", "milestones/first/")
    assert_landed(result)
    assert changes(git, project, environment) == deleted(FIRST)
    assert stray.read_bytes() == b"never tracked\n"
    assert status(git, project, environment) == ["?? milestones/first/"]


def test_a_tracked_file_deleted_by_hand_under_the_removal_is_recorded_as_removed(run_commit, project, git, environment):
    (project / "milestones" / "first" / "TASKS_TODO.md").unlink()
    result = run_commit(project, "--subject", "Partly gone", "--remove", "milestones/first/")
    assert_landed(result)
    assert changes(git, project, environment) == deleted(FIRST)
    assert not (project / "milestones" / "first").exists()


# --- the retry --------------------------------------------------------------------------


def test_a_lock_released_within_the_window_lets_the_removal_land(project, git, environment, logged):
    env, calls = logged()
    lock = project / ".git" / "index.lock"
    lock.write_bytes(b"")
    process = subprocess.Popen(
        [sys.executable, "-B", str(COMMIT_TOOL), "--subject", "Released", "--remove", "milestones/first/"],
        cwd=str(project),
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        deadline = time.monotonic() + WINDOW
        while len(of(calls(), "rm")) < 2 and time.monotonic() < deadline:
            time.sleep(0.02)
        assert len(of(calls(), "rm")) >= 2, "the removal was not repeated while the lock was held"
    finally:
        lock.unlink()
    stdout, stderr = process.communicate(timeout=WINDOW + 30)
    assert (process.returncode, stdout, stderr) == (0, b"", b"")
    assert changes(git, project, environment) == deleted(FIRST)
    assert len(of(calls(), "commit")) == 1


def test_a_lock_never_released_ends_the_removal_after_the_last_attempt_with_nothing_recorded(run_commit, project, git, environment, logged):
    env, calls = logged()
    before = head(git, project, environment)
    (project / "README.md").write_bytes(b"# An edited project\n")
    (project / ".git" / "index.lock").write_bytes(b"")
    started = time.monotonic()
    result = run_commit(project, "--subject", "Held", "--remove", "milestones/first/", "--", "README.md", env=env)
    elapsed = time.monotonic() - started
    line = assert_one_error_line(result)
    assert line.startswith(f"Error: git rm exited 128 on all {commit.ATTEMPTS} attempts: ")
    assert "Unable to create '" in line and "/.git/index.lock'" in line
    assert WINDOW <= elapsed < WINDOW + 15
    logged_calls = calls()
    assert len(of(logged_calls, "rm")) == commit.ATTEMPTS
    assert of(logged_calls, "add") == [] and of(logged_calls, "commit") == []
    (project / ".git" / "index.lock").unlink()
    assert head(git, project, environment) == before
    assert staged(git, project, environment) == []
    assert all((project / path).exists() for path in FIRST)


def test_the_removal_is_repeated_on_128_while_attempts_remain(run_commit, project, git, environment, logged):
    env, calls = logged(failures={"rm": 3})
    result = run_commit(project, "--subject", "Removal repeated", "--remove", "milestones/first/", env=env)
    assert_landed(result)
    assert len(of(calls(), "rm")) == 4
    assert len(of(calls(), "commit")) == 1
    assert changes(git, project, environment) == deleted(FIRST)


def test_a_removal_git_refuses_is_passed_on_at_once_and_loses_nothing(run_commit, project, git, environment, logged):
    env, calls = logged()
    before = head(git, project, environment)
    edited = project / "milestones" / "first" / "TASKS_TODO.md"
    edited.write_bytes(b"# TASKS TODO\n\n## An uncommitted task\n")
    started = time.monotonic()
    result = run_commit(project, "--subject", "Refused", "--remove", "milestones/first/", env=env)
    elapsed = time.monotonic() - started
    line = assert_one_error_line(result)
    assert line.startswith("Error: git rm exited 1: ")
    assert "local modifications" in line and "attempts" not in line
    assert elapsed < WINDOW
    assert len(of(calls(), "rm")) == 1 and of(calls(), "commit") == []
    assert head(git, project, environment) == before
    assert edited.read_bytes() == b"# TASKS TODO\n\n## An uncommitted task\n"
    assert (project / "milestones" / "first" / "requirements.md").exists()


# --- a later run of the same call -------------------------------------------------------


def test_a_removal_left_staged_by_a_failed_commit_is_recorded_by_the_next_run(run_commit, project, git, environment, logged):
    env, calls = logged()
    before = head(git, project, environment)
    hook = project / ".git" / "hooks" / "pre-commit"
    hook.parent.mkdir(exist_ok=True)
    hook.write_text("#!/bin/sh\necho 'the hook refused this commit' >&2\nexit 1\n", encoding="utf-8")
    hook.chmod(0o755)
    (project / "README.md").write_bytes(b"# An edited project\n")
    arguments = ("--subject", "Resumed", "--remove", "milestones/first/", "--", "README.md")
    result = run_commit(project, *arguments, env=env)
    assert result.stderr == b"Error: git commit exited 1: the hook refused this commit\n"
    assert head(git, project, environment) == before
    assert staged(git, project, environment) == sorted(FIRST + ["README.md"])
    hook.unlink()
    calls.reset()
    result = run_commit(project, *arguments, env=env)
    assert_landed(result)
    assert subcommands(calls()) == ["status", "ls-files", "add", "commit"]
    assert changes(git, project, environment) == sorted(deleted(FIRST) + ["M\tREADME.md"])
    assert status(git, project, environment) == []


def test_a_landed_removal_run_again_is_the_no_op(run_commit, project, git, environment, logged):
    env, calls = logged()
    assert_landed(run_commit(project, "--subject", "Landed", "--remove", "milestones/first/"))
    landed = head(git, project, environment)
    result = run_commit(project, "--subject", "Landed", "--remove", "milestones/first/", env=env)
    assert (result.returncode, result.stdout, result.stderr) == (0, (NO_OP_LINE + "\n").encode("utf-8"), b"")
    assert subcommands(calls()) == ["status", "ls-files"]
    assert head(git, project, environment) == landed


# --- refusals and help ------------------------------------------------------------------


def test_an_empty_removal_is_refused_before_any_git_command(run_commit, project, git, environment, logged):
    env, calls = logged()
    before = head(git, project, environment)
    (project / "README.md").write_bytes(b"# An edited project\n")
    result = run_commit(project, "--subject", "Empty removal", "--remove", "", "--", "README.md", env=env)
    line = assert_one_error_line(result)
    assert "a path given as --remove is empty" in line
    assert calls() == []
    assert head(git, project, environment) == before
    assert all((project / path).exists() for path in FIRST)


def test_a_removal_flag_without_its_value_is_a_usage_error(run_commit, project):
    result = run_commit(project, "--subject", "No value", "--remove")
    assert result.returncode == 2
    assert b"usage: commit.py" in result.stderr and b"expected one argument" in result.stderr


def test_the_help_text_states_the_removal(run_commit, project):
    result = run_commit(project, "--help")
    assert result.returncode == 0 and result.stderr == b""
    text = " ".join(result.stdout.decode("utf-8").split())
    assert "--remove PATH" in text
    assert "git rm -r -q -- PATH" in text
    assert "before the other paths are staged" in text
    assert "recorded by the same commit" in text
    assert "repeatable" in text


# --- every call without the option ------------------------------------------------------


def test_a_call_without_the_option_runs_exactly_the_commands_it_ran_before(run_commit, project, git, environment, logged):
    env, calls = logged()
    (project / "README.md").write_bytes(b"# An edited project\n")
    result = run_commit(project, "--subject", "Plain", "--body", "A body", "--", "README.md", "notes/a.md", env=env)
    assert_landed(result)
    assert calls() == [
        ("0", "status", ["--literal-pathspecs", "status", "--porcelain", "--", "README.md", "notes/a.md"]),
        ("", "add", ["--literal-pathspecs", "add", "--", "README.md", "notes/a.md"]),
        ("", "commit", ["--literal-pathspecs", "commit", "-m", "Plain", "-m", "A body", "--", "README.md", "notes/a.md"]),
    ]
    assert changes(git, project, environment) == ["M\tREADME.md"]


def test_a_path_file_call_without_the_option_runs_exactly_the_commands_it_ran_before(run_commit, project, git, environment, logged, tmp_path):
    env, calls = logged()
    (project / "notes" / "a.md").write_bytes(b"a changed\n")
    path_file = tmp_path / "paths.txt"
    path_file.write_bytes(b"notes/a.md\nnotes/b.md")
    result = run_commit(project, "--subject", "From a file", "--path-file", str(path_file), env=env)
    assert_landed(result)
    assert calls() == [
        ("0", "status", ["--literal-pathspecs", "status", "--porcelain", "--", "notes/a.md", "notes/b.md"]),
        ("", "add", ["--literal-pathspecs", "add", "--", "notes/a.md", "notes/b.md"]),
        ("", "commit", ["--literal-pathspecs", "commit", "-m", "From a file", "--", "notes/a.md", "notes/b.md"]),
    ]


def test_a_no_op_without_the_option_runs_the_status_alone(run_commit, project, git, environment, logged):
    env, calls = logged()
    before = head(git, project, environment)
    result = run_commit(project, "--subject", "Nothing", "--", "README.md", env=env)
    assert (result.returncode, result.stdout, result.stderr) == (0, (NO_OP_LINE + "\n").encode("utf-8"), b"")
    assert calls() == [("0", "status", ["--literal-pathspecs", "status", "--porcelain", "--", "README.md"])]
    assert head(git, project, environment) == before


def test_a_call_naming_neither_a_path_nor_a_removal_is_still_refused(run_commit, project, logged):
    env, calls = logged()
    result = run_commit(project, "--subject", "No paths", env=env)
    line = assert_one_error_line(result)
    assert line.startswith("Error: no path is given")
    assert calls() == []
