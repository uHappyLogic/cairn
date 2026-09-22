"""The strip subcommand: every child but <question> deleted from each named block, the
wrapper and <question> kept, every other block — a <depends-on> tag naming the stripped
block included — untouched, an unknown id refused with the document unchanged, and a bare
block left as it is; with --recommendation only the <recommendation>, <depends-on>, and
<applied-principle> children deleted and the <alternative> children left standing, through
the one per-block primitive the cascade's partial strip reuses."""

from pathlib import Path

import pytest

import open_questions
from open_questions import Alternative, Dependency, Question, Recommendation

FIXTURES = Path(__file__).resolve().parent / "fixtures"
ENTITIES_TITLE = "Ampersand & angle <brackets>, \"quotes\", 'apostrophes'"


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


def bare_block(short_title, question):
    return [
        f'  <open-question id="{open_questions.escape(short_title)}">',
        f"    <question>{open_questions.escape(question)}</question>",
        "  </open-question>",
    ]


def test_strip_leaves_only_the_wrapper_and_the_question(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    result = run_tool("strip", str(target), "Escape hatch under sole writer")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    after = document_of(target).decode("utf-8")
    assert block_lines(after, "Escape hatch under sole writer") == bare_block(
        "Escape hatch under sole writer",
        "With the tool as the file's only writer, how does a user clear a stale recommendation to force "
        "its regeneration — a `strip` subcommand or a documented hand-edit exception?",
    )


def test_strip_deletes_every_kind_of_child(run_tool, milestone_dir):
    target = milestone_dir("entities")
    before = open_questions.load_document(str(target)).questions[0]
    assert before.alternatives and before.principles and before.depends_on and before.recommendation is not None
    result = run_tool("strip", str(target), ENTITIES_TITLE)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    after = open_questions.load_document(str(target)).questions[0]
    assert after == Question(id=before.id, question=before.question)
    assert open_questions.is_bare(after)
    assert document_of(target).decode("utf-8") == (
        "<open-questions>\n"
        '  <open-question id="Ampersand &amp; angle &lt;brackets&gt;, &quot;quotes&quot;, &apos;apostrophes&apos;">\n'
        "    <question>Does text with &amp;, &lt;tag&gt;, &quot;double&quot; and &apos;single&apos; quotes survive a round trip?</question>\n"
        "  </open-question>\n"
        "</open-questions>\n"
    )


def test_strip_touches_no_dependent_and_no_depends_on_tag_naming_the_block(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = read_fixture("annotated")
    result = run_tool("strip", str(target), "Escape hatch under sole writer")
    assert result.returncode == 0
    after = document_of(target).decode("utf-8")
    dependent = block_lines(after, "Root element form")
    assert dependent == block_lines(before, "Root element form")
    assert '    <depends-on question="Escape hatch under sole writer" option="Strip subcommand"/>' in dependent
    assert '    <recommendation option="Self-closing root">' in "\n".join(dependent)
    assert block_lines(after, "Fixture bare block") == block_lines(before, "Fixture bare block")


def test_strip_keeps_every_other_line_of_the_document(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = read_fixture("annotated")
    run_tool("strip", str(target), "Escape hatch under sole writer")
    after = document_of(target).decode("utf-8")
    stripped = block_lines(before, "Escape hatch under sole writer")
    expected = before.replace(
        "\n".join(stripped),
        "\n".join(bare_block("Escape hatch under sole writer", open_questions.load_document(str(target)).questions[0].question)),
    )
    assert after == expected


def test_strip_keeps_the_document_canonical(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    run_tool("strip", str(target), "Root element form")
    text = document_of(target).decode("utf-8")
    assert open_questions.render_document(open_questions.parse_document(text)) == text


def test_strip_of_several_blocks_strips_each(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    result = run_tool("strip", str(target), "Root element form", "Escape hatch under sole writer")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    document = open_questions.load_document(str(target))
    assert [question.id for question in document.questions] == [
        "Escape hatch under sole writer",
        "Root element form",
        "Fixture bare block",
    ]
    assert all(open_questions.is_bare(question) for question in document.questions)
    assert run_tool("list", str(target), "--unannotated").stdout == (
        b"Escape hatch under sole writer\nRoot element form\nFixture bare block\n"
    )


def test_strip_of_a_block_named_twice_strips_it_once(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    result = run_tool("strip", str(target), "Root element form", "ROOT element FORM")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    document = open_questions.load_document(str(target))
    assert open_questions.is_bare(document.questions[1])
    assert not open_questions.is_bare(document.questions[0])


def test_strip_matches_the_short_title_case_folded(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    result = run_tool("strip", str(target), "root ELEMENT form")
    assert result.returncode == 0
    assert open_questions.is_bare(open_questions.load_document(str(target)).questions[1])


def test_strip_matches_the_short_title_against_the_un_escaped_id(run_tool, milestone_dir):
    target = milestone_dir("entities")
    before = document_of(target)
    escaped = run_tool("strip", str(target), "Ampersand &amp; angle &lt;brackets&gt;, &quot;quotes&quot;, &apos;apostrophes&apos;")
    assert escaped.returncode == 1
    assert document_of(target) == before
    un_escaped = run_tool("strip", str(target), "ampersand & ANGLE <brackets>, \"quotes\", 'apostrophes'")
    assert un_escaped.returncode == 0
    assert open_questions.is_bare(open_questions.load_document(str(target)).questions[0])


def test_strip_of_a_bare_block_does_nothing(run_tool, milestone_dir):
    target = milestone_dir("bare")
    document = target / open_questions.DOCUMENT_NAME
    before = document.read_bytes()
    stat_before = document.stat()
    result = run_tool("strip", str(target), "First bare question", "Second bare question")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert document.read_bytes() == before
    assert document.stat().st_ino == stat_before.st_ino
    assert document.stat().st_mtime_ns == stat_before.st_mtime_ns


def test_strip_of_a_bare_block_beside_an_annotated_one_strips_only_the_annotated(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = read_fixture("annotated")
    result = run_tool("strip", str(target), "Fixture bare block", "Root element form")
    assert result.returncode == 0
    after = document_of(target).decode("utf-8")
    assert block_lines(after, "Fixture bare block") == block_lines(before, "Fixture bare block")
    assert block_lines(after, "Escape hatch under sole writer") == block_lines(before, "Escape hatch under sole writer")
    assert block_lines(after, "Root element form") == bare_block(
        "Root element form", "Is the empty document a self-closing root or an open and close tag pair?"
    )


def test_strip_of_an_unknown_id_fails_naming_the_ids_the_document_holds(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = document_of(target)
    result = run_tool("strip", str(target), "Missing question")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.decode("utf-8") == (
        'Error: no <open-question> block has the id "Missing question"; the document holds '
        '"Escape hatch under sole writer", "Root element form", "Fixture bare block"\n'
    )
    assert document_of(target) == before


def test_strip_with_one_unknown_id_among_known_ones_strips_nothing(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = document_of(target)
    result = run_tool("strip", str(target), "Root element form", "Missing", "Escape hatch under sole writer")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.startswith(b'Error: no <open-question> block has the id "Missing"')
    assert result.stderr.count(b"\n") == 1
    assert document_of(target) == before


def test_strip_on_an_empty_document_fails_saying_it_holds_no_blocks(run_tool, milestone_dir):
    target = milestone_dir("empty")
    result = run_tool("strip", str(target), "Anything")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == b'Error: no <open-question> block has the id "Anything"; the document holds no blocks\n'
    assert document_of(target) == b"<open-questions/>\n"


def test_strip_requires_at_least_one_short_title(run_tool, milestone_dir):
    result = run_tool("strip", str(milestone_dir("annotated")))
    assert result.returncode == 2
    assert result.stdout == b""
    assert b"SHORT_TITLE" in result.stderr


def test_strip_fails_when_the_document_is_missing(run_tool, tmp_path):
    result = run_tool("strip", str(tmp_path), "Anything")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == f"Error: {tmp_path / open_questions.DOCUMENT_NAME} does not exist\n".encode("utf-8")
    assert list(tmp_path.iterdir()) == []


def test_strip_fails_on_a_malformed_document_and_leaves_it_unchanged(run_tool, tmp_path):
    document = tmp_path / open_questions.DOCUMENT_NAME
    document.write_text("<open-questions>", encoding="utf-8")
    result = run_tool("strip", str(tmp_path), "Anything")
    assert result.returncode == 1
    assert result.stdout == b""
    assert b"not well-formed XML" in result.stderr
    assert result.stderr.count(b"\n") == 1
    assert document.read_text(encoding="utf-8") == "<open-questions>"


def test_strip_leaves_no_temporary_file_behind(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    run_tool("strip", str(target), "Root element form")
    run_tool("strip", str(target), "Missing")
    assert sorted(path.name for path in target.iterdir()) == [open_questions.DOCUMENT_NAME]


def test_main_strips_in_process_silently(capsys, milestone_dir):
    target = milestone_dir("annotated")
    assert open_questions.main(["strip", str(target), "Escape hatch under sole writer"]) == 0
    assert capsys.readouterr() == ("", "")
    assert open_questions.is_bare(open_questions.load_document(str(target)).questions[0])


def test_strip_question_is_the_per_block_primitive_and_reports_whether_it_changed_anything():
    question = Question(
        id="Annotated",
        question="What?",
        alternatives=[Alternative(id="A", text="a", advantages=["+"], drawbacks=["-"])],
        principles=["P"],
        depends_on=[Dependency(question="Other", option="O")],
        recommendation=Recommendation(option="A", rationale="because"),
    )
    assert not open_questions.is_bare(question)
    assert open_questions.strip_question(question) is True
    assert question == Question(id="Annotated", question="What?")
    assert open_questions.is_bare(question)
    assert open_questions.strip_question(question) is False
    assert question == Question(id="Annotated", question="What?")


@pytest.mark.parametrize(
    "children",
    [
        {"alternatives": [Alternative(id="A", text="a")]},
        {"principles": ["P"]},
        {"depends_on": [Dependency(question="Other", option="O")]},
        {"recommendation": Recommendation(option="A")},
    ],
)
def test_strip_question_treats_any_single_child_as_something_to_strip(children):
    question = Question(id="One child", question="What?", **children)
    assert not open_questions.is_bare(question)
    assert open_questions.strip_question(question) is True
    assert question == Question(id="One child", question="What?")


# --- strip --recommendation: the recommendation half alone -----------------------------


RECOMMENDATION_HALF = ("<applied-principle>", "<depends-on ", "<recommendation ")


def without_recommendation_half(lines):
    """The block lines with every <applied-principle>, <depends-on>, and <recommendation> line
    removed — what strip --recommendation leaves of a block."""
    return [line for line in lines if not line.lstrip().startswith(RECOMMENDATION_HALF)]


def test_strip_recommendation_keeps_the_alternatives_and_deletes_the_rest(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = open_questions.load_document(str(target)).questions[1]
    assert before.alternatives and before.principles and before.depends_on and before.recommendation is not None
    result = run_tool("strip", str(target), "--recommendation", "Root element form")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    after = open_questions.load_document(str(target)).questions[1]
    assert after == Question(id=before.id, question=before.question, alternatives=before.alternatives)
    assert not open_questions.is_bare(after)
    block = block_lines(document_of(target).decode("utf-8"), "Root element form")
    assert block == without_recommendation_half(block_lines(read_fixture("annotated"), "Root element form"))
    assert sum(line.startswith('    <alternative id="') for line in block) == 2
    assert not any(line.lstrip().startswith(RECOMMENDATION_HALF) for line in block)


def test_strip_recommendation_deletes_the_three_kinds_and_keeps_the_escaped_alternative(run_tool, milestone_dir):
    target = milestone_dir("entities")
    result = run_tool("strip", str(target), "--recommendation", ENTITIES_TITLE)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert document_of(target).decode("utf-8") == (
        "<open-questions>\n"
        '  <open-question id="Ampersand &amp; angle &lt;brackets&gt;, &quot;quotes&quot;, &apos;apostrophes&apos;">\n'
        "    <question>Does text with &amp;, &lt;tag&gt;, &quot;double&quot; and &apos;single&apos; quotes survive a round trip?</question>\n"
        '    <alternative id="A &amp; B">\n'
        "      What &lt;it&gt; is &amp; isn&apos;t, &quot;quoted&quot;.\n"
        "      <advantage>Keeps &amp;, &lt;, &gt;, &quot;, and &apos; escaped in text.</advantage>\n"
        "      <drawback>Every apostrophe is stored as &apos;.</drawback>\n"
        "    </alternative>\n"
        "  </open-question>\n"
        "</open-questions>\n"
    )


def test_strip_recommendation_touches_no_dependent_and_no_depends_on_tag_naming_the_block(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = read_fixture("annotated")
    result = run_tool("strip", str(target), "--recommendation", "Escape hatch under sole writer")
    assert result.returncode == 0
    after = document_of(target).decode("utf-8")
    dependent = block_lines(after, "Root element form")
    assert dependent == block_lines(before, "Root element form")
    assert '    <depends-on question="Escape hatch under sole writer" option="Strip subcommand"/>' in dependent
    assert block_lines(after, "Fixture bare block") == block_lines(before, "Fixture bare block")


def test_strip_recommendation_keeps_every_other_line_of_the_document(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = read_fixture("annotated")
    run_tool("strip", str(target), "--recommendation", "Escape hatch under sole writer")
    stripped = block_lines(before, "Escape hatch under sole writer")
    expected = before.replace("\n".join(stripped), "\n".join(without_recommendation_half(stripped)))
    assert document_of(target).decode("utf-8") == expected


def test_strip_recommendation_keeps_the_document_canonical(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    run_tool("strip", str(target), "--recommendation", "Root element form")
    text = document_of(target).decode("utf-8")
    assert open_questions.render_document(open_questions.parse_document(text)) == text


def test_strip_recommendation_of_several_blocks_strips_each(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = open_questions.load_document(str(target))
    result = run_tool("strip", str(target), "--recommendation", "Root element form", "Escape hatch under sole writer")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    document = open_questions.load_document(str(target))
    assert [question.id for question in document.questions] == [question.id for question in before.questions]
    for held, question in zip(before.questions, document.questions):
        assert question.alternatives == held.alternatives
        assert (question.principles, question.depends_on, question.recommendation) == ([], [], None)
    assert run_tool("list", str(target), "--unannotated").stdout == (
        b"Escape hatch under sole writer\nRoot element form\nFixture bare block\n"
    )


def test_strip_recommendation_accepts_the_flag_in_any_position(run_tool, milestone_dir):
    documents = []
    for arguments in (
        ("--recommendation", "{dir}", "Root element form", "Escape hatch under sole writer"),
        ("{dir}", "--recommendation", "Root element form", "Escape hatch under sole writer"),
        ("{dir}", "Root element form", "Escape hatch under sole writer", "--recommendation"),
    ):
        target = milestone_dir("annotated")
        result = run_tool("strip", *(argument.format(dir=str(target)) for argument in arguments))
        assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
        documents.append(document_of(target))
        (target / open_questions.DOCUMENT_NAME).unlink()
        target.rmdir()
    assert documents[0] == documents[1] == documents[2]
    assert b"<recommendation" not in documents[0]
    assert b"<alternative" in documents[0]


def test_strip_recommendation_of_a_block_carrying_only_alternatives_does_nothing(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    document = target / open_questions.DOCUMENT_NAME
    assert run_tool("strip", str(target), "--recommendation", "Root element form").returncode == 0
    before = document.read_bytes()
    stat_before = document.stat()
    result = run_tool("strip", str(target), "--recommendation", "Root element form", "Fixture bare block")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert document.read_bytes() == before
    assert document.stat().st_ino == stat_before.st_ino
    assert document.stat().st_mtime_ns == stat_before.st_mtime_ns


def test_strip_recommendation_of_a_bare_block_does_nothing(run_tool, milestone_dir):
    target = milestone_dir("bare")
    document = target / open_questions.DOCUMENT_NAME
    before = document.read_bytes()
    stat_before = document.stat()
    result = run_tool("strip", str(target), "--recommendation", "First bare question", "Second bare question")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert document.read_bytes() == before
    assert document.stat().st_ino == stat_before.st_ino
    assert document.stat().st_mtime_ns == stat_before.st_mtime_ns


def test_strip_recommendation_of_an_unknown_id_fails_naming_the_ids_the_document_holds(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = document_of(target)
    result = run_tool("strip", str(target), "--recommendation", "Root element form", "Missing question")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.decode("utf-8") == (
        'Error: no <open-question> block has the id "Missing question"; the document holds '
        '"Escape hatch under sole writer", "Root element form", "Fixture bare block"\n'
    )
    assert document_of(target) == before


def test_bare_strip_after_strip_recommendation_clears_the_alternatives_too(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    assert run_tool("strip", str(target), "--recommendation", "Root element form").returncode == 0
    assert not open_questions.is_bare(open_questions.load_document(str(target)).questions[1])
    result = run_tool("strip", str(target), "Root element form")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert block_lines(document_of(target).decode("utf-8"), "Root element form") == bare_block(
        "Root element form", "Is the empty document a self-closing root or an open and close tag pair?"
    )


def test_main_strips_the_recommendation_half_in_process_silently(capsys, milestone_dir):
    target = milestone_dir("annotated")
    assert open_questions.main(["strip", str(target), "--recommendation", "Escape hatch under sole writer"]) == 0
    assert capsys.readouterr() == ("", "")
    question = open_questions.load_document(str(target)).questions[0]
    assert question.recommendation is None and not question.depends_on and not question.principles
    assert len(question.alternatives) == 3


def test_strip_recommendation_is_the_per_block_primitive_and_reports_whether_it_changed_anything():
    alternatives = [Alternative(id="A", text="a", advantages=["+"], drawbacks=["-"])]
    question = Question(
        id="Annotated",
        question="What?",
        alternatives=list(alternatives),
        principles=["P"],
        depends_on=[Dependency(question="Other", option="O")],
        recommendation=Recommendation(option="A", rationale="because"),
    )
    assert open_questions.strip_recommendation(question) is True
    assert question == Question(id="Annotated", question="What?", alternatives=alternatives)
    assert not open_questions.is_bare(question)
    assert open_questions.strip_recommendation(question) is False
    assert question == Question(id="Annotated", question="What?", alternatives=alternatives)
    assert open_questions.strip_question(question) is True
    assert question == Question(id="Annotated", question="What?")


@pytest.mark.parametrize(
    "children",
    [
        {"principles": ["P"]},
        {"depends_on": [Dependency(question="Other", option="O")]},
        {"recommendation": Recommendation(option="A")},
    ],
)
def test_strip_recommendation_treats_any_single_child_of_its_half_as_something_to_strip(children):
    question = Question(id="One child", question="What?", alternatives=[Alternative(id="A", text="a")], **children)
    assert open_questions.strip_recommendation(question) is True
    assert question == Question(id="One child", question="What?", alternatives=[Alternative(id="A", text="a")])


def test_strip_recommendation_leaves_a_block_carrying_only_alternatives_unchanged():
    question = Question(id="Alternatives only", question="What?", alternatives=[Alternative(id="A", text="a")])
    assert open_questions.strip_recommendation(question) is False
    assert question == Question(id="Alternatives only", question="What?", alternatives=[Alternative(id="A", text="a")])
