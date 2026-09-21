"""The create subcommand: the serializer's empty document, written once and never over."""

from pathlib import Path

import open_questions

FIXTURES = Path(__file__).resolve().parent / "fixtures"
EMPTY = (FIXTURES / "empty" / open_questions.DOCUMENT_NAME).read_bytes()


def test_create_writes_the_empty_document_silently(run_tool, tmp_path):
    target = tmp_path / "milestone_01_first"
    target.mkdir()
    result = run_tool("create", str(target))
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert (target / open_questions.DOCUMENT_NAME).read_bytes() == EMPTY


def test_create_makes_a_missing_milestone_directory(run_tool, tmp_path):
    target = tmp_path / "milestones" / "milestone_02_second"
    result = run_tool("create", str(target))
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert sorted(path.name for path in target.iterdir()) == [open_questions.DOCUMENT_NAME]
    assert (target / open_questions.DOCUMENT_NAME).read_bytes() == b"<open-questions/>\n"


def test_create_refuses_an_existing_document_and_leaves_it_unchanged(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    document = target / open_questions.DOCUMENT_NAME
    before = document.read_bytes()
    result = run_tool("create", str(target))
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == f"Error: {document} already exists\n".encode("utf-8")
    assert document.read_bytes() == before


def test_created_document_is_what_the_serializer_writes_for_no_questions():
    assert open_questions.render_document(open_questions.Document()).encode("utf-8") == EMPTY


def test_created_document_parses_to_no_questions(run_tool, tmp_path):
    run_tool("create", str(tmp_path))
    assert open_questions.load_document(str(tmp_path)) == open_questions.Document()
