"""The replace rewrites one whole "## Decisions" subsection in place: its body, from the first
non-blank line after the heading line to the last non-blank line, becomes the new body, for both
recorded decision shapes (prose paragraphs and topical bullets); the heading line, the blank lines
around the body, and every byte outside the subsection are written back unchanged, and an empty
subsection takes the new body the way a fold places a block."""

import difflib
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
BULLETS_BODY = (
    b"- **First lead.** A bullet decision under a topical subsection.\n"
    b"- **Second lead.** A bullet whose text wraps\n"
    b"  onto an indented continuation line.\n"
)
UNICODE_BODY = "Carry `code`, ${VAR}, $(cmd), &amp; entities, and \"quotes\" through untouched, including zażółć gęślą jaźń.\n".encode("utf-8")


def replace(run_requirements, target, section, body):
    result = run_requirements("replace", str(target), "--section", section, stdin=body)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    return (target / NAME).read_bytes()


def swapped(data, old, new):
    """data with its one occurrence of old replaced by new."""
    assert data.count(old) == 1
    offset = data.index(old)
    return data[:offset] + new + data[offset + len(old):]


def changed_run(before, after):
    """The (removed, added) lines a line diff of before against after shows, asserting it shows
    exactly one contiguous changed run."""
    old, new = before.splitlines(keepends=True), after.splitlines(keepends=True)
    opcodes = [op for op in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes() if op[0] != "equal"]
    assert len(opcodes) == 1
    _, old_start, old_end, new_start, new_end = opcodes[0]
    return b"".join(old[old_start:old_end]), b"".join(new[new_start:new_end])


# --- the golden file --------------------------------------------------------------------


def test_the_golden_file_holds_both_decision_shapes():
    decisions = GOLDEN.split(b"\n## Decisions\n")[1]
    assert b"### Prose decision\n\n" + PROSE_BODY + b"\n### Topical bullets\n" in decisions
    assert b"### Topical bullets\n\n" + BULLETS_BODY + b"\n### Render Unicode" in decisions


def test_a_prose_subsection_is_rewritten_whole(run_requirements, requirements_dir):
    target = requirements_dir()
    body = b"The rewritten decision, one paragraph in place of two.\n"
    result = replace(run_requirements, target, "Prose decision", body)
    assert result == swapped(GOLDEN, b"\n## Decisions\n\n### Prose decision\n\n" + PROSE_BODY, b"\n## Decisions\n\n### Prose decision\n\n" + body)
    assert changed_run(GOLDEN, result) == (PROSE_BODY, body)


def test_a_topical_subsection_is_rewritten_whole_with_its_unchanged_bullets(run_requirements, requirements_dir):
    target = requirements_dir()
    body = (
        b"- **First lead.** A bullet decision under a topical subsection.\n"
        b"- **Second lead.** The second bullet, rewritten to supersede what it said.\n"
    )
    result = replace(run_requirements, target, "Topical bullets", body)
    assert result == swapped(GOLDEN, b"### Topical bullets\n\n" + BULLETS_BODY, b"### Topical bullets\n\n" + body)
    removed, added = changed_run(GOLDEN, result)
    assert removed == b"- **Second lead.** A bullet whose text wraps\n  onto an indented continuation line.\n"
    assert added == b"- **Second lead.** The second bullet, rewritten to supersede what it said.\n"


def test_a_topical_subsection_may_lose_and_gain_bullets(run_requirements, requirements_dir):
    target = requirements_dir()
    body = b"- **Only lead.** One bullet in place of two.\n- **New lead.** And one more.\n"
    result = replace(run_requirements, target, "Topical bullets", body)
    assert result == swapped(GOLDEN, BULLETS_BODY, body)


def test_the_last_subsection_is_rewritten_up_to_the_next_section(run_requirements, requirements_dir):
    target = requirements_dir()
    body = b"The last subsection, rewritten.\n"
    result = replace(run_requirements, target, "Render Unicode — Text As Given", body)
    assert result == swapped(GOLDEN, UNICODE_BODY + b"\n## Out of Scope\n", body + b"\n## Out of Scope\n")
    assert changed_run(GOLDEN, result) == (UNICODE_BODY, body)


@pytest.mark.parametrize(
    "section, heading_line",
    [
        ("Prose decision", b"### Prose decision\n"),
        ("Topical bullets", b"### Topical bullets\n"),
        ("Render Unicode — Text As Given", "### Render Unicode — Text As Given\n".encode("utf-8")),
    ],
)
def test_the_heading_line_and_every_byte_outside_the_body_are_unchanged(run_requirements, requirements_dir, section, heading_line):
    target = requirements_dir()
    result = replace(run_requirements, target, section, b"The rewritten body.\n")
    decisions_at = GOLDEN.index(b"\n## Decisions\n")
    heading_at = GOLDEN.index(heading_line, decisions_at)
    kept_prefix = GOLDEN[:heading_at + len(heading_line) + 1]
    assert result.startswith(kept_prefix)
    following = GOLDEN.find(b"\n### ", heading_at + 1)
    out_of_scope = GOLDEN.index(b"\n## Out of Scope\n")
    end = following if following != -1 and following < out_of_scope else out_of_scope
    kept_suffix = GOLDEN[end:]
    assert result.endswith(kept_suffix)
    assert result == kept_prefix + b"The rewritten body.\n" + kept_suffix


def test_successive_replaces_each_change_only_their_own_subsection(run_requirements, requirements_dir):
    target = requirements_dir()
    before = GOLDEN
    for section, body in [
        ("Prose decision", b"First rewrite.\n"),
        ("Topical bullets", b"- **Lead.** Second rewrite.\n"),
        ("prose decision", b"Third rewrite.\n"),
    ]:
        after = replace(run_requirements, target, section, body)
        assert changed_run(before, after)[1] == body
        before = after
    assert before == swapped(swapped(GOLDEN, PROSE_BODY, b"Third rewrite.\n"), BULLETS_BODY, b"- **Lead.** Second rewrite.\n")


# --- blank lines around the body --------------------------------------------------------


@pytest.mark.parametrize(
    "original, expected",
    [
        (
            b"## Decisions\n\n### Kept\n\nPara.\n\n### Next\n\nOther.\n",
            b"## Decisions\n\n### Kept\n\nNew.\n\n### Next\n\nOther.\n",
        ),
        (
            b"## Decisions\n\n### Kept\n\nPara.\n### Next\n\nOther.\n",
            b"## Decisions\n\n### Kept\n\nNew.\n### Next\n\nOther.\n",
        ),
        (
            b"## Decisions\n\n### Kept\nPara.\n\n### Next\n",
            b"## Decisions\n\n### Kept\nNew.\n\n### Next\n",
        ),
        (
            b"## Decisions\n\n### Kept\n\n\nPara.\n\n\n\n### Next\n",
            b"## Decisions\n\n### Kept\n\n\nNew.\n\n\n\n### Next\n",
        ),
        (
            b"## Decisions\n\n### Kept\n\nOne.\n\n\nTwo.\n  Three.\n\n## Out of Scope\n",
            b"## Decisions\n\n### Kept\n\nNew.\n\n## Out of Scope\n",
        ),
        (
            b"## Decisions\n\n### Kept\n\nPara.\n## Out of Scope\n",
            b"## Decisions\n\n### Kept\n\nNew.\n## Out of Scope\n",
        ),
    ],
    ids=["blank-before-next", "no-blank-before-next", "no-blank-after-heading", "several-blanks-kept", "inner-blanks-replaced", "no-blank-before-section"],
)
def test_the_blank_lines_around_the_body_are_kept_as_they_are(run_requirements, requirements_dir, original, expected):
    target = requirements_dir(original)
    assert replace(run_requirements, target, "Kept", b"New.\n") == expected


@pytest.mark.parametrize(
    "original, expected",
    [
        (b"## Decisions\n\n### Kept\n\nPara.\n", b"## Decisions\n\n### Kept\n\nNew.\n"),
        (b"## Decisions\n\n### Kept\n\nPara.", b"## Decisions\n\n### Kept\n\nNew."),
        (b"## Decisions\n\n### Kept\n\nPara.\n\n", b"## Decisions\n\n### Kept\n\nNew.\n\n"),
        (b"## Decisions\n\n### Kept\n\nPara.\n\n\n", b"## Decisions\n\n### Kept\n\nNew.\n\n\n"),
    ],
    ids=["one-newline", "no-newline", "one-trailing-blank", "two-trailing-blanks"],
)
def test_the_file_end_seam(run_requirements, requirements_dir, original, expected):
    target = requirements_dir(original)
    assert replace(run_requirements, target, "Kept", b"New.\n") == expected


def test_a_file_ending_without_a_newline_keeps_ending_without_one(run_requirements, requirements_dir):
    original = b"# Milestone 1: Tail\n\n## Decisions\n\n### Kept\n\nLast line has no ending."
    target = requirements_dir(original)
    result = replace(run_requirements, target, "Kept", b"Line one.\nLine two.\n")
    assert result == b"# Milestone 1: Tail\n\n## Decisions\n\n### Kept\n\nLine one.\nLine two."


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
def test_an_empty_subsection_takes_the_body_as_a_fold_places_a_block(run_requirements, requirements_dir, original, expected):
    target = requirements_dir(original)
    assert replace(run_requirements, target, "Empty", b"New.\n") == expected


# --- line endings -----------------------------------------------------------------------


def test_a_crlf_file_gets_crlf_body_lines_and_keeps_every_other_byte(run_requirements, requirements_dir):
    original = b"# Milestone 1: CRLF\r\n\r\n## Decisions\r\n\r\n### Kept\r\n\r\nPara.\r\n\r\n## Out of Scope\r\n"
    target = requirements_dir(original)
    result = replace(run_requirements, target, "Kept", b"New line one.\nNew line two.\n")
    assert result == swapped(original, b"Para.\r\n", b"New line one.\r\nNew line two.\r\n")


def test_an_empty_subsection_in_a_crlf_file_takes_crlf(run_requirements, requirements_dir):
    original = b"## Decisions\r\n\r\n### Empty\r\n\r\n## Out of Scope\r\n"
    target = requirements_dir(original)
    result = replace(run_requirements, target, "Empty", b"New.\n")
    assert result == b"## Decisions\r\n\r\n### Empty\r\n\r\nNew.\r\n\r\n## Out of Scope\r\n"
