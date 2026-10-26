"""The replace's refusals: a heading no "## Decisions" subsection carries, named in the Error line
and never created, plus the refusals it shares with the fold (an empty heading or body, a missing
or non-UTF-8 requirements.md, and a file holding no column-0 "## Decisions" heading or more than
one), each one Error line with exit 1 and the file byte-for-byte unchanged."""

from pathlib import Path

import pytest

import requirements

FIXTURES = Path(__file__).resolve().parent / "fixtures"
NAME = requirements.REQUIREMENTS_NAME
GOLDEN = (FIXTURES / NAME).read_bytes()


def assert_refused(result, reason):
    assert result.returncode == 1
    assert result.stdout == b""
    lines = result.stderr.decode("utf-8").split("\n")
    assert len(lines) == 2 and lines[1] == ""
    assert lines[0].startswith("Error: ")
    assert reason in lines[0]
    assert "Traceback" not in lines[0]


# --- a missing subsection ---------------------------------------------------------------


@pytest.mark.parametrize(
    "section, named",
    [
        ("A Missing Heading", '"### A Missing Heading"'),
        ("  A  Missing\tHeading ", '"### A Missing Heading"'),
        ("Prose", '"### Prose"'),
        ("Prose decision extended", '"### Prose decision extended"'),
    ],
    ids=["absent", "folded-in-the-message", "a-prefix-is-not-a-match", "a-longer-title-is-not-a-match"],
)
def test_a_missing_subsection_is_refused_naming_the_heading(run_requirements, requirements_dir, section, named):
    target = requirements_dir()
    result = run_requirements("replace", str(target), "--section", section, stdin=b"A new body.\n")
    assert_refused(result, named)
    assert 'under "## Decisions"' in result.stderr.decode("utf-8")
    assert (target / NAME).read_bytes() == GOLDEN


def test_a_missing_subsection_is_never_created(run_requirements, requirements_dir):
    target = requirements_dir()
    result = run_requirements("replace", str(target), "--section", "A Missing Heading", stdin=b"A new body.\n")
    assert_refused(result, "never creates one")
    after = (target / NAME).read_bytes()
    assert after == GOLDEN
    assert b"A Missing Heading" not in after
    assert b"A new body." not in after


def test_an_empty_decisions_section_has_no_subsection_to_replace(run_define, run_requirements, workspace):
    root = workspace()
    defined = run_define("--title", "First", stdin=b"Ship it.\n", cwd=root)
    assert defined.returncode == 0, defined.stderr
    target = root / "milestones" / "milestone_01_first"
    template = (target / NAME).read_bytes()
    result = run_requirements("replace", str(target), "--section", "Opening Decision", stdin=b"A new body.\n")
    assert_refused(result, '"### Opening Decision"')
    assert (target / NAME).read_bytes() == template


# --- an empty heading or body -----------------------------------------------------------


@pytest.mark.parametrize("body", [b"", b"\n", b"\n\n\n", b"  \n\t\n \r\n"], ids=["empty", "newline", "newlines", "whitespace"])
def test_an_empty_body_is_refused(run_requirements, requirements_dir, body):
    target = requirements_dir()
    result = run_requirements("replace", str(target), "--section", "Prose decision", stdin=body)
    assert_refused(result, "the new subsection body on standard input is empty")
    assert (target / NAME).read_bytes() == GOLDEN


@pytest.mark.parametrize("section", ["", "   ", "\n\t"], ids=["empty", "spaces", "whitespace"])
def test_an_empty_heading_is_refused(run_requirements, requirements_dir, section):
    target = requirements_dir()
    result = run_requirements("replace", str(target), "--section", section, stdin=b"A new body.\n")
    assert_refused(result, "the subsection heading given as --section is empty")
    assert (target / NAME).read_bytes() == GOLDEN


# --- a missing or non-UTF-8 file --------------------------------------------------------


def test_a_missing_requirements_file_is_refused_and_nothing_is_created(run_requirements, tmp_path):
    target = tmp_path / "milestone"
    target.mkdir()
    result = run_requirements("replace", str(target), "--section", "Prose decision", stdin=b"A new body.\n")
    assert_refused(result, "does not exist")
    assert list(target.iterdir()) == []


def test_a_non_utf8_requirements_file_is_refused(run_requirements, requirements_dir):
    original = b"# Milestone 1: Bad \xff bytes\n\n## Decisions\n\n### Kept\n\nPara.\n"
    target = requirements_dir(original)
    result = run_requirements("replace", str(target), "--section", "Kept", stdin=b"A new body.\n")
    assert_refused(result, "is not UTF-8 text")
    assert (target / NAME).read_bytes() == original


# --- no single Decisions section --------------------------------------------------------


@pytest.mark.parametrize(
    "original",
    [
        b"# Milestone 1: None\n\n## Goal\n\nShip it.\n\n### Kept\n\nPara.\n\n## Out of Scope\n",
        b"## Goal\n\n ## Decisions\n\n### Kept\n\nAn indented heading is not a section.\n",
        b"## Goal\n\n### Decisions\n\n### Kept\n\nA subsection is not the section.\n",
        b"## Goal\n\n## Decision\n\n### Kept\n\nThe singular is another title.\n",
        b"## Goal\n\n## Decisions made\n\n### Kept\n\nA longer title is another title.\n",
        b"## Goal\n\nThe prose names `## Decisions` without holding the heading.\n\n### Kept\n\nPara.\n",
        b"",
    ],
    ids=["absent", "indented", "subsection", "singular", "longer", "in-prose", "empty-file"],
)
def test_a_file_holding_no_decisions_heading_is_refused(run_requirements, requirements_dir, original):
    target = requirements_dir(original)
    result = run_requirements("replace", str(target), "--section", "Kept", stdin=b"A new body.\n")
    assert_refused(result, 'holds no column-0 "## Decisions" heading')
    assert (target / NAME).read_bytes() == original


@pytest.mark.parametrize(
    "original, numbers",
    [
        (b"## Decisions\n\n### Kept\n\nPara.\n\n## Decisions\n\nAgain.\n", "lines 1, 7"),
        (b"## Goal\n\n## Decisions\n\n### Kept\n\nPara.\n\n## decisions\n", "lines 3, 9"),
        (b"## Decisions\n## Decisions\n### Kept\n## Decisions\n", "lines 1, 2, 4"),
    ],
    ids=["two", "case-folded", "three"],
)
def test_a_file_holding_more_than_one_decisions_heading_is_refused(run_requirements, requirements_dir, original, numbers):
    target = requirements_dir(original)
    result = run_requirements("replace", str(target), "--section", "Kept", stdin=b"A new body.\n")
    assert_refused(result, 'column-0 "## Decisions" headings')
    assert numbers in result.stderr.decode("utf-8")
    assert (target / NAME).read_bytes() == original
