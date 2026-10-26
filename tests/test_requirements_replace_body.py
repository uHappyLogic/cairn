"""The new body on standard input is opaque Markdown: written verbatim in place of the old body
with only its leading and trailing blank lines trimmed, adding no bullet, bold lead, or wrapping,
a heading line in it kept as given, and a body equal to the one standing written back unchanged."""

import pytest

import requirements

NAME = requirements.REQUIREMENTS_NAME
ORIGINAL = b"## Decisions\n\n### Kept\n\nPara.\n\n## Out of Scope\n"


def replace(run_requirements, target, body, section="Kept"):
    result = run_requirements("replace", str(target), "--section", section, stdin=body)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    return (target / NAME).read_bytes()


def rewritten(body):
    """ORIGINAL with the body of its "### Kept" subsection replaced by the given lines."""
    return b"## Decisions\n\n### Kept\n\n" + body + b"\n## Out of Scope\n"


@pytest.mark.parametrize(
    "body",
    [
        b"The new body.\n",
        b"The new body.",
        b"\n\nThe new body.\n\n\n",
        b"  \n\t\nThe new body.\n \n\t \n",
        b"\r\n\r\nThe new body.\r\n\r\n",
    ],
    ids=["one-newline", "no-newline", "blank-lines", "whitespace-lines", "crlf-blank-lines"],
)
def test_only_the_outer_blank_lines_are_trimmed(run_requirements, requirements_dir, body):
    target = requirements_dir(ORIGINAL)
    assert replace(run_requirements, target, body) == rewritten(b"The new body.\n")


def test_inner_blank_lines_and_indentation_are_kept(run_requirements, requirements_dir):
    target = requirements_dir(ORIGINAL)
    body = b"First paragraph.\n\n\nSecond paragraph,\n    indented code,\n\tand a tab.\n"
    assert replace(run_requirements, target, body) == rewritten(body)


def test_leading_whitespace_on_the_first_line_is_kept(run_requirements, requirements_dir):
    target = requirements_dir(ORIGINAL)
    assert replace(run_requirements, target, b"\n    An indented first line.\n") == rewritten(b"    An indented first line.\n")


def test_no_bullet_bold_lead_or_wrapping_is_added(run_requirements, requirements_dir):
    target = requirements_dir(ORIGINAL)
    long_line = b"A plain sentence that runs well past any column a wrapping writer would break at, " * 4
    body = long_line.rstrip() + b"\n"
    assert replace(run_requirements, target, body) == rewritten(body)


def test_bullets_with_bold_leads_are_written_as_given(run_requirements, requirements_dir):
    target = requirements_dir(ORIGINAL)
    body = b"- **Lead.** The first bullet\n  with a continuation line.\n- **Other lead.** The second bullet.\n"
    assert replace(run_requirements, target, body) == rewritten(body)


def test_heading_lines_in_the_body_are_kept(run_requirements, requirements_dir):
    target = requirements_dir(ORIGINAL)
    body = b"### A heading inside the body\n\nText under it.\n\n## Even a section heading\n"
    assert replace(run_requirements, target, body) == rewritten(body)


def test_markup_and_non_ascii_text_are_written_verbatim(run_requirements, requirements_dir):
    target = requirements_dir(ORIGINAL)
    body = "Carry `code`, ${VAR}, $(cmd), 'quotes', \"quotes\", &amp; <tags>, and zażółć gęślą jaźń — as given.\n".encode("utf-8")
    assert replace(run_requirements, target, body) == rewritten(body)


def test_crlf_body_lines_take_the_file_line_ending(run_requirements, requirements_dir):
    target = requirements_dir(ORIGINAL)
    assert replace(run_requirements, target, b"Line one.\r\nLine two.\r\n") == rewritten(b"Line one.\nLine two.\n")


def test_the_standing_body_given_again_leaves_the_file_unchanged(run_requirements, requirements_dir):
    target = requirements_dir(ORIGINAL)
    assert replace(run_requirements, target, b"Para.\n") == ORIGINAL


def test_a_repeated_replace_writes_the_body_once(run_requirements, requirements_dir):
    target = requirements_dir(ORIGINAL)
    first = replace(run_requirements, target, b"The same body.\n")
    second = replace(run_requirements, target, b"The same body.\n")
    assert first == second == rewritten(b"The same body.\n")
    assert second.count(b"The same body.") == 1
