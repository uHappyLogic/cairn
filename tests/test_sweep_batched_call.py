"""The answer sweep's batched call, as the committed Claude Code tree renders it: the one fenced
block of the sweep file holding the fold command, split at the boundaries its step states (the
question section from its fixed opening line through the column-0 line that closes it, the
footer from the fixed header line to the fence's end), with the section filled once per walked
question of the golden sweep fixture and the call run under bash in a temporary git repository
with the tree's plugin-root variable exported to the tree root. A clean run makes one
Recommendation-answer commit per answered question, path-scoped to the milestone's two files,
and skips the dependent whose pick the target's remove stripped with no commit and no output; a
dirty milestone file stops the call before any write. The stop path after a fold is left to the
hands-on check, so nothing here provokes one."""

import os
import re
import shlex
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
TREE = REPO_ROOT / "hosts" / "claude"
SWEEP = TREE / "skills" / "answer-all-open-questions-with-recommendation" / "SKILL.md"
TOOL = TREE / "tools" / "open_questions.py"
PLUGIN_ROOT_VARIABLE = "CLAUDE_PLUGIN_ROOT"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "sweep"

FOLD_COMMAND = "/tools/requirements.py fold "
SECTION_OPENING = "if pick="
SECTION_CLOSING = "fi &&"
FOOTER_HEADER = "echo 'completeness walk'"

# <MILESTONE_DIR> as the runner fills it: the pointer's path, its trailing slash included.
MILESTONE = "milestones/milestone_07_golden-sweep-fixture/"
DOCUMENT = MILESTONE + "open_questions.xml"
REQUIREMENTS = MILESTONE + "requirements.md"

STORAGE = "Storage backend"
EVICTION = "Cache eviction"
WARMUP = "Cache warmup"
RETRY = "Retry limit"
WALK_ORDER = [STORAGE, RETRY, EVICTION]
ANSWERED = [STORAGE, RETRY]

# What the runner composes in step 3a for each walked question: the heading its decision lands
# under (an existing subsection, or a new one holding characters the double quotes must escape)
# and the decision itself. The eviction section is composed and run, but its lift fails once
# the storage section's remove has stripped its pick, so its decision never lands.
COMPOSED = {
    STORAGE: (
        "Storage",
        "- **SQLite file.** Every entry lives in one SQLite database file beside the project, so a\n"
        "  crash mid-write cannot corrupt the store.",
    ),
    RETRY: (
        'Retry `$MAX_RETRIES` "budget"',
        "A failed read is retried three times, `${MAX_RETRIES}` and $(cmd) kept verbatim, before\n"
        "its last error is reported.",
    ),
    EVICTION: (
        "Eviction",
        "- **Drop whole file.** The store is deleted whole once it outgrows its limit.",
    ),
}

# The ### headings the fixture's ## Decisions already holds, which a fold lands under unchanged.
FIXTURE_HEADINGS = ("Storage",)

ANSWER_COMMIT_LANDED = "answer commit landed\n"
COMPLETENESS_WALK = "completeness walk\n"


# --- extracting and splitting the call ----------------------------------------------------


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
    assert current is None, "an unclosed fence in the sweep file"
    return blocks


def sweep_text():
    return SWEEP.read_text(encoding="utf-8")


def batched_call():
    """The one fence of the rendered sweep file holding the fold command."""
    holding = [block for block in fenced_blocks(sweep_text()) if any(FOLD_COMMAND in line for line in block)]
    assert len(holding) == 1, f"{len(holding)} fences of the sweep file hold the fold command, not one"
    return holding[0]


def split_call(lines):
    """The call's opening lines, its question section, and its footer: the section runs from
    its fixed opening line through the column-0 line closing it, the footer from the fixed
    header line to the fence's end, and the three cover the whole fence."""
    openings = [index for index, line in enumerate(lines) if line.startswith(SECTION_OPENING)]
    assert len(openings) == 1, "the call holds no single question-section opening line"
    start = openings[0]
    closings = [index for index in range(start + 1, len(lines)) if lines[index] == SECTION_CLOSING]
    assert closings, "the question section has no column-0 closing line"
    end = closings[0] + 1
    footers = [index for index, line in enumerate(lines) if line.startswith(FOOTER_HEADER)]
    assert footers == [end], "the footer's header line does not follow the question section"
    return lines[:start], lines[start:end], lines[end:]


def double_quoted(value):
    """A value as the step writes it inside the template's double quotes: every \\, ", $, and `
    escaped by a backslash."""
    for character in ("\\", '"', "$", "`"):
        value = value.replace(character, "\\" + character)
    return value


def compose(questions):
    """The call written out for the given (Short Title, heading, decision, option) questions,
    one filled question section each, in the order given."""
    opening, section, footer = split_call(batched_call())
    lines = list(opening)
    for title, heading, decision, option in questions:
        for line in section:
            if line == "<the decision>":
                lines.extend(decision.splitlines())
            else:
                lines.append(
                    line.replace("<Short Title>", double_quoted(title))
                    .replace("<Heading>", double_quoted(heading))
                    .replace("<Option>", double_quoted(option))
                )
    lines.extend(footer)
    call = "\n".join(lines).replace("<MILESTONE_DIR>", MILESTONE) + "\n"
    assert not re.search(r"<[A-Za-z][A-Za-z_ ]*>", call), "a placeholder is left unfilled"
    return call


# --- the temporary repository and the run ---------------------------------------------------


@pytest.fixture
def environment(tmp_path):
    """The call's environment: the tree's plugin-root variable exported to the tree root,
    `python3` resolving to the interpreter running the suite (so each pytest run drives the
    rendered tools under its own interpreter), no bytecode written into the tree, and git
    isolated from every global or system configuration with a fixed identity."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    wrapper = bin_dir / "python3"
    wrapper.write_text(f'#!/bin/sh\nexec {shlex.quote(sys.executable)} "$@"\n', encoding="utf-8")
    wrapper.chmod(0o755)
    home = tmp_path / "home"
    home.mkdir()
    env = dict(os.environ)
    env.update(
        {
            PLUGIN_ROOT_VARIABLE: str(TREE),
            "PATH": str(bin_dir) + os.pathsep + env.get("PATH", ""),
            "PYTHONDONTWRITEBYTECODE": "1",
            "HOME": str(home),
            "XDG_CONFIG_HOME": str(home / ".config"),
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_AUTHOR_NAME": "Sweep Test",
            "GIT_AUTHOR_EMAIL": "sweep@example.invalid",
            "GIT_COMMITTER_NAME": "Sweep Test",
            "GIT_COMMITTER_EMAIL": "sweep@example.invalid",
        }
    )
    return env


def git(repo, env, *args):
    result = subprocess.run(["git", *args], cwd=str(repo), env=env, capture_output=True, check=False)
    assert result.returncode == 0, result.stderr.decode("utf-8", "replace")
    return result.stdout.decode("utf-8")


@pytest.fixture
def repo(tmp_path, environment):
    """A temporary git repository whose one commit holds the golden sweep milestone and an
    unrelated tracked file."""
    root = tmp_path / "repo"
    shutil.copytree(FIXTURE, root / MILESTONE)
    (root / "README.md").write_bytes(b"An unrelated tracked file.\n")
    git(root, environment, "init", "-q")
    git(root, environment, "add", "README.md", DOCUMENT, REQUIREMENTS)
    git(root, environment, "commit", "-q", "-m", "Initial commit")
    return root


def tool(repo, env, *args):
    result = subprocess.run(
        [sys.executable, "-B", str(TOOL), *args], cwd=str(repo), env=env, capture_output=True, check=False
    )
    assert (result.returncode, result.stderr) == (0, b"")
    return result.stdout.decode("utf-8")


def walked_questions(repo, env):
    """What the runner holds from step 1's view before composing: each walked id in walk order
    with its lifted line, and the option as the line's text before its first spaced em dash."""
    order = tool(repo, env, "walk", MILESTONE).splitlines()
    assert order == WALK_ORDER
    lifted = {title: tool(repo, env, "lift", MILESTONE, title).rstrip("\n") for title in order}
    questions = [(title, *COMPOSED[title], lifted[title].split(" — ", 1)[0]) for title in order]
    return questions, lifted


def run_call(repo, env, call):
    result = subprocess.run(
        ["bash", "-c", call], cwd=str(repo), env=env, stdin=subprocess.DEVNULL, capture_output=True, check=False
    )
    return result.returncode, result.stdout.decode("utf-8"), result.stderr.decode("utf-8")


# --- reading the outcome --------------------------------------------------------------------


def block_lines(document, title):
    """The lines of the named block, from its opening tag through its closing tag."""
    lines = document.splitlines()
    start = lines.index(f'  <open-question id="{title}">')
    return lines[start : lines.index("  </open-question>", start) + 1]


def diff_lines(repo, env, commit, path):
    """The removed and the added lines a commit's diff shows for one path."""
    removed, added = [], []
    for line in git(repo, env, "show", "--format=", "--no-color", commit, "--", path).splitlines():
        if line.startswith("-") and not line.startswith("---"):
            removed.append(line[1:])
        elif line.startswith("+") and not line.startswith("+++"):
            added.append(line[1:])
    return removed, added


def decision_subsections(text):
    """Each ### heading under ## Decisions mapped to the text of its subsection's body."""
    lines = text.splitlines()
    start = lines.index("## Decisions") + 1
    end = next((index for index in range(start, len(lines)) if lines[index].startswith("## ")), len(lines))
    subsections, heading = {}, None
    for line in lines[start:end]:
        if line.startswith("### "):
            heading = line[len("### ") :]
            subsections[heading] = []
        elif heading is not None:
            subsections[heading].append(line)
    return {heading: "\n".join(body) for heading, body in subsections.items()}


# --- the template as the rendered tree holds it ---------------------------------------------


def test_the_step_states_the_boundaries_the_call_is_split_at():
    prose = " ".join(sweep_text().split())
    assert f"the lines from `{SECTION_OPENING}` through the column-0 `{SECTION_CLOSING}` that closes it" in prose
    assert f"the lines from `{FOOTER_HEADER}` to the end are written once" in prose


def test_the_call_splits_into_opening_section_and_footer_with_every_placeholder():
    lines = batched_call()
    opening, section, footer = split_call(lines)
    assert opening + section + footer == lines
    assert opening and footer[0].startswith(FOOTER_HEADER) and footer[-1].endswith("walk <MILESTONE_DIR>")
    section_text = "\n".join(section)
    for placeholder in ("<MILESTONE_DIR>", "<Short Title>", "<Heading>", "<Option>"):
        assert placeholder in section_text
    assert section.count("<the decision>") == 1
    assert FOLD_COMMAND in section_text
    assert f"${{{PLUGIN_ROOT_VARIABLE}}}/tools/" in section_text


# --- the call run under bash ----------------------------------------------------------------


def test_a_clean_run_commits_each_answer_and_skips_the_stripped_dependent(repo, environment):
    pristine = (repo / DOCUMENT).read_text(encoding="utf-8")
    questions, lifted = walked_questions(repo, environment)
    (repo / "README.md").write_bytes(b"An unrelated tracked file, edited.\n")
    (repo / "notes.txt").write_bytes(b"An untracked file.\n")

    status, stdout, stderr = run_call(repo, environment, compose(questions))

    assert (status, stdout, stderr) == (0, ANSWER_COMMIT_LANDED * len(ANSWERED) + COMPLETENESS_WALK, "")
    commits = git(repo, environment, "rev-list", "--reverse", "HEAD").split()[1:]
    assert len(commits) == len(ANSWERED)
    for commit, title in zip(commits, ANSWERED):
        heading, decision = COMPOSED[title]
        assert git(repo, environment, "log", "-1", "--format=%s", commit).rstrip("\n") == f"Recommendation-answer: {title}"
        assert git(repo, environment, "log", "-1", "--format=%b", commit).strip("\n") == lifted[title]
        touched = git(repo, environment, "show", "--name-only", "--format=", commit).split("\n")
        assert sorted(filter(None, touched)) == sorted([DOCUMENT, REQUIREMENTS])
        removed, _ = diff_lines(repo, environment, commit, DOCUMENT)
        assert not Counter(block_lines(pristine, title)) - Counter(removed)
        removed, added = diff_lines(repo, environment, commit, REQUIREMENTS)
        assert removed == []
        new_heading = [] if heading in FIXTURE_HEADINGS else [f"### {heading}"]
        assert [line for line in added if line.strip()] == new_heading + decision.splitlines()

    # The storage answer's remove stripped the dependent's pick in the same write and commit.
    removed, _ = diff_lines(repo, environment, commits[0], DOCUMENT)
    eviction_pick = [line for line in block_lines(pristine, EVICTION) if "<recommendation " in line]
    assert len(eviction_pick) == 1 and eviction_pick[0] in removed

    requirements = (repo / REQUIREMENTS).read_text(encoding="utf-8")
    subsections = decision_subsections(requirements)
    for title in ANSWERED:
        heading, decision = COMPOSED[title]
        assert decision in subsections[heading]
    assert "Eviction" not in subsections and "Drop whole file" not in requirements
    assert all(EVICTION not in git(repo, environment, "log", "-1", "--format=%B", commit) for commit in commits)
    assert tool(repo, environment, "list", MILESTONE).splitlines() == [EVICTION, WARMUP]
    assert tool(repo, environment, "walk", MILESTONE) == ""
    assert git(repo, environment, "status", "--porcelain").splitlines() == [" M README.md", "?? notes.txt"]


def test_a_dirty_milestone_file_stops_the_call_before_any_write(repo, environment):
    questions, _ = walked_questions(repo, environment)
    edited = (FIXTURE / "requirements.md").read_bytes() + b"\nA hand edit left uncommitted.\n"
    (repo / REQUIREMENTS).write_bytes(edited)

    status, stdout, stderr = run_call(repo, environment, compose(questions))

    assert status != 0
    assert (stdout, stderr) == (f"dirty before start\n M {REQUIREMENTS}\n", "")
    assert git(repo, environment, "rev-list", "--count", "HEAD").strip() == "1"
    assert (repo / DOCUMENT).read_bytes() == (FIXTURE / "open_questions.xml").read_bytes()
    assert (repo / REQUIREMENTS).read_bytes() == edited
