"""The embed subcommand and its two shapes, selected by a required, mutually exclusive flag
pair over one shared validation core. The whole message carrying the half is read from
standard input and the fragment sliced out of it — with --alternatives from the first
<alternative line through the last </alternative> line, with --recommendation from the first
<applied-principle, <depends-on, or <recommendation line through the last </recommendation>
line (the identity on a clean message either way) — then parsed and validated: no wrapper or
<question> line, no text outside the elements, no element of an unknown kind and none of the
other half, never the order of the children. --alternatives is accepted only into a block
carrying no <alternative> yet and writes only the alternatives; --recommendation is accepted
only into a block carrying at least one <alternative> and no <recommendation> yet, checks the
recommendation's option against the block's own alternative ids, resolves every <depends-on>
one hop against a sibling carrying <alternative> elements and one of its ids (whether that
sibling carries a <recommendation> is not asked), and writes only its own three kinds, so the
alternative set stays frozen. Every miss is one Error line with the document unchanged."""

import io
import os
import subprocess
import sys
from pathlib import Path

import pytest

import open_questions
from open_questions import (
    ALTERNATIVES_SHAPE,
    RECOMMENDATION_SHAPE,
    Alternative,
    Dependency,
    Document,
    Question,
    Recommendation,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"
TOOL = Path(open_questions.__file__).resolve()
ENTITIES_TITLE = "Ampersand & angle <brackets>, \"quotes\", 'apostrophes'"
HATCH = "Escape hatch under sole writer"
ROOT_FORM = "Root element form"
BARE = "Fixture bare block"
FIRST = "First bare question"
SECOND = "Second bare question"
SHAPES = ("--alternatives", "--recommendation")

ALTERNATIVES = """\
  <alternative id="Option A">
    What option A is.
    <advantage>The strongest reason to choose A.</advantage>
    <drawback>The main cost A carries.</drawback>
  </alternative>
  <alternative id="Option B">
    What option B is.
    <advantage>The strongest reason to choose B.</advantage>
    <drawback>The main cost B carries.</drawback>
  </alternative>"""

RECOMMENDATION = """\
  <applied-principle>One rule over two</applied-principle>
  <depends-on question="Root element form" option="Self-closing root"/>
  <recommendation option="Option A">A wins because of one stated reason.</recommendation>"""

ONLY_ALTERNATIVE = '<alternative id="Only">Just this.</alternative>'
ONLY_RECOMMENDATION = '<recommendation option="Only">Nothing else applies.</recommendation>'

ALTERNATIVE_LINES = [
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
]
RECOMMENDATION_LINES = [
    "    <applied-principle>One rule over two</applied-principle>",
    '    <depends-on question="Root element form" option="Self-closing root"/>',
    '    <recommendation option="Option A">A wins because of one stated reason.</recommendation>',
]
BARE_HEAD = [
    '  <open-question id="Fixture bare block">',
    "    <question>Does a bare block sit beside annotated siblings without change?</question>",
]


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
    """The named block's child lines as the document holds them: every line between its
    <question> line and its </open-question> line."""
    return block_lines(text, short_title)[2:-1]


def halves_of(text, short_title):
    """The named block's child lines split into the two halves embed takes, each joined: the
    <alternative> elements with everything inside them, and the recommendation half."""
    recommendation_half = ("    <applied-principle", "    <depends-on", "    <recommendation")
    lines = children_of(text, short_title)
    alternatives = [line for line in lines if not line.startswith(recommendation_half)]
    recommendation = [line for line in lines if line.startswith(recommendation_half)]
    return "\n".join(alternatives), "\n".join(recommendation)


def load(target):
    return open_questions.load_document(str(target))


def by_id(target, short_title):
    return open_questions.find_question(load(target), short_title)


def write_document(directory, *questions):
    directory.mkdir(parents=True, exist_ok=True)
    open_questions.save_document(str(directory), Document(list(questions)))
    return directory


def give_alternatives(target, short_title, *alternative_ids):
    """Put alternatives with the given ids into the named block on disk, in place."""
    document = load(target)
    block = open_questions.find_question(document, short_title)
    block.alternatives = [Alternative(id=alternative_id, text=f"{alternative_id} is this") for alternative_id in alternative_ids]
    open_questions.save_document(str(target), document)
    return target


def prepared(milestone_dir, shape, short_title=FIRST):
    """A copy of the bare fixture whose named block is in the state the shape writes into:
    bare for --alternatives, carrying the alternatives "A" and "B" for --recommendation."""
    target = milestone_dir("bare")
    if shape == "--recommendation":
        give_alternatives(target, short_title, "A", "B")
    return target


def framed(shape, line):
    """A fragment of the shape with the given line inside it, between two of its elements."""
    if shape == "--alternatives":
        return f'<alternative id="A">a</alternative>\n{line}\n<alternative id="B">b</alternative>'
    return f'<applied-principle>P</applied-principle>\n{line}\n<recommendation option="A">r</recommendation>'


def minimal(shape):
    return ONLY_ALTERNATIVE if shape == "--alternatives" else '<recommendation option="A">r</recommendation>'


def embed(run_tool, target, short_title, body, shape):
    if isinstance(body, str):
        body = body.encode("utf-8")
    return run_tool("embed", shape, str(target), short_title, stdin=body)


def embed_alternatives(run_tool, target, short_title, body):
    return embed(run_tool, target, short_title, body, "--alternatives")


def embed_recommendation(run_tool, target, short_title, body):
    return embed(run_tool, target, short_title, body, "--recommendation")


def assert_ok(result):
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def assert_refused(result, target, before, reason):
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == f"Error: {reason}\n".encode("utf-8")
    assert b"Traceback" not in result.stderr
    assert document_of(target) == before


# --- the shape flag -------------------------------------------------------------------


def test_embed_requires_exactly_one_shape_flag(run_tool, milestone_dir):
    target = milestone_dir("bare")
    before = document_of(target)
    neither = run_tool("embed", str(target), FIRST, stdin=ONLY_ALTERNATIVE.encode("utf-8"))
    assert neither.returncode == 2
    assert neither.stdout == b""
    assert b"--alternatives" in neither.stderr and b"--recommendation" in neither.stderr
    assert b"required" in neither.stderr
    both = run_tool("embed", "--alternatives", "--recommendation", str(target), FIRST, stdin=ONLY_ALTERNATIVE.encode("utf-8"))
    assert both.returncode == 2
    assert both.stdout == b""
    assert b"not allowed with" in both.stderr
    assert document_of(target) == before


def test_embed_accepts_the_shape_flag_before_or_after_the_positional_arguments(run_tool, milestone_dir):
    target = milestone_dir("bare")
    assert_ok(run_tool("embed", "--alternatives", str(target), FIRST, stdin=ONLY_ALTERNATIVE.encode("utf-8")))
    assert_ok(run_tool("embed", str(target), FIRST, "--recommendation", stdin=ONLY_RECOMMENDATION.encode("utf-8")))
    assert_ok(run_tool("embed", str(target), "--alternatives", SECOND, stdin=ONLY_ALTERNATIVE.encode("utf-8")))
    assert by_id(target, FIRST).recommendation == Recommendation(option="Only", rationale="Nothing else applies.")
    assert by_id(target, SECOND).alternatives == [Alternative(id="Only", text="Just this.")]


# --- a clean --alternatives message ---------------------------------------------------


def test_embed_alternatives_writes_the_alternatives_as_the_block_children_in_canonical_form(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = read_fixture("annotated")
    assert_ok(embed_alternatives(run_tool, target, BARE, ALTERNATIVES))
    after = document_of(target).decode("utf-8")
    assert block_lines(after, BARE) == BARE_HEAD + ALTERNATIVE_LINES + ["  </open-question>"]
    assert block_lines(after, HATCH) == block_lines(before, HATCH)
    assert block_lines(after, ROOT_FORM) == block_lines(before, ROOT_FORM)
    assert after == open_questions.render_document(load(target))


def test_embed_alternatives_then_recommendation_reproduces_a_stripped_block_byte_for_byte(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    fixture = read_fixture("annotated")
    for short_title in (HATCH, ROOT_FORM):
        alternatives, recommendation = halves_of(fixture, short_title)
        assert run_tool("strip", str(target), short_title).returncode == 0
        assert document_of(target).decode("utf-8") != fixture
        assert_ok(embed_alternatives(run_tool, target, short_title, alternatives))
        assert document_of(target).decode("utf-8") != fixture
        assert_ok(embed_recommendation(run_tool, target, short_title, recommendation))
        assert document_of(target).decode("utf-8") == fixture


def test_embed_recommendation_alone_reproduces_a_partially_stripped_block_byte_for_byte(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    fixture = read_fixture("annotated")
    _, recommendation = halves_of(fixture, ROOT_FORM)
    assert run_tool("strip", "--recommendation", str(target), ROOT_FORM).returncode == 0
    assert document_of(target).decode("utf-8") != fixture
    assert_ok(embed_recommendation(run_tool, target, ROOT_FORM, recommendation))
    assert document_of(target).decode("utf-8") == fixture


def test_embed_of_the_entities_block_halves_reproduces_the_fixture(run_tool, milestone_dir):
    # The <depends-on> of this block names a block the document does not hold, so it is left
    # out of the recommendation half; the entities themselves are what the round trip checks.
    target = milestone_dir("entities")
    fixture = read_fixture("entities")
    alternatives, recommendation = halves_of(fixture, ENTITIES_TITLE)
    without_dependency = "\n".join(line for line in recommendation.split("\n") if "<depends-on" not in line)
    assert run_tool("strip", str(target), ENTITIES_TITLE).returncode == 0
    assert_ok(embed_alternatives(run_tool, target, ENTITIES_TITLE, alternatives))
    assert_ok(embed_recommendation(run_tool, target, ENTITIES_TITLE, without_dependency))
    expected = "\n".join(line for line in fixture.split("\n") if "<depends-on" not in line)
    assert document_of(target).decode("utf-8") == expected


def test_extract_fragment_is_the_identity_on_a_clean_message_of_either_shape():
    assert open_questions.extract_fragment(ALTERNATIVES, ALTERNATIVES_SHAPE) == ALTERNATIVES
    assert open_questions.extract_fragment(ONLY_ALTERNATIVE, ALTERNATIVES_SHAPE) == ONLY_ALTERNATIVE
    assert open_questions.extract_fragment(ALTERNATIVES + "\n", ALTERNATIVES_SHAPE) == ALTERNATIVES
    assert open_questions.extract_fragment(RECOMMENDATION, RECOMMENDATION_SHAPE) == RECOMMENDATION
    assert open_questions.extract_fragment(ONLY_RECOMMENDATION, RECOMMENDATION_SHAPE) == ONLY_RECOMMENDATION
    assert open_questions.extract_fragment(RECOMMENDATION + "\n", RECOMMENDATION_SHAPE) == RECOMMENDATION


def test_embed_alternatives_the_minimal_fragment(run_tool, milestone_dir):
    target = milestone_dir("bare")
    assert_ok(embed_alternatives(run_tool, target, FIRST, ONLY_ALTERNATIVE))
    assert by_id(target, FIRST) == Question(
        id=FIRST,
        question="What is the first thing to decide?",
        alternatives=[Alternative(id="Only", text="Just this.")],
    )
    assert block_lines(document_of(target).decode("utf-8"), FIRST) == [
        '  <open-question id="First bare question">',
        "    <question>What is the first thing to decide?</question>",
        '    <alternative id="Only">',
        "      Just this.",
        "    </alternative>",
        "  </open-question>",
    ]


def test_embed_alternatives_makes_the_block_leave_the_without_alternatives_list(run_tool, milestone_dir):
    target = milestone_dir("bare")
    assert run_tool("list", "--without-alternatives", str(target)).stdout == b"First bare question\nSecond bare question\n"
    assert_ok(embed_alternatives(run_tool, target, SECOND, ONLY_ALTERNATIVE))
    assert run_tool("list", "--without-alternatives", str(target)).stdout == b"First bare question\n"
    assert run_tool("list", "--without-recommendation", str(target)).stdout == b"First bare question\nSecond bare question\n"
    assert run_tool("list", str(target)).stdout == b"First bare question\nSecond bare question\n"
    assert run_tool("lift", str(target), SECOND, "--alternative", "only").stdout.decode("utf-8") == "Only — Just this.\n"


def test_embed_alternatives_writes_only_the_alternatives_and_leaves_the_other_half_as_held(run_tool, tmp_path):
    # A block carrying the recommendation half and no alternatives is not a state the tool
    # writes, but the shape's contract is per half: whatever the other half holds stays.
    target = write_document(
        tmp_path / "half",
        Question(
            id="Held",
            question="held?",
            principles=["Kept"],
            depends_on=[Dependency(question="Elsewhere", option="X")],
            recommendation=Recommendation(option="Only", rationale="kept too"),
        ),
    )
    assert_ok(embed_alternatives(run_tool, target, "Held", ONLY_ALTERNATIVE))
    assert by_id(target, "Held") == Question(
        id="Held",
        question="held?",
        alternatives=[Alternative(id="Only", text="Just this.")],
        principles=["Kept"],
        depends_on=[Dependency(question="Elsewhere", option="X")],
        recommendation=Recommendation(option="Only", rationale="kept too"),
    )


def test_embed_alternatives_discards_a_recommendation_half_below_the_last_alternative_line(run_tool, milestone_dir):
    # A whole two-half message piped to --alternatives embeds the alternatives alone: the
    # slice closes on the last </alternative> line and the shape writes only its own half.
    target = milestone_dir("annotated")
    assert_ok(embed_alternatives(run_tool, target, BARE, ALTERNATIVES + "\n" + RECOMMENDATION + "\n"))
    assert block_lines(document_of(target).decode("utf-8"), BARE) == BARE_HEAD + ALTERNATIVE_LINES + ["  </open-question>"]


def test_embed_matches_the_short_title_case_folded_and_un_escaped(run_tool, milestone_dir):
    target = milestone_dir("entities")
    assert run_tool("strip", str(target), ENTITIES_TITLE).returncode == 0
    before = document_of(target)
    escaped = embed_alternatives(run_tool, target, "Ampersand &amp; angle &lt;brackets&gt;, &quot;quotes&quot;, &apos;apostrophes&apos;", ONLY_ALTERNATIVE)
    assert escaped.returncode == 1
    assert escaped.stderr.startswith(b"Error: no <open-question> block has the id ")
    assert document_of(target) == before
    un_escaped = embed_alternatives(run_tool, target, "ampersand & ANGLE <brackets>, \"quotes\", 'apostrophes'", ONLY_ALTERNATIVE)
    assert_ok(un_escaped)
    assert by_id(target, ENTITIES_TITLE).alternatives == [Alternative(id="Only", text="Just this.")]
    assert_ok(embed_recommendation(run_tool, target, "AMPERSAND & angle <brackets>, \"quotes\", 'apostrophes'", ONLY_RECOMMENDATION))
    assert by_id(target, ENTITIES_TITLE).recommendation == Recommendation(option="Only", rationale="Nothing else applies.")


# --- a clean --recommendation message -------------------------------------------------


def test_embed_recommendation_writes_its_half_and_leaves_the_alternatives_frozen(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = read_fixture("annotated")
    assert_ok(embed_alternatives(run_tool, target, BARE, ALTERNATIVES))
    frozen = document_of(target)
    assert_ok(embed_recommendation(run_tool, target, BARE, RECOMMENDATION))
    after = document_of(target).decode("utf-8")
    assert block_lines(after, BARE) == BARE_HEAD + RECOMMENDATION_LINES + ALTERNATIVE_LINES + ["  </open-question>"]
    assert block_lines(after, BARE)[5:15] == block_lines(frozen.decode("utf-8"), BARE)[2:12]
    assert block_lines(after, HATCH) == block_lines(before, HATCH)
    assert block_lines(after, ROOT_FORM) == block_lines(before, ROOT_FORM)
    assert after == open_questions.render_document(load(target))


def test_embed_recommendation_promotes_the_named_alternative_and_keeps_the_set_frozen(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    assert_ok(embed_alternatives(run_tool, target, BARE, ALTERNATIVES))
    assert_ok(embed_recommendation(run_tool, target, BARE, RECOMMENDATION.replace('option="Option A"', 'option="option b"')))
    after = block_lines(document_of(target).decode("utf-8"), BARE)
    promoted = RECOMMENDATION_LINES[:2] + ['    <recommendation option="option b">A wins because of one stated reason.</recommendation>']
    assert after == BARE_HEAD + promoted + ALTERNATIVE_LINES[5:] + ALTERNATIVE_LINES[:5] + ["  </open-question>"]
    assert [alternative.id for alternative in by_id(target, BARE).alternatives] == ["Option B", "Option A"]


def test_embed_recommendation_the_minimal_fragment(run_tool, milestone_dir):
    target = milestone_dir("bare")
    assert_ok(embed_alternatives(run_tool, target, FIRST, ONLY_ALTERNATIVE))
    assert_ok(embed_recommendation(run_tool, target, FIRST, ONLY_RECOMMENDATION))
    assert by_id(target, FIRST) == Question(
        id=FIRST,
        question="What is the first thing to decide?",
        alternatives=[Alternative(id="Only", text="Just this.")],
        recommendation=Recommendation(option="Only", rationale="Nothing else applies."),
    )
    assert block_lines(document_of(target).decode("utf-8"), FIRST) == [
        '  <open-question id="First bare question">',
        "    <question>What is the first thing to decide?</question>",
        '    <recommendation option="Only">Nothing else applies.</recommendation>',
        '    <alternative id="Only">',
        "      Just this.",
        "    </alternative>",
        "  </open-question>",
    ]


def test_embed_recommendation_keeps_several_principles_and_dependencies(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    assert_ok(embed_alternatives(run_tool, target, BARE, '<alternative id="X">x</alternative>'))
    body = (
        "<applied-principle>First</applied-principle>\n"
        "<applied-principle>Second</applied-principle>\n"
        '<depends-on question="Root element form" option="Open and close pair"/>\n'
        '<depends-on question="Escape hatch under sole writer" option="Strip subcommand"/>\n'
        '<recommendation option="X">x it is</recommendation>'
    )
    assert_ok(embed_recommendation(run_tool, target, BARE, body))
    block = by_id(target, BARE)
    assert block.alternatives == [Alternative(id="X", text="x")]
    assert block.principles == ["First", "Second"]
    assert block.depends_on == [
        Dependency(question="Root element form", option="Open and close pair"),
        Dependency(question="Escape hatch under sole writer", option="Strip subcommand"),
    ]
    assert block.recommendation == Recommendation(option="X", rationale="x it is")


def test_embed_recommendation_makes_the_block_annotated_for_list_lift_and_walk(run_tool, milestone_dir):
    target = milestone_dir("bare")
    assert_ok(embed_alternatives(run_tool, target, SECOND, ONLY_ALTERNATIVE))
    assert run_tool("list", "--without-recommendation", str(target)).stdout == b"First bare question\nSecond bare question\n"
    assert run_tool("walk", str(target)).stdout == b""
    assert_ok(embed_recommendation(run_tool, target, SECOND, ONLY_RECOMMENDATION))
    assert run_tool("list", "--without-recommendation", str(target)).stdout == b"First bare question\n"
    assert run_tool("list", str(target)).stdout == b"First bare question\nSecond bare question\n"
    assert run_tool("lift", str(target), SECOND).stdout.decode("utf-8") == "Only — Nothing else applies.\n"
    assert run_tool("walk", str(target)).stdout == b"Second bare question\n"


def test_embed_recommendation_compares_the_option_against_the_block_alternatives_un_escaped_and_case_folded(run_tool, milestone_dir):
    target = milestone_dir("bare")
    assert_ok(embed_alternatives(run_tool, target, FIRST, '<alternative id="A &amp; B">a</alternative>'))
    assert_ok(embed_recommendation(run_tool, target, FIRST, '<recommendation option="a &amp; b">r</recommendation>'))
    assert by_id(target, FIRST).recommendation == Recommendation(option="a & b", rationale="r")


def test_embed_recommendation_discards_alternative_lines_above_the_first_anchor_line(run_tool, milestone_dir):
    # A whole two-half message piped to --recommendation embeds the recommendation half alone:
    # the slice opens on the first line of that half, and the block's own alternatives — not
    # the message's — are what the option is checked against.
    target = milestone_dir("annotated")
    give_alternatives(target, BARE, "Option A", "Option B")
    frozen = block_lines(document_of(target).decode("utf-8"), BARE)
    assert_ok(embed_recommendation(run_tool, target, BARE, ALTERNATIVES + "\n" + RECOMMENDATION))
    after = block_lines(document_of(target).decode("utf-8"), BARE)
    assert after == frozen[:2] + RECOMMENDATION_LINES + frozen[2:]
    assert "      What option A is." not in after


# --- a prose-wrapped message ----------------------------------------------------------


def test_embed_discards_a_grounding_summary_above_and_a_closing_remark_below(run_tool, milestone_dir, tmp_path):
    clean = milestone_dir("annotated")
    assert_ok(embed_alternatives(run_tool, clean, BARE, ALTERNATIVES))
    assert_ok(embed_recommendation(run_tool, clean, BARE, RECOMMENDATION))
    target = tmp_path / "wrapped"
    target.mkdir()
    (target / open_questions.DOCUMENT_NAME).write_text(read_fixture("annotated"), encoding="utf-8")
    alternatives_message = (
        "I grounded this in the live project.\n"
        "\n"
        "Two options are realistic here.\n"
        "\n"
        f"{ALTERNATIVES}\n"
        "\n"
        "Those are the alternatives; let me know if anything is unclear.\n"
    )
    recommendation_message = (
        "Reasoning over the whole set, the sibling pick on Root element form settles the root.\n"
        "\n"
        f"{RECOMMENDATION}\n"
        "\n"
        "That is the recommendation.\n"
    )
    assert_ok(embed_alternatives(run_tool, target, BARE, alternatives_message))
    assert_ok(embed_recommendation(run_tool, target, BARE, recommendation_message))
    assert document_of(target) == document_of(clean)


def test_embed_discards_a_returned_wrapper_and_question_outside_the_fragment(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    wrapped = (
        '<open-question id="Fixture bare block">\n'
        "  <question>Does a bare block sit beside annotated siblings without change?</question>\n"
        "{half}\n"
        "</open-question>\n"
    )
    assert_ok(embed_alternatives(run_tool, target, BARE, wrapped.format(half=ALTERNATIVES)))
    assert_ok(embed_recommendation(run_tool, target, BARE, wrapped.format(half=RECOMMENDATION)))
    assert by_id(target, BARE).alternatives[0].id == "Option A"
    assert by_id(target, BARE).recommendation == Recommendation(option="Option A", rationale="A wins because of one stated reason.")


def test_embed_reads_a_message_with_crlf_line_ends(run_tool, milestone_dir):
    target = milestone_dir("bare")
    alternatives = ("Summary.\r\n" + ALTERNATIVES.replace("\n", "\r\n") + "\r\nRemark.\r\n").encode("utf-8")
    assert_ok(embed_alternatives(run_tool, target, FIRST, alternatives))
    assert [alternative.id for alternative in by_id(target, FIRST).alternatives] == ["Option A", "Option B"]
    recommendation = ("Summary.\r\n" + ONLY_RECOMMENDATION.replace("Only", "Option B").replace("\n", "\r\n") + "\r\nRemark.\r\n").encode("utf-8")
    assert_ok(embed_recommendation(run_tool, target, FIRST, recommendation))
    assert by_id(target, FIRST).recommendation == Recommendation(option="Option B", rationale="Nothing else applies.")


def test_extract_fragment_slices_from_the_first_opening_line_to_the_last_closing_line():
    message = "above\n" + ONLY_ALTERNATIVE + "\nbelow </alternative> mention\nafter"
    # The last line holding </alternative> is the "below" line, so it is inside the slice.
    assert open_questions.extract_fragment(message, ALTERNATIVES_SHAPE) == ONLY_ALTERNATIVE + "\nbelow </alternative> mention"
    assert open_questions.extract_fragment("x\ny\n" + ONLY_ALTERNATIVE, ALTERNATIVES_SHAPE) == ONLY_ALTERNATIVE
    message = "above\n" + ONLY_RECOMMENDATION + "\nbelow </recommendation> mention\nafter"
    assert open_questions.extract_fragment(message, RECOMMENDATION_SHAPE) == ONLY_RECOMMENDATION + "\nbelow </recommendation> mention"
    assert open_questions.extract_fragment("x\ny\n" + ONLY_RECOMMENDATION, RECOMMENDATION_SHAPE) == ONLY_RECOMMENDATION


def test_extract_fragment_opens_the_recommendation_half_on_any_of_its_three_start_tags():
    for first in ("<applied-principle>P</applied-principle>", '<depends-on question="Q" option="O"/>'):
        message = "above\n" + first + "\n" + ONLY_RECOMMENDATION + "\nbelow"
        assert open_questions.extract_fragment(message, RECOMMENDATION_SHAPE) == first + "\n" + ONLY_RECOMMENDATION


def test_extract_fragment_alternatives_shape_slices_past_a_recommendation_half_below():
    message = ALTERNATIVES + "\n" + RECOMMENDATION
    assert open_questions.extract_fragment(message, ALTERNATIVES_SHAPE) == ALTERNATIVES
    assert open_questions.extract_fragment(message, RECOMMENDATION_SHAPE) == RECOMMENDATION


# --- a misordered fragment ------------------------------------------------------------


def test_embed_groups_misordered_children_by_kind(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    # Complete but misordered: the extraction anchors of each half hold, and everything between
    # them is out of the canonical sequence, the children inside each alternative included.
    alternatives = (
        '<alternative id="Option A">\n'
        "  <drawback>A costs.</drawback>\n"
        "  What A is.\n"
        "  <advantage>A helps.</advantage>\n"
        "</alternative>\n"
        '<alternative id="Option B">\n'
        "  <advantage>B helps.</advantage>\n"
        "  <drawback>B costs.</drawback>\n"
        "  What B is.\n"
        "</alternative>"
    )
    recommendation = (
        '<depends-on question="Root element form" option="Self-closing root"/>\n'
        "<applied-principle>One rule over two</applied-principle>\n"
        '<depends-on question="Escape hatch under sole writer" option="Strip subcommand"/>\n'
        '<recommendation option="Option A">A wins after all.</recommendation>'
    )
    assert_ok(embed_alternatives(run_tool, target, BARE, alternatives))
    assert_ok(embed_recommendation(run_tool, target, BARE, recommendation))
    assert block_lines(document_of(target).decode("utf-8"), BARE) == [
        '  <open-question id="Fixture bare block">',
        "    <question>Does a bare block sit beside annotated siblings without change?</question>",
        "    <applied-principle>One rule over two</applied-principle>",
        '    <depends-on question="Root element form" option="Self-closing root"/>',
        '    <depends-on question="Escape hatch under sole writer" option="Strip subcommand"/>',
        '    <recommendation option="Option A">A wins after all.</recommendation>',
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
        "  </open-question>",
    ]


def test_embed_recommendation_takes_the_recommendation_before_its_siblings(run_tool, milestone_dir):
    # The slice opens on the first of the half's three start tags, whichever it is, and the
    # recommendation need not come last: the closing anchor is the last </recommendation> line.
    target = milestone_dir("annotated")
    assert_ok(embed_alternatives(run_tool, target, BARE, ALTERNATIVES))
    body = (
        '<recommendation option="Option B">B after all.</recommendation>\n'
        "<applied-principle>Late principle</applied-principle>\n"
        "<!-- </recommendation> -->"
    )
    assert_ok(embed_recommendation(run_tool, target, BARE, body))
    block = by_id(target, BARE)
    assert block.principles == ["Late principle"]
    assert block.recommendation == Recommendation(option="Option B", rationale="B after all.")


def test_extract_fragment_anchors_on_a_misordered_fragment_first_opening_and_last_closing():
    message = (
        "Note.\n"
        '<alternative id="A">a</alternative>\n'
        '<alternative id="B">b</alternative>\n'
        "Done.\n"
        '<alternative id="C">c\n'
    )
    # The trailing alternative has no closing line below the last </alternative> line, so it
    # is discarded — a misordering that loses an element is caught only by the agent's own
    # self-check, as the format decision says.
    assert open_questions.extract_fragment(message, ALTERNATIVES_SHAPE) == '<alternative id="A">a</alternative>\n<alternative id="B">b</alternative>'


def test_embed_normalizes_indentation_escaping_and_folded_text(run_tool, milestone_dir):
    target = milestone_dir("bare")
    alternatives = (
        '\t\t<alternative id="Tabs &amp; spaces">\n'
        "\t\t\t\tWhat it\n"
        "   is, over\n"
        "\t\tthree lines with 'quotes' and \"doubles\".\n"
        '\t\t\t<advantage>Keeps <![CDATA[<raw>]]> text.</advantage>\n'
        "  <drawback>Costs   extra\tspace.</drawback></alternative>"
    )
    recommendation = (
        '<depends-on question="Second bare question" option="Only" />\n'
        '<recommendation   option="tabs &amp; SPACES"  >It &gt; the rest.</recommendation>'
    )
    assert_ok(embed_alternatives(run_tool, target, SECOND, ONLY_ALTERNATIVE))
    assert_ok(embed_alternatives(run_tool, target, FIRST, alternatives))
    assert_ok(embed_recommendation(run_tool, target, FIRST, recommendation))
    assert block_lines(document_of(target).decode("utf-8"), FIRST) == [
        '  <open-question id="First bare question">',
        "    <question>What is the first thing to decide?</question>",
        '    <depends-on question="Second bare question" option="Only"/>',
        '    <recommendation option="tabs &amp; SPACES">It &gt; the rest.</recommendation>',
        '    <alternative id="Tabs &amp; spaces">',
        "      What it is, over three lines with &apos;quotes&apos; and &quot;doubles&quot;.",
        "      <advantage>Keeps &lt;raw&gt; text.</advantage>",
        "      <drawback>Costs extra space.</drawback>",
        "    </alternative>",
        "  </open-question>",
    ]


# --- <depends-on> resolution ----------------------------------------------------------


def test_embed_resolves_a_dependency_against_a_block_with_alternatives_un_escaped_and_case_folded(run_tool, milestone_dir):
    target = milestone_dir("entities")
    document = load(target)
    document.questions.append(Question(id="Dependent", question="Does it resolve?", alternatives=[Alternative(id="Yes", text="It does.")]))
    open_questions.save_document(str(target), document)
    body = (
        f'<depends-on question="{open_questions.escape(ENTITIES_TITLE.upper())}" option="a &amp; b"/>\n'
        '<recommendation option="Yes">Resolved.</recommendation>'
    )
    assert_ok(embed_recommendation(run_tool, target, "Dependent", body))
    assert by_id(target, "Dependent").depends_on == [Dependency(question=ENTITIES_TITLE.upper(), option="a & b")]


def test_embed_resolves_a_dependency_on_a_sibling_carrying_alternatives_and_no_recommendation(run_tool, milestone_dir):
    # The dropped half of the check: the target need not carry a <recommendation>, so the
    # recommendation pass may write its blocks in any order.
    target = milestone_dir("annotated")
    assert_ok(embed_alternatives(run_tool, target, BARE, ALTERNATIVES))
    assert run_tool("strip", "--recommendation", str(target), ROOT_FORM).returncode == 0
    assert by_id(target, BARE).recommendation is None
    body = '<depends-on question="fixture BARE block" option="option b"/>\n<recommendation option="Self-closing root">r</recommendation>'
    assert_ok(embed_recommendation(run_tool, target, ROOT_FORM, body))
    assert by_id(target, ROOT_FORM).depends_on == [Dependency(question="fixture BARE block", option="option b")]
    assert run_tool("walk", str(target)).stdout == b"Escape hatch under sole writer\nRoot element form\n"


def test_embed_resolves_one_hop_only_and_follows_no_tag_of_the_target(run_tool, milestone_dir):
    # The entities block's own <depends-on> names a block the document does not hold; a
    # dependency on that block still resolves, because the target's tags are not followed.
    target = milestone_dir("entities")
    document = load(target)
    assert document.questions[0].depends_on[0].question == 'Some "other" question & more'
    document.questions.append(Question(id="Dependent", question="One hop?", alternatives=[Alternative(id="Yes")]))
    open_questions.save_document(str(target), document)
    body = (
        f'<depends-on question="{open_questions.escape(ENTITIES_TITLE)}" option="A &amp; B"/>\n'
        '<recommendation option="Yes">Resolved.</recommendation>'
    )
    assert_ok(embed_recommendation(run_tool, target, "Dependent", body))


def test_embed_tolerates_a_dependency_cycle(run_tool, tmp_path):
    target = write_document(
        tmp_path / "cycle",
        Question(id="A", question="a?", alternatives=[Alternative(id="A1")], depends_on=[Dependency(question="B", option="B1")], recommendation=Recommendation(option="A1")),
        Question(id="B", question="b?", alternatives=[Alternative(id="B1")]),
    )
    body = '<depends-on question="A" option="A1"/>\n<recommendation option="B1">r</recommendation>'
    assert_ok(embed_recommendation(run_tool, target, "B", body))
    assert by_id(target, "B").depends_on == [Dependency(question="A", option="A1")]


@pytest.mark.parametrize("question", ["No such block", "Fixture bare block"])
def test_embed_refuses_a_dependency_on_a_missing_block_or_one_without_alternatives(run_tool, milestone_dir, question):
    target = milestone_dir("annotated")
    assert run_tool("strip", "--recommendation", str(target), ROOT_FORM).returncode == 0
    before = document_of(target)
    body = f'<depends-on question="{question}" option="Y"/>\n<recommendation option="Self-closing root">r</recommendation>'
    result = embed_recommendation(run_tool, target, ROOT_FORM, body)
    assert_refused(
        result,
        target,
        before,
        f'the <depends-on question="{question}"/> names no block that carries <alternative> elements; '
        'the blocks carrying them are "Escape hatch under sole writer"',
    )


def test_embed_refuses_a_dependency_on_a_bare_sibling_when_no_other_block_has_alternatives(run_tool, milestone_dir):
    target = milestone_dir("bare")
    give_alternatives(target, FIRST, "X")
    before = document_of(target)
    body = '<depends-on question="Second bare question" option="Y"/>\n<recommendation option="X">r</recommendation>'
    result = embed_recommendation(run_tool, target, FIRST, body)
    assert_refused(
        result,
        target,
        before,
        'the <depends-on question="Second bare question"/> names no block that carries <alternative> elements; no other block carries any',
    )


def test_embed_refuses_a_dependency_whose_option_names_none_of_the_target_alternatives(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    give_alternatives(target, BARE, "X")
    before = document_of(target)
    body = '<depends-on question="root element FORM" option="Neither"/>\n<recommendation option="X">r</recommendation>'
    result = embed_recommendation(run_tool, target, BARE, body)
    assert_refused(
        result,
        target,
        before,
        'the <depends-on question="root element FORM" option="Neither"/> names none of that block\'s <alternative> ids, '
        'which are "Self-closing root", "Open and close pair"',
    )


def test_embed_refuses_a_dependency_on_the_block_being_embedded(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    give_alternatives(target, BARE, "X")
    before = document_of(target)
    body = '<depends-on question="Fixture bare block" option="X"/>\n<recommendation option="X">r</recommendation>'
    result = embed_recommendation(run_tool, target, BARE, body)
    assert result.returncode == 1
    assert result.stderr.startswith(b'Error: the <depends-on question="Fixture bare block"/> names no block that carries <alternative> elements')
    assert document_of(target) == before


# --- the block state each shape writes into -------------------------------------------


@pytest.mark.parametrize("short_title", [HATCH, ROOT_FORM])
def test_embed_alternatives_refuses_a_block_already_carrying_alternatives(run_tool, milestone_dir, short_title):
    target = milestone_dir("annotated")
    assert run_tool("strip", "--recommendation", str(target), ROOT_FORM).returncode == 0
    before = document_of(target)
    result = embed_alternatives(run_tool, target, short_title.upper(), ONLY_ALTERNATIVE)
    assert_refused(
        result,
        target,
        before,
        f'<open-question id="{short_title}"> already carries <alternative> elements; strip it first to embed a new set',
    )


def test_embed_recommendation_refuses_a_block_carrying_no_alternatives(run_tool, milestone_dir):
    target = milestone_dir("bare")
    before = document_of(target)
    result = embed_recommendation(run_tool, target, "first BARE question", ONLY_RECOMMENDATION)
    assert_refused(
        result,
        target,
        before,
        '<open-question id="First bare question"> carries no <alternative> elements; embed --alternatives first',
    )


def test_embed_recommendation_refuses_a_block_already_carrying_a_recommendation(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = document_of(target)
    result = embed_recommendation(run_tool, target, "root ELEMENT form", '<recommendation option="Self-closing root">r</recommendation>')
    assert_refused(
        result,
        target,
        before,
        '<open-question id="Root element form"> already carries a <recommendation> element; strip --recommendation first to embed a new one',
    )


def test_embed_checks_the_block_state_before_reading_the_message(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = document_of(target)
    # An unpiped, closed stdin would be its own refusal; the block's state is reported first.
    alternatives = run_tool("embed", "--alternatives", str(target), HATCH, stdin=b"")
    assert alternatives.stderr.startswith(b'Error: <open-question id="Escape hatch under sole writer"> already carries <alternative>')
    recommendation = run_tool("embed", "--recommendation", str(target), BARE, stdin=b"")
    assert recommendation.stderr.startswith(b'Error: <open-question id="Fixture bare block"> carries no <alternative>')
    assert document_of(target) == before


# --- the two extraction misses of each shape ------------------------------------------


@pytest.mark.parametrize(
    "body",
    [
        b"",
        b"   \n\n",
        b"I could not ground this question in the project.\n",
        b'<recommendation option="A">no alternatives above</recommendation>\n',
        b"The word &lt;alternative escaped is not a line to extract from.\n</alternative>\n",
    ],
)
def test_embed_alternatives_refuses_a_message_with_no_alternative_line(run_tool, milestone_dir, body):
    target = milestone_dir("bare")
    before = document_of(target)
    assert_refused(embed_alternatives(run_tool, target, FIRST, body), target, before, "no <alternative> line to extract from")


@pytest.mark.parametrize(
    "body",
    [
        b'<alternative id="A"/>\n',
        b'<alternative id="A">unterminated\n',
        b'<alternative id="A">a\n<recommendation option="A">r</recommendation>\n',
    ],
)
def test_embed_alternatives_refuses_a_message_with_no_closing_alternative_line(run_tool, milestone_dir, body):
    target = milestone_dir("bare")
    before = document_of(target)
    assert_refused(embed_alternatives(run_tool, target, FIRST, body), target, before, "no </alternative> line to extract to")


def test_embed_alternatives_refuses_a_closing_alternative_line_above_the_first_alternative_line(run_tool, milestone_dir):
    target = milestone_dir("bare")
    before = document_of(target)
    body = b'</alternative>\n<alternative id="A">a\n'
    assert_refused(
        embed_alternatives(run_tool, target, FIRST, body),
        target,
        before,
        "the last </alternative> line precedes the first <alternative> line",
    )


@pytest.mark.parametrize(
    "body",
    [
        b"",
        b"   \n\n",
        b"I could not settle this question.\n",
        b'<alternative id="A">an alternative is not this half</alternative>\n',
        b"The word &lt;recommendation escaped is not a line to extract from.\n</recommendation>\n",
    ],
)
def test_embed_recommendation_refuses_a_message_with_no_opening_line_of_its_half(run_tool, milestone_dir, body):
    target = prepared(milestone_dir, "--recommendation")
    before = document_of(target)
    assert_refused(
        embed_recommendation(run_tool, target, FIRST, body),
        target,
        before,
        "no <applied-principle>, <depends-on>, or <recommendation> line to extract from",
    )


@pytest.mark.parametrize(
    "body",
    [
        b"<applied-principle>P</applied-principle>\n",
        b'<depends-on question="Q" option="O"/>\n',
        b'<recommendation option="A">unterminated\n',
        b'<recommendation option="A"/>\n',
    ],
)
def test_embed_recommendation_refuses_a_message_with_no_closing_recommendation_line(run_tool, milestone_dir, body):
    target = prepared(milestone_dir, "--recommendation")
    before = document_of(target)
    assert_refused(embed_recommendation(run_tool, target, FIRST, body), target, before, "no </recommendation> line to extract to")


def test_embed_recommendation_refuses_a_closing_recommendation_line_above_the_first_opening_line(run_tool, milestone_dir):
    target = prepared(milestone_dir, "--recommendation")
    before = document_of(target)
    body = b'</recommendation>\n<applied-principle>P</applied-principle>\n<recommendation option="A">r\n'
    assert_refused(
        embed_recommendation(run_tool, target, FIRST, body),
        target,
        before,
        "the last </recommendation> line precedes the first <applied-principle>, <depends-on>, or <recommendation> line",
    )


# --- each failing fragment, under both shapes -----------------------------------------


@pytest.mark.parametrize("shape", SHAPES)
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
def test_embed_refuses_a_wrapper_or_question_line_inside_the_fragment(run_tool, milestone_dir, shape, line, tag, article):
    target = prepared(milestone_dir, shape)
    before = document_of(target)
    assert_refused(
        embed(run_tool, target, FIRST, framed(shape, line), shape),
        target,
        before,
        f"the fragment contains {article} {tag} line; the <open-question> wrapper and its <question> element belong to "
        "the document, not to the fragment",
    )


@pytest.mark.parametrize("shape", SHAPES)
def test_embed_does_not_mistake_a_longer_tag_or_escaped_text_for_a_question_line(run_tool, milestone_dir, shape):
    target = prepared(milestone_dir, shape)
    before = document_of(target)
    body = framed(shape, "<questionable>x &lt;question&gt; in text</questionable>")
    result = embed(run_tool, target, FIRST, body, shape)
    assert_refused(result, target, before, "the fragment carries an unexpected <questionable> element")


@pytest.mark.parametrize(
    "shape, body, reason",
    [
        ("--alternatives", 'Here they are: <alternative id="A">a</alternative>', "text precedes <alternative> on the fragment's opening line"),
        ("--recommendation", 'Here it is: <recommendation option="A">r</recommendation>', "text precedes <recommendation> on the fragment's opening line"),
        ("--recommendation", "Cited: <applied-principle>P</applied-principle>\n" + '<recommendation option="A">r</recommendation>', "text precedes <applied-principle> on the fragment's opening line"),
    ],
)
def test_embed_refuses_text_preceding_the_first_element(run_tool, milestone_dir, shape, body, reason):
    target = prepared(milestone_dir, shape)
    before = document_of(target)
    assert_refused(embed(run_tool, target, FIRST, body, shape), target, before, reason)


@pytest.mark.parametrize(
    "shape, body, reason",
    [
        ("--alternatives", '<alternative id="A">a</alternative> That is all.', "text trails </alternative> on the fragment's closing line"),
        ("--recommendation", '<recommendation option="A">r</recommendation> That is all.', "text trails </recommendation> on the fragment's closing line"),
    ],
)
def test_embed_refuses_text_trailing_the_last_element(run_tool, milestone_dir, shape, body, reason):
    target = prepared(milestone_dir, shape)
    before = document_of(target)
    assert_refused(embed(run_tool, target, FIRST, body, shape), target, before, reason)


@pytest.mark.parametrize("shape", SHAPES)
def test_embed_refuses_text_between_the_elements(run_tool, milestone_dir, shape):
    target = prepared(milestone_dir, shape)
    before = document_of(target)
    body = framed(shape, "A note between the elements.")
    assert_refused(embed(run_tool, target, FIRST, body, shape), target, before, "the fragment carries text between its elements")


@pytest.mark.parametrize(
    "shape, body, reason",
    [
        (
            "--alternatives",
            '<alternative id="A">a\n<alternative id="B">b</alternative>',
            "mismatched tag at line 3, column 2",
        ),
        (
            "--alternatives",
            '<alternative id="A">a &amp b</alternative>',
            "not well-formed (invalid token) at line 1, column 26",
        ),
        (
            "--recommendation",
            '<applied-principle>P\n<recommendation option="A">r</recommendation>',
            "mismatched tag at line 3, column 2",
        ),
        (
            "--recommendation",
            '<recommendation option=A>r</recommendation>',
            "not well-formed (invalid token) at line 1, column 23",
        ),
    ],
)
def test_embed_refuses_a_fragment_that_is_not_well_formed_xml(run_tool, milestone_dir, shape, body, reason):
    target = prepared(milestone_dir, shape)
    before = document_of(target)
    assert_refused(embed(run_tool, target, FIRST, body, shape), target, before, f"the fragment is not well-formed XML: {reason}")


@pytest.mark.parametrize(
    "shape, body, reason",
    [
        # The anchor lines hold their markers only inside comments, which the parser drops.
        ("--alternatives", '<!-- <alternative id="A"/> -->\n<!-- </alternative> -->', "the fragment contains no <alternative> element"),
        ("--recommendation", '<!-- <recommendation option="A"/> -->\n<!-- </recommendation> -->', "the fragment contains no <recommendation> element"),
        ("--recommendation", "<applied-principle>P</applied-principle>\n<!-- </recommendation> -->", "the fragment contains no <recommendation> element"),
    ],
)
def test_embed_refuses_a_fragment_without_the_required_element(run_tool, milestone_dir, shape, body, reason):
    target = prepared(milestone_dir, shape)
    before = document_of(target)
    assert_refused(embed(run_tool, target, FIRST, body, shape), target, before, reason)


def test_embed_recommendation_refuses_two_recommendation_elements(run_tool, milestone_dir):
    target = prepared(milestone_dir, "--recommendation")
    before = document_of(target)
    body = '<recommendation option="A">r</recommendation>\n<recommendation option="A">again</recommendation>'
    assert_refused(embed_recommendation(run_tool, target, FIRST, body), target, before, "the fragment carries 2 <recommendation> elements")


def test_embed_recommendation_refuses_an_option_naming_none_of_the_block_alternatives(run_tool, milestone_dir):
    target = prepared(milestone_dir, "--recommendation")
    before = document_of(target)
    body = '<recommendation option="C">r</recommendation>'
    assert_refused(
        embed_recommendation(run_tool, target, FIRST, body),
        target,
        before,
        'the <recommendation> option "C" names none of the <alternative> ids of <open-question id="First bare question">, which are "A", "B"',
    )


@pytest.mark.parametrize(
    "shape, body, reason",
    [
        (
            "--alternatives",
            '<alternative id="A">a</alternative>\n<applied-principle>P</applied-principle>\n<alternative id="B">b</alternative>',
            "the fragment carries an <applied-principle> element, which --alternatives does not take",
        ),
        (
            "--alternatives",
            '<alternative id="A">a</alternative>\n<depends-on question="Q" option="O"/>\n<alternative id="B">b</alternative>',
            "the fragment carries a <depends-on> element, which --alternatives does not take",
        ),
        (
            "--alternatives",
            '<alternative id="A">a</alternative>\n<recommendation option="A">r</recommendation>\n<alternative id="B">b</alternative>',
            "the fragment carries a <recommendation> element, which --alternatives does not take",
        ),
        (
            "--recommendation",
            '<applied-principle>P</applied-principle>\n<alternative id="C">c</alternative>\n<recommendation option="A">r</recommendation>',
            "the fragment carries an <alternative> element, which --recommendation does not take",
        ),
        (
            "--recommendation",
            '<recommendation option="A">r</recommendation>\n<alternative id="C">c</alternative>\n<recommendation option="A">again</recommendation>',
            "the fragment carries an <alternative> element, which --recommendation does not take",
        ),
    ],
)
def test_embed_refuses_an_element_of_the_other_half(run_tool, milestone_dir, shape, body, reason):
    target = prepared(milestone_dir, shape)
    before = document_of(target)
    assert_refused(embed(run_tool, target, FIRST, body, shape), target, before, reason)


@pytest.mark.parametrize(
    "shape, body, reason",
    [
        (
            "--alternatives",
            '<alternative id="A">a</alternative>\n<note>n</note>\n<alternative id="B">b</alternative>',
            "the fragment carries an unexpected <note> element",
        ),
        (
            "--alternatives",
            '<alternative id="A">a<benefit>b</benefit></alternative>',
            '<alternative id="A"> of the fragment carries an unexpected <benefit> element',
        ),
        (
            "--recommendation",
            '<applied-principle>P</applied-principle>\n<note>n</note>\n<recommendation option="A">r</recommendation>',
            "the fragment carries an unexpected <note> element",
        ),
        (
            "--recommendation",
            '<applied-principle>P<em>!</em></applied-principle>\n<recommendation option="A">r</recommendation>',
            "an <applied-principle> element of the fragment carries an unexpected <em> element",
        ),
        (
            "--recommendation",
            '<recommendation option="A">r<b>!</b></recommendation>',
            "the <recommendation> element of the fragment carries an unexpected <b> element",
        ),
        (
            "--recommendation",
            '<depends-on question="X" option="Y">text</depends-on>\n<recommendation option="A">r</recommendation>',
            "a <depends-on> element of the fragment carries text",
        ),
    ],
)
def test_embed_refuses_an_element_of_an_unknown_kind(run_tool, milestone_dir, shape, body, reason):
    target = prepared(milestone_dir, shape)
    before = document_of(target)
    assert_refused(embed(run_tool, target, FIRST, body, shape), target, before, reason)


@pytest.mark.parametrize(
    "shape, body, reason",
    [
        (
            "--alternatives",
            '<alternative id="A">a</alternative>\n<alternative id="a">again</alternative>',
            'the fragment carries two <alternative> elements with the id "a"',
        ),
        (
            "--alternatives",
            "<alternative>a</alternative>",
            "an <alternative> element of the fragment has no id attribute",
        ),
        (
            "--alternatives",
            '<alternative id="  ">a</alternative>',
            "an <alternative> element of the fragment has an empty id attribute",
        ),
        (
            "--alternatives",
            '<alternative id="A" rank="1">a</alternative>',
            'an <alternative> element of the fragment carries an unknown attribute "rank"',
        ),
        (
            "--recommendation",
            "<recommendation>r</recommendation>",
            "the <recommendation> element of the fragment has no option attribute",
        ),
        (
            "--recommendation",
            '<recommendation option="">r</recommendation>',
            "the <recommendation> element of the fragment has an empty option attribute",
        ),
        (
            "--recommendation",
            '<depends-on question="X"/>\n<recommendation option="A">r</recommendation>',
            "a <depends-on> element of the fragment has no option attribute",
        ),
        (
            "--recommendation",
            '<applied-principle weight="2">P</applied-principle>\n<recommendation option="A">r</recommendation>',
            'an <applied-principle> element of the fragment carries an unknown attribute "weight"',
        ),
    ],
)
def test_embed_refuses_a_malformed_attribute(run_tool, milestone_dir, shape, body, reason):
    target = prepared(milestone_dir, shape)
    before = document_of(target)
    assert_refused(embed(run_tool, target, FIRST, body, shape), target, before, reason)


# --- the block and the document -------------------------------------------------------


@pytest.mark.parametrize("shape", SHAPES)
def test_embed_refuses_an_unknown_short_title(run_tool, milestone_dir, shape):
    target = milestone_dir("bare")
    before = document_of(target)
    result = embed(run_tool, target, "Missing", minimal(shape), shape)
    assert_refused(
        result,
        target,
        before,
        'no <open-question> block has the id "Missing"; the document holds "First bare question", "Second bare question"',
    )


@pytest.mark.parametrize("shape", SHAPES)
def test_embed_refuses_an_unknown_short_title_on_an_empty_document(run_tool, milestone_dir, shape):
    target = milestone_dir("empty")
    result = embed(run_tool, target, "Anything", minimal(shape), shape)
    assert_refused(result, target, b"<open-questions/>\n", 'no <open-question> block has the id "Anything"; the document holds no blocks')


@pytest.mark.parametrize("shape", SHAPES)
def test_embed_requires_a_short_title(run_tool, milestone_dir, shape):
    result = run_tool("embed", shape, str(milestone_dir("bare")), stdin=minimal(shape).encode("utf-8"))
    assert result.returncode == 2
    assert result.stdout == b""
    assert b"SHORT_TITLE" in result.stderr


@pytest.mark.parametrize("shape", SHAPES)
def test_embed_fails_when_the_document_is_missing_and_creates_nothing(run_tool, tmp_path, shape):
    result = embed(run_tool, tmp_path, "Anything", minimal(shape), shape)
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == f"Error: {tmp_path / open_questions.DOCUMENT_NAME} does not exist\n".encode("utf-8")
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("shape", SHAPES)
def test_embed_fails_on_a_malformed_document_and_leaves_it_unchanged(run_tool, tmp_path, shape):
    document = tmp_path / open_questions.DOCUMENT_NAME
    document.write_text("<open-questions>", encoding="utf-8")
    result = embed(run_tool, tmp_path, "Anything", minimal(shape), shape)
    assert result.returncode == 1
    assert result.stdout == b""
    assert b"not well-formed XML" in result.stderr
    assert result.stderr.count(b"\n") == 1
    assert document.read_text(encoding="utf-8") == "<open-questions>"


# --- the stdin channel ----------------------------------------------------------------


@pytest.mark.parametrize("shape", SHAPES)
def test_embed_refuses_a_terminal_stdin_without_blocking(milestone_dir, shape):
    pty = pytest.importorskip("pty")
    target = prepared(milestone_dir, shape)
    before = document_of(target)
    master, slave = pty.openpty()
    try:
        result = subprocess.run(
            [sys.executable, "-B", str(TOOL), "embed", shape, str(target), FIRST],
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
        f"Error: the {shape.lstrip('-')} message must be piped on standard input (as a quoted heredoc or a "
        "redirected file), not typed at a terminal\n"
    ).encode("utf-8")
    assert document_of(target) == before


@pytest.mark.parametrize("shape", SHAPES)
def test_main_refuses_a_closed_stdin(capsys, monkeypatch, milestone_dir, shape):
    target = prepared(milestone_dir, shape)
    before = document_of(target)
    monkeypatch.setattr(sys, "stdin", None)
    assert open_questions.main(["embed", shape, str(target), FIRST]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == f"Error: the {shape.lstrip('-')} message must be supplied on standard input, which is closed\n"
    assert document_of(target) == before


def test_main_reads_the_message_from_stdin_buffer_once(capsys, monkeypatch, milestone_dir):
    target = milestone_dir("bare")
    stream = io.TextIOWrapper(io.BytesIO(("Summary — dashes …\n" + ONLY_ALTERNATIVE + "\n").encode("utf-8")))
    monkeypatch.setattr(sys, "stdin", stream)
    assert open_questions.main(["embed", "--alternatives", str(target), FIRST]) == 0
    assert capsys.readouterr() == ("", "")
    assert stream.buffer.read() == b""
    stream = io.TextIOWrapper(io.BytesIO(("Summary — dashes …\n" + ONLY_RECOMMENDATION + "\n").encode("utf-8")))
    monkeypatch.setattr(sys, "stdin", stream)
    assert open_questions.main(["embed", "--recommendation", str(target), FIRST]) == 0
    assert capsys.readouterr() == ("", "")
    assert stream.buffer.read() == b""
    assert by_id(target, FIRST).recommendation == Recommendation(option="Only", rationale="Nothing else applies.")


@pytest.mark.parametrize("shape", SHAPES)
def test_embed_refuses_a_non_utf8_message(run_tool, milestone_dir, shape):
    target = prepared(milestone_dir, shape)
    before = document_of(target)
    result = embed(run_tool, target, FIRST, minimal(shape).encode("utf-8") + b"\n<!-- caf\xe9 -->", shape)
    assert_refused(result, target, before, f"the {shape.lstrip('-')} message on standard input is not UTF-8 text")


def test_embed_reads_the_message_verbatim_with_nothing_expanded(run_tool, milestone_dir):
    target = milestone_dir("bare")
    alternatives = '<alternative id="A">Does `code`, ${VAR}, $(cmd), and a literal &amp;apos; travel untouched?</alternative>'
    assert_ok(embed_alternatives(run_tool, target, FIRST, alternatives))
    assert by_id(target, FIRST).alternatives[0].text == "Does `code`, ${VAR}, $(cmd), and a literal &apos; travel untouched?"
    recommendation = '<recommendation option="A">Does `code`, ${VAR}, $(cmd), and a literal &amp;apos; travel untouched?</recommendation>'
    assert_ok(embed_recommendation(run_tool, target, FIRST, recommendation))
    assert by_id(target, FIRST).recommendation.rationale == "Does `code`, ${VAR}, $(cmd), and a literal &apos; travel untouched?"


# --- the single write -----------------------------------------------------------------


def test_embed_writes_exactly_once_on_success_and_never_on_a_refusal(monkeypatch, milestone_dir):
    target = milestone_dir("annotated")
    calls = []
    original = open_questions.save_document

    def counting(milestone_dir, document):
        calls.append(milestone_dir)
        original(milestone_dir, document)

    monkeypatch.setattr(open_questions, "save_document", counting)
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(ALTERNATIVES.encode("utf-8"))))
    assert open_questions.main(["embed", "--alternatives", str(target), BARE]) == 0
    assert calls == [str(target)]
    calls.clear()
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(RECOMMENDATION.encode("utf-8"))))
    assert open_questions.main(["embed", "--recommendation", str(target), BARE]) == 0
    assert calls == [str(target)]
    calls.clear()
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(b"prose only")))
    assert open_questions.main(["embed", "--alternatives", str(target), HATCH]) == 1
    open_questions.main(["strip", "--recommendation", str(target), HATCH])
    calls.clear()
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(b'<depends-on question="Nope" option="X"/>\n<recommendation option="Strip subcommand">r</recommendation>')))
    assert open_questions.main(["embed", "--recommendation", str(target), HATCH]) == 1
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(b'<recommendation option="Nope">r</recommendation>')))
    assert open_questions.main(["embed", "--recommendation", str(target), HATCH]) == 1
    assert calls == []


def test_embed_leaves_no_temporary_file_behind(run_tool, milestone_dir):
    target = milestone_dir("bare")
    embed_alternatives(run_tool, target, FIRST, ONLY_ALTERNATIVE)
    embed_alternatives(run_tool, target, FIRST, ONLY_ALTERNATIVE)
    embed_recommendation(run_tool, target, FIRST, ONLY_RECOMMENDATION)
    embed_recommendation(run_tool, target, FIRST, ONLY_RECOMMENDATION)
    embed_alternatives(run_tool, target, SECOND, b"prose only")
    embed_recommendation(run_tool, target, SECOND, b"prose only")
    assert sorted(path.name for path in target.iterdir()) == [open_questions.DOCUMENT_NAME]


def test_embed_fragment_writes_each_half_on_the_parsed_tree(tmp_path):
    target = Question(id="Target", question="target?", alternatives=[Alternative(id="B", text="b")])
    bare = Question(id="Bare", question="bare?")
    document = Document([target, bare])
    alternatives = open_questions.parse_fragment('<alternative id="X">x</alternative>', ALTERNATIVES_SHAPE)
    assert alternatives == Question(id="", alternatives=[Alternative(id="X", text="x")])
    open_questions.embed_fragment(document, bare, alternatives, ALTERNATIVES_SHAPE)
    assert bare == Question(id="Bare", question="bare?", alternatives=[Alternative(id="X", text="x")])
    recommendation = open_questions.parse_fragment(
        '<depends-on question="target" option="b"/>\n<recommendation option="x">r</recommendation>', RECOMMENDATION_SHAPE
    )
    assert recommendation == Question(
        id="",
        depends_on=[Dependency(question="target", option="b")],
        recommendation=Recommendation(option="x", rationale="r"),
    )
    open_questions.embed_fragment(document, bare, recommendation, RECOMMENDATION_SHAPE)
    assert bare == Question(
        id="Bare",
        question="bare?",
        alternatives=[Alternative(id="X", text="x")],
        depends_on=[Dependency(question="target", option="b")],
        recommendation=Recommendation(option="x", rationale="r"),
    )
    assert target == Question(id="Target", question="target?", alternatives=[Alternative(id="B", text="b")])
