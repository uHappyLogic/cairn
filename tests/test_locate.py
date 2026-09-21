"""The locate subcommand: each named block printed verbatim, byte-for-byte the lines the
document holds, in the order named, once each."""

from pathlib import Path

import pytest

import open_questions

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def block_text(fixture, short_title):
    """The named block's lines exactly as the golden file holds them, sliced from the raw
    text by its opening and closing lines."""
    lines = (FIXTURES / fixture / open_questions.DOCUMENT_NAME).read_text(encoding="utf-8").split("\n")
    opening = f'  <open-question id="{open_questions.escape(short_title)}">'
    start = lines.index(opening)
    end = lines.index("  </open-question>", start)
    return "\n".join(lines[start : end + 1]) + "\n"


@pytest.mark.parametrize(
    ("fixture", "short_title"),
    [
        ("annotated", "Escape hatch under sole writer"),
        ("annotated", "Root element form"),
        ("annotated", "Fixture bare block"),
        ("bare", "First bare question"),
        ("bare", "Second bare question"),
        ("entities", "Ampersand & angle <brackets>, \"quotes\", 'apostrophes'"),
    ],
)
def test_locate_prints_the_block_verbatim_as_the_file_holds_it(run_tool, milestone_dir, fixture, short_title):
    result = run_tool("locate", str(milestone_dir(fixture)), short_title)
    assert (result.returncode, result.stderr) == (0, b"")
    assert result.stdout.decode("utf-8") == block_text(fixture, short_title)


def test_locate_keeps_the_entities_and_indentation_of_the_file(run_tool, milestone_dir):
    result = run_tool("locate", str(milestone_dir("entities")), "Ampersand & angle <brackets>, \"quotes\", 'apostrophes'")
    text = result.stdout.decode("utf-8")
    assert text.startswith('  <open-question id="Ampersand &amp; angle &lt;brackets&gt;, &quot;quotes&quot;, &apos;apostrophes&apos;">\n')
    assert '    <recommendation option="A &amp; B">' in text
    assert text.endswith("  </open-question>\n")


def test_locate_of_a_bare_block_is_the_wrapper_question_and_closing_tag(run_tool, milestone_dir):
    result = run_tool("locate", str(milestone_dir("bare")), "Second bare question")
    assert result.stdout.decode("utf-8") == (
        '  <open-question id="Second bare question">\n'
        "    <question>What follows from the first decision?</question>\n"
        "  </open-question>\n"
    )


def test_locate_prints_several_blocks_in_the_order_named(run_tool, milestone_dir):
    result = run_tool("locate", str(milestone_dir("annotated")), "Fixture bare block", "Root element form")
    assert (result.returncode, result.stderr) == (0, b"")
    assert result.stdout.decode("utf-8") == (
        block_text("annotated", "Fixture bare block") + block_text("annotated", "Root element form")
    )


def test_locate_matches_the_short_title_case_folded(run_tool, milestone_dir):
    target = str(milestone_dir("annotated"))
    exact = run_tool("locate", target, "Root element form")
    folded = run_tool("locate", target, "ROOT ELEMENT form")
    assert folded.returncode == 0
    assert folded.stdout == exact.stdout


def test_locate_matches_the_short_title_against_the_un_escaped_id(run_tool, milestone_dir):
    target = str(milestone_dir("entities"))
    un_escaped = run_tool("locate", target, "ampersand & ANGLE <brackets>, \"quotes\", 'apostrophes'")
    assert un_escaped.returncode == 0
    assert un_escaped.stdout.decode("utf-8") == block_text("entities", "Ampersand & angle <brackets>, \"quotes\", 'apostrophes'")
    escaped = run_tool("locate", target, "Ampersand &amp; angle &lt;brackets&gt;, &quot;quotes&quot;, &apos;apostrophes&apos;")
    assert escaped.returncode == 1


def test_locate_prints_a_block_named_twice_once(run_tool, milestone_dir):
    result = run_tool("locate", str(milestone_dir("bare")), "First bare question", "first BARE question")
    assert (result.returncode, result.stderr) == (0, b"")
    assert result.stdout.decode("utf-8") == block_text("bare", "First bare question")


def test_locate_of_an_unknown_id_fails_naming_the_ids_the_document_holds(run_tool, milestone_dir):
    target = milestone_dir("bare")
    result = run_tool("locate", str(target), "Third bare question")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.decode("utf-8") == (
        'Error: no <open-question> block has the id "Third bare question"; '
        'the document holds "First bare question", "Second bare question"\n'
    )


def test_locate_on_an_empty_document_fails_saying_it_holds_no_blocks(run_tool, milestone_dir):
    result = run_tool("locate", str(milestone_dir("empty")), "Anything")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == b'Error: no <open-question> block has the id "Anything"; the document holds no blocks\n'


def test_locate_with_one_unknown_id_among_known_ones_prints_nothing(run_tool, milestone_dir):
    result = run_tool("locate", str(milestone_dir("bare")), "First bare question", "Missing", "Second bare question")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.startswith(b'Error: no <open-question> block has the id "Missing"')
    assert result.stderr.count(b"\n") == 1


def test_locate_requires_at_least_one_short_title(run_tool, milestone_dir):
    result = run_tool("locate", str(milestone_dir("bare")))
    assert result.returncode == 2
    assert result.stdout == b""
    assert b"SHORT_TITLE" in result.stderr


def test_locate_fails_when_the_document_is_missing(run_tool, tmp_path):
    result = run_tool("locate", str(tmp_path), "Anything")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == f"Error: {tmp_path / open_questions.DOCUMENT_NAME} does not exist\n".encode("utf-8")


def test_locate_leaves_the_document_unchanged(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    document = target / open_questions.DOCUMENT_NAME
    before = document.read_bytes()
    run_tool("locate", str(target), "Root element form")
    run_tool("locate", str(target), "Missing")
    assert document.read_bytes() == before
    assert sorted(path.name for path in target.iterdir()) == [open_questions.DOCUMENT_NAME]


def test_find_question_is_case_folded_and_find_questions_is_ordered_and_deduplicated():
    document = open_questions.parse_document(
        (FIXTURES / "bare" / open_questions.DOCUMENT_NAME).read_text(encoding="utf-8")
    )
    first, second = document.questions
    assert open_questions.find_question(document, "FIRST BARE QUESTION") is first
    assert open_questions.find_questions(document, ["Second bare question", "first bare question", "SECOND BARE QUESTION"]) == [second, first]
    with pytest.raises(open_questions.ToolError) as info:
        open_questions.find_questions(document, ["First bare question", "Nope"])
    assert 'no <open-question> block has the id "Nope"' in str(info.value)
