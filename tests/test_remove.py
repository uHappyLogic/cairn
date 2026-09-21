"""The remove subcommand: the named block deleted and its dependents reconciled before the
one write — with --option a dependent whose <depends-on> names the removed id with that same
option (un-escaped, case-folded) loses only the tag and every other dependent is stripped,
without it every dependent is stripped, both transitively over the dependents of a stripped
block — so no removal leaves a <depends-on> tag naming a removed or stripped block; an
--option naming none of the removed block's own <alternative> ids is refused with the
document unchanged."""

from pathlib import Path

import pytest

import open_questions
from open_questions import Alternative, Dependency, Document, Question, Recommendation

FIXTURES = Path(__file__).resolve().parent / "fixtures"
ENTITIES_TITLE = "Ampersand & angle <brackets>, \"quotes\", 'apostrophes'"
HATCH = "Escape hatch under sole writer"
ROOT_FORM = "Root element form"
BARE = "Fixture bare block"


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


def has_block(text, short_title):
    return f'  <open-question id="{open_questions.escape(short_title)}">' in text.split("\n")


def bare_block(short_title, question):
    return [
        f'  <open-question id="{open_questions.escape(short_title)}">',
        f"    <question>{open_questions.escape(question)}</question>",
        "  </open-question>",
    ]


def annotated(block_id, depends_on=(), option="A", alternatives=("A", "B")):
    """A fully annotated block whose <depends-on> tags are the (question, option) pairs given."""
    return Question(
        id=block_id,
        question=f"What about {block_id}?",
        alternatives=[
            Alternative(id=alternative_id, text=f"{alternative_id} is this", advantages=["+"], drawbacks=["-"])
            for alternative_id in alternatives
        ],
        principles=["A principle"],
        depends_on=[Dependency(question=target, option=assumed) for target, assumed in depends_on],
        recommendation=Recommendation(option=option, rationale=f"because of {block_id}"),
    )


def write_document(directory, *questions):
    directory.mkdir(parents=True, exist_ok=True)
    open_questions.save_document(str(directory), Document(list(questions)))
    return directory


def load(target):
    return open_questions.load_document(str(target))


def by_id(document, block_id):
    return open_questions.find_question(document, block_id)


def tags_naming(document, block_id):
    wanted = open_questions.id_key(block_id)
    return [
        (question.id, dependency.option)
        for question in document.questions
        for dependency in question.depends_on
        if open_questions.id_key(dependency.question) == wanted
    ]


# --- the removal itself ---------------------------------------------------------------


def test_remove_deletes_the_named_block_and_keeps_every_other_line(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = read_fixture("annotated")
    result = run_tool("remove", str(target), BARE)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    after = document_of(target).decode("utf-8")
    assert not has_block(after, BARE)
    assert after == before.replace("\n".join(block_lines(before, BARE)) + "\n", "")
    assert block_lines(after, HATCH) == block_lines(before, HATCH)
    assert block_lines(after, ROOT_FORM) == block_lines(before, ROOT_FORM)


def test_remove_of_the_last_block_leaves_the_empty_document(run_tool, milestone_dir):
    target = milestone_dir("entities")
    result = run_tool("remove", str(target), ENTITIES_TITLE)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert document_of(target) == b"<open-questions/>\n"


def test_remove_matches_the_short_title_case_folded_and_un_escaped(run_tool, milestone_dir):
    target = milestone_dir("entities")
    before = document_of(target)
    escaped = run_tool("remove", str(target), "Ampersand &amp; angle &lt;brackets&gt;, &quot;quotes&quot;, &apos;apostrophes&apos;")
    assert escaped.returncode == 1
    assert document_of(target) == before
    un_escaped = run_tool("remove", str(target), "ampersand & ANGLE <brackets>, \"quotes\", 'apostrophes'")
    assert (un_escaped.returncode, un_escaped.stdout, un_escaped.stderr) == (0, b"", b"")
    assert load(target) == Document()


def test_remove_keeps_the_document_canonical(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    run_tool("remove", str(target), HATCH, "--option", "Strip subcommand")
    text = document_of(target).decode("utf-8")
    assert open_questions.render_document(open_questions.parse_document(text)) == text


def test_remove_with_an_option_and_no_dependents_just_deletes_the_block(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = read_fixture("annotated")
    result = run_tool("remove", str(target), ROOT_FORM, "--option", "Self-closing root")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    after = document_of(target).decode("utf-8")
    assert not has_block(after, ROOT_FORM)
    assert block_lines(after, HATCH) == block_lines(before, HATCH)
    assert block_lines(after, BARE) == block_lines(before, BARE)


# --- tag-drop: the dependent assumed the recorded option ------------------------------


def test_remove_with_the_recorded_option_drops_only_the_agreeing_tag(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = read_fixture("annotated")
    result = run_tool("remove", str(target), HATCH, "--option", "Strip subcommand")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    after = document_of(target).decode("utf-8")
    assert not has_block(after, HATCH)
    tag = '    <depends-on question="Escape hatch under sole writer" option="Strip subcommand"/>'
    expected = [line for line in block_lines(before, ROOT_FORM) if line != tag]
    assert tag in block_lines(before, ROOT_FORM)
    assert block_lines(after, ROOT_FORM) == expected
    dependent = by_id(load(target), ROOT_FORM)
    assert [alternative.id for alternative in dependent.alternatives] == ["Self-closing root", "Open and close pair"]
    assert dependent.principles == ["One rule over two", "Prefer the writer's invariant"]
    assert dependent.depends_on == []
    assert dependent.recommendation == Recommendation(
        option="Self-closing root",
        rationale="The serializer already writes every empty element self-closing, and the root is an "
        "element like any other; a second rule for one tag buys a slightly prettier first diff at the "
        "cost of a special case in the one place the format is defined.",
    )
    assert block_lines(after, BARE) == block_lines(before, BARE)


def test_remove_compares_the_recorded_option_case_folded(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    result = run_tool("remove", str(target), HATCH, "--option", "strip SUBCOMMAND")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    dependent = by_id(load(target), ROOT_FORM)
    assert dependent.depends_on == []
    assert dependent.recommendation is not None


def test_remove_compares_the_recorded_option_against_the_un_escaped_tag_option(run_tool, tmp_path):
    option = "A & \"B\" <c> 'd'"
    target = write_document(
        tmp_path / "m",
        annotated("Target", option=option, alternatives=(option, "Plain")),
        annotated("Dependent", depends_on=[("Target", option)]),
    )
    assert f'option="{open_questions.escape(option)}"' in document_of(target).decode("utf-8")
    result = run_tool("remove", str(target), "Target", "--option", option)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    dependent = by_id(load(target), "Dependent")
    assert dependent.depends_on == []
    assert dependent.recommendation is not None
    assert dependent.alternatives and dependent.principles


def test_remove_keeps_the_agreeing_dependents_tags_naming_other_blocks(run_tool, tmp_path):
    target = write_document(
        tmp_path / "m",
        annotated("Target"),
        annotated("Other"),
        annotated("Dependent", depends_on=[("Target", "A"), ("Other", "B")]),
    )
    result = run_tool("remove", str(target), "Target", "--option", "A")
    assert result.returncode == 0
    dependent = by_id(load(target), "Dependent")
    assert dependent.depends_on == [Dependency(question="Other", option="B")]
    assert dependent.recommendation is not None


def test_remove_drops_every_agreeing_tag_a_dependent_carries_for_the_removed_block(run_tool, tmp_path):
    target = write_document(
        tmp_path / "m",
        annotated("Target"),
        annotated("Dependent", depends_on=[("Target", "A"), ("target", "a")]),
    )
    result = run_tool("remove", str(target), "Target", "--option", "A")
    assert result.returncode == 0
    dependent = by_id(load(target), "Dependent")
    assert dependent.depends_on == []
    assert dependent.recommendation is not None


# --- strip-all: no option, a differing option, or doubt --------------------------------


def test_remove_without_an_option_strips_every_dependent(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = read_fixture("annotated")
    result = run_tool("remove", str(target), HATCH)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    after = document_of(target).decode("utf-8")
    assert not has_block(after, HATCH)
    assert block_lines(after, ROOT_FORM) == bare_block(
        ROOT_FORM, "Is the empty document a self-closing root or an open and close tag pair?"
    )
    assert block_lines(after, BARE) == block_lines(before, BARE)
    assert after == (
        "<open-questions>\n"
        + "\n".join(bare_block(ROOT_FORM, "Is the empty document a self-closing root or an open and close tag pair?"))
        + "\n"
        + "\n".join(block_lines(before, BARE))
        + "\n</open-questions>\n"
    )


def test_remove_with_a_differing_option_strips_the_dependent(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    result = run_tool("remove", str(target), HATCH, "--option", "Documented hand-edit exception")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    document = load(target)
    assert [question.id for question in document.questions] == [ROOT_FORM, BARE]
    assert open_questions.is_bare(by_id(document, ROOT_FORM))


def test_remove_strips_a_dependent_carrying_both_an_agreeing_and_a_differing_tag(run_tool, tmp_path):
    target = write_document(
        tmp_path / "m",
        annotated("Target"),
        annotated("Dependent", depends_on=[("Target", "A"), ("Target", "B")]),
    )
    result = run_tool("remove", str(target), "Target", "--option", "A")
    assert result.returncode == 0
    assert open_questions.is_bare(by_id(load(target), "Dependent"))


def test_remove_without_an_option_strips_several_dependents_and_no_other_block(run_tool, tmp_path):
    target = write_document(
        tmp_path / "m",
        annotated("Target"),
        annotated("First dependent", depends_on=[("Target", "A")]),
        annotated("Bystander", depends_on=[("Somebody else", "A")]),
        annotated("Second dependent", depends_on=[("TARGET", "B")]),
    )
    before = document_of(target).decode("utf-8")
    result = run_tool("remove", str(target), "Target")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    after = document_of(target).decode("utf-8")
    document = load(target)
    assert [question.id for question in document.questions] == ["First dependent", "Bystander", "Second dependent"]
    assert open_questions.is_bare(by_id(document, "First dependent"))
    assert open_questions.is_bare(by_id(document, "Second dependent"))
    assert block_lines(after, "Bystander") == block_lines(before, "Bystander")


def test_remove_uses_the_strip_primitive_so_a_stripped_dependent_is_the_bare_block(run_tool, tmp_path):
    target = write_document(tmp_path / "m", annotated("Target"), annotated("Dependent", depends_on=[("Target", "A")]))
    run_tool("remove", str(target), "Target")
    assert block_lines(document_of(target).decode("utf-8"), "Dependent") == bare_block("Dependent", "What about Dependent?")
    assert by_id(load(target), "Dependent") == Question(id="Dependent", question="What about Dependent?")


# --- transitive strip -----------------------------------------------------------------


def test_remove_strips_transitively_over_the_dependents_of_stripped_blocks(run_tool, tmp_path):
    target = write_document(
        tmp_path / "m",
        annotated("Root"),
        annotated("Child", depends_on=[("Root", "A")]),
        annotated("Grandchild", depends_on=[("Child", "A")]),
        annotated("Great-grandchild", depends_on=[("Grandchild", "B")]),
        annotated("Unrelated"),
    )
    before = document_of(target).decode("utf-8")
    result = run_tool("remove", str(target), "Root")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    document = load(target)
    assert [question.id for question in document.questions] == ["Child", "Grandchild", "Great-grandchild", "Unrelated"]
    for block_id in ("Child", "Grandchild", "Great-grandchild"):
        assert open_questions.is_bare(by_id(document, block_id)), block_id
    assert block_lines(document_of(target).decode("utf-8"), "Unrelated") == block_lines(before, "Unrelated")


def test_remove_with_an_agreeing_option_propagates_nothing_from_the_untagged_dependent(run_tool, tmp_path):
    target = write_document(
        tmp_path / "m",
        annotated("Root"),
        annotated("Child", depends_on=[("Root", "A")]),
        annotated("Grandchild", depends_on=[("Child", "B")]),
    )
    before = document_of(target).decode("utf-8")
    result = run_tool("remove", str(target), "Root", "--option", "A")
    assert result.returncode == 0
    after = document_of(target).decode("utf-8")
    document = load(target)
    child = by_id(document, "Child")
    assert child.depends_on == [] and child.recommendation is not None
    assert block_lines(after, "Grandchild") == block_lines(before, "Grandchild")
    assert by_id(document, "Grandchild").depends_on == [Dependency(question="Child", option="B")]


def test_remove_with_a_differing_option_propagates_the_strip(run_tool, tmp_path):
    target = write_document(
        tmp_path / "m",
        annotated("Root"),
        annotated("Child", depends_on=[("Root", "B")]),
        annotated("Grandchild", depends_on=[("Child", "A")]),
    )
    result = run_tool("remove", str(target), "Root", "--option", "A")
    assert result.returncode == 0
    document = load(target)
    assert open_questions.is_bare(by_id(document, "Child"))
    assert open_questions.is_bare(by_id(document, "Grandchild"))


def test_remove_strips_an_untagged_dependent_that_also_depends_on_a_stripped_block(run_tool, tmp_path):
    target = write_document(
        tmp_path / "m",
        annotated("Root"),
        annotated("Agreeing", depends_on=[("Root", "A"), ("Differing", "A")]),
        annotated("Differing", depends_on=[("Root", "B")]),
    )
    result = run_tool("remove", str(target), "Root", "--option", "A")
    assert result.returncode == 0
    document = load(target)
    assert open_questions.is_bare(by_id(document, "Differing"))
    assert open_questions.is_bare(by_id(document, "Agreeing"))


def test_remove_strips_a_block_reached_through_two_stripped_blocks_once(run_tool, tmp_path):
    target = write_document(
        tmp_path / "m",
        annotated("Root"),
        annotated("Left", depends_on=[("Root", "A")]),
        annotated("Right", depends_on=[("Root", "B")]),
        annotated("Join", depends_on=[("Left", "A"), ("Right", "A")]),
    )
    document = load(target)
    stripped = open_questions.remove_question(document, by_id(document, "Root"))
    assert stripped == ["Left", "Right", "Join"]
    assert all(open_questions.is_bare(question) for question in document.questions)


# --- cycles ---------------------------------------------------------------------------


def test_remove_terminates_on_a_cycle_among_the_dependents_and_strips_each_member(run_tool, tmp_path):
    target = write_document(
        tmp_path / "m",
        annotated("Root"),
        annotated("Ring one", depends_on=[("Root", "A"), ("Ring two", "A")]),
        annotated("Ring two", depends_on=[("Ring three", "B")]),
        annotated("Ring three", depends_on=[("Ring one", "A")]),
    )
    result = run_tool("remove", str(target), "Root")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    document = load(target)
    assert [question.id for question in document.questions] == ["Ring one", "Ring two", "Ring three"]
    assert all(open_questions.is_bare(question) for question in document.questions)


def test_remove_of_a_block_inside_a_cycle_strips_the_rest_of_the_cycle(run_tool, tmp_path):
    target = write_document(
        tmp_path / "m",
        annotated("Ring one", depends_on=[("Ring two", "A")]),
        annotated("Ring two", depends_on=[("Ring one", "A")]),
        annotated("Unrelated"),
    )
    before = document_of(target).decode("utf-8")
    result = run_tool("remove", str(target), "Ring one", "--option", "A")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    after = document_of(target).decode("utf-8")
    document = load(target)
    assert [question.id for question in document.questions] == ["Ring two", "Unrelated"]
    ring_two = by_id(document, "Ring two")
    assert ring_two.depends_on == [] and ring_two.recommendation is not None
    assert block_lines(after, "Unrelated") == block_lines(before, "Unrelated")


def test_remove_leaves_a_cycle_not_reachable_from_the_removed_block_alone(run_tool, tmp_path):
    target = write_document(
        tmp_path / "m",
        annotated("Target"),
        annotated("Ring one", depends_on=[("Ring two", "A")]),
        annotated("Ring two", depends_on=[("Ring one", "B")]),
    )
    before = document_of(target).decode("utf-8")
    result = run_tool("remove", str(target), "Target")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    after = document_of(target).decode("utf-8")
    assert block_lines(after, "Ring one") == block_lines(before, "Ring one")
    assert block_lines(after, "Ring two") == block_lines(before, "Ring two")


def test_remove_terminates_on_a_self_dependent_block(run_tool, tmp_path):
    target = write_document(
        tmp_path / "m",
        annotated("Target"),
        annotated("Narcissus", depends_on=[("Target", "B"), ("Narcissus", "A")]),
    )
    result = run_tool("remove", str(target), "Target", "--option", "A")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert open_questions.is_bare(by_id(load(target), "Narcissus"))


# --- no removal leaves a dangling tag --------------------------------------------------


@pytest.mark.parametrize(
    "arguments",
    [
        (HATCH,),
        (HATCH, "--option", "Strip subcommand"),
        (HATCH, "--option", "Documented hand-edit exception"),
        (ROOT_FORM,),
        (ROOT_FORM, "--option", "Open and close pair"),
        (BARE,),
    ],
)
def test_no_removal_on_the_annotated_fixture_leaves_a_dangling_tag(run_tool, milestone_dir, arguments):
    target = milestone_dir("annotated")
    before = load(target)
    result = run_tool("remove", str(target), *arguments)
    assert result.returncode == 0
    after = load(target)
    removed = arguments[0]
    assert tags_naming(after, removed) == []
    stripped = [
        question.id
        for question in after.questions
        if open_questions.is_bare(question) and not open_questions.is_bare(by_id(before, question.id))
    ]
    for block_id in stripped:
        assert tags_naming(after, block_id) == [], block_id


def test_no_removal_on_a_dependency_web_leaves_a_dangling_tag(tmp_path):
    def web():
        return Document(
            [
                annotated("Root"),
                annotated("A", depends_on=[("Root", "A")]),
                annotated("B", depends_on=[("Root", "B")]),
                annotated("C", depends_on=[("A", "A"), ("B", "A")]),
                annotated("D", depends_on=[("C", "B"), ("E", "A")]),
                annotated("E", depends_on=[("D", "A")]),
                annotated("F"),
            ]
        )

    for block_id in ("Root", "A", "B", "C", "D", "E", "F"):
        for recorded_option in (None, "A", "B"):
            document = web()
            before = web()
            open_questions.remove_question(document, by_id(document, block_id), recorded_option)
            assert by_id(before, block_id) is not None
            assert all(open_questions.id_key(question.id) != open_questions.id_key(block_id) for question in document.questions)
            assert tags_naming(document, block_id) == [], (block_id, recorded_option)
            for question in document.questions:
                if open_questions.is_bare(question) and not open_questions.is_bare(by_id(before, question.id)):
                    assert tags_naming(document, question.id) == [], (block_id, recorded_option, question.id)
            # The re-rendered document parses back to the same tree.
            text = open_questions.render_document(document)
            assert open_questions.parse_document(text) == document


# --- the rejected option ---------------------------------------------------------------


def test_remove_rejects_an_option_naming_none_of_the_blocks_alternatives(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = document_of(target)
    result = run_tool("remove", str(target), HATCH, "--option", "Missing option")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.decode("utf-8") == (
        'Error: --option "Missing option" names none of the <alternative> ids of <open-question id="Escape '
        'hatch under sole writer">, which are "Strip subcommand", "Documented hand-edit exception", '
        '"Strip behind a skill"\n'
    )
    assert document_of(target) == before


def test_remove_rejects_an_option_on_a_block_with_no_alternatives(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = document_of(target)
    result = run_tool("remove", str(target), BARE, "--option", "Anything")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == (
        b'Error: --option "Anything" was given, but <open-question id="Fixture bare block"> carries no '
        b"<alternative> elements\n"
    )
    assert document_of(target) == before


def test_remove_rejects_an_option_naming_a_dependents_option_rather_than_the_blocks_own(run_tool, milestone_dir):
    # "Self-closing root" is Root element form's alternative, not the escape hatch's.
    target = milestone_dir("annotated")
    before = document_of(target)
    result = run_tool("remove", str(target), HATCH, "--option", "Self-closing root")
    assert result.returncode == 1
    assert result.stderr.startswith(b'Error: --option "Self-closing root" names none of the <alternative> ids')
    assert document_of(target) == before


def test_remove_rejects_an_escaped_option_and_accepts_the_un_escaped_one(run_tool, milestone_dir):
    target = milestone_dir("entities")
    before = document_of(target)
    escaped = run_tool("remove", str(target), ENTITIES_TITLE, "--option", "A &amp; B")
    assert escaped.returncode == 1
    assert escaped.stderr.startswith(b'Error: --option "A &amp; B" names none of the <alternative> ids')
    assert document_of(target) == before
    un_escaped = run_tool("remove", str(target), ENTITIES_TITLE, "--option", "a & b")
    assert (un_escaped.returncode, un_escaped.stdout, un_escaped.stderr) == (0, b"", b"")
    assert document_of(target) == b"<open-questions/>\n"


def test_remove_rejects_an_empty_option(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = document_of(target)
    result = run_tool("remove", str(target), HATCH, "--option", "")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.startswith(b'Error: --option "" names none of the <alternative> ids')
    assert document_of(target) == before


def test_a_rejected_option_strips_nothing_even_with_dependents_present(run_tool, tmp_path):
    target = write_document(
        tmp_path / "m",
        annotated("Target"),
        annotated("Dependent", depends_on=[("Target", "A")]),
        annotated("Grandchild", depends_on=[("Dependent", "A")]),
    )
    before = document_of(target)
    result = run_tool("remove", str(target), "Target", "--option", "C")
    assert result.returncode == 1
    assert result.stderr.count(b"\n") == 1
    assert document_of(target) == before


# --- the other clean stops -------------------------------------------------------------


def test_remove_of_an_unknown_id_fails_naming_the_ids_the_document_holds(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = document_of(target)
    result = run_tool("remove", str(target), "Missing question")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.decode("utf-8") == (
        'Error: no <open-question> block has the id "Missing question"; the document holds '
        '"Escape hatch under sole writer", "Root element form", "Fixture bare block"\n'
    )
    assert document_of(target) == before


def test_remove_of_an_unknown_id_with_an_option_fails_on_the_id_first(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = document_of(target)
    result = run_tool("remove", str(target), "Missing question", "--option", "Whatever")
    assert result.returncode == 1
    assert result.stderr.startswith(b'Error: no <open-question> block has the id "Missing question"')
    assert document_of(target) == before


def test_remove_on_an_empty_document_fails_saying_it_holds_no_blocks(run_tool, milestone_dir):
    target = milestone_dir("empty")
    result = run_tool("remove", str(target), "Anything")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == b'Error: no <open-question> block has the id "Anything"; the document holds no blocks\n'
    assert document_of(target) == b"<open-questions/>\n"


def test_remove_takes_exactly_one_short_title(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = document_of(target)
    none = run_tool("remove", str(target))
    assert none.returncode == 2
    assert none.stdout == b""
    assert b"SHORT_TITLE" in none.stderr
    two = run_tool("remove", str(target), HATCH, ROOT_FORM)
    assert two.returncode == 2
    assert two.stdout == b""
    assert b"unrecognized arguments" in two.stderr
    assert document_of(target) == before


def test_remove_fails_when_the_document_is_missing(run_tool, tmp_path):
    result = run_tool("remove", str(tmp_path), "Anything")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == f"Error: {tmp_path / open_questions.DOCUMENT_NAME} does not exist\n".encode("utf-8")
    assert list(tmp_path.iterdir()) == []


def test_remove_fails_on_a_malformed_document_and_leaves_it_unchanged(run_tool, tmp_path):
    document = tmp_path / open_questions.DOCUMENT_NAME
    document.write_text("<open-questions>", encoding="utf-8")
    result = run_tool("remove", str(tmp_path), "Anything")
    assert result.returncode == 1
    assert result.stdout == b""
    assert b"not well-formed XML" in result.stderr
    assert result.stderr.count(b"\n") == 1
    assert document.read_text(encoding="utf-8") == "<open-questions>"


def test_remove_leaves_no_temporary_file_behind(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    run_tool("remove", str(target), HATCH, "--option", "Strip subcommand")
    run_tool("remove", str(target), ROOT_FORM, "--option", "Missing")
    run_tool("remove", str(target), "Missing")
    assert sorted(path.name for path in target.iterdir()) == [open_questions.DOCUMENT_NAME]


# --- the single write ------------------------------------------------------------------


def test_remove_writes_the_document_exactly_once(monkeypatch, milestone_dir):
    target = milestone_dir("annotated")
    writes = []
    real_save = open_questions.save_document

    def counting_save(milestone_dir, document):
        writes.append(open_questions.render_document(document))
        real_save(milestone_dir, document)

    monkeypatch.setattr(open_questions, "save_document", counting_save)
    assert open_questions.main(["remove", str(target), HATCH]) == 0
    assert len(writes) == 1
    assert writes[0].encode("utf-8") == document_of(target)
    assert open_questions.is_bare(by_id(open_questions.parse_document(writes[0]), ROOT_FORM))


def test_a_rejected_option_never_reaches_the_write(monkeypatch, milestone_dir, capsys):
    target = milestone_dir("annotated")
    before = document_of(target)
    writes = []
    monkeypatch.setattr(open_questions, "save_document", lambda *arguments: writes.append(arguments))
    assert open_questions.main(["remove", str(target), HATCH, "--option", "Missing"]) == 1
    assert writes == []
    assert capsys.readouterr().out == ""
    assert document_of(target) == before


def test_main_removes_in_process_silently(capsys, milestone_dir):
    target = milestone_dir("annotated")
    assert open_questions.main(["remove", str(target), HATCH, "--option", "Strip subcommand"]) == 0
    assert capsys.readouterr() == ("", "")
    document = load(target)
    assert [question.id for question in document.questions] == [ROOT_FORM, BARE]
    assert by_id(document, ROOT_FORM).depends_on == []


# --- the module-level primitives -------------------------------------------------------


def test_remove_question_deletes_the_block_and_returns_the_stripped_ids_in_order():
    document = Document(
        [
            annotated("Root"),
            annotated("Agreeing", depends_on=[("Root", "A")]),
            annotated("Differing", depends_on=[("Root", "B")]),
            annotated("Downstream", depends_on=[("Differing", "A")]),
        ]
    )
    stripped = open_questions.remove_question(document, by_id(document, "Root"), "A")
    assert stripped == ["Differing", "Downstream"]
    assert [question.id for question in document.questions] == ["Agreeing", "Differing", "Downstream"]
    agreeing = by_id(document, "Agreeing")
    assert agreeing.depends_on == [] and agreeing.recommendation is not None
    assert open_questions.is_bare(by_id(document, "Differing"))
    assert open_questions.is_bare(by_id(document, "Downstream"))


def test_remove_question_without_an_option_strips_every_dependent_and_returns_them():
    document = Document([annotated("Root"), annotated("One", depends_on=[("Root", "A")]), annotated("Two", depends_on=[("ROOT", "A")])])
    assert open_questions.remove_question(document, by_id(document, "Root")) == ["One", "Two"]
    assert all(open_questions.is_bare(question) for question in document.questions)


def test_remove_question_with_no_dependents_strips_nothing():
    document = Document([annotated("Root"), annotated("Other")])
    assert open_questions.remove_question(document, by_id(document, "Root"), "A") == []
    assert document == Document([annotated("Other")])


def test_dependents_of_matches_the_question_attribute_case_folded_in_document_order():
    document = Document(
        [
            annotated("Target"),
            annotated("Second", depends_on=[("TARGET", "A")]),
            annotated("Bystander", depends_on=[("Other", "A")]),
            annotated("First", depends_on=[("target", "B")]),
        ]
    )
    assert [question.id for question in open_questions.dependents_of(document, "Target")] == ["Second", "First"]
    assert open_questions.dependents_of(document, "Nobody") == []


def test_check_recorded_option_accepts_the_blocks_own_alternatives_only():
    question = annotated("Target", alternatives=("Keep it", "Drop it"))
    assert open_questions.check_recorded_option(question, "keep IT") is None
    with pytest.raises(open_questions.ToolError) as missing:
        open_questions.check_recorded_option(question, "Something else")
    assert str(missing.value) == (
        '--option "Something else" names none of the <alternative> ids of <open-question id="Target">, '
        'which are "Keep it", "Drop it"'
    )
    with pytest.raises(open_questions.ToolError) as bare:
        open_questions.check_recorded_option(Question(id="Bare", question="What?"), "Anything")
    assert str(bare.value) == '--option "Anything" was given, but <open-question id="Bare"> carries no <alternative> elements'
