"""The derive-tasks refresh test: one headless process of the chosen host, the derive-tasks skill
run on the fixture milestone in a seeded repository whose history has moved since that
milestone's starting state was recorded, asserted from the repository's git log to commit a
`Starting-state:` refresh before its `Task-derivation:` commit.

The history is built here, on top of the shared one-commit seed, through the plugin's own
tools, and only through them for every write the workflow gives a tool: the fixture
milestone's three questions answered and removed, so the derivation's open-question
precondition holds; its `Starting-state: <path>` commit, the anchor; then a second milestone in
the same root container, so its scope overlaps the first's, defined, its tasks derived and
completed, each completion committing a deliverable at the repository root with its verified
bar as the body, and finished by the `Milestone-finish: <path>` commit that removes its
directory. The second milestone is therefore finished when the host runs: the scope gate on the
first milestone is open, while the milestones tool's `since --milestones` lists the second
milestone's task and finish commits beneath the anchor, which is what sends derive-tasks into
its refresh. The deliverables contradict the first milestone's recorded starting state, which
says no documentation or configuration exists, so the refresh has a fact to change and its
commit has a change to record. Both are asserted on the built history before the host runs, so
a test that fails on the host's side never fails for a history that did not hold.

Only the git log of the seeded repository is read for the result, never the host's records
beyond whether the run ended normally, so nothing here names a host.
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
# The plugin's tools, byte-identical in every host tree, run from the source layer so the
# history is built the same way whichever host the suite drives.
TOOLS = REPO_ROOT / "core" / "tools"

# The fixture milestone, by the path the seeded copy holds it under, written as the required
# `--milestone <path>` takes it, trailing slash included.
FIXTURE_MILESTONE = "milestones/milestone_01_pocket-ledger-foundations/"
FIXTURE_REQUIREMENTS = FIXTURE_MILESTONE + "requirements.md"
FIXTURE_QUESTIONS = FIXTURE_MILESTONE + "open_questions.xml"

# The fixture's three open questions, by Short Title, each with the decision its answer folds
# into the milestone's `## Decisions`.
ANSWERS = {
    "Data file format": (
        "- **Data file format.** The data file is one JSON document holding a list of entries, "
        "each with its amount, category, and date."
    ),
    "Date input form": (
        "- **Date input form.** A date is entered as an ISO 8601 calendar date, YYYY-MM-DD, "
        "and an entry given no date takes today's."
    ),
    "Summary period selection": (
        "- **Summary period selection.** A summary covers one calendar month, named as YYYY-MM, "
        "and the current month when none is named."
    ),
}

# The fixture's starting state as its `Starting-state:` commit records it: the seed's facts,
# written in the section's subsection form.
STARTING_STATE = """\
### The repository

The repository holds only the milestone files under `milestones/`; no source code, \
configuration, or documentation exists yet.

### The ledger's environment

The ledger will be one Python 3.9+ script using the standard library alone, run from a \
terminal, keeping its data in a single file inside the user's home directory. The person using \
it tracks a few dozen expenses a month in one currency and reads the summary at month end.
"""

# The second milestone, in the same root container as the fixture's, so the two scopes are the
# same directory and overlap.
SECOND_MILESTONE = "milestones/repository-conventions/"
SECOND_TITLE = "Repository Conventions"
SECOND_REQUIREMENTS = f"""\
# {SECOND_TITLE}

## Goal

Give the Pocket Ledger repository its working conventions before the ledger's first source \
file lands: a contributing guide stating how changes are made and verified, and an ignore file \
keeping generated files out of the history.

## Relevant starting state

### The repository

The repository holds only the milestone files under `milestones/`; no source code, \
configuration, or documentation exists yet.

## Decisions

- **Conventions as two root files.** The conventions live in `CONTRIBUTING.md` and \
`.gitignore` at the repository root, and nowhere else.

## Out of Scope

- Any source code of the ledger.
"""
# The second milestone's tasks, in order: each one's `##` heading, its brief, the deliverable it
# lands at the repository root, the deliverable's content, and its verified bar.
SECOND_TASKS = (
    (
        "Add The Contributing Guide",
        "Create `CONTRIBUTING.md` at the repository root stating that the ledger is one "
        "stdlib-only Python 3.9+ script and that a change is verified by running the script "
        "from a terminal. Verified by the file existing at the root with the heading "
        "`# Contributing` as its first line.",
        "CONTRIBUTING.md",
        "# Contributing\n\nPocket Ledger is one stdlib-only Python 3.9+ script. Verify every "
        "change by running the script from a terminal.\n",
        "- `CONTRIBUTING.md` exists at the repository root\n"
        "- its first line is `# Contributing`\n"
        "- it states the stdlib-only Python 3.9+ script and verification by running it",
    ),
    (
        "Add The Ignore File",
        "Create `.gitignore` at the repository root ignoring `__pycache__/`, so no bytecode "
        "the ledger's runs generate enters the history. Verified by the file existing at the "
        "root holding that one pattern.",
        ".gitignore",
        "__pycache__/\n",
        "- `.gitignore` exists at the repository root\n"
        "- it holds the one pattern `__pycache__/`",
    ),
)
# The second milestone's finish body: its title, a blank line, and the summary's bullets.
SECOND_SUMMARY = (
    f"{SECOND_TITLE}\n\n"
    "- Added `CONTRIBUTING.md` at the repository root, stating the stdlib-only Python 3.9+ "
    "script and verification by running it\n"
    "- Added `.gitignore` at the repository root, ignoring `__pycache__/`"
)

# The two subjects the refresh run commits, in this order, each naming the fixture milestone by
# its path exactly as resolved.
STARTING_STATE_SUBJECT = f"Starting-state: {FIXTURE_MILESTONE}"
DERIVATION_SUBJECT = f"Task-derivation: {FIXTURE_MILESTONE}"


def run(repository, command, *, stdin=None):
    """Run one command in the repository, its stdin the given text or nothing -> its stdout,
    failing the calling test with the command's stderr on a non-zero exit."""
    completed = subprocess.run(
        command,
        cwd=str(repository),
        input=stdin if stdin is not None else "",
        capture_output=True,
        encoding="utf-8",
    )
    assert completed.returncode == 0, f"{command} exited {completed.returncode}: {completed.stderr}"
    return completed.stdout


def tool(repository, name, *arguments, stdin=None):
    """Run one of the plugin's tools in the repository, from the workspace root as every runner
    runs it -> its stdout."""
    return run(repository, [sys.executable, str(TOOLS / name), *arguments], stdin=stdin)


def commit(repository, subject, *paths, body=None, removals=()):
    """Commit exactly the named paths, and the named removals, through the plugin's commit tool,
    asserting the commit landed: the tool prints nothing when it does."""
    arguments = ["--subject", subject]
    if body is not None:
        arguments += ["--body", body]
    for removal in removals:
        arguments += ["--remove", removal]
    printed = tool(repository, "commit.py", *arguments, "--", *paths)
    assert printed == "", f"{subject}: {printed}"


def git(repository, *args):
    return run(repository, ["git", *args])


def replace_section(text, heading, body):
    """The requirements text with the body of its `## <heading>` section, up to the next `## `
    heading, replaced by the given body."""
    start = text.index(f"## {heading}\n\n") + len(f"## {heading}\n\n")
    end = text.index("\n## ", start)
    return text[:start] + body + text[end:]


def build_moved_history(repository):
    """Build, on top of the seed, the history in which the fixture milestone's starting state is
    stale: its questions answered, its `Starting-state:` anchor, then a second, overlapping
    milestone defined, derived, completed, and finished after it."""
    requirements = repository / FIXTURE_REQUIREMENTS

    # The fixture's questions answered one at a time, each decision folded ahead of its block's
    # removal and committed with it, so the derivation's precondition holds.
    for short_title, decision in ANSWERS.items():
        text = requirements.read_text(encoding="utf-8")
        position = text.index("\n## Out of Scope")
        requirements.write_text(text[:position] + decision + "\n" + text[position:], encoding="utf-8")
        tool(repository, "open_questions.py", "remove", FIXTURE_MILESTONE, short_title)
        commit(repository, f"Manual-answer: {short_title}", FIXTURE_QUESTIONS, FIXTURE_REQUIREMENTS)

    # The anchor: the fixture's starting state recorded under its path.
    text = requirements.read_text(encoding="utf-8")
    requirements.write_text(replace_section(text, "Relevant starting state", STARTING_STATE), encoding="utf-8")
    commit(repository, STARTING_STATE_SUBJECT, FIXTURE_REQUIREMENTS)

    # The second milestone's files added, as the definition tool lays them out.
    second = repository / SECOND_MILESTONE
    second.mkdir()
    (second / "requirements.md").write_text(SECOND_REQUIREMENTS, encoding="utf-8")
    (second / "open_questions.xml").write_text("<open-questions/>\n", encoding="utf-8")
    (second / "TASKS_TODO.md").write_text("# TASKS TODO\n\n", encoding="utf-8")
    commit(
        repository,
        f"Milestone-definition: {SECOND_MILESTONE}",
        *(SECOND_MILESTONE + name for name in ("requirements.md", "open_questions.xml", "TASKS_TODO.md")),
    )

    # Its tasks entered, which starts it.
    sections = "".join(f"## {title}\n\n{brief}\n\n---\n\n" for title, brief, *_ in SECOND_TASKS)
    tool(repository, "task_list.py", "initialize", SECOND_MILESTONE, stdin=sections)
    commit(repository, f"Task-derivation: {SECOND_MILESTONE}", SECOND_MILESTONE + "TASKS_TODO.md")

    # Its tasks completed, each committing its deliverable and the list the removal changed,
    # with its verified bar as the body.
    for title, _, deliverable, content, bar in SECOND_TASKS:
        (repository / deliverable).write_text(content, encoding="utf-8")
        tool(repository, "task_list.py", "remove", SECOND_MILESTONE, title)
        commit(repository, f"Task-completion: {title}", deliverable, SECOND_MILESTONE + "TASKS_TODO.md", body=bar)

    # Its finish, removing its directory, with its summary as the body.
    commit(repository, f"Milestone-finish: {SECOND_MILESTONE}", body=SECOND_SUMMARY, removals=(SECOND_MILESTONE,))


def subjects_since(repository, revision):
    """The subjects of the commits reachable from HEAD and not from the revision, oldest
    first."""
    return git(repository, "log", "--reverse", "--format=%s", f"{revision}..HEAD").splitlines()


def test_derive_tasks_refreshes_a_stale_starting_state_before_deriving(seeded_repo, host, run_host):
    repository = seeded_repo()
    build_moved_history(repository)
    built = git(repository, "rev-parse", "HEAD").strip()

    # The history holds as built: the gate on the fixture milestone open, nothing printed, and
    # other milestones' work beneath its anchor, which is the derivation's reason to refresh.
    assert tool(repository, "milestones.py", "gate", FIXTURE_MILESTONE) == ""
    moved = tool(repository, "milestones.py", "since", FIXTURE_MILESTONE, "--milestones").splitlines()
    assert moved and moved[0].endswith("\t" + STARTING_STATE_SUBJECT), moved
    assert len(moved) > 1, moved
    assert tool(repository, "open_questions.py", "list", FIXTURE_MILESTONE) == ""

    completed = run_host(f"/cairn:derive-tasks --milestone {FIXTURE_MILESTONE}", cwd=repository)
    assert completed.returncode == 0, completed.stderr
    records = host.records(completed.stdout)
    assert records.succeeded, records.closing

    # The pass signal, read from the log: the run committed a starting-state refresh of the
    # fixture milestone, and its task derivation after it.
    subjects = subjects_since(repository, built)
    assert STARTING_STATE_SUBJECT in subjects, subjects
    assert DERIVATION_SUBJECT in subjects, subjects
    assert subjects.index(STARTING_STATE_SUBJECT) < subjects.index(DERIVATION_SUBJECT), subjects
