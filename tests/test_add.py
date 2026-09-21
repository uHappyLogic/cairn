"""The add subcommand: one bare block appended in canonical form, its question text the one
body read from standard input, with a terminal stdin, an empty body, and a duplicate id
refused."""

import io
import os
import subprocess
import sys
from pathlib import Path

import pytest

import open_questions
from open_questions import Document, Question

FIXTURES = Path(__file__).resolve().parent / "fixtures"
TOOL = Path(open_questions.__file__).resolve()


def read_fixture(name):
    return (FIXTURES / name / open_questions.DOCUMENT_NAME).read_bytes()


def document_of(target):
    return (target / open_questions.DOCUMENT_NAME).read_bytes()


def test_add_to_an_empty_document_writes_the_bare_block_in_canonical_form(run_tool, milestone_dir):
    target = milestone_dir("empty")
    result = run_tool("add", str(target), "First bare question", stdin=b"What is the first thing to decide?\n")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert document_of(target) == (
        b"<open-questions>\n"
        b'  <open-question id="First bare question">\n'
        b"    <question>What is the first thing to decide?</question>\n"
        b"  </open-question>\n"
        b"</open-questions>\n"
    )


def test_add_appends_after_every_existing_block(run_tool, milestone_dir):
    target = milestone_dir("bare")
    first = run_tool("add", str(target), "Third bare question", stdin=b"What is third?")
    assert (first.returncode, first.stdout, first.stderr) == (0, b"", b"")
    second = run_tool("add", str(target), "Fourth bare question", stdin=b"What is fourth?")
    assert (second.returncode, second.stdout, second.stderr) == (0, b"", b"")
    assert document_of(target) == read_fixture("bare")[: -len(b"</open-questions>\n")] + (
        b'  <open-question id="Third bare question">\n'
        b"    <question>What is third?</question>\n"
        b"  </open-question>\n"
        b'  <open-question id="Fourth bare question">\n'
        b"    <question>What is fourth?</question>\n"
        b"  </open-question>\n"
        b"</open-questions>\n"
    )
    assert run_tool("list", str(target)).stdout == (
        b"First bare question\nSecond bare question\nThird bare question\nFourth bare question\n"
    )


def test_add_two_bare_blocks_reproduces_the_bare_fixture(run_tool, milestone_dir):
    target = milestone_dir("empty")
    run_tool("add", str(target), "First bare question", stdin=b"What is the first thing to decide?")
    run_tool("add", str(target), "Second bare question", stdin=b"What follows from the first decision?")
    assert document_of(target) == read_fixture("bare")


def test_add_leaves_annotated_siblings_byte_for_byte_unchanged(run_tool, milestone_dir):
    target = milestone_dir("annotated")
    before = document_of(target)
    result = run_tool("add", str(target), "Fourth question", stdin=b"Is the fourth block bare?")
    assert result.returncode == 0
    after = document_of(target)
    assert after.startswith(before[: -len(b"</open-questions>\n")])
    assert after.endswith(
        b'  <open-question id="Fourth question">\n'
        b"    <question>Is the fourth block bare?</question>\n"
        b"  </open-question>\n"
        b"</open-questions>\n"
    )


def test_add_writes_only_the_wrapper_and_the_question_child(run_tool, milestone_dir):
    target = milestone_dir("empty")
    run_tool("add", str(target), "Only a question", stdin=b"Is there anything else?")
    document = open_questions.load_document(str(target))
    assert document == Document(questions=[Question(id="Only a question", question="Is there anything else?")])
    assert open_questions.is_bare(document.questions[0])


def test_add_folds_the_body_to_one_line(run_tool, milestone_dir):
    target = milestone_dir("empty")
    body = b"  Does a\tmulti-line\n\n   body   fold\r\nto one line?  \n\n"
    result = run_tool("add", str(target), "Folded body", stdin=body)
    assert result.returncode == 0
    assert b"    <question>Does a multi-line body fold to one line?</question>\n" in document_of(target)


def test_add_folds_the_short_title_to_one_line(run_tool, milestone_dir):
    target = milestone_dir("empty")
    result = run_tool("add", str(target), "  Spaced \n title  ", stdin=b"Is the id folded?")
    assert result.returncode == 0
    assert b'  <open-question id="Spaced title">\n' in document_of(target)
    assert run_tool("list", str(target)).stdout == b"Spaced title\n"


def test_add_escapes_the_five_entities_in_the_id_and_the_text(run_tool, milestone_dir):
    target = milestone_dir("empty")
    title = "Ampersand & angle <brackets>, \"quotes\", 'apostrophes'"
    body = "Does <text> with &, \"double\" and 'single' quotes survive?".encode("utf-8")
    result = run_tool("add", str(target), title, stdin=body)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert document_of(target) == (
        b"<open-questions>\n"
        b'  <open-question id="Ampersand &amp; angle &lt;brackets&gt;, &quot;quotes&quot;, &apos;apostrophes&apos;">\n'
        b"    <question>Does &lt;text&gt; with &amp;, &quot;double&quot; and &apos;single&apos; quotes survive?</question>\n"
        b"  </open-question>\n"
        b"</open-questions>\n"
    )
    assert run_tool("list", str(target)).stdout.decode("utf-8") == title + "\n"


def test_add_decodes_the_body_as_utf8(run_tool, milestone_dir):
    target = milestone_dir("empty")
    body = "Is the em dash — and the ellipsis … kept as UTF-8?".encode("utf-8")
    result = run_tool("add", str(target), "UTF-8 body", stdin=body)
    assert result.returncode == 0
    assert "<question>Is the em dash — and the ellipsis … kept as UTF-8?</question>" in document_of(target).decode("utf-8")


def test_add_reads_the_body_verbatim_with_nothing_expanded(run_tool, milestone_dir):
    target = milestone_dir("empty")
    body = b"Does `code`, ${VAR}, $(cmd), and a literal &apos; travel untouched?"
    result = run_tool("add", str(target), "Verbatim body", stdin=body)
    assert result.returncode == 0
    assert (
        b"    <question>Does `code`, ${VAR}, $(cmd), and a literal &amp;apos; travel untouched?</question>\n"
        in document_of(target)
    )


def test_add_refuses_a_terminal_stdin_without_blocking(milestone_dir):
    pty = pytest.importorskip("pty")
    target = milestone_dir("bare")
    before = document_of(target)
    master, slave = pty.openpty()
    try:
        # A pseudo-terminal on fd 0 with nothing ever written to it: a read would block, so
        # the refusal is what lets the call finish inside the timeout.
        result = subprocess.run(
            [sys.executable, "-B", str(TOOL), "add", str(target), "Typed at a terminal"],
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
        b"Error: the question text must be piped on standard input (as a quoted heredoc or a "
        b"redirected file), not typed at a terminal\n"
    )
    assert document_of(target) == before


def test_main_refuses_an_isatty_stdin_in_process(capsys, monkeypatch, milestone_dir):
    target = milestone_dir("bare")
    before = document_of(target)

    class Terminal:
        closed = False

        def isatty(self):
            return True

        @property
        def buffer(self):
            raise AssertionError("a terminal stdin must be refused before it is read")

    monkeypatch.setattr(sys, "stdin", Terminal())
    assert open_questions.main(["add", str(target), "Typed at a terminal"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("Error: the question text must be piped on standard input")
    assert document_of(target) == before


def test_main_refuses_a_closed_stdin(capsys, monkeypatch, milestone_dir):
    target = milestone_dir("bare")
    monkeypatch.setattr(sys, "stdin", None)
    assert open_questions.main(["add", str(target), "No stdin"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "Error: the question text must be supplied on standard input, which is closed\n"
    assert document_of(target) == read_fixture("bare")


def test_main_reads_the_body_from_stdin_buffer_once(capsys, monkeypatch, milestone_dir):
    target = milestone_dir("empty")
    stream = io.TextIOWrapper(io.BytesIO("Is the body read from sys.stdin.buffer — as bytes?".encode("utf-8")))
    monkeypatch.setattr(sys, "stdin", stream)
    assert open_questions.main(["add", str(target), "In-process body"]) == 0
    assert capsys.readouterr() == ("", "")
    assert stream.buffer.read() == b""
    assert "<question>Is the body read from sys.stdin.buffer — as bytes?</question>" in document_of(target).decode("utf-8")


@pytest.mark.parametrize("body", [b"", b"   \n\t\n"])
def test_add_refuses_an_empty_body(run_tool, milestone_dir, body):
    target = milestone_dir("bare")
    before = document_of(target)
    result = run_tool("add", str(target), "Empty body", stdin=body)
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == b"Error: the question text on standard input is empty\n"
    assert document_of(target) == before


def test_add_refuses_a_non_utf8_body(run_tool, milestone_dir):
    target = milestone_dir("bare")
    before = document_of(target)
    result = run_tool("add", str(target), "Latin-1 body", stdin=b"Is caf\xe9 UTF-8?")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == b"Error: the question text on standard input is not UTF-8 text\n"
    assert document_of(target) == before


def test_add_refuses_a_duplicate_id_naming_the_existing_block(run_tool, milestone_dir):
    target = milestone_dir("bare")
    before = document_of(target)
    result = run_tool("add", str(target), "First bare question", stdin=b"Again?")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == b'Error: an <open-question> block with the id "First bare question" already exists\n'
    assert document_of(target) == before


def test_add_compares_the_id_case_folded_and_whitespace_folded(run_tool, milestone_dir):
    target = milestone_dir("bare")
    before = document_of(target)
    result = run_tool("add", str(target), "  FIRST  bare QUESTION ", stdin=b"Again?")
    assert result.returncode == 1
    assert result.stderr == b'Error: an <open-question> block with the id "First bare question" already exists\n'
    assert document_of(target) == before


def test_add_compares_the_id_against_the_un_escaped_value(run_tool, milestone_dir):
    target = milestone_dir("entities")
    before = document_of(target)
    un_escaped = run_tool("add", str(target), "ampersand & ANGLE <brackets>, \"quotes\", 'apostrophes'", stdin=b"Again?")
    assert un_escaped.returncode == 1
    assert un_escaped.stderr.startswith(b"Error: an <open-question> block with the id ")
    assert document_of(target) == before
    escaped = run_tool("add", str(target), "Ampersand &amp; angle &lt;brackets&gt;, &quot;quotes&quot;, &apos;apostrophes&apos;", stdin=b"A new one?")
    assert escaped.returncode == 0
    assert run_tool("list", str(target)).stdout.count(b"\n") == 2


def test_add_refuses_an_empty_short_title(run_tool, milestone_dir):
    target = milestone_dir("bare")
    before = document_of(target)
    result = run_tool("add", str(target), "   ", stdin=b"Whose question is this?")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == b"Error: the Short Title is empty\n"
    assert document_of(target) == before


def test_add_requires_a_short_title(run_tool, milestone_dir):
    result = run_tool("add", str(milestone_dir("bare")), stdin=b"Whose question is this?")
    assert result.returncode == 2
    assert result.stdout == b""
    assert b"SHORT_TITLE" in result.stderr


def test_add_fails_when_the_document_is_missing_and_creates_nothing(run_tool, tmp_path):
    result = run_tool("add", str(tmp_path), "Anything", stdin=b"Is there a document?")
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == f"Error: {tmp_path / open_questions.DOCUMENT_NAME} does not exist\n".encode("utf-8")
    assert list(tmp_path.iterdir()) == []


def test_add_fails_on_a_malformed_document_and_leaves_it_unchanged(run_tool, tmp_path):
    document = tmp_path / open_questions.DOCUMENT_NAME
    document.write_text("<open-questions>", encoding="utf-8")
    result = run_tool("add", str(tmp_path), "Anything", stdin=b"Is the document well-formed?")
    assert result.returncode == 1
    assert result.stdout == b""
    assert b"not well-formed XML" in result.stderr
    assert result.stderr.count(b"\n") == 1
    assert document.read_text(encoding="utf-8") == "<open-questions>"


def test_add_leaves_no_temporary_file_behind(run_tool, milestone_dir):
    target = milestone_dir("bare")
    run_tool("add", str(target), "Third bare question", stdin=b"What is third?")
    run_tool("add", str(target), "Third bare question", stdin=b"Again?")
    assert sorted(path.name for path in target.iterdir()) == [open_questions.DOCUMENT_NAME]
