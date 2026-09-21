"""The lift subcommand: one line of answer text, "<option> — <rationale>" from the block's
<recommendation> or "<id> — <what-it-is>" from a named <alternative>, un-escaped."""

import pytest

import open_questions
from open_questions import Alternative, Document, Question, Recommendation

ENTITIES_TITLE = "Ampersand & angle <brackets>, \"quotes\", 'apostrophes'"


def test_lift_prints_the_recommendation_as_option_em_dash_rationale(run_tool, milestone_dir):
    result = run_tool("lift", str(milestone_dir("annotated")), "Root element form")
    assert (result.returncode, result.stderr) == (0, b"")
    assert result.stdout.decode("utf-8") == (
        "Self-closing root — The serializer already writes every empty element self-closing, and the "
        "root is an element like any other; a second rule for one tag buys a slightly prettier first "
        "diff at the cost of a special case in the one place the format is defined.\n"
    )


def test_lift_prints_exactly_one_line(run_tool, milestone_dir):
    result = run_tool("lift", str(milestone_dir("annotated")), "Escape hatch under sole writer")
    assert result.returncode == 0
    text = result.stdout.decode("utf-8")
    assert text.count("\n") == 1 and text.endswith("\n")
    assert text.startswith("Strip subcommand — The goal gives the tool every deterministic edit")


def test_lift_un_escapes_the_option_and_the_rationale(run_tool, milestone_dir):
    result = run_tool("lift", str(milestone_dir("entities")), ENTITIES_TITLE)
    assert (result.returncode, result.stderr) == (0, b"")
    assert result.stdout.decode("utf-8") == "A & B — One rule for text & attributes: <, >, \", '.\n"


def test_lift_alternative_prints_id_em_dash_what_it_is(run_tool, milestone_dir):
    result = run_tool("lift", str(milestone_dir("annotated")), "Root element form", "--alternative", "Open and close pair")
    assert (result.returncode, result.stderr) == (0, b"")
    assert result.stdout.decode("utf-8") == (
        "Open and close pair — A two-line `<open-questions>` … `</open-questions>` document with "
        "nothing between the tags.\n"
    )


def test_lift_alternative_excludes_the_advantage_and_drawback_children(run_tool, milestone_dir):
    result = run_tool("lift", str(milestone_dir("annotated")), "Root element form", "--alternative", "Self-closing root")
    text = result.stdout.decode("utf-8")
    assert text == (
        "Self-closing root — The one rule for an element that holds nothing & needs no body: write it "
        "as `<open-questions/>`.\n"
    )
    assert "One serializer rule covers the root" not in text
    assert "rewrites the root line" not in text


def test_lift_alternative_un_escapes_the_id_and_the_what_it_is_text(run_tool, milestone_dir):
    result = run_tool("lift", str(milestone_dir("entities")), ENTITIES_TITLE, "--alternative", "A & B")
    assert (result.returncode, result.stderr) == (0, b"")
    assert result.stdout.decode("utf-8") == "A & B — What <it> is & isn't, \"quoted\".\n"


def test_lift_matches_the_short_title_case_folded(run_tool, milestone_dir):
    target = str(milestone_dir("annotated"))
    assert run_tool("lift", target, "ROOT ELEMENT FORM").stdout == run_tool("lift", target, "Root element form").stdout
    assert run_tool("lift", target, "ROOT ELEMENT FORM").returncode == 0


def test_lift_alternative_matches_case_folded_and_prints_the_stored_id(run_tool, milestone_dir):
    result = run_tool("lift", str(milestone_dir("annotated")), "root ELEMENT form", "--alternative", "OPEN and close PAIR")
    assert result.returncode == 0
    assert result.stdout.decode("utf-8").startswith("Open and close pair — A two-line")


def test_lift_compares_ids_un_escaped_not_as_stored(run_tool, milestone_dir):
    target = str(milestone_dir("entities"))
    assert run_tool("lift", target, ENTITIES_TITLE, "--alternative", "a & b").returncode == 0
    assert run_tool("lift", target, ENTITIES_TITLE, "--alternative", "A &amp; B").returncode == 1


def test_lift_fails_when_the_block_carries_no_recommendation(run_tool, milestone_dir):
    result = run_tool("lift", str(milestone_dir("annotated")), "Fixture bare block")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == b'Error: <open-question id="Fixture bare block"> carries no <recommendation> element\n'


def test_lift_fails_when_no_block_has_the_id_naming_the_ids_the_document_holds(run_tool, milestone_dir):
    result = run_tool("lift", str(milestone_dir("annotated")), "Missing question")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.decode("utf-8") == (
        'Error: no <open-question> block has the id "Missing question"; the document holds '
        '"Escape hatch under sole writer", "Root element form", "Fixture bare block"\n'
    )


def test_lift_alternative_fails_when_no_block_has_the_id(run_tool, milestone_dir):
    result = run_tool("lift", str(milestone_dir("bare")), "Missing", "--alternative", "X")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.startswith(b'Error: no <open-question> block has the id "Missing"')


def test_lift_alternative_fails_when_the_block_carries_no_alternatives(run_tool, milestone_dir):
    result = run_tool("lift", str(milestone_dir("bare")), "First bare question", "--alternative", "Anything")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == b'Error: <open-question id="First bare question"> carries no <alternative> elements\n'


def test_lift_alternative_fails_when_no_alternative_matches_naming_the_ids_it_carries(run_tool, milestone_dir):
    result = run_tool("lift", str(milestone_dir("annotated")), "Root element form", "--alternative", "Third way")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.decode("utf-8") == (
        'Error: <open-question id="Root element form"> has no <alternative> with the id "Third way"; '
        'its alternatives are "Self-closing root", "Open and close pair"\n'
    )


def test_lift_on_an_empty_document_fails_saying_it_holds_no_blocks(run_tool, milestone_dir):
    result = run_tool("lift", str(milestone_dir("empty")), "Anything")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == b'Error: no <open-question> block has the id "Anything"; the document holds no blocks\n'


def test_lift_fails_when_the_document_is_missing(run_tool, tmp_path):
    result = run_tool("lift", str(tmp_path), "Anything")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == f"Error: {tmp_path / open_questions.DOCUMENT_NAME} does not exist\n".encode("utf-8")


def test_lift_requires_a_short_title(run_tool, milestone_dir):
    result = run_tool("lift", str(milestone_dir("bare")))
    assert result.returncode == 2
    assert result.stdout == b""
    assert b"SHORT_TITLE" in result.stderr


def test_lift_alternative_requires_a_value(run_tool, milestone_dir):
    result = run_tool("lift", str(milestone_dir("annotated")), "Root element form", "--alternative")
    assert result.returncode == 2
    assert result.stdout == b""
    assert b"--alternative" in result.stderr


def test_lift_leaves_the_document_unchanged(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    document = target / open_questions.DOCUMENT_NAME
    before = document.read_bytes()
    run_tool("lift", str(target), "Root element form")
    run_tool("lift", str(target), "Root element form", "--alternative", "Open and close pair")
    run_tool("lift", str(target), "Fixture bare block")
    run_tool("lift", str(target), "Root element form", "--alternative", "Missing")
    assert document.read_bytes() == before
    assert sorted(path.name for path in target.iterdir()) == [open_questions.DOCUMENT_NAME]


def test_lift_omits_the_dash_when_the_text_is_empty(capsys, tmp_path):
    document = Document(
        [
            Question(
                "Q",
                "Why?",
                alternatives=[Alternative("Only", "", advantages=["Fast"])],
                recommendation=Recommendation("Only", ""),
            )
        ]
    )
    open_questions.save_document(str(tmp_path), document)
    assert open_questions.main(["lift", str(tmp_path), "Q"]) == 0
    assert capsys.readouterr().out == "Only\n"
    assert open_questions.main(["lift", str(tmp_path), "Q", "--alternative", "only"]) == 0
    assert capsys.readouterr().out == "Only\n"


def test_find_alternative_is_case_folded_and_names_the_ids_on_a_miss():
    question = Question("Q", "Why?", alternatives=[Alternative("First", "a"), Alternative("Second", "b")])
    assert open_questions.find_alternative(question, "SECOND") is question.alternatives[1]
    with pytest.raises(open_questions.ToolError) as info:
        open_questions.find_alternative(question, "Third")
    assert str(info.value) == '<open-question id="Q"> has no <alternative> with the id "Third"; its alternatives are "First", "Second"'
    with pytest.raises(open_questions.ToolError) as info:
        open_questions.find_alternative(Question("R", "Why?"), "Any")
    assert str(info.value) == '<open-question id="R"> carries no <alternative> elements'
