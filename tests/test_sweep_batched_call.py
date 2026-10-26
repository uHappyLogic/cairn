"""The answer sweep's batched call, as the committed Claude Code tree renders it: the one fenced
block of the sweep file holding the fold command, split at the boundaries its step states (the
question section from its fixed opening line through the column-0 line that closes it, the
footer from the fixed header line to the fence's end), and the conflict section, cut at the same
boundaries from the one fence holding the replace command. Each walked question of the golden
sweep fixture gets one filled section, the conflict section for the one whose question text, as
the view's `list --with-question` prints it, opens with the review pass's fixed phrase, and the
call is run under bash in a temporary git repository with the tree's plugin-root variable
exported to the tree root. A clean run makes one Recommendation-answer commit per answered
question, path-scoped to the milestone's two files, the conflict answer's rewriting only the
losing entry's subsection body, and skips the dependent whose pick the target's remove stripped
with no commit and no output; a dirty milestone file stops the call before any write. The stop
path after a fold or a replace is left to the hands-on check, so nothing here provokes one."""

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
REVIEW = TREE / "skills" / "review-milestone-requirements" / "SKILL.md"
TOOL = TREE / "tools" / "open_questions.py"
PLUGIN_ROOT_VARIABLE = "CLAUDE_PLUGIN_ROOT"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "sweep"

FOLD_COMMAND = "/tools/requirements.py fold "
REPLACE_COMMAND = "/tools/requirements.py replace "
SECTION_OPENING = "if pick="
SECTION_CLOSING = "fi &&"
FOOTER_HEADER = "echo 'completeness walk'"
DECISION_PLACEHOLDER = "<the decision>"
NEW_BODY_PLACEHOLDER = "<the new body>"
# The opening the review pass gives every conflict question and the sweep tests by exact prefix.
CONFLICT_OPENING = "Which conflicting decision stands:"

# <MILESTONE_DIR> as the runner fills it: the pointer's path, its trailing slash included.
MILESTONE = "milestones/milestone_07_golden-sweep-fixture/"
DOCUMENT = MILESTONE + "open_questions.xml"
REQUIREMENTS = MILESTONE + "requirements.md"

STORAGE = "Storage backend"
EVICTION = "Cache eviction"
WARMUP = "Cache warmup"
RETRY = "Retry limit"
ENTRY_CAP = "Entry cap"
WALK_ORDER = [STORAGE, RETRY, ENTRY_CAP, EVICTION]
ANSWERED = [STORAGE, RETRY, ENTRY_CAP]

# The conflict question's pair as the fixture's ## Decisions holds it: the entry its pick keeps,
# a prose subsection, and the losing entry's topical subsection, whose whole body the runner
# rewrites with the conflicting bullet changed and the other bullet carried unchanged. The
# losing subsection is the fixture's last, so the retry section's fold, run before it, creates
# the heading that bounds it.
STANDING_HEADING = "Cache size"
LOSING_HEADING = "Memory budget"
LOSING_BODY = (
    "- **Entry cap.** The cache holds at most 500 entries, so a full scan stays fast.\n"
    "- **No disk spill.** An entry that does not fit in the cache is never written to disk."
)
NEW_BODY = (
    "- **Entry cap.** The cache holds at most 100 entries, so a full scan stays fast.\n"
    "- **No disk spill.** An entry that does not fit in the cache is never written to disk."
)

# What the runner composes in step 3a for each walked question: for an ordinary question the
# heading its decision lands under (an existing subsection, or a new one holding characters the
# double quotes must escape) and the decision itself, and for the conflict question the losing
# entry's heading and the whole new body of its subsection. The eviction section is composed
# and run, but its lift fails once the storage section's remove has stripped its pick, so its
# decision never lands.
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
    ENTRY_CAP: (LOSING_HEADING, NEW_BODY),
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


def fence_holding(command):
    """The one fence of the rendered sweep file holding the given command."""
    holding = [block for block in fenced_blocks(sweep_text()) if any(command in line for line in block)]
    assert len(holding) == 1, f"{len(holding)} fences of the sweep file hold {command.strip()!r}, not one"
    return holding[0]


def batched_call():
    """The one fence of the rendered sweep file holding the fold command."""
    return fence_holding(FOLD_COMMAND)


def section_bounds(lines):
    """Where a fence's section starts and ends: from its one fixed opening line through the
    first column-0 closing line after it."""
    openings = [index for index, line in enumerate(lines) if line.startswith(SECTION_OPENING)]
    assert len(openings) == 1, "the fence holds no single section opening line"
    start = openings[0]
    closings = [index for index in range(start + 1, len(lines)) if lines[index] == SECTION_CLOSING]
    assert closings, "the section has no column-0 closing line"
    return start, closings[0] + 1


def split_call(lines):
    """The call's opening lines, its question section, and its footer: the section runs from
    its fixed opening line through the column-0 line closing it, the footer from the fixed
    header line to the fence's end, and the three cover the whole fence."""
    start, end = section_bounds(lines)
    footers = [index for index, line in enumerate(lines) if line.startswith(FOOTER_HEADER)]
    assert footers == [end], "the footer's header line does not follow the question section"
    return lines[:start], lines[start:end], lines[end:]


def conflict_section():
    """The conflict section, cut from the one fence holding the replace command at the same
    boundaries as the question section."""
    lines = fence_holding(REPLACE_COMMAND)
    start, end = section_bounds(lines)
    return lines[start:end]


def double_quoted(value):
    """A value as the step writes it inside the template's double quotes: every \\, ", $, and `
    escaped by a backslash."""
    for character in ("\\", '"', "$", "`"):
        value = value.replace(character, "\\" + character)
    return value


def compose(questions):
    """The call written out for the given (Short Title, heading, text, option, conflict)
    questions, in the order given: one filled question section each, its decision as the text,
    or for a conflict question one filled conflict section, its new body as the text."""
    opening, section, footer = split_call(batched_call())
    conflict = conflict_section()
    lines = list(opening)
    for title, heading, text, option, is_conflict in questions:
        template, placeholder = (conflict, NEW_BODY_PLACEHOLDER) if is_conflict else (section, DECISION_PLACEHOLDER)
        for line in template:
            if line == placeholder:
                lines.extend(text.splitlines())
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


def question_texts(repo, env):
    """Each block's id mapped to its question text, as `list --with-question` prints them."""
    printed = tool(repo, env, "list", "--with-question", MILESTONE).splitlines()
    return dict(line.split("\t", 1) for line in printed)


def walked_questions(repo, env):
    """What the runner holds from step 1's view before composing: each walked id in walk order
    with its lifted line, the option as the line's text before its first spaced em dash, and
    its kind, a conflict question being one whose printed question text starts with the fixed
    opening."""
    order = tool(repo, env, "walk", MILESTONE).splitlines()
    assert order == WALK_ORDER
    texts = question_texts(repo, env)
    lifted = {title: tool(repo, env, "lift", MILESTONE, title).rstrip("\n") for title in order}
    questions = [
        (title, *COMPOSED[title], lifted[title].split(" — ", 1)[0], texts[title].startswith(CONFLICT_OPENING))
        for title in order
    ]
    assert [question[0] for question in questions if question[-1]] == [ENTRY_CAP]
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
    conflict = f"again the lines from `{SECTION_OPENING}` through the column-0 `{SECTION_CLOSING}` that closes it"
    assert conflict in prose
    assert f"starts with exactly `{CONFLICT_OPENING}`" in prose


def test_the_call_splits_into_opening_section_and_footer_with_every_placeholder():
    lines = batched_call()
    opening, section, footer = split_call(lines)
    assert opening + section + footer == lines
    assert opening and footer[0].startswith(FOOTER_HEADER) and footer[-1].endswith("walk <MILESTONE_DIR>")
    section_text = "\n".join(section)
    for placeholder in ("<MILESTONE_DIR>", "<Short Title>", "<Heading>", "<Option>"):
        assert placeholder in section_text
    assert section.count(DECISION_PLACEHOLDER) == 1
    assert FOLD_COMMAND in section_text
    assert f"${{{PLUGIN_ROOT_VARIABLE}}}/tools/" in section_text


def test_the_conflict_section_holds_one_replace_where_the_question_section_folds_and_no_fold():
    section = conflict_section()
    assert section == fence_holding(REPLACE_COMMAND), "the conflict fence holds more than its section"
    assert sum(REPLACE_COMMAND in line for line in section) == 1
    assert not any(FOLD_COMMAND in line for line in section)
    assert section.count(NEW_BODY_PLACEHOLDER) == 1 and DECISION_PLACEHOLDER not in section
    section_text = "\n".join(section)
    for placeholder in ("<MILESTONE_DIR>", "<Short Title>", "<Heading>", "<Option>"):
        assert placeholder in section_text
    _, ordinary, _ = split_call(batched_call())
    assert len(section) == len(ordinary)
    write = next(line for line in ordinary if FOLD_COMMAND in line)
    differing = [(plain, conflict) for plain, conflict in zip(ordinary, section) if plain != conflict]
    assert differing == [
        (write, write.replace(FOLD_COMMAND, REPLACE_COMMAND)),
        (DECISION_PLACEHOLDER, NEW_BODY_PLACEHOLDER),
    ]


# --- the fixture's conflict question --------------------------------------------------------


def test_the_conflict_question_opens_with_the_review_pass_phrase_naming_the_fixture_pair(repo, environment):
    phrases = [
        block for block in fenced_blocks(REVIEW.read_text(encoding="utf-8")) if block[:1] and block[0].startswith(CONFLICT_OPENING)
    ]
    assert len(phrases) == 1 and len(phrases[0]) == 1, "the review pass states no single fixed phrase"
    phrase = phrases[0][0].replace("<first heading>", STANDING_HEADING).replace("<second heading>", LOSING_HEADING)
    assert not re.search(r"<[A-Za-z][A-Za-z_ ]*>", phrase), "a placeholder of the phrase is left unfilled"
    assert question_texts(repo, environment)[ENTRY_CAP].startswith(phrase)
    subsections = decision_subsections((FIXTURE / "requirements.md").read_text(encoding="utf-8"))
    headings = list(subsections)
    assert headings.index(STANDING_HEADING) < headings.index(LOSING_HEADING) == len(headings) - 1
    assert subsections[LOSING_HEADING].strip("\n") == LOSING_BODY


# --- the call run under bash ----------------------------------------------------------------


def test_a_clean_run_commits_each_answer_rewrites_the_losing_entry_and_skips_the_stripped_dependent(
    repo, environment
):
    pristine = (repo / DOCUMENT).read_text(encoding="utf-8")
    questions, lifted = walked_questions(repo, environment)
    (repo / "README.md").write_bytes(b"An unrelated tracked file, edited.\n")
    (repo / "notes.txt").write_bytes(b"An untracked file.\n")
    call = compose(questions)
    assert call.count(REPLACE_COMMAND) == 1 and call.count(FOLD_COMMAND) == len(WALK_ORDER) - 1

    status, stdout, stderr = run_call(repo, environment, call)

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
        if title == ENTRY_CAP:
            continue
        removed, added = diff_lines(repo, environment, commit, REQUIREMENTS)
        assert removed == []
        new_heading = [] if heading in FIXTURE_HEADINGS else [f"### {heading}"]
        assert [line for line in added if line.strip()] == new_heading + decision.splitlines()

    # The storage answer's remove stripped the dependent's pick in the same write and commit.
    removed, _ = diff_lines(repo, environment, commits[0], DOCUMENT)
    eviction_pick = [line for line in block_lines(pristine, EVICTION) if "<recommendation " in line]
    assert len(eviction_pick) == 1 and eviction_pick[0] in removed

    # The conflict answer's commit rewrote the losing entry's whole subsection body and nothing
    # else: the file after it is the file before it with that body swapped for the new one, the
    # body running from below the heading line to the heading the retry section's fold created.
    conflict = commits[ANSWERED.index(ENTRY_CAP)]
    before = git(repo, environment, "show", f"{conflict}^:{REQUIREMENTS}")
    after = git(repo, environment, "show", f"{conflict}:{REQUIREMENTS}")
    bounded = "\n### {}\n\n{}\n\n### {}\n"
    retry_heading = COMPOSED[RETRY][0]
    assert before.count(LOSING_BODY) == 1
    assert bounded.format(LOSING_HEADING, LOSING_BODY, retry_heading) in before
    assert after == before.replace(LOSING_BODY, NEW_BODY)
    assert bounded.format(LOSING_HEADING, NEW_BODY, retry_heading) in after
    rewritten = [(old, new) for old, new in zip(LOSING_BODY.splitlines(), NEW_BODY.splitlines()) if old != new]
    assert rewritten and diff_lines(repo, environment, conflict, REQUIREMENTS) == (
        [old for old, _ in rewritten],
        [new for _, new in rewritten],
    )

    requirements = (repo / REQUIREMENTS).read_text(encoding="utf-8")
    subsections = decision_subsections(requirements)
    for title in ANSWERED:
        heading, decision = COMPOSED[title]
        assert decision in subsections[heading]
    fixture_subsections = decision_subsections((FIXTURE / "requirements.md").read_text(encoding="utf-8"))
    assert subsections[STANDING_HEADING] == fixture_subsections[STANDING_HEADING]
    assert LOSING_BODY not in requirements
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
