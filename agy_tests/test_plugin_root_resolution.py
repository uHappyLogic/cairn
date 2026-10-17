"""The plugin-root resolution test: one dispatch-free headless agy process, the submit-task
skill run in a seeded repository, whose printed output asserts separately that the
orchestrator read a shared procedure at the global ~/.gemini/config/plugins/cairn path and
ran a python3 tool command there.

The skill is the vehicle because its steps make both acts mandatory and dispatch no agent:
step 0 follows the shared get-current-milestone procedure, step 4 reads the shared task
format, and step 5 runs the task-list tool's `insert` in one shell call, every path rendered
as the tilde literal. The run's `--output-format stream-json` records each tool call with its
parameters and its DONE or ERROR state, so the evidence is the host's own record of the
orchestrator's calls, never a transcript file or the final message.

What the test pins about the tilde path: the host's file-reading tool (`view_file`) refuses a
path that starts with `~` ("must be an absolute path"), so the orchestrator reaches a shared
procedure only by expanding the rendered literal to an absolute path, while the shell expands
the same literal in a `python3` command unaided. A `view_file` call that carried a tilde path
and still ended DONE fails the test, which is the signal that this pin needs rewriting.

No dispatched agent's resolution is asserted here: the agents' own reads and commands are the
subagent probe's business, and this process is asserted to have dispatched none.
"""

import json

# The one issue the skill is asked to queue: inside the fixture milestone's scope, distinct
# from the fixture's own task, and concrete enough to be authored without a question back.
ISSUE = (
    "Reject an expense whose amount is zero or negative with a one-line error and a non-zero "
    "exit status, so the ledger never records a non-expense; verify by adding an entry with "
    "amount 0 and checking the error line and the exit status."
)
FIXTURE_TASKS_TODO = "milestones/milestone_01_pocket-ledger-foundations/TASKS_TODO.md"

# The host's tool names, the one parameter of each this test reads, and the tools that
# dispatch an agent.
FILE_READING_TOOL = "view_file"  # parameters.AbsolutePath
SHELL_TOOL = "run_command"  # parameters.CommandLine
DISPATCH_TOOLS = {"invoke_subagent", "define_subagent", "manage_subagents", "browser_subagent"}


def records_of(stdout):
    """Every stream-json record of a run, one per non-empty stdout line."""
    return [json.loads(line) for line in stdout.splitlines() if line.strip()]


def tool_steps(records):
    """The run's tool steps in order, each the last record of its step index, so every step
    read here is in its final DONE or ERROR state, never ACTIVE."""
    steps = {}
    for record in records:
        if record.get("event") != "step_update":
            continue
        update = record["step_update"]
        if update.get("step_type") == "tool":
            steps[update["step_index"]] = update
    return [steps[index] for index in sorted(steps)]


def parameter(step, name):
    return step.get("tool_info", {}).get("parameters", {}).get(name, "")


def output_of(step):
    return step.get("tool_info", {}).get("output") or ""


def test_the_orchestrator_reads_and_runs_at_the_global_plugin_root(seeded_repo, run_agy, plugin_root):
    tilde, root = plugin_root
    repository = seeded_repo()

    completed = run_agy(f"/cairn:submit-task {ISSUE}", cwd=repository, output_format="stream-json")
    assert completed.returncode == 0, completed.stderr
    records = records_of(completed.stdout)
    assert records[-1].get("event") == "result", records[-1]
    assert records[-1]["result"]["status"] == "SUCCESS", records[-1]["result"]
    steps = tool_steps(records)

    # Dispatch-free: every step below is the orchestrator's own.
    dispatched = [step["tool_name"] for step in steps if step["tool_name"] in DISPATCH_TOOLS]
    assert dispatched == [], dispatched

    # The orchestrator read a shared procedure at the global path.
    reads = [
        (parameter(step, "AbsolutePath"), step["state"])
        for step in steps
        if step["tool_name"] == FILE_READING_TOOL
    ]
    shared_prefix = str(root / "shared") + "/"
    shared_reads = sorted(path for path, state in reads if state == "DONE" and path.startswith(shared_prefix))
    assert shared_reads, f"no DONE {FILE_READING_TOOL} call under {shared_prefix}; the calls were {reads}"

    # The pin: the file-reading tool takes no tilde path. The shared procedure was reached at
    # the expanded absolute path above, and a tilde path, whenever one was tried, ended in ERROR.
    tilde_reads = [(path, state) for path, state in reads if path.startswith("~")]
    assert all(state == "ERROR" for _, state in tilde_reads), tilde_reads

    # The orchestrator ran a python3 tool command there: the task-list tool's insert, under
    # the root in either form (the shell expands the rendered tilde literal), whose output is
    # the chained call's own success line or nothing (the tool is silent on success), never an
    # interpreter failing to open the tool.
    commands = [step for step in steps if step["tool_name"] == SHELL_TOOL]
    tool_prefixes = (f"python3 {tilde}/tools/", f"python3 {root}/tools/")
    inserts = [
        step
        for step in commands
        if step["state"] == "DONE"
        and any(prefix in parameter(step, "CommandLine") for prefix in tool_prefixes)
        and "task_list.py insert" in parameter(step, "CommandLine")
    ]
    assert inserts, (
        f"no DONE {SHELL_TOOL} call running task_list.py insert under {tilde}/tools/; "
        f"the commands were {[parameter(step, 'CommandLine') for step in commands]}"
    )
    outputs = [output_of(step).strip() for step in inserts]
    assert any(output in ("", "submission commit landed") for output in outputs), outputs

    # The tool at that root did the insert: the seeded task list gained its second section.
    todo = (repository / FIXTURE_TASKS_TODO).read_text(encoding="utf-8")
    assert todo.count("\n## ") == 2, todo
