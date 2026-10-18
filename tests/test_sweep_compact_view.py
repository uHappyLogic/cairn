"""The answer sweep's compact view call, as the committed Claude Code tree renders it: the one
fenced block of the sweep file holding `list` with its `--with-question` flag, with
<MILESTONE_DIR> replaced by the path of a copy of the golden compact-view fixture milestone and
the call run under bash with the tree's plugin-root variable exported to the tree root. The
call writes nothing, so no git repository is needed. Its print is asserted exactly: every
block's id, a tab, and its question text in document order, recommendation-less blocks
included, then for each walked id in walk order the id, its lifted line, and its picked
alternative's what-it-is line. The failed-lift branch, which no valid fixture provokes, is left
to the hands-on check."""

import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
TREE = REPO_ROOT / "hosts" / "claude"
SWEEP = TREE / "skills" / "answer-all-open-questions-with-recommendation" / "SKILL.md"
PLUGIN_ROOT_VARIABLE = "CLAUDE_PLUGIN_ROOT"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "compact_view"

LIST_COMMAND = "/tools/open_questions.py list --with-question "
FOLD_COMMAND = "/tools/requirements.py fold "

# <MILESTONE_DIR> as the runner fills it: the pointer's path, its trailing slash included.
MILESTONE = "milestones/milestone_09_golden-compact-view/"

# The fixture holds three recommendation-bearing blocks (one a dependent of another, one
# rationale holding a spaced em dash of its own, one option holding an entity) and two
# recommendation-less ones (one with alternatives, one bare), in the tool's sorted form.
EXPECTED = "".join(
    line + "\n"
    for line in (
        "Log format\tWhich format are log lines written in?",
        "Log level default\tWhich level does a run log at when none is configured?",
        "Rotation trigger\tWhat triggers a log file's rotation: its size & age, or a \"nightly\" <cron> schedule?",
        "Log shipping\tAre logs shipped to a central collector?",
        "Log sampling\tAre repeated log lines sampled under load?",
        "Log format",
        "JSON lines — One object per line keeps every field machine-readable — and grep still finds a line by its text.",
        "JSON lines — Write each log entry as one JSON object on its own line.",
        "Log level default",
        "Info — Info records every state change a user would ask about without the noise of debug output.",
        "Info — Log at info level unless a level is configured.",
        "Rotation trigger",
        "Size & age — JSON lines grow fast under load, so size bounds a file where a schedule cannot.",
        "Size & age — Rotate a file once it passes 10 MB or turns a day old, whichever comes first.",
    )
)


# --- extracting the call ----------------------------------------------------------------------


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


def compact_view_call():
    """The one fence of the rendered sweep file holding `list` with its question flag."""
    text = SWEEP.read_text(encoding="utf-8")
    holding = [block for block in fenced_blocks(text) if any(LIST_COMMAND in line for line in block)]
    assert len(holding) == 1, f"{len(holding)} fences of the sweep file hold list --with-question, not one"
    return holding[0]


def filled(lines, milestone):
    """The call written out with only <MILESTONE_DIR> replaced."""
    return "\n".join(lines).replace("<MILESTONE_DIR>", milestone) + "\n"


# --- the environment and the run --------------------------------------------------------------


@pytest.fixture
def environment(tmp_path):
    """The call's environment: the tree's plugin-root variable exported to the tree root,
    `python3` resolving to the interpreter running the suite (so each pytest run drives the
    rendered tools under its own interpreter), no bytecode written into the tree, and no
    startup file read by the non-interactive shell."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    wrapper = bin_dir / "python3"
    wrapper.write_text(f'#!/bin/sh\nexec {shlex.quote(sys.executable)} "$@"\n', encoding="utf-8")
    wrapper.chmod(0o755)
    env = dict(os.environ)
    for name in ("BASH_ENV", "ENV"):
        env.pop(name, None)
    env.update(
        {
            PLUGIN_ROOT_VARIABLE: str(TREE),
            "PATH": str(bin_dir) + os.pathsep + env.get("PATH", ""),
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    return env


@pytest.fixture
def project(tmp_path):
    """A project directory holding a copy of the golden compact-view milestone at MILESTONE."""
    root = tmp_path / "project"
    shutil.copytree(FIXTURE, root / MILESTONE)
    return root


def run_call(cwd, env, call):
    result = subprocess.run(
        ["bash", "-c", call], cwd=str(cwd), env=env, stdin=subprocess.DEVNULL, capture_output=True, check=False
    )
    return result.returncode, result.stdout.decode("utf-8"), result.stderr.decode("utf-8")


# --- the template as the rendered tree holds it -----------------------------------------------


def test_the_call_is_the_one_fence_holding_list_with_its_question_flag_and_names_only_the_milestone():
    lines = compact_view_call()
    call = "\n".join(lines)
    assert FOLD_COMMAND not in call
    assert f"${{{PLUGIN_ROOT_VARIABLE}}}/tools/open_questions.py " in call
    assert "<MILESTONE_DIR>" in call
    assert not re.search(r"<[A-Za-z][A-Za-z_ ]*>", filled(lines, MILESTONE)), "a placeholder is left unfilled"


# --- the call run under bash ------------------------------------------------------------------


def test_the_call_prints_every_block_then_each_walked_pick_and_its_what_it_is(project, environment):
    document = project / MILESTONE / "open_questions.xml"
    pristine = document.read_bytes()

    status, stdout, stderr = run_call(project, environment, filled(compact_view_call(), MILESTONE))

    assert (status, stderr) == (0, "")
    assert stdout == EXPECTED
    assert document.read_bytes() == pristine
    assert sorted(path.name for path in (project / MILESTONE).iterdir()) == ["open_questions.xml"]
