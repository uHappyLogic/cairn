"""The embed subcommand: the recommend agent's whole final message read from standard input,
the fragment sliced from its first <alternative line through its last </recommendation> line
(the identity on a clean return), parsed and validated — no wrapper or <question> line, no
text outside the elements, at least one <alternative>, exactly one <recommendation> naming one
of the fragment's alternatives, every <depends-on> resolving one hop against an annotated block
and one of its alternatives, no element of an unknown kind, and never the order of the
children — then written as the block's children grouped by kind; every miss, the two extraction
misses included, is one Error line with the document unchanged."""

import io
import os
import subprocess
import sys
from pathlib import Path

import pytest

import open_questions
from open_questions import Alternative, Dependency, Document, Question, Recommendation

FIXTURES = Path(__file__).resolve().parent / "fixtures"
TOOL = Path(open_questions.__file__).resolve()
ENTITIES_TITLE = "Ampersand & angle <brackets>, \"quotes\", 'apostrophes'"
HATCH = "Escape hatch under sole writer"
ROOT_FORM = "Root element form"
BARE = "Fixture bare block"

CLEAN = """\
  <alternative id="Option A">
    What option A is.
    <advantage>The strongest reason to choose A.</advantage>
    <drawback>The main cost A carries.</drawback>
  </alternative>
  <alternative id="Option B">
    What option B is.
    <advantage>The strongest reason to choose B.</advantage>
    <drawback>The main cost B carries.</drawback>
  </alternative>
  <applied-principle>One rule over two</applied-principle>
  <depends-on question="Root element form" option="Self-closing root"/>
  <recommendation option="Option A">A wins because of one stated reason.</recommendation>"""

MINIMAL = """\
<alternative id="Only">Just this.</alternative>
<recommendation option="Only">Nothing else applies.</recommendation>"""


def read_fixture(name):
    return (FIXTURES / name / open_questions.DOCUMENT_NAME).read_text(encoding="utf-8")


def document_of(target):
    return (target / open_questions.DOCUMENT_NAME).read_bytes()


def block_lines(text, short_title):
    """The named block's lines exactly as the text holds them."""
    lines = text.split("\n")
    start = lines.index(f'  <open-question id="{open_questions.escape(short_title)}">')
    end = lines.index("  </open-question>", start)
    return lines[start : end + 1]


def children_of(text, short_title):
    """The named block's children as the document holds them: every line between its
    <question> line and its </open-question> line."""
    return "\n".join(block_lines(text, short_title)[2:-1])


def load(target):
    return open_questions.load_document(str(target))


def by_id(target, short_title):
    return open_questions.find_question(load(target), short_title)


def write_document(directory, *questions):
    directory.mkdir(parents=True, exist_ok=True)
    open_questions.save_document(str(directory), Document(list(questions)))
    return directory


def annotated(block_id, alternatives=("A", "B"), option="A"):
    return Question(
        id=block_id,
        question=f"What about {block_id}?",
        alternatives=[Alternative(id=alternative_id, text=f"{alternative_id} is this") for alternative_id in alternatives],
        recommendation=Recommendation(option=option, rationale=f"because of {block_id}"),
    )


def embed(run_tool, target, short_title, body):
    if isinstance(body, str):
        body = body.encode("utf-8")
    return run_tool("embed", str(target), short_title, stdin=body)


def assert_refused(result, target, before, reason):
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == f"Error: {reason}\n".encode("utf-8")
    assert b"Traceback" not in result.stderr
    assert document_of(target) == before


# --- a clean return -------------------------------------------------------------------


def test_embed_writes_the_fragment_as_the_block_children_in_canonical_form(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = read_fixture("annotated")
    result = embed(run_tool, target, BARE, CLEAN)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    after = document_of(target).decode("utf-8")
    assert block_lines(after, BARE) == [
        '  <open-question id="Fixture bare block">',
        "    <question>Does a bare block sit beside annotated siblings without change?</question>",
        '    <alternative id="Option A">',
        "      What option A is.",
        "      <advantage>The strongest reason to choose A.</advantage>",
        "      <drawback>The main cost A carries.</drawback>",
        "    </alternative>",
        '    <alternative id="Option B">',
        "      What option B is.",
        "      <advantage>The strongest reason to choose B.</advantage>",
        "      <drawback>The main cost B carries.</drawback>",
        "    </alternative>",
        "    <applied-principle>One rule over two</applied-principle>",
        '    <depends-on question="Root element form" option="Self-closing root"/>',
        '    <recommendation option="Option A">A wins because of one stated reason.</recommendation>',
        "  </open-question>",
    ]
    assert block_lines(after, HATCH) == block_lines(before, HATCH)
    assert block_lines(after, ROOT_FORM) == block_lines(before, ROOT_FORM)
    assert after == open_questions.render_document(load(target))


def test_embed_of_a_stripped_block_children_reproduces_the_fixture_byte_for_byte(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    fixture = read_fixture("annotated")
    for short_title in (HATCH, ROOT_FORM):
        assert run_tool("strip", str(target), short_title).returncode == 0
        assert document_of(target).decode("utf-8") != fixture
        result = embed(run_tool, target, short_title, children_of(fixture, short_title))
        assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
        assert document_of(target).decode("utf-8") == fixture


def test_embed_of_the_entities_block_children_reproduces_the_fixture(run_tool, milestone_dir):
    # The <depends-on> of this block names a block the document does not hold, so the target
    # must be annotated first; the entities themselves are what the round trip checks.
    target = milestone_dir("entities")
    fixture = read_fixture("entities")
    stripped_children = children_of(fixture, ENTITIES_TITLE)
    without_dependency = "\n".join(line for line in stripped_children.split("\n") if "<depends-on" not in line)
    assert run_tool("strip", str(target), ENTITIES_TITLE).returncode == 0
    result = embed(run_tool, target, ENTITIES_TITLE, without_dependency)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    expected = "\n".join(line for line in fixture.split("\n") if "<depends-on" not in line)
    assert document_of(target).decode("utf-8") == expected


def test_extract_fragment_is_the_identity_on_a_clean_return():
    assert open_questions.extract_fragment(CLEAN) == CLEAN
    assert open_questions.extract_fragment(MINIMAL) == MINIMAL
    assert open_questions.extract_fragment(CLEAN + "\n") == CLEAN


def test_embed_the_minimal_fragment_with_no_principle_and_no_dependency(run_tool, milestone_dir):
    target = milestone_dir("bare")
    result = embed(run_tool, target, "First bare question", MINIMAL)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert by_id(target, "First bare question") == Question(
        id="First bare question",
        question="What is the first thing to decide?",
        alternatives=[Alternative(id="Only", text="Just this.")],
        recommendation=Recommendation(option="Only", rationale="Nothing else applies."),
    )
    assert block_lines(document_of(target).decode("utf-8"), "First bare question") == [
        '  <open-question id="First bare question">',
        "    <question>What is the first thing to decide?</question>",
        '    <alternative id="Only">',
        "      Just this.",
        "    </alternative>",
        '    <recommendation option="Only">Nothing else applies.</recommendation>',
        "  </open-question>",
    ]


def test_embed_keeps_several_principles_and_dependencies(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    body = (
        '<alternative id="X">x</alternative>\n'
        "<applied-principle>First</applied-principle>\n"
        "<applied-principle>Second</applied-principle>\n"
        '<depends-on question="Root element form" option="Open and close pair"/>\n'
        '<depends-on question="Escape hatch under sole writer" option="Strip subcommand"/>\n'
        '<recommendation option="X">x it is</recommendation>'
    )
    assert embed(run_tool, target, BARE, body).returncode == 0
    block = by_id(target, BARE)
    assert block.principles == ["First", "Second"]
    assert block.depends_on == [
        Dependency(question="Root element form", option="Open and close pair"),
        Dependency(question="Escape hatch under sole writer", option="Strip subcommand"),
    ]


def test_embed_makes_the_block_annotated_for_list_and_lift(run_tool, milestone_dir):
    target = milestone_dir("bare")
    assert run_tool("list", "--unannotated", str(target)).stdout == b"First bare question\nSecond bare question\n"
    assert embed(run_tool, target, "Second bare question", MINIMAL).returncode == 0
    assert run_tool("list", "--unannotated", str(target)).stdout == b"First bare question\n"
    assert run_tool("list", str(target)).stdout == b"First bare question\nSecond bare question\n"
    assert run_tool("lift", str(target), "Second bare question").stdout.decode("utf-8") == "Only — Nothing else applies.\n"


def test_embed_matches_the_short_title_case_folded_and_un_escaped(run_tool, milestone_dir):
    target = milestone_dir("entities")
    assert run_tool("strip", str(target), ENTITIES_TITLE).returncode == 0
    before = document_of(target)
    escaped = embed(run_tool, target, "Ampersand &amp; angle &lt;brackets&gt;, &quot;quotes&quot;, &apos;apostrophes&apos;", MINIMAL)
    assert escaped.returncode == 1
    assert escaped.stderr.startswith(b"Error: no <open-question> block has the id ")
    assert document_of(target) == before
    un_escaped = embed(run_tool, target, "ampersand & ANGLE <brackets>, \"quotes\", 'apostrophes'", MINIMAL)
    assert (un_escaped.returncode, un_escaped.stdout, un_escaped.stderr) == (0, b"", b"")
    assert by_id(target, ENTITIES_TITLE).recommendation == Recommendation(option="Only", rationale="Nothing else applies.")


# --- a prose-wrapped return -----------------------------------------------------------


def test_embed_discards_a_grounding_summary_above_and_a_closing_remark_below(run_tool, milestone_dir, tmp_path):
    clean = milestone_dir("annotated")
    assert embed(run_tool, clean, BARE, CLEAN).returncode == 0
    target = tmp_path / "wrapped"
    target.mkdir()
    (target / open_questions.DOCUMENT_NAME).write_text(read_fixture("annotated"), encoding="utf-8")
    message = (
        "I grounded this in the live project and the principle store.\n"
        "\n"
        "Two options are realistic here; the sibling recommendation on Root element form settles the root.\n"
        "\n"
        f"{CLEAN}\n"
        "\n"
        "That is my recommendation; let me know if anything is unclear.\n"
    )
    result = embed(run_tool, target, BARE, message)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert document_of(target) == document_of(clean)


def test_embed_discards_a_returned_wrapper_and_question_outside_the_fragment(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    message = (
        '<open-question id="Fixture bare block">\n'
        "  <question>Does a bare block sit beside annotated siblings without change?</question>\n"
        f"{CLEAN}\n"
        "</open-question>\n"
    )
    result = embed(run_tool, target, BARE, message)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert by_id(target, BARE).recommendation == Recommendation(option="Option A", rationale="A wins because of one stated reason.")


def test_embed_reads_a_return_with_crlf_line_ends(run_tool, milestone_dir):
    target = milestone_dir("bare")
    body = ("Summary.\r\n" + MINIMAL.replace("\n", "\r\n") + "\r\nRemark.\r\n").encode("utf-8")
    result = embed(run_tool, target, "First bare question", body)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert by_id(target, "First bare question").alternatives == [Alternative(id="Only", text="Just this.")]


def test_extract_fragment_slices_from_the_first_alternative_line_to_the_last_recommendation_line():
    message = "above\n" + MINIMAL + "\nbelow </recommendation> mention\nafter"
    # The last line holding </recommendation> is the "below" line, so it is inside the slice.
    assert open_questions.extract_fragment(message) == MINIMAL + "\nbelow </recommendation> mention"
    assert open_questions.extract_fragment("x\ny\n" + MINIMAL) == MINIMAL


# --- a misordered fragment ------------------------------------------------------------


def test_embed_groups_misordered_children_by_kind(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    # Complete but misordered: the two extraction anchors — an alternative first and the
    # recommendation last — hold, and everything between them is out of the canonical sequence,
    # the children inside each alternative included.
    misordered = (
        '<alternative id="Option A">\n'
        "  <drawback>A costs.</drawback>\n"
        "  What A is.\n"
        "  <advantage>A helps.</advantage>\n"
        "</alternative>\n"
        '<depends-on question="Root element form" option="Self-closing root"/>\n'
        "<applied-principle>One rule over two</applied-principle>\n"
        '<alternative id="Option B">\n'
        "  <advantage>B helps.</advantage>\n"
        "  <drawback>B costs.</drawback>\n"
        "  What B is.\n"
        "</alternative>\n"
        '<depends-on question="Escape hatch under sole writer" option="Strip subcommand"/>\n'
        '<recommendation option="Option A">A wins after all.</recommendation>'
    )
    result = embed(run_tool, target, BARE, misordered)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert block_lines(document_of(target).decode("utf-8"), BARE) == [
        '  <open-question id="Fixture bare block">',
        "    <question>Does a bare block sit beside annotated siblings without change?</question>",
        '    <alternative id="Option A">',
        "      What A is.",
        "      <advantage>A helps.</advantage>",
        "      <drawback>A costs.</drawback>",
        "    </alternative>",
        '    <alternative id="Option B">',
        "      What B is.",
        "      <advantage>B helps.</advantage>",
        "      <drawback>B costs.</drawback>",
        "    </alternative>",
        "    <applied-principle>One rule over two</applied-principle>",
        '    <depends-on question="Root element form" option="Self-closing root"/>',
        '    <depends-on question="Escape hatch under sole writer" option="Strip subcommand"/>',
        '    <recommendation option="Option A">A wins after all.</recommendation>',
        "  </open-question>",
    ]


def test_extract_fragment_anchors_on_a_misordered_fragment_first_alternative_and_last_recommendation():
    message = (
        "Note.\n"
        '<applied-principle>P</applied-principle>\n'
        '<alternative id="A">a</alternative>\n'
        '<recommendation option="A">r</recommendation>\n'
        '<alternative id="B">b</alternative>\n'
        "Done.\n"
    )
    # The principle line sits above the first <alternative line and the trailing alternative
    # sits below the last </recommendation> line, so both are discarded — a misordering that
    # loses an element is caught only by the agent's own self-check, as the format decision says.
    assert open_questions.extract_fragment(message) == '<alternative id="A">a</alternative>\n<recommendation option="A">r</recommendation>'


def test_embed_normalizes_indentation_escaping_and_folded_text(run_tool, milestone_dir):
    target = milestone_dir("bare")
    body = (
        '\t\t<alternative id="Tabs &amp; spaces">\n'
        "\t\t\t\tWhat it\n"
        "   is, over\n"
        "\t\tthree lines with 'quotes' and \"doubles\".\n"
        '\t\t\t<advantage>Keeps <![CDATA[<raw>]]> text.</advantage>\n'
        "  <drawback>Costs   extra\tspace.</drawback></alternative>\n"
        '<depends-on question="Second bare question" option="Only" />\n'
        '<recommendation   option="tabs &amp; SPACES"  >It &gt; the rest.</recommendation>'
    )
    assert embed(run_tool, target, "Second bare question", MINIMAL).returncode == 0
    result = embed(run_tool, target, "First bare question", body)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert block_lines(document_of(target).decode("utf-8"), "First bare question") == [
        '  <open-question id="First bare question">',
        "    <question>What is the first thing to decide?</question>",
        '    <alternative id="Tabs &amp; spaces">',
        "      What it is, over three lines with &apos;quotes&apos; and &quot;doubles&quot;.",
        "      <advantage>Keeps &lt;raw&gt; text.</advantage>",
        "      <drawback>Costs extra space.</drawback>",
        "    </alternative>",
        '    <depends-on question="Second bare question" option="Only"/>',
        '    <recommendation option="tabs &amp; SPACES">It &gt; the rest.</recommendation>',
        "  </open-question>",
    ]


# --- <depends-on> resolution ----------------------------------------------------------


def test_embed_resolves_a_dependency_against_an_annotated_block_un_escaped_and_case_folded(run_tool, milestone_dir):
    target = milestone_dir("entities")
    document = load(target)
    document.questions.append(Question(id="Dependent", question="Does it resolve?"))
    open_questions.save_document(str(target), document)
    body = (
        '<alternative id="Yes">It does.</alternative>\n'
        f'<depends-on question="{open_questions.escape(ENTITIES_TITLE.upper())}" option="a &amp; b"/>\n'
        '<recommendation option="Yes">Resolved.</recommendation>'
    )
    result = embed(run_tool, target, "Dependent", body)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert by_id(target, "Dependent").depends_on == [Dependency(question=ENTITIES_TITLE.upper(), option="a & b")]


def test_embed_resolves_one_hop_only_and_follows_no_tag_of_the_target(run_tool, milestone_dir):
    # The entities block's own <depends-on> names a block the document does not hold; a
    # dependency on that block still resolves, because the target's tags are not followed.
    target = milestone_dir("entities")
    document = load(target)
    assert document.questions[0].depends_on[0].question == 'Some "other" question & more'
    document.questions.append(Question(id="Dependent", question="One hop?"))
    open_questions.save_document(str(target), document)
    body = (
        '<alternative id="Yes">One hop.</alternative>\n'
        f'<depends-on question="{open_questions.escape(ENTITIES_TITLE)}" option="A &amp; B"/>\n'
        '<recommendation option="Yes">Resolved.</recommendation>'
    )
    assert embed(run_tool, target, "Dependent", body).returncode == 0


def test_embed_tolerates_a_dependency_cycle(run_tool, tmp_path):
    target = write_document(
        tmp_path / "cycle",
        Question(id="A", question="a?", alternatives=[Alternative(id="A1")], depends_on=[Dependency(question="B", option="B1")], recommendation=Recommendation(option="A1")),
        Question(id="B", question="b?", alternatives=[Alternative(id="B1")]),
    )
    body = '<alternative id="B1">b1</alternative>\n<depends-on question="A" option="A1"/>\n<recommendation option="B1">r</recommendation>'
    result = embed(run_tool, target, "B", body)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert by_id(target, "B").depends_on == [Dependency(question="A", option="A1")]


@pytest.mark.parametrize(
    "question, held",
    [
        ("No such block", 'the annotated blocks are "Escape hatch under sole writer", "Root element form"'),
        ("Fixture bare block", 'the annotated blocks are "Escape hatch under sole writer", "Root element form"'),
    ],
)
def test_embed_refuses_a_dependency_on_a_missing_or_unannotated_block(run_tool, milestone_dir, question, held):
    target = milestone_dir("annotated")
    before = document_of(target)
    body = f'<alternative id="X">x</alternative>\n<depends-on question="{question}" option="Y"/>\n<recommendation option="X">r</recommendation>'
    result = embed(run_tool, target, BARE, body)
    assert_refused(
        result, target, before, f'the <depends-on question="{question}"/> names no block that carries a <recommendation>; {held}'
    )


def test_embed_refuses_a_dependency_on_a_bare_sibling_when_no_block_is_annotated(run_tool, milestone_dir):
    target = milestone_dir("bare")
    before = document_of(target)
    body = '<alternative id="X">x</alternative>\n<depends-on question="Second bare question" option="Y"/>\n<recommendation option="X">r</recommendation>'
    result = embed(run_tool, target, "First bare question", body)
    assert_refused(
        result,
        target,
        before,
        'the <depends-on question="Second bare question"/> names no block that carries a <recommendation>; no other block carries one',
    )


def test_embed_refuses_a_dependency_whose_option_names_none_of_the_target_alternatives(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = document_of(target)
    body = '<alternative id="X">x</alternative>\n<depends-on question="root element FORM" option="Neither"/>\n<recommendation option="X">r</recommendation>'
    result = embed(run_tool, target, BARE, body)
    assert_refused(
        result,
        target,
        before,
        'the <depends-on question="root element FORM" option="Neither"/> names none of that block\'s <alternative> ids, '
        'which are "Self-closing root", "Open and close pair"',
    )


def test_embed_refuses_a_dependency_on_the_block_being_embedded(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = document_of(target)
    body = '<alternative id="X">x</alternative>\n<depends-on question="Fixture bare block" option="X"/>\n<recommendation option="X">r</recommendation>'
    result = embed(run_tool, target, BARE, body)
    assert result.returncode == 1
    assert result.stderr.startswith(b'Error: the <depends-on question="Fixture bare block"/> names no block that carries a <recommendation>')
    assert document_of(target) == before


# --- the two extraction misses --------------------------------------------------------


@pytest.mark.parametrize(
    "body",
    [
        b"",
        b"   \n\n",
        b"I could not ground this question in the project.\n",
        b'<recommendation option="A">no alternatives above</recommendation>\n',
        b"The word &lt;alternative escaped is not a line to extract from.\n</recommendation>\n",
    ],
)
def test_embed_refuses_a_message_with_no_alternative_line(run_tool, milestone_dir, body):
    target = milestone_dir("bare")
    before = document_of(target)
    assert_refused(embed(run_tool, target, "First bare question", body), target, before, "no <alternative> line to extract from")


@pytest.mark.parametrize(
    "body",
    [
        b'<alternative id="A">a</alternative>\n',
        b'<alternative id="A">a</alternative>\n<recommendation option="A">unterminated\n',
        b'<alternative id="A">a</alternative>\n<recommendation option="A"/>\n',
    ],
)
def test_embed_refuses_a_message_with_no_closing_recommendation_line(run_tool, milestone_dir, body):
    target = milestone_dir("bare")
    before = document_of(target)
    assert_refused(embed(run_tool, target, "First bare question", body), target, before, "no </recommendation> line to extract to")


def test_embed_refuses_a_closing_recommendation_line_above_the_first_alternative_line(run_tool, milestone_dir):
    target = milestone_dir("bare")
    before = document_of(target)
    body = b'<recommendation option="A">first</recommendation>\n<alternative id="A">a</alternative>\n'
    assert_refused(
        embed(run_tool, target, "First bare question", body),
        target,
        before,
        "the last </recommendation> line precedes the first <alternative> line",
    )


# --- each failing fragment ------------------------------------------------------------


@pytest.mark.parametrize(
    "line, tag, article",
    [
        ("<question>Which?</question>", "<question>", "a"),
        ("<question/>", "<question>", "a"),
        ("</question>", "</question>", "a"),
        ('<open-question id="Another">', "<open-question>", "an"),
        ("</open-question>", "</open-question>", "a"),
        ("  </open-question>  ", "</open-question>", "a"),
    ],
)
def test_embed_refuses_a_wrapper_or_question_line_inside_the_fragment(run_tool, milestone_dir, line, tag, article):
    target = milestone_dir("bare")
    before = document_of(target)
    body = f'<alternative id="A">a</alternative>\n{line}\n<recommendation option="A">r</recommendation>'
    assert_refused(
        embed(run_tool, target, "First bare question", body),
        target,
        before,
        f"the fragment contains {article} {tag} line; the <open-question> wrapper and its <question> element belong to "
        "the document, not to the fragment",
    )


def test_embed_does_not_mistake_a_longer_tag_or_escaped_text_for_a_question_line(run_tool, milestone_dir):
    target = milestone_dir("bare")
    before = document_of(target)
    body = '<alternative id="A">a &lt;question&gt; in text</alternative>\n<questionable>x</questionable>\n<recommendation option="A">r</recommendation>'
    result = embed(run_tool, target, "First bare question", body)
    assert_refused(result, target, before, "the fragment carries an unexpected <questionable> element")


def test_embed_refuses_text_preceding_the_first_alternative(run_tool, milestone_dir):
    target = milestone_dir("bare")
    before = document_of(target)
    body = 'Here they are: <alternative id="A">a</alternative>\n<recommendation option="A">r</recommendation>'
    assert_refused(
        embed(run_tool, target, "First bare question", body), target, before, "text precedes <alternative> on the fragment's opening line"
    )


def test_embed_refuses_text_trailing_the_last_recommendation(run_tool, milestone_dir):
    target = milestone_dir("bare")
    before = document_of(target)
    body = '<alternative id="A">a</alternative>\n<recommendation option="A">r</recommendation> That is all.'
    assert_refused(
        embed(run_tool, target, "First bare question", body), target, before, "text trails </recommendation> on the fragment's closing line"
    )


def test_embed_refuses_text_between_the_elements(run_tool, milestone_dir):
    target = milestone_dir("bare")
    before = document_of(target)
    body = '<alternative id="A">a</alternative>\nA note between the elements.\n<recommendation option="A">r</recommendation>'
    assert_refused(embed(run_tool, target, "First bare question", body), target, before, "the fragment carries text between its elements")


@pytest.mark.parametrize(
    "body, reason",
    [
        (
            '<alternative id="A">a\n<recommendation option="A">r</recommendation>',
            "mismatched tag at line 3, column 2",
        ),
        (
            '<alternative id="A">a &amp b</alternative>\n<recommendation option="A">r</recommendation>',
            "not well-formed (invalid token) at line 1, column 26",
        ),
        (
            '<alternative id="A">a</alternative>\n<recommendation option=A>r</recommendation>',
            "not well-formed (invalid token) at line 2, column 23",
        ),
    ],
)
def test_embed_refuses_a_fragment_that_is_not_well_formed_xml(run_tool, milestone_dir, body, reason):
    target = milestone_dir("bare")
    before = document_of(target)
    assert_refused(embed(run_tool, target, "First bare question", body), target, before, f"the fragment is not well-formed XML: {reason}")


def test_embed_refuses_a_fragment_with_no_alternative_element(run_tool, milestone_dir):
    target = milestone_dir("bare")
    before = document_of(target)
    # The anchor line holds "<alternative" only inside a comment, which the parser drops.
    body = '<!-- <alternative id="A"/> -->\n<recommendation option="A">r</recommendation>'
    assert_refused(embed(run_tool, target, "First bare question", body), target, before, "the fragment contains no <alternative> element")


def test_embed_refuses_a_fragment_with_no_recommendation_element(run_tool, milestone_dir):
    target = milestone_dir("bare")
    before = document_of(target)
    body = '<alternative id="A">a</alternative>\n<!-- </recommendation> -->'
    assert_refused(embed(run_tool, target, "First bare question", body), target, before, "the fragment contains no <recommendation> element")


def test_embed_refuses_two_recommendation_elements(run_tool, milestone_dir):
    target = milestone_dir("bare")
    before = document_of(target)
    body = '<alternative id="A">a</alternative>\n<recommendation option="A">r</recommendation>\n<recommendation option="A">again</recommendation>'
    assert_refused(embed(run_tool, target, "First bare question", body), target, before, "the fragment carries 2 <recommendation> elements")


def test_embed_refuses_a_recommendation_option_naming_no_alternative(run_tool, milestone_dir):
    target = milestone_dir("bare")
    before = document_of(target)
    body = '<alternative id="A">a</alternative>\n<alternative id="B">b</alternative>\n<recommendation option="C">r</recommendation>'
    assert_refused(
        embed(run_tool, target, "First bare question", body),
        target,
        before,
        'the <recommendation> option "C" names none of the fragment\'s <alternative> ids, which are "A", "B"',
    )


def test_embed_compares_the_recommendation_option_un_escaped_and_case_folded(run_tool, milestone_dir):
    target = milestone_dir("bare")
    body = '<alternative id="A &amp; B">a</alternative>\n<recommendation option="a &amp; b">r</recommendation>'
    assert embed(run_tool, target, "First bare question", body).returncode == 0
    assert by_id(target, "First bare question").recommendation == Recommendation(option="a & b", rationale="r")


@pytest.mark.parametrize(
    "body, reason",
    [
        (
            '<alternative id="A">a</alternative>\n<note>n</note>\n<recommendation option="A">r</recommendation>',
            "the fragment carries an unexpected <note> element",
        ),
        (
            '<alternative id="A">a<benefit>b</benefit></alternative>\n<recommendation option="A">r</recommendation>',
            '<alternative id="A"> of the fragment carries an unexpected <benefit> element',
        ),
        (
            '<alternative id="A">a</alternative>\n<applied-principle>P<em>!</em></applied-principle>\n<recommendation option="A">r</recommendation>',
            "an <applied-principle> element of the fragment carries an unexpected <em> element",
        ),
        (
            '<alternative id="A">a</alternative>\n<recommendation option="A">r<b>!</b></recommendation>',
            "the <recommendation> element of the fragment carries an unexpected <b> element",
        ),
        (
            '<alternative id="A">a</alternative>\n<depends-on question="X" option="Y">text</depends-on>\n<recommendation option="A">r</recommendation>',
            "a <depends-on> element of the fragment carries text",
        ),
    ],
)
def test_embed_refuses_an_element_of_an_unknown_kind(run_tool, milestone_dir, body, reason):
    target = milestone_dir("bare")
    before = document_of(target)
    assert_refused(embed(run_tool, target, "First bare question", body), target, before, reason)


@pytest.mark.parametrize(
    "body, reason",
    [
        (
            '<alternative id="A">a</alternative>\n<alternative id="a">again</alternative>\n<recommendation option="A">r</recommendation>',
            'the fragment carries two <alternative> elements with the id "a"',
        ),
        (
            '<alternative>a</alternative>\n<recommendation option="A">r</recommendation>',
            "an <alternative> element of the fragment has no id attribute",
        ),
        (
            '<alternative id="  ">a</alternative>\n<recommendation option="A">r</recommendation>',
            "an <alternative> element of the fragment has an empty id attribute",
        ),
        (
            '<alternative id="A">a</alternative>\n<recommendation>r</recommendation>',
            "the <recommendation> element of the fragment has no option attribute",
        ),
        (
            '<alternative id="A" rank="1">a</alternative>\n<recommendation option="A">r</recommendation>',
            'an <alternative> element of the fragment carries an unknown attribute "rank"',
        ),
        (
            '<alternative id="A">a</alternative>\n<depends-on question="X"/>\n<recommendation option="A">r</recommendation>',
            "a <depends-on> element of the fragment has no option attribute",
        ),
    ],
)
def test_embed_refuses_a_malformed_attribute(run_tool, milestone_dir, body, reason):
    target = milestone_dir("bare")
    before = document_of(target)
    assert_refused(embed(run_tool, target, "First bare question", body), target, before, reason)


# --- the block and the document -------------------------------------------------------


def test_embed_refuses_a_block_already_carrying_a_recommendation(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = document_of(target)
    result = embed(run_tool, target, "root ELEMENT form", MINIMAL)
    assert_refused(
        result,
        target,
        before,
        '<open-question id="Root element form"> already carries a <recommendation> element; strip it first to embed a new one',
    )


def test_embed_refuses_an_unknown_short_title(run_tool, milestone_dir):
    target = milestone_dir("bare")
    before = document_of(target)
    result = embed(run_tool, target, "Missing", MINIMAL)
    assert_refused(
        result,
        target,
        before,
        'no <open-question> block has the id "Missing"; the document holds "First bare question", "Second bare question"',
    )


def test_embed_refuses_an_unknown_short_title_on_an_empty_document(run_tool, milestone_dir):
    target = milestone_dir("empty")
    result = embed(run_tool, target, "Anything", MINIMAL)
    assert_refused(result, target, b"<open-questions/>\n", 'no <open-question> block has the id "Anything"; the document holds no blocks')


def test_embed_requires_a_short_title(run_tool, milestone_dir):
    result = run_tool("embed", str(milestone_dir("bare")), stdin=MINIMAL.encode("utf-8"))
    assert result.returncode == 2
    assert result.stdout == b""
    assert b"SHORT_TITLE" in result.stderr


def test_embed_fails_when_the_document_is_missing_and_creates_nothing(run_tool, tmp_path):
    result = embed(run_tool, tmp_path, "Anything", MINIMAL)
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == f"Error: {tmp_path / open_questions.DOCUMENT_NAME} does not exist\n".encode("utf-8")
    assert list(tmp_path.iterdir()) == []


def test_embed_fails_on_a_malformed_document_and_leaves_it_unchanged(run_tool, tmp_path):
    document = tmp_path / open_questions.DOCUMENT_NAME
    document.write_text("<open-questions>", encoding="utf-8")
    result = embed(run_tool, tmp_path, "Anything", MINIMAL)
    assert result.returncode == 1
    assert result.stdout == b""
    assert b"not well-formed XML" in result.stderr
    assert result.stderr.count(b"\n") == 1
    assert document.read_text(encoding="utf-8") == "<open-questions>"


# --- the stdin channel ----------------------------------------------------------------


def test_embed_refuses_a_terminal_stdin_without_blocking(milestone_dir):
    pty = pytest.importorskip("pty")
    target = milestone_dir("bare")
    before = document_of(target)
    master, slave = pty.openpty()
    try:
        result = subprocess.run(
            [sys.executable, "-B", str(TOOL), "embed", str(target), "First bare question"],
            stdin=slave,
            capture_output=True,
            check=False,
            timeout=30,
        )
    finally:
        os.close(slave)
        os.close(master)
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == (
        b"Error: the recommend agent's message must be piped on standard input (as a quoted heredoc or a "
        b"redirected file), not typed at a terminal\n"
    )
    assert document_of(target) == before


def test_main_refuses_a_closed_stdin(capsys, monkeypatch, milestone_dir):
    target = milestone_dir("bare")
    monkeypatch.setattr(sys, "stdin", None)
    assert open_questions.main(["embed", str(target), "First bare question"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "Error: the recommend agent's message must be supplied on standard input, which is closed\n"
    assert document_of(target) == read_fixture("bare").encode("utf-8")


def test_main_reads_the_message_from_stdin_buffer_once(capsys, monkeypatch, milestone_dir):
    target = milestone_dir("bare")
    stream = io.TextIOWrapper(io.BytesIO(("Summary — dashes …\n" + MINIMAL + "\n").encode("utf-8")))
    monkeypatch.setattr(sys, "stdin", stream)
    assert open_questions.main(["embed", str(target), "First bare question"]) == 0
    assert capsys.readouterr() == ("", "")
    assert stream.buffer.read() == b""
    assert by_id(target, "First bare question").recommendation == Recommendation(option="Only", rationale="Nothing else applies.")


def test_embed_refuses_a_non_utf8_message(run_tool, milestone_dir):
    target = milestone_dir("bare")
    before = document_of(target)
    result = embed(run_tool, target, "First bare question", MINIMAL.encode("utf-8") + b"\n<!-- caf\xe9 -->")
    assert_refused(result, target, before, "the recommend agent's message on standard input is not UTF-8 text")


def test_embed_reads_the_message_verbatim_with_nothing_expanded(run_tool, milestone_dir):
    target = milestone_dir("bare")
    body = '<alternative id="A">Does `code`, ${VAR}, $(cmd), and a literal &amp;apos; travel untouched?</alternative>\n<recommendation option="A">r</recommendation>'
    assert embed(run_tool, target, "First bare question", body).returncode == 0
    assert by_id(target, "First bare question").alternatives[0].text == "Does `code`, ${VAR}, $(cmd), and a literal &apos; travel untouched?"


# --- the single write -----------------------------------------------------------------


def test_embed_writes_exactly_once_on_success_and_never_on_a_refusal(monkeypatch, milestone_dir):
    target = milestone_dir("annotated")
    calls = []
    original = open_questions.save_document

    def counting(milestone_dir, document):
        calls.append(milestone_dir)
        original(milestone_dir, document)

    monkeypatch.setattr(open_questions, "save_document", counting)
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(CLEAN.encode("utf-8"))))
    assert open_questions.main(["embed", str(target), BARE]) == 0
    assert calls == [str(target)]
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(b"prose only")))
    assert open_questions.main(["embed", str(target), HATCH]) == 1
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(b'<alternative id="A">a</alternative>\n<depends-on question="Nope" option="X"/>\n<recommendation option="A">r</recommendation>')))
    open_questions.main(["strip", str(target), HATCH])
    calls.clear()
    assert open_questions.main(["embed", str(target), HATCH]) == 1
    assert calls == []


def test_embed_leaves_no_temporary_file_behind(run_tool, milestone_dir):
    target = milestone_dir("bare")
    embed(run_tool, target, "First bare question", MINIMAL)
    embed(run_tool, target, "First bare question", MINIMAL)
    embed(run_tool, target, "Second bare question", b"prose only")
    assert sorted(path.name for path in target.iterdir()) == [open_questions.DOCUMENT_NAME]


def test_embed_fragment_replaces_the_children_on_the_parsed_tree():
    document = Document([annotated("Target"), Question(id="Bare", question="bare?")])
    fragment = open_questions.parse_fragment('<alternative id="X">x</alternative>\n<depends-on question="target" option="b"/>\n<recommendation option="x">r</recommendation>')
    assert fragment == Question(
        id="",
        alternatives=[Alternative(id="X", text="x")],
        depends_on=[Dependency(question="target", option="b")],
        recommendation=Recommendation(option="x", rationale="r"),
    )
    open_questions.embed_fragment(document, document.questions[1], fragment)
    assert document.questions[1] == Question(
        id="Bare",
        question="bare?",
        alternatives=[Alternative(id="X", text="x")],
        depends_on=[Dependency(question="target", option="b")],
        recommendation=Recommendation(option="x", rationale="r"),
    )
    assert document.questions[0] == annotated("Target")
