"""The fold is a byte-preserving splice: every byte outside the inserted block is written back
unchanged, one blank line separates the block from each neighbour (added only where that
neighbour is not already blank), and the file-end, empty-subsection, and bullet-list seams
each get exactly the blank lines they need."""

import difflib
from pathlib import Path

import pytest

import requirements

FIXTURES = Path(__file__).resolve().parent / "fixtures"
NAME = requirements.REQUIREMENTS_NAME
GOLDEN = (FIXTURES / NAME).read_bytes()


def fold(run_requirements, target, section, decision):
    result = run_requirements("fold", str(target), "--section", section, stdin=decision)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    return (target / NAME).read_bytes()


def after_line(data, line):
    """The offset just past the one occurrence of line (its ending included) in data."""
    assert data.count(line) == 1
    return data.index(line) + len(line)


def only_inserted_lines(before, after):
    """The lines a line diff of before against after shows, asserting it shows insertions
    only, as one contiguous run; the diff may align a blank line at either end of the run,
    so the run is returned with its outer newlines stripped."""
    old, new = before.splitlines(keepends=True), after.splitlines(keepends=True)
    opcodes = [op for op in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes() if op[0] != "equal"]
    assert len(opcodes) == 1
    tag, _, _, start, end = opcodes[0]
    assert tag == "insert"
    return b"".join(new[start:end]).strip(b"\n")


# --- the golden file --------------------------------------------------------------------


def test_the_golden_file_uses_lf_and_ends_in_one_newline():
    assert b"\r" not in GOLDEN
    assert GOLDEN.endswith(b".\n") and not GOLDEN.endswith(b"\n\n")
    assert GOLDEN.count(b"\n## Decisions\n") == 1


@pytest.mark.parametrize(
    "section, last_line, inserted",
    [
        (
            "Prose decision",
            b"It carries a second paragraph, so a fold lands after this one.\n",
            b"\nThe folded decision.\n",
        ),
        (
            "Topical bullets",
            b"  onto an indented continuation line.\n",
            b"\nThe folded decision.\n",
        ),
        (
            "Render Unicode — Text As Given",
            "including zażółć gęślą jaźń.\n".encode("utf-8"),
            b"\nThe folded decision.\n",
        ),
        (
            "A New Subsection",
            "including zażółć gęślą jaźń.\n".encode("utf-8"),
            b"\n### A New Subsection\n\nThe folded decision.\n",
        ),
    ],
)
def test_every_byte_outside_the_inserted_block_is_unchanged(run_requirements, requirements_dir, section, last_line, inserted):
    target = requirements_dir()
    result = fold(run_requirements, target, section, b"The folded decision.\n")
    offset = after_line(GOLDEN, last_line)
    assert result == GOLDEN[:offset] + inserted + GOLDEN[offset:]
    assert only_inserted_lines(GOLDEN, result) == inserted.strip(b"\n")


def test_successive_folds_each_add_only_their_own_lines(run_requirements, requirements_dir):
    target = requirements_dir()
    before = GOLDEN
    for section, decision in [
        ("Prose decision", b"First fold.\n"),
        ("Topical bullets", b"- **Third lead.** Second fold.\n"),
        ("A New Subsection", b"Third fold.\n"),
        ("a new subsection", b"Fourth fold.\n"),
    ]:
        after = fold(run_requirements, target, section, decision)
        assert only_inserted_lines(before, after).endswith(decision.strip(b"\n"))
        before = after


# --- blank lines at the seams -----------------------------------------------------------


@pytest.mark.parametrize(
    "original, expected",
    [
        (
            b"## Decisions\n\n### Kept\n\nPara.\n\n### Next\n\nOther.\n",
            b"## Decisions\n\n### Kept\n\nPara.\n\nNew.\n\n### Next\n\nOther.\n",
        ),
        (
            b"## Decisions\n\n### Kept\n\nPara.\n### Next\n\nOther.\n",
            b"## Decisions\n\n### Kept\n\nPara.\n\nNew.\n\n### Next\n\nOther.\n",
        ),
        (
            b"## Decisions\n\n### Kept\n\nPara.\n\n\n\n### Next\n",
            b"## Decisions\n\n### Kept\n\nPara.\n\nNew.\n\n\n\n### Next\n",
        ),
        (
            b"## Decisions\n\n### Kept\n\nPara.\n\n## Out of Scope\n",
            b"## Decisions\n\n### Kept\n\nPara.\n\nNew.\n\n## Out of Scope\n",
        ),
        (
            b"## Decisions\n\n### Kept\n\nPara.\n## Out of Scope\n",
            b"## Decisions\n\n### Kept\n\nPara.\n\nNew.\n\n## Out of Scope\n",
        ),
    ],
    ids=["blank-before-next", "no-blank-before-next", "several-blanks-kept", "blank-before-section", "no-blank-before-section"],
)
def test_a_blank_line_is_added_only_where_the_neighbour_is_not_blank(run_requirements, requirements_dir, original, expected):
    target = requirements_dir(original)
    assert fold(run_requirements, target, "Kept", b"New.\n") == expected


@pytest.mark.parametrize(
    "original, expected",
    [
        (b"## Decisions\n\n### Kept\n\nPara.\n", b"## Decisions\n\n### Kept\n\nPara.\n\nNew.\n"),
        (b"## Decisions\n\n### Kept\n\nPara.", b"## Decisions\n\n### Kept\n\nPara.\n\nNew."),
        (b"## Decisions\n\n### Kept\n\nPara.\n\n", b"## Decisions\n\n### Kept\n\nPara.\n\nNew.\n\n"),
        (b"## Decisions\n\n### Kept\n\nPara.\n\n\n", b"## Decisions\n\n### Kept\n\nPara.\n\nNew.\n\n\n"),
        (b"## Decisions\n", b"## Decisions\n\n### Kept\n\nNew.\n"),
        (b"## Decisions", b"## Decisions\n\n### Kept\n\nNew."),
    ],
    ids=["one-newline", "no-newline", "one-trailing-blank", "two-trailing-blanks", "bare-heading", "bare-heading-no-newline"],
)
def test_the_file_end_seam(run_requirements, requirements_dir, original, expected):
    target = requirements_dir(original)
    assert fold(run_requirements, target, "Kept", b"New.\n") == expected


def test_a_file_ending_without_a_newline_keeps_its_bytes_as_an_exact_prefix(run_requirements, requirements_dir):
    original = b"# Milestone 1: Tail\n\n## Decisions\n\n### Kept\n\nLast line has no ending."
    target = requirements_dir(original)
    result = fold(run_requirements, target, "Kept", b"New.\n")
    assert result == original + b"\n\nNew."


@pytest.mark.parametrize(
    "original, expected",
    [
        (
            b"## Decisions\n\n### Empty\n\n### Next\n\nOther.\n",
            b"## Decisions\n\n### Empty\n\nNew.\n\n### Next\n\nOther.\n",
        ),
        (
            b"## Decisions\n\n### Empty\n### Next\n\nOther.\n",
            b"## Decisions\n\n### Empty\n\nNew.\n\n### Next\n\nOther.\n",
        ),
        (
            b"## Decisions\n\n### Empty\n\n## Out of Scope\n",
            b"## Decisions\n\n### Empty\n\nNew.\n\n## Out of Scope\n",
        ),
        (
            b"## Decisions\n\n### Empty\n",
            b"## Decisions\n\n### Empty\n\nNew.\n",
        ),
        (
            b"## Decisions\n\n### Empty",
            b"## Decisions\n\n### Empty\n\nNew.",
        ),
    ],
    ids=["blank-before-next", "no-blank-before-next", "before-section", "file-end", "file-end-no-newline"],
)
def test_the_empty_subsection_seam(run_requirements, requirements_dir, original, expected):
    target = requirements_dir(original)
    assert fold(run_requirements, target, "Empty", b"New.\n") == expected


@pytest.mark.parametrize(
    "original, expected",
    [
        (
            b"## Decisions\n\n### Bullets\n\n- **A.** One.\n- **B.** Two.\n\n## Out of Scope\n",
            b"## Decisions\n\n### Bullets\n\n- **A.** One.\n- **B.** Two.\n\n- **C.** Three.\n\n## Out of Scope\n",
        ),
        (
            b"## Decisions\n\n### Bullets\n\n- **A.** One.\n- **B.** Two\n  continued.\n\n### Next\n",
            b"## Decisions\n\n### Bullets\n\n- **A.** One.\n- **B.** Two\n  continued.\n\n- **C.** Three.\n\n### Next\n",
        ),
        (
            b"## Decisions\n\n### Bullets\n\n- **A.** One.\n- **B.** Two.\n## Out of Scope\n",
            b"## Decisions\n\n### Bullets\n\n- **A.** One.\n- **B.** Two.\n\n- **C.** Three.\n\n## Out of Scope\n",
        ),
        (
            b"## Decisions\n\n### Bullets\n\n- **A.** One.\n- **B.** Two.",
            b"## Decisions\n\n### Bullets\n\n- **A.** One.\n- **B.** Two.\n\n- **C.** Three.",
        ),
    ],
    ids=["before-section", "continuation-line", "no-blank-before-section", "file-end-no-newline"],
)
def test_the_bullet_list_seam(run_requirements, requirements_dir, original, expected):
    target = requirements_dir(original)
    assert fold(run_requirements, target, "Bullets", b"- **C.** Three.\n") == expected


# --- line endings -----------------------------------------------------------------------


def test_a_crlf_file_gets_crlf_inserted_lines_and_keeps_every_other_byte(run_requirements, requirements_dir):
    original = b"# Milestone 1: CRLF\r\n\r\n## Decisions\r\n\r\n### Kept\r\n\r\nPara.\r\n\r\n## Out of Scope\r\n"
    target = requirements_dir(original)
    result = fold(run_requirements, target, "Kept", b"New line one.\nNew line two.\n")
    offset = after_line(original, b"Para.\r\n")
    assert result == original[:offset] + b"\r\nNew line one.\r\nNew line two.\r\n" + original[offset:]


def test_a_created_subsection_in_a_crlf_file_takes_crlf(run_requirements, requirements_dir):
    original = b"## Decisions\r\n\r\n## Out of Scope\r\n"
    target = requirements_dir(original)
    result = fold(run_requirements, target, "Created", b"New.\n")
    assert result == b"## Decisions\r\n\r\n### Created\r\n\r\nNew.\r\n\r\n## Out of Scope\r\n"
