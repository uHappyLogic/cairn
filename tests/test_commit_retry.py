"""The commit tool's retry: each git write is repeated while git exits with 128, the status a held
.git/index.lock produces, on one fixed schedule of about ten to twenty repeats a quarter to half
a second apart, and every other non-zero status is passed on at once. Git runs through a
logging wrapper put first on PATH, so every test counts the attempts the tool really made; the
lock tests hold a real index.lock, and the commit-write test has the wrapper fail the commit
itself with 128 a set number of times."""

import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

import commit

COMMIT_TOOL = Path(commit.__file__).resolve()

FILES = {"README.md": b"# A project\n", "notes/a.md": b"a\n"}
WINDOW = (commit.ATTEMPTS - 1) * commit.PAUSE


@pytest.fixture
def project(repo):
    """A repository whose initial commit holds README.md and notes/a.md."""
    return repo({}, files=dict(FILES))


@pytest.fixture
def logged(tmp_path, environment):
    """The environment with git replaced on PATH by a wrapper that logs every call as one
    `<GIT_OPTIONAL_LOCKS>|<subcommand>` line and then runs the real git; a subcommand named
    in failures exits 128 that many times first: logged(failures={"commit": 2}) -> (the
    environment, a function returning the logged calls as (optional locks, subcommand) pairs)."""

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
            f'printf \'%s|%s\\n\' "${{GIT_OPTIONAL_LOCKS:-}}" "$sub" >> {shlex.quote(str(log))}',
        ]
        for subcommand, count in failures.items():
            counter = shlex.quote(str(tmp_path / f"{subcommand}.failures"))
            lines += [
                f'if [ "$sub" = {shlex.quote(subcommand)} ]; then',
                f"  done_count=$(cat {counter} 2>/dev/null || echo 0)",
                f'  if [ "$done_count" -lt {count} ]; then',
                f'    echo $((done_count + 1)) > {counter}',
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
            return [tuple(line.split("|", 1)) for line in log.read_text(encoding="utf-8").splitlines()]

        return env, calls

    return build


def subcommands(calls, name):
    return [call for call in calls if call[1] == name]


def head(git, root, environment):
    return git(root, environment, "rev-parse", "HEAD").strip()


def staged(git, root, environment):
    return git(root, environment, "diff", "--cached", "--name-only").split()


def committed(git, root, environment):
    return git(root, environment, "show", "--name-only", "--format=", "HEAD").split()


def test_the_schedule_is_one_constant_within_the_decided_bounds():
    assert commit.LOCK_EXIT == 128
    assert 10 <= commit.ATTEMPTS - 1 <= 20
    assert 0.25 <= commit.PAUSE <= 0.5
    assert 3 <= WINDOW <= 5


def test_a_lock_released_within_the_window_lets_the_commit_land(project, git, environment, logged):
    env, calls = logged()
    (project / "notes" / "a.md").write_bytes(b"a changed\n")
    (project / "README.md").write_bytes(b"# An edited project\n")
    lock = project / ".git" / "index.lock"
    lock.write_bytes(b"")
    process = subprocess.Popen(
        [sys.executable, "-B", str(COMMIT_TOOL), "--subject", "Released", "--", "notes/a.md"],
        cwd=str(project),
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        deadline = time.monotonic() + WINDOW
        while len(subcommands(calls(), "add")) < 2 and time.monotonic() < deadline:
            time.sleep(0.02)
        assert len(subcommands(calls(), "add")) >= 2, "the add was not repeated while the lock was held"
    finally:
        lock.unlink()
    stdout, stderr = process.communicate(timeout=WINDOW + 30)
    assert (process.returncode, stdout, stderr) == (0, b"", b"")
    assert committed(git, project, environment) == ["notes/a.md"]
    assert git(project, environment, "log", "-1", "--format=%s").strip() == "Released"
    assert len(subcommands(calls(), "commit")) == 1


def test_a_lock_never_released_ends_after_the_last_attempt_with_gits_message(run_commit, project, git, environment, logged):
    env, calls = logged()
    before = head(git, project, environment)
    (project / "notes" / "a.md").write_bytes(b"a changed\n")
    (project / ".git" / "index.lock").write_bytes(b"")
    started = time.monotonic()
    result = run_commit(project, "--subject", "Held", "--", "notes/a.md", env=env)
    elapsed = time.monotonic() - started
    assert result.returncode == 1
    assert result.stdout == b""
    lines = result.stderr.decode("utf-8").split("\n")
    assert len(lines) == 2 and lines[1] == ""
    assert lines[0].startswith(f"Error: git add exited 128 on all {commit.ATTEMPTS} attempts: ")
    assert "Unable to create '" in lines[0] and "/.git/index.lock'" in lines[0]
    assert WINDOW <= elapsed < WINDOW + 15
    logged_calls = calls()
    assert len(subcommands(logged_calls, "add")) == commit.ATTEMPTS
    assert subcommands(logged_calls, "commit") == []
    assert subcommands(logged_calls, "status") == [("0", "status")]
    (project / ".git" / "index.lock").unlink()
    assert head(git, project, environment) == before
    assert staged(git, project, environment) == []


def test_the_commit_write_is_repeated_on_128_too(run_commit, project, git, environment, logged):
    env, calls = logged(failures={"commit": 3})
    (project / "notes" / "a.md").write_bytes(b"a changed\n")
    result = run_commit(project, "--subject", "Commit repeated", "--", "notes/a.md", env=env)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert committed(git, project, environment) == ["notes/a.md"]
    assert len(subcommands(calls(), "add")) == 1
    assert len(subcommands(calls(), "commit")) == 4


def test_any_other_failure_is_passed_on_at_once(run_commit, project, git, environment, logged, tmp_path):
    env, calls = logged()
    before = head(git, project, environment)
    runs = tmp_path / "hook-runs"
    hook = project / ".git" / "hooks" / "pre-commit"
    hook.parent.mkdir(exist_ok=True)
    hook.write_text(
        f"#!/bin/sh\necho run >> {shlex.quote(str(runs))}\necho 'the hook refused this commit' >&2\nexit 1\n",
        encoding="utf-8",
    )
    hook.chmod(0o755)
    (project / "notes" / "a.md").write_bytes(b"a changed\n")
    started = time.monotonic()
    result = run_commit(project, "--subject", "Refused", "--", "notes/a.md", env=env)
    elapsed = time.monotonic() - started
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == b"Error: git commit exited 1: the hook refused this commit\n"
    assert elapsed < WINDOW
    assert len(subcommands(calls(), "commit")) == 1
    assert runs.read_text(encoding="utf-8") == "run\n"
    assert head(git, project, environment) == before
    assert staged(git, project, environment) == ["notes/a.md"]
