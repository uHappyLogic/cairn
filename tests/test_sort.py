"""The sort subcommand: the document rewritten with the blocks carrying a <recommendation>
first, in exactly walk's order, and every block carrying none last in its prior document
order — so afterwards walk prints exactly the annotated prefix of list; the identity on a
document already in that order (every golden fixture included), idempotent, silent on
success, one Error line with the document untouched on failure, and the one subcommand that
reorders blocks: render_document and every other write keep the order they were given."""

from pathlib import Path

import pytest

import open_questions
from open_questions import Alternative, Dependency, Document, Question, Recommendation

FIXTURES = Path(__file__).resolve().parent / "fixtures"
FIXTURE_NAMES = sorted(path.name for path in FIXTURES.iterdir() if path.is_dir())
HATCH = "Escape hatch under sole writer"
ROOT_FORM = "Root element form"
BARE = "Fixture bare block"


def annotated(block_id, depends_on=(), option="A"):
    """An annotated block whose <depends-on> tags name the given targets, each assuming "A"."""
    return Question(
        id=block_id,
        question=f"What about {block_id}?",
        alternatives=[Alternative(id=alternative_id, text=f"{alternative_id} is this") for alternative_id in ("A", "B")],
        depends_on=[Dependency(question=target, option="A") for target in depends_on],
        recommendation=Recommendation(option=option, rationale=f"because of {block_id}"),
    )


def bare(block_id):
    return Question(id=block_id, question=f"What about {block_id}?")


def write_document(directory, *questions):
    directory.mkdir(parents=True, exist_ok=True)
    open_questions.save_document(str(directory), Document(list(questions)))
    return directory


def document_of(target):
    return (target / open_questions.DOCUMENT_NAME).read_bytes()


def ids_of(target):
    return [question.id for question in open_questions.load_document(str(target)).questions]


def printed(result):
    assert (result.returncode, result.stderr) == (0, b"")
    return result.stdout.decode("utf-8").splitlines()


def silent(result):
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def block_lines(text, short_title):
    """The named block's lines exactly as the text holds them."""
    lines = text.split("\n")
    start = lines.index(f'  <open-question id="{open_questions.escape(short_title)}">')
    end = lines.index("  </open-question>", start)
    return lines[start : end + 1]


# --- the order written ------------------------------------------------------------------


def test_sort_writes_the_annotated_blocks_first_in_walk_order_then_the_rest_in_prior_order(run_tool, tmp_path):
    target = write_document(tmp_path, bare("U"), annotated("D", ["B", "C"]), bare("V"), annotated("C", ["A"]), annotated("B", ["A"]), annotated("A"))
    walked = printed(run_tool("walk", str(target)))
    assert walked == ["A", "C", "B", "D"]
    silent(run_tool("sort", str(target)))
    assert ids_of(target) == ["A", "C", "B", "D", "U", "V"]
    assert printed(run_tool("list", str(target))) == walked + ["U", "V"]


def test_sort_makes_walk_the_annotated_prefix_of_list(run_tool, tmp_path):
    target = write_document(tmp_path, annotated("C", ["B"]), bare("V"), annotated("B", ["A"]), bare("U"), annotated("A"))
    silent(run_tool("sort", str(target)))
    walked = printed(run_tool("walk", str(target)))
    listed = printed(run_tool("list", str(target)))
    without_recommendation = printed(run_tool("list", str(target), "--without-recommendation"))
    assert listed == walked + without_recommendation
    assert listed[: len(walked)] == ["A", "B", "C"]


def test_sort_keeps_the_un_annotated_blocks_in_their_prior_relative_order(run_tool, tmp_path):
    target = write_document(tmp_path, bare("Z"), annotated("A"), bare("M"), annotated("B", ["A"]), bare("A-bare"))
    silent(run_tool("sort", str(target)))
    assert ids_of(target) == ["A", "B", "Z", "M", "A-bare"]
    assert printed(run_tool("list", str(target), "--without-recommendation")) == ["Z", "M", "A-bare"]


def test_sort_places_dependents_by_depth_with_same_depth_ties_in_prior_order(run_tool, tmp_path):
    target = write_document(tmp_path, annotated("D", ["C", "B"]), annotated("C", ["A"]), annotated("B", ["A"]), annotated("A"))
    silent(run_tool("sort", str(target)))
    assert ids_of(target) == ["A", "C", "B", "D"]


def test_sort_moves_a_bare_block_that_sat_between_a_target_and_its_dependent_to_the_end(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    text = document_of(target).decode("utf-8")
    hatch, root_form, bare_block = (block_lines(text, short_title) for short_title in (HATCH, ROOT_FORM, BARE))
    shuffled = "<open-questions>\n" + "\n".join(bare_block + root_form + hatch) + "\n</open-questions>\n"
    (target / open_questions.DOCUMENT_NAME).write_text(shuffled, encoding="utf-8")
    assert ids_of(target) == [BARE, ROOT_FORM, HATCH]
    silent(run_tool("sort", str(target)))
    assert document_of(target).decode("utf-8") == text
    assert printed(run_tool("walk", str(target))) == [HATCH, ROOT_FORM]


def test_sort_breaks_a_cycle_as_walk_does_and_keeps_the_rest_behind_it(run_tool, tmp_path):
    target = write_document(tmp_path, bare("U"), annotated("B", ["A"]), annotated("A", ["B"]), annotated("O"), annotated("P", ["O"]))
    assert printed(run_tool("walk", str(target))) == ["O", "P", "B", "A"]
    silent(run_tool("sort", str(target)))
    assert ids_of(target) == ["O", "P", "B", "A", "U"]


def test_sort_of_a_bare_document_leaves_its_prior_order(run_tool, tmp_path):
    target = write_document(tmp_path, bare("C"), bare("A"), bare("B"))
    silent(run_tool("sort", str(target)))
    assert ids_of(target) == ["C", "A", "B"]


# --- the blocks themselves -----------------------------------------------------------------


def test_sort_moves_every_block_verbatim_and_keeps_the_document_canonical(run_tool, tmp_path):
    target = write_document(tmp_path, bare("U"), annotated("B", ["A"], option="B"), annotated("A"))
    before = document_of(target).decode("utf-8")
    silent(run_tool("sort", str(target)))
    after = document_of(target).decode("utf-8")
    for short_title in ("U", "A", "B"):
        assert block_lines(after, short_title) == block_lines(before, short_title)
    assert open_questions.render_document(open_questions.parse_document(after)) == after
    assert sorted(after.split("\n")) == sorted(before.split("\n"))


def test_sort_matches_edge_targets_un_escaped_and_case_folded(run_tool, tmp_path):
    target = write_document(tmp_path, annotated("Second & <Last>", ["first & <FIRST>"]), bare("Bare & <bare>"), annotated("First & <first>"))
    silent(run_tool("sort", str(target)))
    assert ids_of(target) == ["First & <first>", "Second & <Last>", "Bare & <bare>"]


# --- reuse of walk_order -------------------------------------------------------------------


def test_sort_order_is_walk_order_followed_by_the_un_annotated_blocks_in_document_order():
    questions = [bare("U"), annotated("B", ["A"]), bare("V"), annotated("A")]
    document = Document(list(questions))
    ordered = open_questions.sort_order(document)
    assert ordered[:2] == open_questions.walk_order(document)
    assert ordered[2:] == [questions[0], questions[2]]
    assert all(placed is held for placed, held in zip(ordered, [questions[3], questions[1], questions[0], questions[2]]))


def test_sort_takes_its_annotated_order_from_walk_order_itself(monkeypatch, tmp_path):
    # Whatever walk_order places is the prefix sort writes: a walk_order that reverses its
    # gather makes sort reverse the annotated blocks, so sort reuses walk_order, not a copy.
    target = write_document(tmp_path, bare("U"), annotated("A"), annotated("B", ["A"]), annotated("C", ["B"]))

    def reversed_walk(document):
        return [question for question in reversed(document.questions) if question.recommendation is not None]

    monkeypatch.setattr(open_questions, "walk_order", reversed_walk)
    assert open_questions.main(["sort", str(target)]) == 0
    assert ids_of(target) == ["C", "B", "A", "U"]


# --- the identity and idempotence --------------------------------------------------------


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_sort_is_the_identity_on_every_golden_fixture(run_tool, milestone_dir, name):
    target = milestone_dir(name)
    document = target / open_questions.DOCUMENT_NAME
    before = document.read_bytes()
    stat_before = document.stat()
    silent(run_tool("sort", str(target)))
    assert document.read_bytes() == before
    assert (document.stat().st_ino, document.stat().st_mtime_ns) == (stat_before.st_ino, stat_before.st_mtime_ns)
    assert sorted(path.name for path in target.iterdir()) == [open_questions.DOCUMENT_NAME]


def test_sort_is_the_identity_on_the_annotated_fixture_and_walk_is_its_annotated_prefix(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = document_of(target)
    silent(run_tool("sort", str(target)))
    assert document_of(target) == before
    assert printed(run_tool("list", str(target))) == [HATCH, ROOT_FORM, BARE]
    assert printed(run_tool("walk", str(target))) == [HATCH, ROOT_FORM]


@pytest.mark.parametrize(
    "web",
    [
        [bare("U"), annotated("D", ["B", "C"]), bare("V"), annotated("C", ["A"]), annotated("B", ["A"]), annotated("A")],
        [annotated("A", ["B"]), bare("U"), annotated("B", ["C"]), annotated("C", ["A"]), annotated("D", ["A"]), annotated("E")],
        [bare("V"), annotated("A", ["A"]), annotated("B", ["B"]), annotated("C", ["A", "B"]), bare("U")],
        [annotated("E", ["A", "D"]), annotated("A"), annotated("D", ["C"]), annotated("C", ["A", "Gone"]), bare("U"), bare("V")],
    ],
    ids=["diamond-interleaved", "cycle-with-tail", "self-edges", "mixed-with-dropped-edge"],
)
def test_sort_is_idempotent_and_a_second_sort_writes_nothing(run_tool, tmp_path, web):
    target = write_document(tmp_path, *web)
    walked = printed(run_tool("walk", str(target)))
    silent(run_tool("sort", str(target)))
    once = document_of(target)
    document = target / open_questions.DOCUMENT_NAME
    stat_once = document.stat()
    silent(run_tool("sort", str(target)))
    assert document_of(target) == once
    assert (document.stat().st_ino, document.stat().st_mtime_ns) == (stat_once.st_ino, stat_once.st_mtime_ns)
    assert printed(run_tool("walk", str(target))) == walked
    assert printed(run_tool("list", str(target))) == walked + [question.id for question in web if question.recommendation is None]


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
  <open-question id="Later">
    <question>And this?</question>
  </open-question>
</open-questions>
"""


def test_sort_writes_nothing_when_no_block_moved_even_on_an_old_order_document(run_tool, tmp_path):
    # The recommendation-bearing block holds its children in the pre-promotion order, which a
    # write would re-render; since no block moves, sort leaves the file exactly as written.
    document = tmp_path / open_questions.DOCUMENT_NAME
    document.write_text(OLD_ORDER, encoding="utf-8")
    stat_before = document.stat()
    silent(run_tool("sort", str(tmp_path)))
    assert document.read_text(encoding="utf-8") == OLD_ORDER
    assert (document.stat().st_ino, document.stat().st_mtime_ns) == (stat_before.st_ino, stat_before.st_mtime_ns)
    assert open_questions.render_document(open_questions.parse_document(OLD_ORDER)) != OLD_ORDER


# --- no other write reorders ----------------------------------------------------------------


def test_render_document_writes_the_blocks_in_the_order_it_is_given():
    text = open_questions.render_document(Document([bare("U"), annotated("B", ["A"]), annotated("A")]))
    assert [question.id for question in open_questions.parse_document(text).questions] == ["U", "B", "A"]


def test_every_other_write_keeps_the_prior_order(run_tool, tmp_path):
    target = write_document(tmp_path, bare("U"), annotated("B", ["A"]), annotated("A"))
    silent(run_tool("add", str(target), "V", stdin=b"What about V?"))
    assert ids_of(target) == ["U", "B", "A", "V"]
    silent(run_tool("strip", str(target), "B"))
    assert ids_of(target) == ["U", "B", "A", "V"]
    silent(run_tool("remove", str(target), "A", "--option", "A"))
    assert ids_of(target) == ["U", "B", "V"]
    assert printed(run_tool("walk", str(target))) == []


# --- the contract ---------------------------------------------------------------------------


def test_sort_prints_nothing_on_success(run_tool, tmp_path):
    target = write_document(tmp_path, bare("U"), annotated("A"))
    silent(run_tool("sort", str(target)))
    assert ids_of(target) == ["A", "U"]


def test_sort_fails_when_the_document_is_missing(run_tool, tmp_path):
    result = run_tool("sort", str(tmp_path))
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == f"Error: {tmp_path / open_questions.DOCUMENT_NAME} does not exist\n".encode("utf-8")
    assert list(tmp_path.iterdir()) == []


def test_sort_fails_on_a_malformed_document_as_one_error_line_and_leaves_it_unchanged(run_tool, tmp_path):
    document = tmp_path / open_questions.DOCUMENT_NAME
    document.write_text("<open-questions>", encoding="utf-8")
    result = run_tool("sort", str(tmp_path))
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.startswith(b"Error: ")
    assert b"not well-formed XML" in result.stderr
    assert result.stderr.count(b"\n") == 1
    assert b"Traceback" not in result.stderr
    assert document.read_text(encoding="utf-8") == "<open-questions>"
    assert sorted(path.name for path in tmp_path.iterdir()) == [open_questions.DOCUMENT_NAME]


def test_sort_rejects_an_extra_argument_as_a_usage_error(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = document_of(target)
    result = run_tool("sort", str(target), HATCH)
    assert result.returncode == 2
    assert result.stdout == b""
    assert b"unrecognized arguments" in result.stderr
    assert document_of(target) == before


def test_sort_without_a_milestone_dir_is_a_usage_error(run_tool):
    result = run_tool("sort")
    assert result.returncode == 2
    assert result.stdout == b""
    assert b"MILESTONE_DIR" in result.stderr


def test_main_sorts_in_process(capsys, tmp_path):
    target = write_document(tmp_path, bare("U"), annotated("B", ["A"]), annotated("A"))
    assert open_questions.main(["sort", str(target)]) == 0
    captured = capsys.readouterr()
    assert (captured.out, captured.err) == ("", "")
    assert ids_of(target) == ["A", "B", "U"]
