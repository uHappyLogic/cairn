"""The inline complete-task skill's fixed call, as the committed Claude Code tree renders it, run
against another process's .git/index.lock: the one fenced block of the skill file holding the
task-list tool's move, filled as the runner fills it (the milestone directory, the task's full
heading, its bar as bullets, and the paths the task edited and created), and run under bash in a
temporary git repository seeded through the conftest factory, with another run's change staged
and an untracked file beside it. Git's own trace, written to a file, counts the attempts the
commit tool makes, so the test knows the first `git add` met the held lock before it releases
it. A lock released within the retry window lets the completion commit land carrying only its
own paths; a lock never released ends the call within a limit a little above the retry bound,
passing git's message on in the commit tool's one Error: line, with no commit. This is the
suite's one fixed call run against a held lock: the retry schedule itself is the commit tool's
and is tested in test_commit_retry.py, and the parallel test is not relied on for it."""

import os
import re
import subprocess
import time
from pathlib import Path

import pytest

import commit

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL = REPO_ROOT / "hosts" / "claude" / "skills" / "complete-task" / "SKILL.md"
FIXTURES = Path(__file__).resolve().parent / "fixtures"

MOVE_COMMAND = "/tools/task_list.py move "
COMMIT_COMMAND = "/tools/commit.py "
BAR_PLACEHOLDER = "- <criterion "
PATHS_PLACEHOLDER = "<recorded path 1> <recorded path 2>"

# <MILESTONE_DIR> as the runner fills it: the pointer's path, its trailing slash included.
MILESTONE = "milestones/milestone_03_lock-retry-fixture/"
TODO = MILESTONE + "TASKS_TODO.md"
DONE = MILESTONE + "TASKS_DONE.md"

# The golden task list's first task, its bar as the runner verified it, and the paths its work
# edited (a tracked file) and created (a new one), in the order the runner recorded them.
TASK_TITLE = "Build The Parser First"
BAR = [
    "- `src/parser.py` reads the whole file into its heading and sections",
    "- `src/parser_test.py` round-trips the golden files byte for byte",
]
EDITED = "src/parser.py"
CREATED = "src/parser_test.py"
OWN_PATHS = [EDITED, CREATED, TODO, DONE]

# Another run's work in the same tree: a staged edit and an untracked file.
STAGED_ELSEWHERE = "README.md"
UNTRACKED_ELSEWHERE = "notes.txt"

COMPLETION_COMMIT_LANDED = "completion commit landed\n"

# The retry bound is the commit tool's one schedule: a pause between every two attempts. The
# limit adds less than one more window, enough for the call's processes, so a call within it
# ran the schedule once and gave up.
WINDOW = (commit.ATTEMPTS - 1) * commit.PAUSE
LIMIT = WINDOW + 3.0

# One line of git's trace per git command run, the subcommand unquoted in current git and
# quoted in older releases.
ADD_TRACE = re.compile(r"trace: built-in: git '?add'? ")
COMMIT_TRACE = re.compile(r"trace: built-in: git '?commit'? ")


# --- extracting and filling the call --------------------------------------------------------


def fenced_blocks(text):
    """Every fenced block of a Markdown file, as the list of its lines between the fences."""
    blocks, current = [], None
    for line in text.splitlines():
        if current is None:
            if line.startswith("```"):
                current = []
        elif line.strip() == "```":
            blocks.append(current)
            current = None
        else:
            current.append(line)
    assert current is None, "an unclosed fence in the skill file"
    return blocks


def fixed_call():
    """The one fence of the rendered skill file holding the move, which also runs the commit
    tool."""
    holding = [block for block in fenced_blocks(SKILL.read_text(encoding="utf-8")) if any(MOVE_COMMAND in line for line in block)]
    assert len(holding) == 1, f"{len(holding)} fences of the skill file hold the move, not one"
    lines = holding[0]
    assert sum(COMMIT_COMMAND in line for line in lines) == 1, "the call does not run the commit tool once"
    return lines


def completion_call():
    """The call written out as the runner writes it: the template's bar bullets replaced by the
    verified bar, the two recorded-path placeholders by the task's paths, and every other
    placeholder by its value."""
    template = fixed_call()
    bullets = [index for index, line in enumerate(template) if line.startswith(BAR_PLACEHOLDER)]
    assert bullets and bullets == list(range(bullets[0], bullets[-1] + 1)), "the bar's bullets are not one run"
    lines = template[: bullets[0]] + BAR + template[bullets[-1] + 1 :]
    call = "\n".join(lines) + "\n"
    assert call.count(PATHS_PLACEHOLDER) == 1
    call = (
        call.replace(PATHS_PLACEHOLDER, f"{EDITED} {CREATED}")
        .replace("<MILESTONE_DIR>", MILESTONE)
        .replace("<Task Title>", TASK_TITLE)
    )
    assert not re.search(r"<[A-Za-z][^<>\n]*>", call), "a placeholder is left unfilled"
    return call


# --- the temporary repository and the run ---------------------------------------------------


@pytest.fixture
def project(repo, environment, git):
    """A repository whose one commit holds the golden task files at MILESTONE, the file the task
    edits, and an unrelated tracked file, with the task's edits made and another run's staged
    edit and untracked file in the tree beside them."""
    root = repo(
        {},
        files={
            TODO: (FIXTURES / "task_list_todo.md").read_bytes(),
            DONE: (FIXTURES / "task_list_done.md").read_bytes(),
            EDITED: b"def parse(text):\n    raise NotImplementedError\n",
            STAGED_ELSEWHERE: b"An unrelated tracked file.\n",
        },
    )
    (root / EDITED).write_bytes(b"def parse(text):\n    return text.split('\\n## ')\n")
    (root / CREATED).write_bytes(b"from parser import parse\n")
    (root / STAGED_ELSEWHERE).write_bytes(b"An unrelated tracked file, edited by another run.\n")
    git(root, environment, "add", "--", STAGED_ELSEWHERE)
    (root / UNTRACKED_ELSEWHERE).write_bytes(b"An untracked file.\n")
    return root


def start(project, environment, trace):
    """Start the filled call under bash from the repository root, git tracing every command it
    runs into the trace file."""
    return subprocess.Popen(
        ["bash", "-c", completion_call()],
        cwd=str(project),
        env=dict(environment, GIT_TRACE=str(trace)),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def finish(process):
    """Wait for the call to end within the limit, killing it and failing otherwise: -> (stdout,
    stderr) as text."""
    try:
        stdout, stderr = process.communicate(timeout=LIMIT)
    except subprocess.TimeoutExpired:
        process.kill()
        process.communicate()
        pytest.fail(f"the call was still running {LIMIT} seconds after it started")
    return stdout.decode("utf-8"), stderr.decode("utf-8")


def attempts(trace, pattern):
    """How many git commands of the given subcommand the trace records."""
    if not trace.exists():
        return 0
    return sum(1 for line in trace.read_text(encoding="utf-8", errors="replace").splitlines() if pattern.search(line))


def head(git, project, environment):
    return git(project, environment, "rev-parse", "HEAD").strip()


def staged(git, project, environment):
    return git(project, environment, "diff", "--cached", "--name-only").split()


# --- the template as the rendered tree holds it ---------------------------------------------


def test_the_call_chains_the_move_with_the_commit_tool_over_every_placeholder():
    lines = fixed_call()
    text = "\n".join(lines)
    assert lines[0].startswith("python3 ") and MOVE_COMMAND in lines[0] and lines[0].endswith("<<'EOF' &&")
    assert lines.index("EOF") == 1 + sum(line.startswith(BAR_PLACEHOLDER) for line in lines)
    commit_line = next(line for line in lines if COMMIT_COMMAND in line)
    assert commit_line.startswith('out="$(python3 ')
    assert '--subject "Task-completion: <Task Title>" -- ' in commit_line
    assert commit_line.endswith("<MILESTONE_DIR>/TASKS_TODO.md <MILESTONE_DIR>/TASKS_DONE.md)\" &&")
    for placeholder in ("<MILESTONE_DIR>", "<Task Title>", PATHS_PLACEHOLDER):
        assert placeholder in text
    assert "echo 'completion commit landed'" in text


# --- the call run under bash against a held lock --------------------------------------------


def test_a_lock_released_within_the_window_lets_the_commit_land_with_only_its_own_paths(
    project, environment, git, tmp_path
):
    trace = tmp_path / "git-trace.log"
    lock = project / ".git" / "index.lock"
    before = head(git, project, environment)
    lock.write_bytes(b"")
    started = time.monotonic()
    process = start(project, environment, trace)
    try:
        # The second `git add` starts only once the first has ended, and the first ran while the
        # lock was held, so two traced adds mean the lock refused one and the tool repeated it.
        while attempts(trace, ADD_TRACE) < 2 and time.monotonic() - started < WINDOW:
            time.sleep(0.02)
        repeated = attempts(trace, ADD_TRACE)
    finally:
        lock.unlink()
    stdout, stderr = finish(process)

    assert repeated >= 2, "the commit tool's git add was not repeated while the lock was held"
    assert (process.returncode, stdout, stderr) == (0, COMPLETION_COMMIT_LANDED, "")
    assert attempts(trace, COMMIT_TRACE) == 1
    assert git(project, environment, "rev-parse", "HEAD^").strip() == before
    assert git(project, environment, "log", "-1", "--format=%s").rstrip("\n") == f"Task-completion: {TASK_TITLE}"
    assert git(project, environment, "log", "-1", "--format=%b").strip() == ""
    committed = git(project, environment, "show", "--name-only", "--format=", "HEAD").split()
    assert sorted(committed) == sorted(OWN_PATHS)
    todo = git(project, environment, "show", f"HEAD:{TODO}")
    done = git(project, environment, "show", f"HEAD:{DONE}")
    assert f"## {TASK_TITLE}\n" not in todo
    assert f"## {TASK_TITLE}\n" in done and "\n".join(BAR) in done
    assert staged(git, project, environment) == [STAGED_ELSEWHERE]
    assert git(project, environment, "status", "--porcelain").splitlines() == [
        f"M  {STAGED_ELSEWHERE}",
        f"?? {UNTRACKED_ELSEWHERE}",
    ]


def test_a_lock_never_released_ends_the_call_within_the_limit_with_gits_message_and_no_commit(
    project, environment, git, tmp_path
):
    trace = tmp_path / "git-trace.log"
    lock = project / ".git" / "index.lock"
    before = head(git, project, environment)
    lock.write_bytes(b"")
    started = time.monotonic()
    process = start(project, environment, trace)
    stdout, stderr = finish(process)
    elapsed = time.monotonic() - started

    assert WINDOW <= elapsed < LIMIT
    assert process.returncode != 0
    assert stdout == ""
    lines = stderr.split("\n")
    assert len(lines) == 2 and lines[1] == "", "the call printed more than the commit tool's one Error: line"
    assert lines[0].startswith("Error: git add ")
    assert f"Unable to create '{os.path.realpath(lock)}': File exists." in lines[0]
    assert attempts(trace, ADD_TRACE) == commit.ATTEMPTS
    assert attempts(trace, COMMIT_TRACE) == 0
    assert head(git, project, environment) == before
    assert git(project, environment, "rev-list", "--count", "HEAD").strip() == "1"
    lock.unlink()
    assert staged(git, project, environment) == [STAGED_ELSEWHERE]
    # The move landed before the commit tool ran, so the completion stays in the tree for a rerun.
    assert f"## {TASK_TITLE}\n" in (project / DONE).read_text(encoding="utf-8")
    assert f"## {TASK_TITLE}\n" not in (project / TODO).read_text(encoding="utf-8")
