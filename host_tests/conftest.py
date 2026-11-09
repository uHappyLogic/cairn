"""Fixtures of the host suite, the on-demand pytest directory that drives the installed CLI of
one host, chosen per run, against that host's installed plugin copy.

The directory sits outside pyproject.toml's `testpaths`, so `uv run pytest` and the 3.9
floor run never reach it; it runs only when named, with the host given by the required
`--host` option: `uv run pytest host_tests --host <host>`, <host> exactly one of claude,
antigravity, or codex. Before any test, one up-front check stops the whole run with a
non-zero exit and one line when the run names no host or an unknown one, or when a
prerequisite of the named host is missing: its CLI on PATH, the installed copy that CLI
reports (Antigravity's at its fixed global path), and that copy equal, file for file, to the
host's plugin directory in the built tree. No other host's prerequisites are checked. The
suite drives the copy already installed in the user's real HOME and writes nothing to any
installation (bringing a copy up to date is the user's own act, by the host's documented
install, which the stop line names), runs every headless process at the account's default
model and effort, and bounds each by one wall-clock limit of its own, the same on every host:
a run that exceeds it is killed with its whole process group and fails its test.

The tests themselves name no host. Each reads a run's tool-call records only through the
chosen host's entry, whose parser turns that host's own record shape into one shape every test
reads (ToolCall and Records below), and words each dispatching process's prompt through the
same entry, which names the host's own dispatch mechanism (Dispatch below).
"""

import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import NamedTuple

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
# Where each host's definition and its committed built tree live, the paths the build itself
# reads from and writes to.
DEFINITIONS_DIR = REPO_ROOT / "scripts" / "hosts"
HOSTS_DIR = REPO_ROOT / "hosts"
FIXTURE_PROJECT = REPO_ROOT / "tests" / "fixtures" / "host_project"
# The fixture project's milestone container, tracked under a name the milestones tool's
# discovery pattern does not match, so this repository's own `live` never lists the fixture's
# milestone, and the name each seeded copy holds it under, where the installed skills find a
# normal root container.
FIXTURE_CONTAINER = "milestones.fixture"
SEEDED_CONTAINER = "milestones"

# The suite's one wall-clock bound on a headless run, in seconds: 20 minutes, one value for
# every host, passed by the run fixture to the subprocess it starts. No host's own time limit
# is passed on its command line, so this is the only bound on every host.
RUN_TIMEOUT = 20 * 60

# The id Claude Code's and Codex's plugin listings give the plugin installed from its own
# marketplace, both named cairn.
PLUGIN_ID = "cairn@cairn"
# Antigravity's install location, the one fixed in the repository: the global path its
# plugin root renders as, which the host loads the plugin from in every project.
ANTIGRAVITY_ROOT = "~/.gemini/config/plugins/cairn"


class CopyNotLocated(Exception):
    """The host's CLI reported no installed copy; the one argument says why."""


class ToolCall(NamedTuple):
    """One tool call of a headless run, as the chosen host's entry reads it from that host's
    own records. `kind` is "read", "shell", "dispatch", "write", or "other", the entry sorting
    the host's own tool names into them, and a call the records show doing more than one of
    these, a shell call printing a file, is read as one ToolCall of each kind it does; `name`
    is the host's own name for the tool; and
    `completed` is True when the host recorded the call as completed and False when it
    recorded it as failed or never as finished. The values the tests read are set for their
    kind alone: a read's `path`; a shell call's `command` and its `output`, what the command
    printed when the host recorded it running to a zero exit and None otherwise; and a
    dispatch's `target`, the agent as the host's records name the dispatched one, and
    `prompt`, the prompt that agent was handed."""

    kind: str
    name: str
    completed: bool
    path: str = ""
    command: str = ""
    output: str | None = None
    target: str = ""
    prompt: str = ""


class Records(NamedTuple):
    """A headless run's records, as the chosen host's entry reads them from the run's stdout:
    `succeeded`, True when the run's closing record reports success; `closing`, that closing
    record as the host printed it (None when it printed none), for a failure message; and
    `calls`, every tool call of the run's own process, in order, each a ToolCall in its final
    state."""

    succeeded: bool
    closing: object
    calls: list


class Dispatch(NamedTuple):
    """One dispatch a test has a headless process make, as the chosen host's entry words it:
    `prompt`, the process's own prompt, naming the host's dispatch mechanism and handing over
    the agent's prompt; `target`, the agent as the host's records name the dispatched one; and
    `handover`, the prompt that agent is to be handed, as the host's records hold it."""

    prompt: str
    target: str
    handover: str


class Host:
    """One host's entry. The values only the suite needs are given here, at construction:
    `cli`, the command the host's CLI is run by; `locate_copy`, taking the entry and returning
    where the installed copy the host loads stands, as the host's CLI reports it (Antigravity's
    at its fixed global path), or raising CopyNotLocated; and `remedy`, taking the entry and
    returning how the user brings that copy up to date by the host's documented install, the
    text the entry then holds as `remedy` and every one of the host's stop lines carries. Three
    more are what the tests run and read through, each None while the entry gives none, which
    fails any test reaching it before a process starts: `headless`, taking the entry and a
    prompt and returning the command line of one headless run of the host's CLI with that
    prompt, in the machine-readable output mode whose records the tests read; `records`,
    taking the entry and a run's stdout and returning its Records, the host's record parser,
    which holds the host's own read, shell, dispatch, and write tool names and its way of
    telling a completed call from a failed one; and `dispatch`, taking the entry, an agent's
    name, a short label for the dispatch, and the agent's prompt, and returning the Dispatch
    that names the host's own dispatch mechanism. `installed_root` is None until the
    prerequisite check has located the copy, and then that copy's root as the suite reaches it.
    The values the host's definition already declares are read from
    scripts/hosts/<name>/settings.toml with tomllib and never restated: `name`, the definition
    directory's name, which names the host as the build does; `plugin_name`; `plugin_dir`;
    `built_tree`, the committed hosts/<name>/ tree the build renders; and `plugin_tree`, the
    directory plugin_dir names inside it, the one an installed copy holds."""

    def __init__(self, name, *, cli, locate_copy, remedy, headless=None, records=None, dispatch=None):
        with open(DEFINITIONS_DIR / name / "settings.toml", "rb") as settings_file:
            settings = tomllib.load(settings_file)
        self.name = name
        self.plugin_name = settings["plugin_name"]
        self.plugin_dir = settings["plugin_dir"]
        self.built_tree = HOSTS_DIR / name
        self.plugin_tree = self.built_tree / self.plugin_dir
        self.cli = cli
        self.locate_copy = locate_copy
        self.remedy = remedy(self)
        self._headless = headless
        self._records = records
        self._dispatch = dispatch
        self.installed_root = None

    def _given(self, value, what):
        if value is None:
            pytest.fail(f"the {self.name} entry gives no {what}", pytrace=False)
        return value

    def headless_command(self, prompt):
        """The command line of one headless run with the prompt."""
        return self._given(self._headless, "headless command")(self, prompt)

    def records(self, stdout):
        """The Records of a run that printed stdout."""
        return self._given(self._records, "record parser")(self, stdout)

    def dispatch(self, agent, label, prompt):
        """The Dispatch of the named agent, labelled, handed the prompt."""
        return self._given(self._dispatch, "dispatch wording")(self, agent, label, prompt)


def _tree_files(root):
    """Every file under root, keyed by its path relative to root."""
    files = {}
    for directory, _, names in os.walk(root):
        for name in names:
            path = Path(directory) / name
            files[path.relative_to(root).as_posix()] = path
    return files


def _plugin_tree_label(host):
    """The host's plugin directory in the built tree, repo-relative with its trailing slash."""
    return f"{host.plugin_tree.relative_to(REPO_ROOT).as_posix()}/"


def _plugin_listing(host):
    """What `<cli> plugin list --json` prints, parsed: the listing Claude Code and Codex both
    give in JSON, never read from their text tables."""
    command = [host.cli, "plugin", "list", "--json"]
    shown = " ".join(command)
    completed = subprocess.run(
        command,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode != 0:
        detail = " ".join(completed.stderr.split()) or f"exit code {completed.returncode}"
        raise CopyNotLocated(f"`{shown}` failed: {detail}")
    try:
        return json.loads(completed.stdout)
    except ValueError:
        raise CopyNotLocated(f"`{shown}` printed no JSON listing") from None


def _claude_copy(host):
    """The copy Claude Code loads in a repository outside any recorded project: the
    cairn@cairn entry of its listing that records no projectPath, since the project and local
    scopes each record the project they apply to, read from its readFromFolder when that is
    set (a directory-marketplace install) and otherwise from its installPath."""
    listing = _plugin_listing(host)
    for entry in listing if isinstance(listing, list) else []:
        if not isinstance(entry, dict):
            continue
        if entry.get("id") == PLUGIN_ID and "projectPath" not in entry:
            root = entry.get("readFromFolder") or entry.get("installPath")
            if root:
                return root
    raise CopyNotLocated(
        f"`{host.cli} plugin list --json` reports no {PLUGIN_ID} install "
        "at a scope outside any project"
    )


def _codex_copy(host):
    """The copy Codex loads: the cache directory of the cairn@cairn version its listing reports
    installed, ~/.codex/plugins/cache/cairn/cairn/<version>."""
    listing = _plugin_listing(host)
    installed = listing.get("installed") if isinstance(listing, dict) else None
    for entry in installed if isinstance(installed, list) else []:
        if not isinstance(entry, dict):
            continue
        if entry.get("pluginId") == PLUGIN_ID and entry.get("installed", True):
            version = entry.get("version")
            if version:
                return f"~/.codex/plugins/cache/cairn/cairn/{version}"
    raise CopyNotLocated(f"`{host.cli} plugin list --json` reports no {PLUGIN_ID} installed")


def _antigravity_copy(host):
    """The copy Antigravity loads, at the fixed global path its CLI lists the plugin under."""
    return ANTIGRAVITY_ROOT


def _cli_on_path(host):
    if shutil.which(host.cli) is None:
        return f"{host.cli} is not resolvable on PATH; put {host.cli} on PATH and {host.remedy}"
    return None


def _copy_located(host):
    try:
        host.installed_root = host.locate_copy(host)
    except CopyNotLocated as reason:
        return f"{reason}; {host.remedy}"
    return None


def _copy_present(host):
    if not Path(os.path.expanduser(host.installed_root)).is_dir():
        return f"no plugin copy at {host.installed_root}; {host.remedy}"
    return None


def _copy_matches_built_tree(host):
    built = _tree_files(host.plugin_tree)
    installed = _tree_files(Path(os.path.expanduser(host.installed_root)))
    for relative in sorted(set(built) | set(installed)):
        if (
            relative not in built
            or relative not in installed
            or built[relative].read_bytes() != installed[relative].read_bytes()
        ):
            return (
                f"the plugin copy at {host.installed_root} differs from "
                f"{_plugin_tree_label(host)} at {relative}; {host.remedy}"
            )
    return None


def _json_lines(stdout):
    """Every JSON record a run printed, one per non-empty stdout line."""
    return [json.loads(line) for line in stdout.splitlines() if line.strip()]


# Claude Code's tool names by kind, as its tool_use blocks name them. The file-reading tool maps
# to the input key holding its path, and each shell tool, Bash and the two that also run a
# command line (Monitor, PowerShell), to the key holding its command line. The dispatch tools
# are every tool that starts or resumes an agent: Agent, which takes the agent's registry name
# as subagent_type and its prompt as prompt, Task, the name an earlier version gave it and the
# session's tool list still carries, SendMessage, which resumes a finished agent, and Workflow,
# which runs agents from a script. The write tools are every tool that writes or edits a file.
CLAUDE_READ_TOOLS = {"Read": "file_path"}
CLAUDE_SHELL_TOOLS = {"Bash": "command", "Monitor": "command", "PowerShell": "command"}
CLAUDE_DISPATCH_TOOLS = {"Agent", "Task", "SendMessage", "Workflow"}
CLAUDE_WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
# The commands a shell call prints a file through, each mapped to its options that take a
# value. With permission checks bypassed, the mode every run of the suite uses, the host
# directs the session to read files through the shell with cat, head, or sed -n, and a session
# following a skill reads the plugin's shared procedures that way rather than with Read, so
# each file one of these commands names is also a read by the shell call that ran it. sed
# counts only when -n keeps it from printing anything but what its script selects.
CLAUDE_FILE_PRINTERS = {"cat": set(), "head": {"-n", "-c"}, "tail": {"-n", "-c"}, "sed": {"-e", "-f"}}
# The characters a shell splits words and operators at, the operator-only tokens holding a <
# or > being redirections and the rest the operators that end one simple command.
SHELL_PUNCTUATION = "();<>|&"
SHELL_ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=")


def _shell_operands(arguments, valued):
    """The operands among a simple command's arguments: every argument after a lone `--`, and
    before it every one that is not an option (an argument of two or more characters opening
    with `-`) or the value of an option in `valued`; a lone `-`, standard input, is none."""
    operands = []
    index = 0
    while index < len(arguments):
        argument = arguments[index]
        if argument == "--":
            operands.extend(arguments[index + 1 :])
            break
        if argument.startswith("-") and len(argument) > 1:
            index += 2 if argument in valued else 1
            continue
        if argument != "-":
            operands.append(argument)
        index += 1
    return operands


def _printed_by(words):
    """The files one simple command, given as its words, prints through cat, head, tail, or
    sed -n, each as the command names it."""
    while words and SHELL_ASSIGNMENT.match(words[0]):
        words = words[1:]
    if not words:
        return []
    program = words[0].rsplit("/", 1)[-1]
    if program not in CLAUDE_FILE_PRINTERS:
        return []
    arguments = words[1:]
    operands = _shell_operands(arguments, CLAUDE_FILE_PRINTERS[program])
    if program != "sed":
        return operands
    options = [argument for argument in arguments if argument.startswith("-") and argument != "--"]
    quiet = any(
        option in ("--quiet", "--silent") or (not option.startswith("--") and "n" in option)
        for option in options
    )
    if not quiet:
        return []
    scripted = any(option in ("-e", "-f") for option in options)
    return operands if scripted else operands[1:]


def _claude_printed_files(command):
    """The files a shell command line prints through cat, head, tail, or sed -n, each as the
    command names it, in order. The command is split one line at a time, its backslash-newline
    continuations joined and each heredoc's body skipped, into simple commands at the shell's
    operators, each redirection and its target dropped; a line that does not split, a quote
    left open across lines, names none, so no file is counted that the command did not name."""
    files = []
    delimiters = []
    for line in command.replace("\\\n", "").split("\n"):
        if delimiters:
            if line.strip() == delimiters[0]:
                delimiters.pop(0)
            continue
        lexer = shlex.shlex(line, posix=True, punctuation_chars=SHELL_PUNCTUATION)
        lexer.whitespace_split = True
        try:
            tokens = list(lexer)
        except ValueError:
            continue
        words = []
        index = 0
        while index < len(tokens):
            token = tokens[index]
            if token and all(character in SHELL_PUNCTUATION for character in token):
                if "<" in token or ">" in token:
                    target = tokens[index + 1] if index + 1 < len(tokens) else ""
                    if token == "<<" and target:
                        delimiters.append(target.removeprefix("-"))
                    if words and words[-1].isdigit():
                        words.pop()
                    index += 2
                    continue
                files.extend(_printed_by(words))
                words = []
            else:
                words.append(token)
            index += 1
        files.extend(_printed_by(words))
    return files


def _claude_result_text(result):
    """A tool_result block's content as text: a string as it stands, a list of content blocks
    by their text joined."""
    content = result.get("content")
    if isinstance(content, list):
        return "\n".join(block.get("text") or "" for block in content if isinstance(block, dict))
    return content or ""


def _claude_command_output(result, detail):
    """A completed shell call's printed output. The record carrying the call's tool_result also
    carries, as tool_use_result, what the command printed on stdout and stderr, an empty print
    included; the tool_result's own content stands in for a print with no output, so it is read
    only where that record carries no such detail."""
    if isinstance(detail, dict) and isinstance(detail.get("stdout"), str):
        printed = (detail["stdout"], detail.get("stderr") or "")
        return "\n".join(part.strip() for part in printed if part.strip())
    return _claude_result_text(result).strip()


def _claude_calls(use, answered):
    """The ToolCalls of one tool_use block, given the (tool_result block, tool_use_result detail)
    pair that answered it, or None when none did. A call answered with no is_error set is
    completed; one answered with is_error set, which a shell call's non-zero exit gives, failed,
    and one never answered never finished. A shell call is followed by one read per file its
    command prints (CLAUDE_FILE_PRINTERS), each completed as the call is, and an Agent or Task
    call is one dispatch, by its subagent_type and prompt."""
    name = use.get("name") or ""
    parameters = use.get("input") or {}
    completed = answered is not None and not answered[0].get("is_error")
    if name in CLAUDE_READ_TOOLS:
        return [ToolCall("read", name, completed, path=parameters.get(CLAUDE_READ_TOOLS[name]) or "")]
    if name in CLAUDE_SHELL_TOOLS:
        output = _claude_command_output(*answered) if completed else None
        command = parameters.get(CLAUDE_SHELL_TOOLS[name]) or ""
        reads = [ToolCall("read", name, completed, path=path) for path in _claude_printed_files(command)]
        return [ToolCall("shell", name, completed, command=command, output=output), *reads]
    if name in CLAUDE_DISPATCH_TOOLS:
        return [
            ToolCall(
                "dispatch",
                name,
                completed,
                target=parameters.get("subagent_type") or "",
                prompt=parameters.get("prompt") or "",
            )
        ]
    if name in CLAUDE_WRITE_TOOLS:
        return [ToolCall("write", name, completed)]
    return [ToolCall("other", name, completed)]


def _claude_records(host, stdout):
    """Claude Code's `--output-format stream-json` records, read into Records. The run prints
    one JSON record per line: `assistant` records whose message content holds the session's
    tool_use blocks, `user` records whose content holds the tool_result block answering each by
    its tool_use_id, and system and rate-limit records between them. It closes on a `result`
    record whose subtype is success and whose is_error is false when the run succeeded; a
    session woken again by a background agent's ending prints a further result, so the closing
    record is the last one printed. The records of every dispatched agent are printed in the
    same stream, each carrying the dispatch's tool_use id as its parent_tool_use_id, so only the
    records with none are the run's own process."""
    printed = _json_lines(stdout)
    closing = printed[-1] if printed else None
    succeeded = (
        isinstance(closing, dict)
        and closing.get("type") == "result"
        and closing.get("subtype") == "success"
        and not closing.get("is_error")
    )
    uses = []
    answers = {}
    for record in printed:
        if not isinstance(record, dict) or record.get("parent_tool_use_id") is not None:
            continue
        content = (record.get("message") or {}).get("content")
        if not isinstance(content, list):
            continue
        blocks = [block for block in content if isinstance(block, dict)]
        if record.get("type") == "assistant":
            uses.extend(block for block in blocks if block.get("type") == "tool_use")
        elif record.get("type") == "user":
            results = [block for block in blocks if block.get("type") == "tool_result"]
            detail = record.get("tool_use_result") if len(results) == 1 else None
            for result in results:
                answers[result.get("tool_use_id")] = (result, detail)
    calls = [call for use in uses for call in _claude_calls(use, answers.get(use.get("id")))]
    return Records(succeeded, closing, calls)


def _claude_dispatch(host, agent, label, prompt):
    """A dispatch through the Agent tool: subagent_type the agent's registry name under the
    plugin's namespace, `<plugin_name>:<agent>`, the name its records give the dispatched agent,
    description the label, and prompt the agent's prompt alone, handed over unchanged."""
    target = f"{host.plugin_name}:{agent}"
    return Dispatch(
        prompt=(
            f"Use the Agent tool once, with subagent_type `{target}`, description `{label}`, and "
            "prompt exactly the text below the blank line. Dispatch nothing else, carry out no "
            "part of the work yourself, and wait for that agent's final message before you end; "
            "then end with no further action.\n\n"
            f"{prompt}"
        ),
        target=target,
        handover=prompt,
    )


# Antigravity's tool names by kind, as its step records name them. Each file-reading tool maps
# to the parameter holding its path: the session's tool is read_file (its path in Path), and
# view_file (AbsolutePath) is the name an agent's tools list grants and an earlier version
# gave the session, so both count. The shell tool maps to the parameter holding its command
# line. The dispatch tools are every tool that starts or defines an agent, and the write tools
# every tool that writes or edits a file.
ANTIGRAVITY_READ_TOOLS = {"read_file": "Path", "view_file": "AbsolutePath"}
ANTIGRAVITY_SHELL_TOOLS = {"run_command": "CommandLine"}
ANTIGRAVITY_DISPATCH_TOOLS = {"invoke_subagent", "define_subagent", "manage_subagents", "browser_subagent"}
ANTIGRAVITY_WRITE_TOOLS = {
    "write_to_file",
    "replace_file_content",
    "multi_replace_file_content",
    "notebook_edit",
    "sed_file",
}


def _antigravity_command_output(update):
    """A completed run_command step's printed output. The host wraps it as an exit-code line,
    then a `Command output:` line over what the command printed (that line and what follows
    absent when it printed nothing); a wrapper reporting a non-zero exit yields None, and an
    unwrapped output is returned as it stands."""
    output = (update.get("tool_info", {}).get("output") or "").replace("\r\n", "\n")
    if not output.startswith("Command exited with code "):
        return output.strip()
    status, _, rest = output.partition("\n")
    if status.strip() != "Command exited with code 0.":
        return None
    _, marker, printed = rest.partition("Command output:")
    return printed.strip() if marker else ""


def _antigravity_calls(update):
    """The ToolCalls one step records in its final update. The step's state tells a completed
    call, DONE, from a failed one, ERROR. A `tool` step is one call, sorted by its tool name; a
    `subagent` step, the record a dispatch through invoke_subagent ends as, is one dispatch per
    agent its subagent_info lists, by that agent's type_name and initial_prompt."""
    name = update.get("tool_name") or ""
    completed = update.get("state") == "DONE"
    if update.get("step_type") == "subagent":
        agents = update.get("subagent_info", {}).get("subagents") or [{}]
        return [
            ToolCall(
                "dispatch",
                name,
                completed,
                target=agent.get("type_name") or "",
                prompt=agent.get("initial_prompt") or "",
            )
            for agent in agents
        ]
    if update.get("step_type") != "tool":
        return []
    parameters = update.get("tool_info", {}).get("parameters", {})
    if name in ANTIGRAVITY_READ_TOOLS:
        return [ToolCall("read", name, completed, path=parameters.get(ANTIGRAVITY_READ_TOOLS[name], ""))]
    if name in ANTIGRAVITY_SHELL_TOOLS:
        output = _antigravity_command_output(update) if completed else None
        command = parameters.get(ANTIGRAVITY_SHELL_TOOLS[name], "")
        return [ToolCall("shell", name, completed, command=command, output=output)]
    if name in ANTIGRAVITY_DISPATCH_TOOLS:
        return [ToolCall("dispatch", name, completed)]
    if name in ANTIGRAVITY_WRITE_TOOLS:
        return [ToolCall("write", name, completed)]
    return [ToolCall("other", name, completed)]


def _antigravity_records(host, stdout):
    """Antigravity's `--output-format stream-json` records, read into Records. The run prints
    `step_update` events, several per step index as the step moves through its states, and
    closes on a `result` event whose status is SUCCESS when the run succeeded. Each step is
    read in its last update, its final state; only the dispatching process's own steps are
    printed, never a dispatched agent's."""
    printed = _json_lines(stdout)
    closing = printed[-1] if printed else None
    succeeded = (
        isinstance(closing, dict)
        and closing.get("event") == "result"
        and closing.get("result", {}).get("status") == "SUCCESS"
    )
    final = {}
    for record in printed:
        if record.get("event") == "step_update":
            update = record["step_update"]
            final[update["step_index"]] = update
    calls = [call for index in sorted(final) for call in _antigravity_calls(final[index])]
    return Records(succeeded, closing, calls)


def _antigravity_dispatch(host, agent, label, prompt):
    """A dispatch through invoke_subagent: one Subagents entry whose TypeName is the agent's
    bare name, the name its records give the dispatched agent, whose Role is the label, and
    whose Prompt is the agent's prompt alone, handed over unchanged."""
    return Dispatch(
        prompt=(
            "Use the invoke_subagent tool with one entry in its Subagents array whose TypeName is "
            f"`{agent}`, whose Role is `{label}`, and whose Prompt is exactly the text below the "
            "blank line. Dispatch nothing else, carry out no part of the work yourself, and wait "
            "for that agent's final message before you end; then end with no further action.\n\n"
            f"{prompt}"
        ),
        target=agent,
        handover=prompt,
    )


# The checks run against the chosen host alone before any test, in order, each taking its
# entry and returning None or the one line's reason and remedy, the first missing one
# stopping the run: the CLI found on PATH, the CLI asked where the installed copy is, that
# copy present, and that copy equal to the host's plugin directory in the built tree file for
# file, a missing or extra file included. The comparison is made even when the copy the host
# loads is the built tree itself, as on a directory-marketplace install of this checkout.
PREREQUISITES = (_cli_on_path, _copy_located, _copy_present, _copy_matches_built_tree)

# One entry per host, keyed by the name `--host` takes, in the order the stop line lists them.
HOSTS = {
    "claude": Host(
        "claude",
        cli="claude",
        locate_copy=_claude_copy,
        remedy=lambda host: (
            "refresh the directory-marketplace install by running "
            f"`claude plugin marketplace add {REPO_ROOT}` and "
            f"`claude plugin install {PLUGIN_ID}`"
        ),
        # Print mode refuses stream-json output without --verbose.
        headless=lambda host, prompt: [
            host.cli,
            "-p",
            prompt,
            "--dangerously-skip-permissions",
            "--output-format",
            "stream-json",
            "--verbose",
        ],
        records=_claude_records,
        dispatch=_claude_dispatch,
    ),
    "antigravity": Host(
        "antigravity",
        cli="agy",
        locate_copy=_antigravity_copy,
        remedy=lambda host: (
            f"copy the built {_plugin_tree_label(host)} tree, or extract the release, "
            f"into {ANTIGRAVITY_ROOT}"
        ),
        headless=lambda host, prompt: [
            host.cli,
            "-p",
            prompt,
            "--dangerously-skip-permissions",
            "--output-format",
            "stream-json",
        ],
        records=_antigravity_records,
        dispatch=_antigravity_dispatch,
    ),
    "codex": Host(
        "codex",
        cli="codex",
        locate_copy=_codex_copy,
        remedy=lambda host: (
            f"re-run `codex plugin marketplace add {host.built_tree}` and "
            f"`codex plugin add {PLUGIN_ID}`"
        ),
    ),
}

ACCEPTED_HOSTS = f"{', '.join(list(HOSTS)[:-1])}, or {list(HOSTS)[-1]}"


def pytest_addoption(parser):
    parser.addoption(
        "--host",
        action="append",
        nargs="?",
        metavar="HOST",
        help=f"the host whose installed CLI and plugin copy the run drives, exactly one of "
        f"{ACCEPTED_HOSTS}; required, with no default",
    )


def chosen_host(config):
    """The entry of the one host the run names with `--host`, or None when it names none, an
    unknown one, or more than one."""
    named = config.getoption("host")
    if named is None or len(named) != 1 or named[0] not in HOSTS:
        return None
    return HOSTS[named[0]]


def _stop(reason):
    sys.stderr.write(f"host suite prerequisite missing: {reason}\n")
    sys.stderr.flush()
    return 1


def pytest_cmdline_main(config):
    """Read the run's host, then stop the whole run before any test when it names none or an
    unknown one, or when one of that host's prerequisites is missing: one line naming it on
    stderr, a non-zero exit, no per-test outcome, and never a skip. Only the named host's
    prerequisites are checked, in PREREQUISITES' order, the first missing one stopping the run.
    Returning the exit code from this hook ends the run before pytest configures its
    reporting, so that line is the run's only output; when the host is named and every one of
    its prerequisites holds, returning None lets pytest carry on as usual."""
    host = chosen_host(config)
    if host is None:
        return _stop(f"--host must name exactly one of {ACCEPTED_HOSTS}")
    for check in PREREQUISITES:
        missing = check(host)
        if missing is not None:
            return _stop(missing)
    return None


def _git(repository, *args):
    subprocess.run(
        ["git", *args],
        cwd=str(repository),
        stdin=subprocess.DEVNULL,
        capture_output=True,
        check=True,
    )


@pytest.fixture
def seeded_repo(tmp_path):
    """A fresh committed copy of the fixture project for one headless process: seeded_repo() ->
    Path. Each call copies tests/fixtures/host_project to its own directory under tmp_path,
    renames the copy's milestones.fixture/ container to milestones/, runs `git init` there, and
    makes the initial commit, so every headless process starts from the same committed tree,
    holding the fixture's milestone at milestones/<slug>/, and nothing it changes reaches the
    fixture or another process."""

    count = 0

    def build():
        nonlocal count
        count += 1
        repository = tmp_path / f"project{count}"
        shutil.copytree(FIXTURE_PROJECT, repository)
        (repository / FIXTURE_CONTAINER).rename(repository / SEEDED_CONTAINER)
        _git(repository, "init", "-q")
        _git(repository, "config", "user.name", "Host Suite")
        _git(repository, "config", "user.email", "host-suite@example.invalid")
        _git(repository, "config", "commit.gpgsign", "false")
        _git(repository, "add", "-A")
        _git(repository, "commit", "-q", "--no-verify", "-m", "Seed the fixture project")
        return repository

    return build


def _kill_group(process):
    """Kill every process of the run's group, the CLI and whatever it started, and reap the
    CLI; a group already gone is nothing to kill."""
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait()


def run_bounded(command, *, cwd, limit):
    """Run one command to its end within `limit` seconds -> CompletedProcess with decoded
    stdout and stderr. The command starts in a session of its own, so it leads a process group
    of its own that everything it starts joins. A run still going at the limit has that whole
    group killed and fails the calling test, and so does a run the test is interrupted during,
    which is killed the same way before the interruption goes on, so no run outlives the
    test that started it."""
    process = subprocess.Popen(
        command,
        cwd=str(cwd),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
        start_new_session=True,
    )
    try:
        stdout, stderr = process.communicate(timeout=limit)
    except subprocess.TimeoutExpired:
        _kill_group(process)
        _, stderr = process.communicate()
        overran = True
    except BaseException:
        _kill_group(process)
        raise
    else:
        overran = False
    if overran:
        pytest.fail(
            f"`{command[0]}` ran past the suite's run limit of {limit} seconds and was killed "
            f"with its whole process group; its stderr until then:\n{stderr}",
            pytrace=False,
        )
    return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)


@pytest.fixture
def host(request):
    """The chosen host's entry, its installed copy located by the prerequisite check: every
    test reads a run's tool-call records through its `records` and words every dispatching
    process's prompt through its `dispatch`, so no test names a host's tools, record shapes,
    or dispatch mechanism of its own."""
    return chosen_host(request.config)


@pytest.fixture
def run_host(host):
    """Run one headless process of the chosen host's CLI in a seeded repository:
    run_host("<prompt>", cwd=repository) -> CompletedProcess with decoded stdout and stderr.
    The command line is the one the chosen host's entry composes for the prompt, with no model
    or effort flag (the account's defaults), and the run is bounded by RUN_TIMEOUT, the one
    limit for every host, which no flag of the host's own adds to. It runs with the user's
    real HOME, so it drives the installed copy. A run past the limit is killed with its whole
    process group and fails its test, and an entry giving no headless command fails the test
    before any process starts."""

    def run(prompt, *, cwd):
        return run_bounded(host.headless_command(prompt), cwd=cwd, limit=RUN_TIMEOUT)

    return run


@pytest.fixture
def plugin_root(host):
    """The chosen host's installed copy's root in the two forms a run meets it in: (located,
    expanded), the root as the host's entry located it, which a rendered command may carry as
    written, and that root with a leading `~` expanded under the user's real HOME, the form an
    absolute path takes. The two are the same path when the entry located an absolute one."""
    return host.installed_root, Path(os.path.expanduser(host.installed_root))
