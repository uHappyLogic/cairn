"""The list subcommand: bare un-escaped ids, one per line in document order, with
--without-alternatives keeping only the blocks that carry no <alternative> element and
--without-recommendation only the blocks that carry no <recommendation> element."""

import pytest

import open_questions


def test_list_prints_every_id_in_document_order(run_tool, milestone_dir):
    result = run_tool("list", str(milestone_dir("annotated")))
    assert (result.returncode, result.stderr) == (0, b"")
    assert result.stdout.decode("utf-8") == (
        "Escape hatch under sole writer\n"
        "Root element form\n"
        "Fixture bare block\n"
    )


def test_list_prints_ids_un_escaped(run_tool, milestone_dir):
    result = run_tool("list", str(milestone_dir("entities")))
    assert (result.returncode, result.stderr) == (0, b"")
    assert result.stdout.decode("utf-8") == "Ampersand & angle <brackets>, \"quotes\", 'apostrophes'\n"


def test_list_of_an_empty_document_prints_nothing_and_exits_zero(run_tool, milestone_dir):
    result = run_tool("list", str(milestone_dir("empty")))
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def test_list_without_recommendation_keeps_only_blocks_without_a_recommendation(run_tool, milestone_dir):
    result = run_tool("list", str(milestone_dir("annotated")), "--without-recommendation")
    assert (result.returncode, result.stderr) == (0, b"")
    assert result.stdout == b"Fixture bare block\n"


def test_list_without_alternatives_keeps_only_blocks_without_an_alternative(run_tool, milestone_dir):
    result = run_tool("list", str(milestone_dir("annotated")), "--without-alternatives")
    assert (result.returncode, result.stderr) == (0, b"")
    assert result.stdout == b"Fixture bare block\n"


def test_list_without_alternatives_keeps_a_block_whose_recommendation_alone_was_stripped(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    assert run_tool("strip", str(target), "--recommendation", "Root element form").returncode == 0
    assert run_tool("list", str(target), "--without-recommendation").stdout == b"Root element form\nFixture bare block\n"
    assert run_tool("list", str(target), "--without-alternatives").stdout == b"Fixture bare block\n"


def test_list_with_both_filters_keeps_only_blocks_carrying_neither(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    assert run_tool("strip", str(target), "--recommendation", "Root element form").returncode == 0
    result = run_tool("list", str(target), "--without-alternatives", "--without-recommendation")
    assert (result.returncode, result.stderr) == (0, b"")
    assert result.stdout == b"Fixture bare block\n"


@pytest.mark.parametrize("flag", ["--without-alternatives", "--without-recommendation"])
def test_list_filter_of_a_bare_document_prints_every_id(run_tool, milestone_dir, flag):
    result = run_tool("list", flag, str(milestone_dir("bare")))
    assert (result.returncode, result.stderr) == (0, b"")
    assert result.stdout == b"First bare question\nSecond bare question\n"


@pytest.mark.parametrize("flag", ["--without-alternatives", "--without-recommendation"])
def test_list_filter_of_a_fully_annotated_document_prints_nothing(run_tool, milestone_dir, flag):
    result = run_tool("list", str(milestone_dir("entities")), flag)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


@pytest.mark.parametrize("flag", ["--without-alternatives", "--without-recommendation"])
def test_list_filter_of_an_empty_document_prints_nothing(run_tool, milestone_dir, flag):
    result = run_tool("list", str(milestone_dir("empty")), flag)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def test_list_leaves_the_document_unchanged(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    document = target / open_questions.DOCUMENT_NAME
    before = document.read_bytes()
    run_tool("list", str(target))
    run_tool("list", str(target), "--without-alternatives")
    run_tool("list", str(target), "--without-recommendation")
    assert document.read_bytes() == before
    assert sorted(path.name for path in target.iterdir()) == [open_questions.DOCUMENT_NAME]


def test_list_fails_when_the_document_is_missing(run_tool, tmp_path):
    result = run_tool("list", str(tmp_path))
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == f"Error: {tmp_path / open_questions.DOCUMENT_NAME} does not exist\n".encode("utf-8")


def test_list_fails_on_a_malformed_document_as_one_error_line(run_tool, tmp_path):
    (tmp_path / open_questions.DOCUMENT_NAME).write_text("<open-questions>", encoding="utf-8")
    result = run_tool("list", str(tmp_path))
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.startswith(b"Error: ")
    assert b"not well-formed XML" in result.stderr
    assert result.stderr.count(b"\n") == 1
    assert b"Traceback" not in result.stderr


def test_list_rejects_an_unknown_flag_as_a_usage_error(run_tool, milestone_dir):
    result = run_tool("list", str(milestone_dir("bare")), "--annotated")
    assert result.returncode == 2
    assert result.stdout == b""
    assert b"unrecognized arguments: --annotated" in result.stderr


def test_main_lists_in_process(capsys, milestone_dir):
    assert open_questions.main(["list", str(milestone_dir("bare"))]) == 0
    captured = capsys.readouterr()
    assert (captured.out, captured.err) == ("First bare question\nSecond bare question\n", "")
