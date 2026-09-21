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
    <alternative id="First">
      The first way, with &apos;quotes&apos; and &quot;doubles&quot; and a &gt; sign.
      <advantage>Simple</advantage>
      <drawback>Slow</drawback>
    </alternative>
    <alternative id="Second">
      The second way.
      <advantage>Fast</advantage>
      <drawback>Complex</drawback>
    </alternative>
    <applied-principle>Prefer the shorter path</applied-principle>
    <depends-on question="Other" option="X"/>
    <recommendation option="Second">Chosen because it is shorter.</recommendation>
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
