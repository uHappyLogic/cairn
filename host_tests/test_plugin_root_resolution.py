"""The plugin-root resolution test: one dispatch-free headless process of the chosen host, the
submit-task skill run in a seeded repository, whose records assert separately that the
orchestrator read a shared procedure at the installed copy's root and ran a python3 tool
command there.

The skill is the vehicle because its steps make both acts mandatory and dispatch no agent:
step 0 follows the shared resolve-milestone procedure, step 4 reads the shared task format,
and step 6 runs the task-list tool's `insert` in one shell call, every path rendered under the
plugin root. The run prints its records in the host's machine-readable output mode, each tool
call with its parameters and whether it completed or failed, so the evidence is the host's own
record of the orchestrator's calls, never a transcript file or the final message. The records
are read only through the chosen host's entry, whose parser holds that host's tool names and
record shapes, so nothing here names a host.

No dispatched agent's resolution is asserted here: the agents' own reads and commands are the
dispatch tests' business, and this process is asserted to have dispatched none.
"""

import shlex

# The one issue the skill is asked to queue: inside the fixture milestone's scope, distinct
# from the fixture's own task, and concrete enough to be authored without a question back.
ISSUE = (
    "Reject an expense whose amount is zero or negative with a one-line error and a non-zero "
    "exit status, so the ledger never records a non-expense; verify by adding an entry with "
    "amount 0 and checking the error line and the exit status."
)
# The fixture milestone, by the path the seeded copy holds it under, written as the required
# `--milestone <path>` takes it, trailing slash included, and its task list.
FIXTURE_MILESTONE = "milestones/milestone_01_pocket-ledger-foundations/"
FIXTURE_TASKS_TODO = FIXTURE_MILESTONE + "TASKS_TODO.md"
# What the chained insert call prints: nothing (the tool is silent on success) or the call's
# own success line.
INSERT_OUTPUTS = ("", "submission commit landed")


def _dequoted_lines(command):
    """Each line of a shell command, as written and, where it splits, with its words' shell
    quoting removed and rejoined by single spaces, so a tool path the runner quoted (the plugin
    root in single or double quotes) reads as the bare path the prefixes name. A line that does
    not split, a quote left open across lines, is kept only as written."""
    lines = []
    for line in command.replace("\\\n", "").split("\n"):
        lines.append(line)
        try:
            lines.append(" ".join(shlex.split(line)))
        except ValueError:
            pass
    return lines


def test_the_orchestrator_reads_and_runs_at_the_installed_plugin_root(seeded_repo, host, run_host, plugin_root):
    located, root = plugin_root
    repository = seeded_repo()

    completed = run_host(f"/cairn:submit-task --milestone {FIXTURE_MILESTONE} {ISSUE}", cwd=repository)
    assert completed.returncode == 0, completed.stderr
    records = host.records(completed.stdout)
    assert records.succeeded, records.closing
    calls = records.calls

    # Dispatch-free: every call below is the orchestrator's own.
    dispatched = [call.name for call in calls if call.kind == "dispatch"]
    assert dispatched == [], dispatched

    # The orchestrator read a shared procedure at the installed root.
    reads = [(call.path, call.completed) for call in calls if call.kind == "read"]
    shared_prefix = str(root / "shared") + "/"
    shared_reads = sorted(path for path, done in reads if done and path.startswith(shared_prefix))
    assert shared_reads, f"no completed file read under {shared_prefix}; the reads were {reads}"

    # The orchestrator ran a python3 tool command there: the task-list tool's insert, under
    # the root in either form it meets it in, its path bare or shell-quoted, whose output is
    # the chained call's own success line or nothing, never an interpreter failing to open the
    # tool.
    commands = [call for call in calls if call.kind == "shell"]
    tool_prefixes = tuple(f"python3 {form}/tools/" for form in (located, root))
    inserts = [
        call
        for call in commands
        if call.completed
        and any(
            any(prefix in line for prefix in tool_prefixes) and "task_list.py insert" in line
            for line in _dequoted_lines(call.command)
        )
    ]
    assert inserts, (
        f"no completed shell call running task_list.py insert under {located}/tools/; "
        f"the commands were {[call.command for call in commands]}"
    )
    outputs = [call.output for call in inserts]
    assert any(output in INSERT_OUTPUTS for output in outputs), outputs

    # The tool at that root did the insert: the seeded task list gained its second section.
    todo = (repository / FIXTURE_TASKS_TODO).read_text(encoding="utf-8")
    assert todo.count("\n## ") == 2, todo
