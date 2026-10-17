"""The subagent write-tool probe: two headless agy processes, each dispatching one plugin
agent directly through the host's `invoke_subagent` tool, by the bare name the plugin
registers it under and with the real prompt its orchestrator skill would pass, so no
orchestrator skill stands between the probe and the agent.

- `provide-alternatives-to-open-question` is dispatched with a fixture Short Title, the
  seeded milestone directory, and a scratch directory this test created. Its pass signal is
  the one file its contract has it land, `<scratch dir>/<Short Title>.xml`, holding
  `<alternative>` elements, with the seeded repository left exactly as committed.
- `complete-task` is dispatched with the heading of the fixture's one trivial task. Its pass
  signal is the task's deliverable landed in the seeded repository and the task's section
  moved from `TASKS_TODO.md` into `TASKS_DONE.md` in the task-list tool's rendering, with
  both task files staged and nothing committed.

Each agent reaches its files only through the write and shell tools (the alternatives agent
runs the open-question tool, writes its file, and renames it; the completion agent writes the
deliverable, runs the task-list tool's move, and stages), so a landed file is the proof those
tools were granted: an agent without them cannot land one, whatever it reports. Nothing of an
agent's final message is read or judged, and no transcript record is opened; the pass signal
is the files alone.

The process's printed `--output-format stream-json` output is read for one thing only: that
the process dispatched the named agent with that prompt and wrote no file and ran no command
of its own, so a landed file is the agent's work and not the dispatching process's. The host
records a dispatch as a `subagent` step whose `subagent_info` lists each dispatched agent's
`type_name` and `initial_prompt`; the dispatched agent's own tool calls never appear in the
dispatching process's output, so that output says nothing about the agent's work.
"""

import json
import subprocess
import xml.etree.ElementTree as ET

FIXTURE_MILESTONE = "milestones/milestone_01_pocket-ledger-foundations"
# A block of the fixture's open_questions.xml, by its Short Title.
SHORT_TITLE = "Data file format"
# The fixture's one trivial task, by its `##` heading, and the file it has the agent create.
TASK_TITLE = "Add The Project README"
TASK_DELIVERABLE = "README.md"
TASK_DELIVERABLE_HEADING = "# Pocket Ledger"

# The two plugin agents, by the bare names the plugin registers them under.
ALTERNATIVES_AGENT = "provide-alternatives-to-open-question"
COMPLETION_AGENT = "complete-task"

# The host's tools that write a file or run a command: a step of the dispatching process
# using one would be work of its own, not the agent's.
WORK_TOOLS = {
    "write_to_file",
    "replace_file_content",
    "multi_replace_file_content",
    "notebook_edit",
    "run_command",
}


def dispatch_prompt(agent, role, prompt):
    """The headless process's own prompt: dispatch one named plugin agent through the host's
    invoke_subagent tool with the real prompt its orchestrator would pass, and nothing else."""
    return (
        "Use the invoke_subagent tool with one entry in its Subagents array whose TypeName is "
        f"`{agent}`, whose Role is `{role}`, and whose Prompt is exactly the text below the blank "
        "line. Dispatch nothing else, carry out no part of the work yourself, and wait for that "
        "agent's final message before you end; then end with no further action.\n\n"
        f"{prompt}"
    )


def alternatives_prompt(milestone_dir, scratch_dir):
    """The alternatives pass's dispatch prompt, as its orchestrator skill shows it: the Short
    Title, the resolved milestone directory, and the run's scratch directory, nothing else."""
    return (
        "Enumerate the alternatives for this single open question.\n\n"
        f"Short Title: {SHORT_TITLE}\n\n"
        f"Milestone directory: {milestone_dir}\n\n"
        f"Scratch directory: {scratch_dir}"
    )


# The completion orchestrator's dispatch prompt, as complete-all-tasks shows it.
COMPLETION_PROMPT = f'Complete the task named: "{TASK_TITLE}"'


def records_of(stdout):
    """Every stream-json record of a run, one per non-empty stdout line."""
    return [json.loads(line) for line in stdout.splitlines() if line.strip()]


def step_updates(records):
    return [record["step_update"] for record in records if record.get("event") == "step_update"]


def final_steps(records):
    """The run's steps in order, each the last record of its step index, so every step read
    here is in its final state: a dispatch's index opens as an `invoke_subagent` tool step and
    ends as the `subagent` step that records what was dispatched."""
    steps = {}
    for update in step_updates(records):
        steps[update["step_index"]] = update
    return [steps[index] for index in sorted(steps)]


def dispatches(records):
    """Every dispatch the process made, as (type_name, initial_prompt), in order."""
    pairs = []
    for update in final_steps(records):
        if update.get("step_type") == "subagent":
            for entry in update.get("subagent_info", {}).get("subagents", []):
                pairs.append((entry.get("type_name"), entry.get("initial_prompt")))
    return pairs


def words_of(text):
    """The text with its whitespace runs folded, so a recorded prompt is compared on its words
    and a blank line or trailing newline the dispatching process rendered differently does
    not count as a different prompt."""
    return " ".join((text or "").split())


def own_work_tool_steps(records):
    """The names of the process's own tool steps that wrote a file or ran a command."""
    return [
        update["tool_name"]
        for update in step_updates(records)
        if update.get("step_type") == "tool" and update.get("tool_name") in WORK_TOOLS
    ]


def assert_dispatched_only(completed, agent, prompt):
    """The process ended normally, dispatched exactly the named agent with the real prompt,
    and did none of the work itself."""
    assert completed.returncode == 0, completed.stderr
    records = records_of(completed.stdout)
    made = dispatches(records)
    assert [(name, words_of(text)) for name, text in made] == [(agent, words_of(prompt))], (
        f"expected one dispatch of {agent} with the real prompt; the dispatches were {made} and "
        f"the steps were {[(step.get('step_type'), step.get('tool_name')) for step in final_steps(records)]}"
    )
    assert own_work_tool_steps(records) == [], own_work_tool_steps(records)


def git(repository, *args):
    return subprocess.run(
        ["git", *args],
        cwd=str(repository),
        stdin=subprocess.DEVNULL,
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout


def test_the_alternatives_agent_lands_its_scratch_file(seeded_repo, run_agy, tmp_path):
    repository = seeded_repo()
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    prompt = alternatives_prompt(repository / FIXTURE_MILESTONE, scratch)

    completed = run_agy(
        dispatch_prompt(ALTERNATIVES_AGENT, SHORT_TITLE, prompt),
        cwd=repository,
        output_format="stream-json",
    )
    assert_dispatched_only(completed, ALTERNATIVES_AGENT, prompt)

    # The pass signal: the agent's return file, at the path the orchestrator derives from the
    # Short Title alone, renamed into place with no temporary name left behind.
    landed = scratch / f"{SHORT_TITLE}.xml"
    assert landed.is_file(), f"no {landed.name} in {scratch}; it holds {sorted(path.name for path in scratch.iterdir())}"
    assert not (scratch / f"{SHORT_TITLE}.xml.part").exists()

    # It holds <alternative> elements and nothing else: the elements the embedding tool keys
    # on, each with its id and its advantage and drawback children.
    text = landed.read_text(encoding="utf-8")
    assert text.strip().startswith("<alternative"), text
    assert text.strip().endswith("</alternative>"), text
    elements = list(ET.fromstring(f"<root>{text}</root>"))
    assert elements, text
    assert all(element.tag == "alternative" for element in elements), [element.tag for element in elements]
    for element in elements:
        assert element.get("id"), ET.tostring(element, encoding="unicode")
        assert element.find("advantage") is not None, ET.tostring(element, encoding="unicode")
        assert element.find("drawback") is not None, ET.tostring(element, encoding="unicode")

    # Read-only toward the project: the seeded repository is exactly as committed.
    assert git(repository, "status", "--porcelain") == ""


def test_the_completion_agent_lands_the_task_and_stages_the_move(seeded_repo, run_agy):
    repository = seeded_repo()
    milestone = repository / FIXTURE_MILESTONE

    completed = run_agy(
        dispatch_prompt(COMPLETION_AGENT, "Task completer", COMPLETION_PROMPT),
        cwd=repository,
        output_format="stream-json",
    )
    assert_dispatched_only(completed, COMPLETION_AGENT, COMPLETION_PROMPT)

    # The task's deliverable, landed by the agent's file-writing tool.
    deliverable = repository / TASK_DELIVERABLE
    assert deliverable.is_file(), sorted(path.name for path in repository.iterdir())
    assert deliverable.read_text(encoding="utf-8").splitlines()[0] == TASK_DELIVERABLE_HEADING

    # The section moved by the task-list tool: gone from TASKS_TODO.md, in TASKS_DONE.md once
    # with its brief kept verbatim, the tool's **Verified:** label, and its closing separator.
    todo = (milestone / "TASKS_TODO.md").read_text(encoding="utf-8")
    done = (milestone / "TASKS_DONE.md").read_text(encoding="utf-8")
    assert "\n## " not in todo, todo
    assert done.count("\n## ") == 1 and f"\n## {TASK_TITLE}\n" in done, done
    seeded_todo = git(repository, "show", f"HEAD:{FIXTURE_MILESTONE}/TASKS_TODO.md")
    brief = seeded_todo.split(f"## {TASK_TITLE}\n", 1)[1].split("\n---", 1)[0].strip()
    assert brief in done, done
    assert "**Verified:**" in done, done
    assert done.rstrip().endswith("---"), done

    # Both task files staged by the agent, and nothing committed: the seed commit stands alone.
    staged = set(git(repository, "diff", "--cached", "--name-only").splitlines())
    task_files = {f"{FIXTURE_MILESTONE}/TASKS_TODO.md", f"{FIXTURE_MILESTONE}/TASKS_DONE.md"}
    assert task_files <= staged, staged
    assert git(repository, "rev-list", "--count", "HEAD").strip() == "1"
