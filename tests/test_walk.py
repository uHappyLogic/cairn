"""The walk subcommand: the ids of every block carrying a <recommendation>, one per line in
the answer sweep's dispatch order — origins first, then every block whose every resolvable
<depends-on> edge names a block already placed, same-depth ties in document order, an edge
naming an absent or recommendation-less block dropped, and a stranded remainder (a cycle)
broken by promoting its document-order-first block to an origin; an empty document or one
with no annotated block prints nothing at exit 0, and the document is never written."""

import pytest

import open_questions
from open_questions import Alternative, Dependency, Document, Question, Recommendation

ENTITIES_TITLE = "Ampersand & angle <brackets>, \"quotes\", 'apostrophes'"
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


def order_of(*questions):
    """The ids walk_order places for a document holding the questions in that order."""
    return [question.id for question in open_questions.walk_order(Document(list(questions)))]


def write_document(directory, *questions):
    directory.mkdir(parents=True, exist_ok=True)
    open_questions.save_document(str(directory), Document(list(questions)))
    return directory


def printed(result):
    assert (result.returncode, result.stderr) == (0, b"")
    return result.stdout.decode("utf-8").splitlines()


# --- the gather ------------------------------------------------------------------------


def test_walk_prints_only_the_annotated_blocks_of_the_fixture_in_dispatch_order(run_tool, milestone_dir):
    result = run_tool("walk", str(milestone_dir("annotated")))
    assert printed(result) == [HATCH, ROOT_FORM]
    assert BARE not in result.stdout.decode("utf-8")


def test_walk_prints_ids_un_escaped(run_tool, milestone_dir):
    result = run_tool("walk", str(milestone_dir("entities")))
    assert printed(result) == [ENTITIES_TITLE]


def test_walk_of_an_empty_document_prints_nothing_and_exits_zero(run_tool, milestone_dir):
    result = run_tool("walk", str(milestone_dir("empty")))
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def test_walk_of_a_document_with_no_annotated_block_prints_nothing_and_exits_zero(run_tool, milestone_dir):
    result = run_tool("walk", str(milestone_dir("bare")))
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def test_walk_gathers_exactly_the_complement_of_list_unannotated(run_tool, tmp_path):
    target = write_document(tmp_path, annotated("A"), bare("U"), annotated("B", ["A"]), bare("V"), annotated("C"))
    walked = printed(run_tool("walk", str(target)))
    unannotated = printed(run_tool("list", str(target), "--unannotated"))
    every = printed(run_tool("list", str(target)))
    assert sorted(walked + unannotated) == sorted(every)
    assert walked == ["A", "C", "B"]


def test_walk_prints_independent_blocks_in_document_order():
    assert order_of(annotated("C"), annotated("A"), annotated("B")) == ["C", "A", "B"]


def test_walk_ignores_a_recommendation_less_block_that_carries_a_tag():
    tagged = Question(id="T", question="Tagged but bare?", depends_on=[Dependency(question="A", option="A")])
    assert order_of(annotated("A", ["T"]), tagged) == ["A"]


# --- a linear chain ---------------------------------------------------------------------


def test_walk_linear_chain_places_each_target_before_its_dependent(run_tool, tmp_path):
    target = write_document(tmp_path, annotated("C", ["B"]), annotated("B", ["A"]), annotated("A"))
    assert printed(run_tool("walk", str(target))) == ["A", "B", "C"]


def test_walk_linear_chain_in_document_order_is_unchanged():
    assert order_of(annotated("A"), annotated("B", ["A"]), annotated("C", ["B"])) == ["A", "B", "C"]


def test_walk_linear_chain_places_one_block_per_depth():
    chain = [annotated("D", ["C"]), annotated("B", ["A"]), annotated("A"), annotated("C", ["B"]), annotated("E", ["D"])]
    assert order_of(*chain) == ["A", "B", "C", "D", "E"]


# --- a diamond --------------------------------------------------------------------------


def test_walk_diamond_places_the_join_after_both_branches_and_breaks_the_branch_tie_in_document_order(run_tool, tmp_path):
    target = write_document(tmp_path, annotated("D", ["B", "C"]), annotated("C", ["A"]), annotated("B", ["A"]), annotated("A"))
    assert printed(run_tool("walk", str(target))) == ["A", "C", "B", "D"]


def test_walk_diamond_same_depth_ties_follow_document_order_not_edge_order():
    assert order_of(annotated("A"), annotated("B", ["A"]), annotated("C", ["A"]), annotated("D", ["C", "B"])) == [
        "A",
        "B",
        "C",
        "D",
    ]


def test_walk_places_a_block_only_once_its_deepest_target_is_placed():
    # E waits on A (depth 0) and D (depth 2), so it is placed at depth 3 though it comes first.
    web = [annotated("E", ["A", "D"]), annotated("A"), annotated("D", ["C"]), annotated("C", ["A"])]
    assert order_of(*web) == ["A", "C", "D", "E"]


# --- dropped edges ----------------------------------------------------------------------


def test_walk_drops_an_edge_to_a_block_absent_from_the_document(run_tool, tmp_path):
    target = write_document(tmp_path, annotated("B", ["Gone"]), annotated("A"))
    assert printed(run_tool("walk", str(target))) == ["B", "A"]


def test_walk_drops_an_edge_to_a_block_that_carries_no_recommendation(run_tool, tmp_path):
    target = write_document(tmp_path, annotated("B", ["U"]), bare("U"), annotated("A"))
    result = run_tool("walk", str(target))
    assert printed(result) == ["B", "A"]
    assert "U" not in result.stdout.decode("utf-8").splitlines()


def test_walk_keeps_the_resolvable_edges_of_a_block_whose_other_edge_is_dropped():
    assert order_of(annotated("B", ["Gone", "A"]), bare("U"), annotated("A", ["U"])) == ["A", "B"]


def test_walk_drops_the_edge_of_the_entities_fixture_to_its_absent_target(milestone_dir):
    document = open_questions.load_document(str(milestone_dir("entities")))
    (question,) = document.questions
    assert [dependency.question for dependency in question.depends_on] == ['Some "other" question & more']
    assert [placed.id for placed in open_questions.walk_order(document)] == [ENTITIES_TITLE]


def test_walk_matches_edge_targets_un_escaped_and_case_folded(run_tool, tmp_path):
    target = write_document(tmp_path, annotated("Second & <Last>", ["first & <FIRST>"]), annotated("First & <first>"))
    assert 'question="first &amp; &lt;FIRST&gt;"' in (target / open_questions.DOCUMENT_NAME).read_text(encoding="utf-8")
    assert printed(run_tool("walk", str(target))) == ["First & <first>", "Second & <Last>"]


def test_walk_reads_only_the_question_value_of_a_tag():
    dependent = annotated("B")
    dependent.depends_on = [Dependency(question="A", option="No such alternative")]
    assert order_of(dependent, annotated("A")) == ["A", "B"]


# --- a cycle ----------------------------------------------------------------------------


def test_walk_cycle_promotes_its_document_order_first_block(run_tool, tmp_path):
    target = write_document(tmp_path, annotated("A", ["B"]), annotated("B", ["A"]))
    assert printed(run_tool("walk", str(target))) == ["A", "B"]


def test_walk_cycle_promotion_follows_document_order_whichever_block_comes_first():
    assert order_of(annotated("B", ["A"]), annotated("A", ["B"])) == ["B", "A"]


def test_walk_cycle_dependents_follow_the_promoted_block():
    assert order_of(annotated("A", ["B"]), annotated("B", ["A"]), annotated("C", ["B"])) == ["A", "B", "C"]


def test_walk_stranded_remainder_promotes_its_document_order_first_block_even_off_the_cycle():
    # C waits on B, A waits on B, B waits on A: nothing is ready, so the first remaining block
    # (C) is promoted, the walk strands again, A is promoted, and B then follows.
    assert order_of(annotated("C", ["B"]), annotated("A", ["B"]), annotated("B", ["A"])) == ["C", "A", "B"]


def test_walk_places_the_origins_before_promoting_into_a_cycle():
    web = [annotated("A", ["B"]), annotated("B", ["A"]), annotated("O"), annotated("P", ["O"])]
    assert order_of(*web) == ["O", "P", "A", "B"]


def test_walk_three_block_cycle_terminates_with_every_member_once():
    assert order_of(annotated("A", ["C"]), annotated("B", ["A"]), annotated("C", ["B"])) == ["A", "B", "C"]


def test_walk_self_edge_is_a_cycle_of_one(run_tool, tmp_path):
    # A waits on itself, so nothing is ready: A is promoted as the document-order-first remaining
    # block and B, whose one edge is now placed, follows.
    target = write_document(tmp_path, annotated("A", ["A"]), annotated("B", ["A"]))
    assert printed(run_tool("walk", str(target))) == ["A", "B"]


def test_walk_two_cycles_are_promoted_one_at_a_time_in_document_order():
    web = [annotated("A", ["B"]), annotated("B", ["A"]), annotated("C", ["D"]), annotated("D", ["C"])]
    assert order_of(*web) == ["A", "B", "C", "D"]


# --- totality ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "web",
    [
        [annotated("A"), annotated("B", ["A"]), annotated("C", ["A", "B"]), annotated("D", ["C", "Gone"]), bare("U")],
        [annotated("A", ["B"]), annotated("B", ["C"]), annotated("C", ["A"]), annotated("D", ["A"]), annotated("E")],
        [annotated("A", ["A"]), annotated("B", ["B"]), annotated("C", ["A", "B"])],
        [annotated("E", ["A", "D"]), annotated("A"), annotated("D", ["C"]), annotated("C", ["A"]), bare("U"), bare("V")],
    ],
    ids=["diamond-with-dropped-edge", "cycle-with-tail", "self-edges", "mixed"],
)
def test_walk_places_every_annotated_block_exactly_once(web):
    order = order_of(*web)
    assert sorted(order) == sorted(question.id for question in web if question.recommendation is not None)
    assert len(order) == len(set(order))


def test_walk_places_every_target_before_its_dependent_when_the_graph_is_acyclic():
    web = [annotated("E", ["C", "D"]), annotated("D", ["B"]), annotated("C", ["A", "B"]), annotated("B", ["A"]), annotated("A")]
    order = order_of(*web)
    for question in web:
        for dependency in question.depends_on:
            assert order.index(dependency.question) < order.index(question.id)


# --- the sweep's use --------------------------------------------------------------------


def test_walk_order_after_an_answer_omits_the_dependents_its_cascade_stripped(run_tool, tmp_path):
    target = write_document(tmp_path, annotated("A"), annotated("B", ["A"]), annotated("C", ["A"], option="B"))
    assert printed(run_tool("walk", str(target))) == ["A", "B", "C"]
    # Recording B for A untags nothing (both dependents assumed A), so both are stripped and
    # the next walk gathers neither; recording A keeps them and their tags are simply dropped.
    stripped = write_document(tmp_path / "stripped", annotated("A"), annotated("B", ["A"]), annotated("C", ["A"], option="B"))
    assert run_tool("remove", str(stripped), "A", "--option", "B").returncode == 0
    assert (run_tool("walk", str(stripped)).stdout, run_tool("list", str(stripped), "--unannotated").stdout) == (b"", b"B\nC\n")
    assert run_tool("remove", str(target), "A", "--option", "A").returncode == 0
    assert printed(run_tool("walk", str(target))) == ["B", "C"]


# --- the contract -----------------------------------------------------------------------


def test_walk_leaves_the_document_unchanged_and_writes_nothing(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    document = target / open_questions.DOCUMENT_NAME
    before = document.read_bytes()
    stat_before = document.stat()
    run_tool("walk", str(target))
    assert document.read_bytes() == before
    assert (document.stat().st_ino, document.stat().st_mtime_ns) == (stat_before.st_ino, stat_before.st_mtime_ns)
    assert sorted(path.name for path in target.iterdir()) == [open_questions.DOCUMENT_NAME]


def test_walk_fails_when_the_document_is_missing(run_tool, tmp_path):
    result = run_tool("walk", str(tmp_path))
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == f"Error: {tmp_path / open_questions.DOCUMENT_NAME} does not exist\n".encode("utf-8")
    assert list(tmp_path.iterdir()) == []


def test_walk_fails_on_a_malformed_document_as_one_error_line(run_tool, tmp_path):
    (tmp_path / open_questions.DOCUMENT_NAME).write_text("<open-questions>", encoding="utf-8")
    result = run_tool("walk", str(tmp_path))
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.startswith(b"Error: ")
    assert b"not well-formed XML" in result.stderr
    assert result.stderr.count(b"\n") == 1
    assert b"Traceback" not in result.stderr


def test_walk_rejects_an_extra_argument_as_a_usage_error(run_tool, milestone_dir):
    result = run_tool("walk", str(milestone_dir("annotated")), HATCH)
    assert result.returncode == 2
    assert result.stdout == b""
    assert b"unrecognized arguments" in result.stderr


def test_walk_without_a_milestone_dir_is_a_usage_error(run_tool):
    result = run_tool("walk")
    assert result.returncode == 2
    assert result.stdout == b""
    assert b"MILESTONE_DIR" in result.stderr


def test_main_walks_in_process(capsys, milestone_dir):
    assert open_questions.main(["walk", str(milestone_dir("annotated"))]) == 0
    captured = capsys.readouterr()
    assert (captured.out, captured.err) == (f"{HATCH}\n{ROOT_FORM}\n", "")
