"""Two milestones' tasks completed in parallel in one working tree, through the two calls of the
completion interface as the committed Claude Code tree renders them: the completion agent's
step-5 fixed call, the one fenced block of the agent file holding the task-list tool's move,
which chains the move with the write of the path file, and the orchestrator's commit-from-file
call, the one fenced block of the complete-all-tasks skill file running the commit tool. Two
golden fixture milestones are seeded into one temporary git repository through the conftest
factory, each run getting its own scratch directory as each complete-all-tasks run creates its
own. For each milestone a thread makes its task's edits (a tracked file edited, a new file
created, one of them holding a space), runs the agent's call filled as the agent fills it, that
milestone's recorded paths substituted, and then runs the orchestrator's call on the path file
the agent's call left behind; the two threads meet before their agent calls and again before
their orchestrator calls, so each commit runs with the other run's whole change set uncommitted
in the tree. Each Task-completion commit is asserted to carry exactly its own paths. The test
writes no path file of its own, so a mismatch between the agent's write and the orchestrator's
read fails here, and it runs no inline complete-task call. It is not relied on for the lock
retry, which test_completion_call_lock_retry.py covers."""

import re
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, NamedTuple

REPO_ROOT = Path(__file__).resolve().parent.parent
TREE = REPO_ROOT / "hosts" / "claude"
AGENT = TREE / "agents" / "complete-task.md"
ORCHESTRATOR = TREE / "skills" / "complete-all-tasks" / "SKILL.md"

MOVE_COMMAND = "/tools/task_list.py move "
COMMIT_COMMAND = "/tools/commit.py "
BAR_PLACEHOLDER = "- <criterion "
PATH_PLACEHOLDER = "<recorded path "
PATH_FILE = "paths.txt"
PROCESSED = "processed"
UNFILLED = re.compile(r"<[A-Za-z][^<>\n]*>")

COMPLETION_COMMIT_LANDED = "completion commit landed\n"

# How long a thread waits for the other at either meeting point before the run is failed.
MEETING_TIMEOUT = 60


class Milestone(NamedTuple):
    """One milestone's run: its fixture and where it is seeded (<MILESTONE_DIR> as the runner
    fills it, the pointer's path with its trailing slash), the task its top section names and
    that task's bar as verified, the tracked file the task edits (its seeded and edited bytes),
    and the file it creates."""

    fixture: str
    directory: str
    title: str
    bar: List[str]
    edited: str
    seeded: bytes
    edit: bytes
    created: str
    creation: bytes

    @property
    def todo(self):
        return self.directory + "TASKS_TODO.md"

    @property
    def done(self):
        return self.directory + "TASKS_DONE.md"

    @property
    def recorded(self):
        """The paths the task created or edited, in the order the runner recorded them."""
        return [self.edited, self.created]

    @property
    def own_paths(self):
        return [self.edited, self.created, self.todo, self.done]

    @property
    def subject(self):
        return f"Task-completion: {self.title}"


IMPORT = Milestone(
    fixture="parallel_first",
    directory="milestones/milestone_01_ledger-import/",
    title="Add The CSV Importer",
    bar=[
        "- `src/importer.py` reads the sample export into ledger entries",
        "- `src/ledger.py` accepts the entries the importer reads",
    ],
    edited="src/ledger.py",
    seeded=b"def add(entry):\n    raise NotImplementedError\n",
    edit=b"def add(entry):\n    ENTRIES.append(entry)\n",
    created="src/importer.py",
    creation=b"import csv\n",
)

REPORT = Milestone(
    fixture="parallel_second",
    directory="milestones/milestone_02_monthly-report/",
    title="Add The Monthly Report",
    bar=[
        "- `src/report.py` prints the per-category totals of each month",
        "- `docs/monthly report.md` describes the report",
    ],
    edited="src/report.py",
    seeded=b"def report(ledger):\n    raise NotImplementedError\n",
    edit=b"def report(ledger):\n    return monthly_totals(ledger)\n",
    created="docs/monthly report.md",
    creation=b"# Monthly report\n",
)

MILESTONES = (IMPORT, REPORT)


# --- extracting and filling the two calls ---------------------------------------------------


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
    assert current is None, "an unclosed fence in a runtime file"
    return blocks


def fence_holding(path, command):
    """The one fence of the rendered file holding the given command."""
    holding = [block for block in fenced_blocks(path.read_text(encoding="utf-8")) if any(command in line for line in block)]
    assert len(holding) == 1, f"{len(holding)} fences of {path.name} hold {command.strip()!r}, not one"
    return holding[0]


def agent_template():
    return fence_holding(AGENT, MOVE_COMMAND)


def orchestrator_template():
    return fence_holding(ORCHESTRATOR, COMMIT_COMMAND)


def replace_run(lines, prefix, replacement):
    """The lines with their one run of lines opening with the prefix replaced."""
    run = [index for index, line in enumerate(lines) if line.startswith(prefix)]
    assert run and run == list(range(run[0], run[-1] + 1)), f"the lines opening {prefix!r} are not one run"
    return lines[: run[0]] + replacement + lines[run[-1] + 1 :]


def filled(lines, values):
    call = "\n".join(lines) + "\n"
    for placeholder, value in values.items():
        assert placeholder in call
        call = call.replace(placeholder, value)
    assert not UNFILLED.search(call), "a placeholder is left unfilled"
    return call


def agent_call(milestone, scratch):
    """The agent's step-5 call as the agent writes it: the bar's bullets replaced by the verified
    bar, the recorded-path lines by the task's recorded paths, one per line, and every other
    placeholder by its value."""
    lines = replace_run(agent_template(), BAR_PLACEHOLDER, milestone.bar)
    lines = replace_run(lines, PATH_PLACEHOLDER, milestone.recorded)
    return filled(
        lines,
        {"<MILESTONE_DIR>": milestone.directory, "<Task Title>": milestone.title, "<scratch dir>": str(scratch)},
    )


def orchestrator_call(milestone, scratch):
    """The orchestrator's commit call as it writes it, for the task its agent completed."""
    return filled(orchestrator_template(), {"<scratch dir>": str(scratch), "<TASK_NAME>": milestone.title})


# --- the two templates as the rendered tree holds them --------------------------------------


def test_the_agent_call_writes_the_path_file_the_orchestrator_call_commits_from():
    agent = agent_template()
    assert MOVE_COMMAND in agent[0] and agent[0].endswith("<<'EOF' &&")
    path_file_line = f'cat > "<scratch dir>/{PATH_FILE}" <<\'EOF\''
    assert agent.count(path_file_line) == 1
    path_lines = agent[agent.index(path_file_line) + 1 :]
    assert path_lines[-1] == "EOF"
    assert path_lines[-3:-1] == ["<MILESTONE_DIR>/TASKS_TODO.md", "<MILESTONE_DIR>/TASKS_DONE.md"]
    assert not any(re.search(r"\bgit\b", line) for line in agent), "the agent's call runs git"

    orchestrator = "\n".join(orchestrator_template())
    assert f'--subject "Task-completion: <TASK_NAME>" --path-file "<scratch dir>/{PATH_FILE}"' in orchestrator
    assert "echo 'completion commit landed'" in orchestrator


# --- the two runs in one tree ---------------------------------------------------------------


def complete(project, environment, run_call, milestone, scratch, meeting):
    """One run's sequence: the task's edits, then the agent's call, then the orchestrator's call
    on the path file the agent's call left, meeting the other run before each call: -> the two
    calls' (exit status, stdout, stderr)."""
    try:
        (project / milestone.edited).write_bytes(milestone.edit)
        (project / milestone.created).parent.mkdir(parents=True, exist_ok=True)
        (project / milestone.created).write_bytes(milestone.creation)
        meeting.wait()
        agent = run_call(project, environment, agent_call(milestone, scratch))
        meeting.wait()
        orchestrator = run_call(project, environment, orchestrator_call(milestone, scratch))
    except BaseException:
        meeting.abort()
        raise
    return agent, orchestrator


def test_two_milestones_completed_in_parallel_in_one_tree_commit_only_their_own_paths(
    repo, environment, git, run_call, tmp_path
):
    project = repo(
        {milestone.directory: milestone.fixture for milestone in MILESTONES},
        files={milestone.edited: milestone.seeded for milestone in MILESTONES},
    )
    initial = git(project, environment, "rev-parse", "HEAD").strip()
    scratches = []
    for index in range(len(MILESTONES)):
        scratch = tmp_path / f"scratch-{index}"
        scratch.mkdir()
        scratches.append(scratch)

    meeting = threading.Barrier(len(MILESTONES), timeout=MEETING_TIMEOUT)
    with ThreadPoolExecutor(max_workers=len(MILESTONES)) as pool:
        runs = [
            pool.submit(complete, project, environment, run_call, milestone, scratch, meeting)
            for milestone, scratch in zip(MILESTONES, scratches)
        ]
        results = [run.result() for run in runs]

    for milestone, (agent, orchestrator) in zip(MILESTONES, results):
        assert agent == (0, "", ""), milestone.title
        assert orchestrator == (0, COMPLETION_COMMIT_LANDED, ""), milestone.title

    log = git(project, environment, "log", "--format=%H %P%x09%s", f"{initial}..HEAD").splitlines()
    assert len(log) == len(MILESTONES), "not one commit per completed task"
    commits = {}
    for entry in log:
        hashes, subject = entry.split("\t", 1)
        commit, parents = hashes.split(" ", 1)
        assert len(parents.split()) == 1
        commits[subject] = commit
    assert sorted(commits) == sorted(milestone.subject for milestone in MILESTONES)

    for milestone in MILESTONES:
        commit = commits[milestone.subject]
        assert git(project, environment, "log", "-1", "--format=%b", commit).strip() == ""
        committed = git(project, environment, "show", "--name-only", "--format=", commit).splitlines()
        assert sorted(committed) == sorted(milestone.own_paths), milestone.title
        todo = git(project, environment, "show", f"{commit}:{milestone.todo}")
        done = git(project, environment, "show", f"{commit}:{milestone.done}")
        assert f"## {milestone.title}\n" not in todo
        assert f"## {milestone.title}\n" in done and "\n".join(milestone.bar) in done

    assert git(project, environment, "status", "--porcelain") == ""
    for scratch in scratches:
        assert not (scratch / PATH_FILE).exists()
        assert len(list((scratch / PROCESSED).iterdir())) == 1
