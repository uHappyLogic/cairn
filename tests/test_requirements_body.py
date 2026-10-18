"""The decision on standard input is opaque Markdown: written verbatim with only its leading and
trailing blank lines trimmed, adding no bullet, bold lead, or wrapping, a heading line in it
kept as given, and a decision the section already holds folded again."""

import pytest

import requirements

NAME = requirements.REQUIREMENTS_NAME
ORIGINAL = b"## Decisions\n\n### Kept\n\nPara.\n\n## Out of Scope\n"


def fold(run_requirements, target, decision, section="Kept"):
    result = run_requirements("fold", str(target), "--section", section, stdin=decision)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    return (target / NAME).read_bytes()


def landed(inserted):
    """ORIGINAL with the given lines folded under its "### Kept" subsection."""
    return b"## Decisions\n\n### Kept\n\nPara.\n\n" + inserted + b"\n## Out of Scope\n"


@pytest.mark.parametrize(
    "decision",
    [
        b"The decision.\n",
        b"The decision.",
        b"\n\nThe decision.\n\n\n",
        b"  \n\t\nThe decision.\n \n\t \n",
        b"\r\n\r\nThe decision.\r\n\r\n",
    ],
    ids=["one-newline", "no-newline", "blank-lines", "whitespace-lines", "crlf-blank-lines"],
)
def test_only_the_outer_blank_lines_are_trimmed(run_requirements, requirements_dir, decision):
    target = requirements_dir(ORIGINAL)
    assert fold(run_requirements, target, decision) == landed(b"The decision.\n")


def test_inner_blank_lines_and_indentation_are_kept(run_requirements, requirements_dir):
    target = requirements_dir(ORIGINAL)
    decision = b"First paragraph.\n\n\nSecond paragraph,\n    indented code,\n\tand a tab.\n"
    assert fold(run_requirements, target, decision) == landed(decision)


def test_leading_whitespace_on_the_first_line_is_kept(run_requirements, requirements_dir):
    target = requirements_dir(ORIGINAL)
    assert fold(run_requirements, target, b"\n    An indented first line.\n") == landed(b"    An indented first line.\n")


def test_no_bullet_bold_lead_or_wrapping_is_added(run_requirements, requirements_dir):
    target = requirements_dir(ORIGINAL)
    long_line = b"A plain sentence that runs well past any column a wrapping writer would break at, " * 4
    decision = long_line.rstrip() + b"\n"
    assert fold(run_requirements, target, decision) == landed(decision)


def test_a_bullet_with_a_bold_lead_is_written_as_given(run_requirements, requirements_dir):
    target = requirements_dir(ORIGINAL)
    decision = b"- **Lead.** The decision as a bullet\n  with a continuation line.\n"
    assert fold(run_requirements, target, decision) == landed(decision)


def test_heading_lines_in_the_decision_are_kept(run_requirements, requirements_dir):
    target = requirements_dir(ORIGINAL)
    decision = b"### A heading inside the decision\n\nText under it.\n\n## Even a section heading\n"
    assert fold(run_requirements, target, decision) == landed(decision)


def test_markup_and_non_ascii_text_are_written_verbatim(run_requirements, requirements_dir):
    target = requirements_dir(ORIGINAL)
    decision = "Carry `code`, ${VAR}, $(cmd), 'quotes', \"quotes\", &amp; <tags>, and zażółć gęślą jaźń — as given.\n".encode("utf-8")
    assert fold(run_requirements, target, decision) == landed(decision)


def test_crlf_decision_lines_take_the_file_line_ending(run_requirements, requirements_dir):
    target = requirements_dir(ORIGINAL)
    assert fold(run_requirements, target, b"Line one.\r\nLine two.\r\n") == landed(b"Line one.\nLine two.\n")


def test_a_repeated_decision_is_folded_twice(run_requirements, requirements_dir):
    target = requirements_dir(ORIGINAL)
    fold(run_requirements, target, b"The same decision.\n")
    result = fold(run_requirements, target, b"The same decision.\n")
    assert result == landed(b"The same decision.\n\nThe same decision.\n")


def test_a_decision_the_subsection_already_holds_is_folded_again(run_requirements, requirements_dir):
    target = requirements_dir(ORIGINAL)
    result = fold(run_requirements, target, b"Para.\n")
    assert result == landed(b"Para.\n")
    assert result.count(b"Para.\n") == 2
