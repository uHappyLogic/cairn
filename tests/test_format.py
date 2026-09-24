"""The canonical document format: parse and render are inverse on a golden file, and every
non-canonical input renders to the same fixed shape."""

from pathlib import Path

import pytest

import open_questions
from open_questions import (
    Alternative,
    Dependency,
    Document,
    Question,
    Recommendation,
    ToolError,
    escape,
    fold,
    parse_document,
    render_document,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"
FIXTURE_NAMES = sorted(path.name for path in FIXTURES.iterdir() if path.is_dir())


def read_fixture(name):
    return (FIXTURES / name / open_questions.DOCUMENT_NAME).read_text(encoding="utf-8")


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_write_read_round_trip_is_the_identity_on_a_golden_file(name):
    text = read_fixture(name)
    assert render_document(parse_document(text)) == text


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_golden_files_use_lf_and_end_with_one_newline(name):
    data = (FIXTURES / name / open_questions.DOCUMENT_NAME).read_bytes()
    assert b"\r" not in data
    assert data.endswith(b"\n") and not data.endswith(b"\n\n")


def test_the_empty_document_is_one_self_closing_root():
    assert render_document(Document()) == "<open-questions/>\n"
    assert render_document(Document()) == read_fixture("empty")
    assert render_document(parse_document("<open-questions>\n</open-questions>\n")) == "<open-questions/>\n"


def test_escape_substitutes_the_five_predefined_entities():
    assert escape("""& < > " '""") == "&amp; &lt; &gt; &quot; &apos;"
    assert escape("&amp;") == "&amp;amp;"


def test_fold_collapses_whitespace_runs_and_trims():
    assert fold("  one\n  two\t\tthree  \n") == "one two three"
    assert fold(None) == ""


NON_CANONICAL = """\
<?xml version="1.0" encoding="UTF-8"?>
<open-questions>
    <open-question id="  Spaced   id ">
        <recommendation option="Second">Chosen
because it is
   shorter.</recommendation>
        <applied-principle>Prefer the shorter path</applied-principle>
        <alternative id="First">
            <drawback>Slow</drawback>
            The first way, with 'quotes' and "doubles" and a > sign.
            <advantage>Simple</advantage>
        </alternative>
        <depends-on question="Other" option="X" />
        <alternative id="Second">
            The second\tway.
            <advantage>Fast</advantage>
            <drawback>Complex</drawback>
        </alternative>
        <question>Which
way?</question>
    </open-question>
</open-questions>
"""

CANONICAL = """\
<open-questions>
  <open-question id="Spaced id">
    <question>Which way?</question>
    <applied-principle>Prefer the shorter path</applied-principle>
    <depends-on question="Other" option="X"/>
    <recommendation option="Second">Chosen because it is shorter.</recommendation>
    <alternative id="Second">
      The second way.
      <advantage>Fast</advantage>
      <drawback>Complex</drawback>
    </alternative>
    <alternative id="First">
      The first way, with &apos;quotes&apos; and &quot;doubles&quot; and a &gt; sign.
      <advantage>Simple</advantage>
      <drawback>Slow</drawback>
    </alternative>
  </open-question>
</open-questions>
"""


def test_render_normalizes_indentation_child_order_whitespace_and_escaping():
    assert render_document(parse_document(NON_CANONICAL)) == CANONICAL


def test_render_is_idempotent():
    once = render_document(parse_document(NON_CANONICAL))
    assert render_document(parse_document(once)) == once


def test_parse_builds_the_model():
    document = parse_document(NON_CANONICAL)
    assert document == Document(
        [
            Question(
                id="Spaced id",
                question="Which way?",
                alternatives=[
                    Alternative("First", "The first way, with 'quotes' and \"doubles\" and a > sign.", ["Simple"], ["Slow"]),
                    Alternative("Second", "The second way.", ["Fast"], ["Complex"]),
                ],
                principles=["Prefer the shorter path"],
                depends_on=[Dependency("Other", "X")],
                recommendation=Recommendation("Second", "Chosen because it is shorter."),
            )
        ]
    )


def child_heads(text):
    """The opening line of every child of the document's blocks, in document order."""
    return [line.strip() for line in text.split("\n") if line.startswith("    <") and not line.startswith("    </")]


def recommended(option, *alternative_ids, principles=("P",), depends_on=(Dependency("Other", "X"),)):
    return Question(
        id="Q",
        question="Which?",
        alternatives=[Alternative(alternative_id, f"{alternative_id} is this.") for alternative_id in alternative_ids],
        principles=list(principles),
        depends_on=list(depends_on),
        recommendation=Recommendation(option, "Because."),
    )


def test_render_promotes_the_named_alternative_and_keeps_the_rest_in_relative_order():
    text = render_document(Document([recommended("c", "A", "B", "C", "D")]))
    assert child_heads(text) == [
        "<question>Which?</question>",
        "<applied-principle>P</applied-principle>",
        '<depends-on question="Other" option="X"/>',
        '<recommendation option="c">Because.</recommendation>',
        '<alternative id="C">',
        '<alternative id="A">',
        '<alternative id="B">',
        '<alternative id="D">',
    ]
    reparsed = parse_document(text).questions[0]
    assert [alternative.id for alternative in reparsed.alternatives] == ["C", "A", "B", "D"]
    assert render_document(parse_document(text)) == text


def test_render_of_an_already_first_named_alternative_moves_only_the_recommendation_half():
    text = render_document(Document([recommended("A", "A", "B", principles=(), depends_on=())]))
    assert child_heads(text) == [
        "<question>Which?</question>",
        '<recommendation option="A">Because.</recommendation>',
        '<alternative id="A">',
        '<alternative id="B">',
    ]


def test_render_of_an_unmatched_option_puts_the_recommendation_half_first_and_promotes_nothing():
    text = render_document(Document([recommended("Nope", "X", "Y", "Z")]))
    assert child_heads(text) == [
        "<question>Which?</question>",
        "<applied-principle>P</applied-principle>",
        '<depends-on question="Other" option="X"/>',
        '<recommendation option="Nope">Because.</recommendation>',
        '<alternative id="X">',
        '<alternative id="Y">',
        '<alternative id="Z">',
    ]
    assert render_document(parse_document(text)) == text


def test_a_writer_saves_a_block_with_an_unmatched_option_without_failing(run_tool, tmp_path):
    open_questions.save_document(str(tmp_path), Document([recommended("Nope", "Y", "X")]))
    result = run_tool("add", str(tmp_path), "Later", stdin=b"Is there more?")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    text = (tmp_path / open_questions.DOCUMENT_NAME).read_text(encoding="utf-8")
    assert child_heads(text) == [
        "<question>Which?</question>",
        "<applied-principle>P</applied-principle>",
        '<depends-on question="Other" option="X"/>',
        '<recommendation option="Nope">Because.</recommendation>',
        '<alternative id="Y">',
        '<alternative id="X">',
        "<question>Is there more?</question>",
    ]


def test_render_of_a_block_without_a_recommendation_keeps_the_alternatives_first():
    question = recommended("B", "A", "B")
    question.recommendation = None
    assert child_heads(render_document(Document([question]))) == [
        "<question>Which?</question>",
        '<alternative id="A">',
        '<alternative id="B">',
        "<applied-principle>P</applied-principle>",
        '<depends-on question="Other" option="X"/>',
    ]


OLD_ORDER = """\
<open-questions>
  <open-question id="Old">
    <question>Which one?</question>
    <alternative id="First">
      First way.
    </alternative>
    <alternative id="Second">
      Second way.
    </alternative>
    <applied-principle>Keep it short</applied-principle>
    <recommendation option="Second">Second is shorter.</recommendation>
  </open-question>
</open-questions>
"""


def test_an_old_order_document_stays_as_written_until_a_writer_next_saves_it(run_tool, tmp_path):
    target = tmp_path / open_questions.DOCUMENT_NAME
    target.write_text(OLD_ORDER, encoding="utf-8")
    directory = str(tmp_path)
    reading = (
        ("list", directory),
        ("list", "--without-recommendation", directory),
        ("walk", directory),
        ("locate", directory, "Old"),
        ("lift", directory, "Old"),
        ("sort", directory),
    )
    for args in reading:
        result = run_tool(*args)
        assert (result.returncode, result.stderr) == (0, b"")
        assert target.read_text(encoding="utf-8") == OLD_ORDER
    assert run_tool("add", str(tmp_path), "New", stdin=b"And this?").returncode == 0
    assert target.read_text(encoding="utf-8") == (
        "<open-questions>\n"
        '  <open-question id="Old">\n'
        "    <question>Which one?</question>\n"
        "    <applied-principle>Keep it short</applied-principle>\n"
        '    <recommendation option="Second">Second is shorter.</recommendation>\n'
        '    <alternative id="Second">\n'
        "      Second way.\n"
        "    </alternative>\n"
        '    <alternative id="First">\n'
        "      First way.\n"
        "    </alternative>\n"
        "  </open-question>\n"
        '  <open-question id="New">\n'
        "    <question>And this?</question>\n"
        "  </open-question>\n"
        "</open-questions>\n"
    )


def test_an_alternative_without_advantage_or_drawback_keeps_its_text_on_its_own_line():
    document = Document([Question("Q", "Why?", alternatives=[Alternative("Only", "Just this.")])])
    assert render_document(document) == (
        "<open-questions>\n"
        '  <open-question id="Q">\n'
        "    <question>Why?</question>\n"
        '    <alternative id="Only">\n'
        "      Just this.\n"
        "    </alternative>\n"
        "  </open-question>\n"
        "</open-questions>\n"
    )


def test_ids_and_options_are_escaped_in_attributes():
    document = Document([Question('A & "B"', "Q?", recommendation=Recommendation("It's <x>", "Because."))])
    text = render_document(document)
    assert '<open-question id="A &amp; &quot;B&quot;">' in text
    assert '<recommendation option="It&apos;s &lt;x&gt;">Because.</recommendation>' in text
    assert render_document(parse_document(text)) == text


BLOCK = '<open-questions><open-question id="A">{body}</open-question></open-questions>'


@pytest.mark.parametrize(
    ("text", "reason"),
    [
        ("<open-questions>", "not well-formed XML"),
        ("<questions/>", "<questions> root, not <open-questions>"),
        ('<open-questions version="1"/>', 'unknown attribute "version"'),
        ("<open-questions>stray</open-questions>", "<open-questions> carries text"),
        ("<open-questions><question>Q</question></open-questions>", "unexpected <question> element"),
        (BLOCK.format(body="<question>Q</question><foo/>"), 'id="A"> carries an unexpected <foo> element'),
        (BLOCK.format(body="stray<question>Q</question>"), 'id="A"> carries text outside'),
        (BLOCK.format(body="<question>Q</question>stray"), 'id="A"> carries text outside'),
        (BLOCK.format(body="<alternative id='X'>t</alternative>"), "has no <question> element"),
        (BLOCK.format(body="<question>Q</question><question>R</question>"), "carries 2 <question> elements"),
        (
            BLOCK.format(body='<question>Q</question><recommendation option="X">a</recommendation><recommendation option="X">b</recommendation>'),
            "carries 2 <recommendation> elements",
        ),
        (BLOCK.format(body="<question>Q<b>bold</b></question>"), "<question> element of <open-question id=\"A\"> carries an unexpected <b>"),
        (BLOCK.format(body='<question>Q</question><depends-on question="B"/>'), "<depends-on> element of <open-question id=\"A\"> has no option attribute"),
        (BLOCK.format(body='<question>Q</question><depends-on question="B" option="X">t</depends-on>'), "<depends-on> element of <open-question id=\"A\"> carries text"),
        (BLOCK.format(body='<question>Q</question><recommendation>r</recommendation>'), "has no option attribute"),
        (BLOCK.format(body='<question>Q</question><recommendation option="">r</recommendation>'), "has an empty option attribute"),
        (BLOCK.format(body='<question>Q</question><alternative id="X">t</alternative><alternative id="x">u</alternative>'), 'two <alternative> elements with the id "x"'),
        (BLOCK.format(body='<question>Q</question><alternative id="X"><note/></alternative>'), '<alternative id="X"> of <open-question id="A"> carries an unexpected <note>'),
        ('<open-questions><open-question><question>Q</question></open-question></open-questions>', "an <open-question> element has no id attribute"),
        (
            '<open-questions><open-question id="A"><question>Q</question></open-question><open-question id="a"><question>R</question></open-question></open-questions>',
            'two <open-question> blocks carry the id "a"',
        ),
    ],
)
def test_parse_rejects_every_shape_outside_the_model(text, reason):
    with pytest.raises(ToolError) as info:
        parse_document(text)
    assert reason in str(info.value)
    assert "\n" not in str(info.value)
