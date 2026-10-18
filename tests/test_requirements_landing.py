"""Where a fold lands: at the end of the "## Decisions" subsection whose "### " heading equals
the --section heading after whitespace and case folding, or under a new "### " heading created
at the end of the section, just before the next "## " heading, when none carries it; the fresh
requirements.md define_milestone.py writes takes its first decision the same way."""

from pathlib import Path

import pytest

import requirements

FIXTURES = Path(__file__).resolve().parent / "fixtures"
NAME = requirements.REQUIREMENTS_NAME
GOLDEN = (FIXTURES / NAME).read_bytes()

PROSE_END = b"It carries a second paragraph, so a fold lands after this one.\n"
UNICODE_END = "including zażółć gęślą jaźń.\n".encode("utf-8")


def fold(run_requirements, target, section, decision):
    result = run_requirements("fold", str(target), "--section", section, stdin=decision)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    return (target / NAME).read_bytes()


def inserted_after(data, line, inserted):
    assert data.count(line) == 1
    offset = data.index(line) + len(line)
    return data[:offset] + inserted + data[offset:]


# --- an existing subsection -------------------------------------------------------------


@pytest.mark.parametrize(
    "section",
    ["Prose decision", "prose decision", "PROSE DECISION", "  Prose   decision  ", "Prose\tDecision", "Prose\ndecision"],
)
def test_an_existing_subsection_is_matched_after_whitespace_and_case_folding(run_requirements, requirements_dir, section):
    target = requirements_dir()
    result = fold(run_requirements, target, section, b"Folded.\n")
    assert result == inserted_after(GOLDEN, PROSE_END, b"\nFolded.\n")


def test_a_non_ascii_heading_is_matched_after_case_folding(run_requirements, requirements_dir):
    target = requirements_dir()
    result = fold(run_requirements, target, "render unicode —  text as given", b"Folded.\n")
    assert result == inserted_after(GOLDEN, UNICODE_END, b"\nFolded.\n")


def test_a_heading_line_with_extra_whitespace_in_the_file_is_matched(run_requirements, requirements_dir):
    original = b"## Decisions\n\n###   Spaced    Heading  \n\nPara.\n\n## Out of Scope\n"
    target = requirements_dir(original)
    result = fold(run_requirements, target, "spaced heading", b"Folded.\n")
    assert result == b"## Decisions\n\n###   Spaced    Heading  \n\nPara.\n\nFolded.\n\n## Out of Scope\n"


def test_a_same_named_subsection_outside_decisions_is_never_the_landing_point(run_requirements, requirements_dir):
    target = requirements_dir()
    result = fold(run_requirements, target, "Prose decision", b"Folded.\n")
    starting_state = GOLDEN.split(b"## Decisions\n")[0]
    assert result.startswith(starting_state + b"## Decisions\n")
    assert result.count(b"Folded.") == 1
    assert result.index(b"Folded.") > result.index(b"## Decisions\n")


def test_when_two_subsections_carry_the_heading_the_first_is_used(run_requirements, requirements_dir):
    original = b"## Decisions\n\n### Twice\n\nFirst.\n\n### Twice\n\nSecond.\n"
    target = requirements_dir(original)
    result = fold(run_requirements, target, "twice", b"Folded.\n")
    assert result == b"## Decisions\n\n### Twice\n\nFirst.\n\nFolded.\n\n### Twice\n\nSecond.\n"


def test_a_deeper_heading_is_body_text_of_its_subsection(run_requirements, requirements_dir):
    original = b"## Decisions\n\n### Outer\n\nPara.\n\n#### Inner\n\nDeeper.\n\n## Out of Scope\n"
    target = requirements_dir(original)
    result = fold(run_requirements, target, "Outer", b"Folded.\n")
    assert result == b"## Decisions\n\n### Outer\n\nPara.\n\n#### Inner\n\nDeeper.\n\nFolded.\n\n## Out of Scope\n"


# --- a missing subsection ---------------------------------------------------------------


def test_a_missing_subsection_is_created_at_the_end_of_decisions_before_the_next_section(run_requirements, requirements_dir):
    target = requirements_dir()
    result = fold(run_requirements, target, "A New Subsection", b"Folded.\n")
    assert result == inserted_after(GOLDEN, UNICODE_END, b"\n### A New Subsection\n\nFolded.\n")
    assert result.index(b"### A New Subsection") < result.index(b"## Out of Scope")


def test_a_created_heading_is_folded_to_one_line(run_requirements, requirements_dir):
    target = requirements_dir()
    result = fold(run_requirements, target, "  A  New\n Subsection\t", b"Folded.\n")
    assert result == inserted_after(GOLDEN, UNICODE_END, b"\n### A New Subsection\n\nFolded.\n")


def test_a_created_subsection_takes_the_next_fold_under_any_spelling(run_requirements, requirements_dir):
    target = requirements_dir()
    fold(run_requirements, target, "A New Subsection", b"First.\n")
    result = fold(run_requirements, target, "a new SUBSECTION", b"Second.\n")
    assert result == inserted_after(GOLDEN, UNICODE_END, b"\n### A New Subsection\n\nFirst.\n\nSecond.\n")
    assert result.count(b"### A New Subsection") == 1


def test_a_missing_subsection_in_a_last_decisions_section_is_created_at_the_end_of_the_file(run_requirements, requirements_dir):
    original = b"## Goal\n\nShip it.\n\n## Decisions\n\n### Kept\n\nPara.\n"
    target = requirements_dir(original)
    result = fold(run_requirements, target, "Created", b"Folded.\n")
    assert result == original + b"\n### Created\n\nFolded.\n"


def test_the_section_heading_itself_is_matched_after_whitespace_and_case_folding(run_requirements, requirements_dir):
    original = b"## Goal\n\nShip it.\n\n##   decisions  \n\n## Out of Scope\n"
    target = requirements_dir(original)
    result = fold(run_requirements, target, "Created", b"Folded.\n")
    assert result == b"## Goal\n\nShip it.\n\n##   decisions  \n\n### Created\n\nFolded.\n\n## Out of Scope\n"


# --- the fresh template -----------------------------------------------------------------


def test_the_fresh_template_takes_its_first_and_later_decisions(run_define, run_requirements, workspace):
    root = workspace()
    defined = run_define("--title", "First", stdin=b"Ship it.\n", cwd=root)
    assert defined.returncode == 0, defined.stderr
    target = root / "milestones" / "milestone_01_first"
    template = (target / NAME).read_bytes()
    assert template == b"# Milestone 1: First\n\n## Goal\n\nShip it.\n\n## Relevant starting state\n\n## Decisions\n\n## Out of Scope\n\n"

    first = fold(run_requirements, target, "Opening Decision", b"The first decision.\n")
    assert first == inserted_after(template, b"## Decisions\n", b"\n### Opening Decision\n\nThe first decision.\n")

    second = fold(run_requirements, target, "opening decision", b"A second decision under the same heading.\n")
    third = fold(run_requirements, target, "Another Decision", b"A third decision under its own heading.\n")
    assert second == inserted_after(first, b"The first decision.\n", b"\nA second decision under the same heading.\n")
    assert third == (
        b"# Milestone 1: First\n\n## Goal\n\nShip it.\n\n## Relevant starting state\n\n## Decisions\n\n"
        b"### Opening Decision\n\nThe first decision.\n\nA second decision under the same heading.\n\n"
        b"### Another Decision\n\nA third decision under its own heading.\n\n## Out of Scope\n\n"
    )
