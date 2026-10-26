"""Which subsection a replace rewrites: the "## Decisions" subsection whose "### " heading equals
the --section heading after whitespace and case folding, the first of two when two carry it,
running to the next "### " heading or the end of the section; a same-named subsection outside
"## Decisions" is never matched, so a heading only it carries is refused with the file unchanged."""

from pathlib import Path

import pytest

import requirements

FIXTURES = Path(__file__).resolve().parent / "fixtures"
NAME = requirements.REQUIREMENTS_NAME
GOLDEN = (FIXTURES / NAME).read_bytes()

PROSE_BODY = (
    b"The first decision is one prose paragraph under its own subsection.\n"
    b"\n"
    b"It carries a second paragraph, so a fold lands after this one.\n"
)
UNICODE_BODY = "Carry `code`, ${VAR}, $(cmd), &amp; entities, and \"quotes\" through untouched, including zażółć gęślą jaźń.\n".encode("utf-8")
DECOY = b"### Prose decision\n\nA subsection outside `## Decisions` that shares a decision's heading is never a landing point.\n"


def replace(run_requirements, target, section, body):
    result = run_requirements("replace", str(target), "--section", section, stdin=body)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    return (target / NAME).read_bytes()


def swapped(data, old, new):
    """data with its one occurrence of old replaced by new."""
    assert data.count(old) == 1
    offset = data.index(old)
    return data[:offset] + new + data[offset + len(old):]


# --- the folded heading match -----------------------------------------------------------


@pytest.mark.parametrize(
    "section",
    ["Prose decision", "prose decision", "PROSE DECISION", "  Prose   decision  ", "Prose\tDecision", "Prose\ndecision"],
)
def test_a_subsection_is_matched_after_whitespace_and_case_folding(run_requirements, requirements_dir, section):
    target = requirements_dir()
    result = replace(run_requirements, target, section, b"Rewritten.\n")
    assert result == swapped(GOLDEN, PROSE_BODY, b"Rewritten.\n")


def test_a_non_ascii_heading_is_matched_after_case_folding(run_requirements, requirements_dir):
    target = requirements_dir()
    result = replace(run_requirements, target, "render unicode —  text as given", b"Rewritten.\n")
    assert result == swapped(GOLDEN, UNICODE_BODY, b"Rewritten.\n")


def test_a_heading_line_with_extra_whitespace_in_the_file_is_matched_and_kept(run_requirements, requirements_dir):
    original = b"## Decisions\n\n###   Spaced    Heading  \n\nPara.\n\n## Out of Scope\n"
    target = requirements_dir(original)
    result = replace(run_requirements, target, "spaced heading", b"Rewritten.\n")
    assert result == b"## Decisions\n\n###   Spaced    Heading  \n\nRewritten.\n\n## Out of Scope\n"


def test_the_section_heading_itself_is_matched_after_whitespace_and_case_folding(run_requirements, requirements_dir):
    original = b"## Goal\n\nShip it.\n\n##   decisions  \n\n### Kept\n\nPara.\n\n## Out of Scope\n"
    target = requirements_dir(original)
    result = replace(run_requirements, target, "Kept", b"Rewritten.\n")
    assert result == b"## Goal\n\nShip it.\n\n##   decisions  \n\n### Kept\n\nRewritten.\n\n## Out of Scope\n"


# --- the first of two matches -----------------------------------------------------------


def test_when_two_subsections_carry_the_heading_the_first_is_rewritten(run_requirements, requirements_dir):
    original = b"## Decisions\n\n### Twice\n\nFirst.\n\n### Twice\n\nSecond.\n"
    target = requirements_dir(original)
    result = replace(run_requirements, target, "twice", b"Rewritten.\n")
    assert result == b"## Decisions\n\n### Twice\n\nRewritten.\n\n### Twice\n\nSecond.\n"


def test_two_differently_spelled_matches_still_rewrite_the_first(run_requirements, requirements_dir):
    original = b"## Decisions\n\n### twice  over\n\nFirst.\n\n### Other\n\nMiddle.\n\n### TWICE OVER\n\nSecond.\n\n## Out of Scope\n"
    target = requirements_dir(original)
    result = replace(run_requirements, target, "Twice Over", b"Rewritten.\n")
    assert result == swapped(original, b"First.\n", b"Rewritten.\n")


# --- the subsection's extent ------------------------------------------------------------


def test_a_deeper_heading_is_body_text_rewritten_with_its_subsection(run_requirements, requirements_dir):
    original = b"## Decisions\n\n### Outer\n\nPara.\n\n#### Inner\n\nDeeper.\n\n### Next\n\nOther.\n"
    target = requirements_dir(original)
    result = replace(run_requirements, target, "Outer", b"Rewritten.\n")
    assert result == b"## Decisions\n\n### Outer\n\nRewritten.\n\n### Next\n\nOther.\n"


def test_the_last_subsection_ends_at_the_next_section_heading(run_requirements, requirements_dir):
    original = b"## Decisions\n\n### Last\n\nPara.\n\n## Out of Scope\n\n### Last\n\nOutside the section.\n"
    target = requirements_dir(original)
    result = replace(run_requirements, target, "Last", b"Rewritten.\n")
    assert result == b"## Decisions\n\n### Last\n\nRewritten.\n\n## Out of Scope\n\n### Last\n\nOutside the section.\n"


# --- a same-named subsection outside the section ----------------------------------------


def test_a_same_named_subsection_outside_decisions_is_never_rewritten(run_requirements, requirements_dir):
    target = requirements_dir()
    result = replace(run_requirements, target, "Prose decision", b"Rewritten.\n")
    starting_state = GOLDEN.split(b"## Decisions\n")[0]
    assert DECOY in starting_state
    assert result.startswith(starting_state + b"## Decisions\n")
    assert result.count(b"Rewritten.") == 1
    assert result.index(b"Rewritten.") > result.index(b"## Decisions\n")


@pytest.mark.parametrize(
    "original",
    [
        b"## Relevant starting state\n\n### Only Outside\n\nState.\n\n## Decisions\n\n### Kept\n\nPara.\n\n## Out of Scope\n",
        b"## Decisions\n\n### Kept\n\nPara.\n\n## Out of Scope\n\n### Only Outside\n\nScope.\n",
    ],
    ids=["before-decisions", "after-decisions"],
)
def test_a_heading_only_a_subsection_outside_decisions_carries_is_refused(run_requirements, requirements_dir, original):
    target = requirements_dir(original)
    result = run_requirements("replace", str(target), "--section", "Only Outside", stdin=b"Rewritten.\n")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.startswith(b"Error: ")
    assert b'"### Only Outside"' in result.stderr
    assert (target / NAME).read_bytes() == original
