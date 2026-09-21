"""The output and error contract every subcommand shares: silent mutators, one Error line
with exit 1 and the document untouched, argparse's own exit 2, and never a traceback."""

import stat

import open_questions


def test_no_subcommand_is_a_usage_error(run_tool):
    result = run_tool()
    assert result.returncode == 2
    assert result.stdout == b""
    assert result.stderr.startswith(b"usage: open_questions.py")


def test_unknown_subcommand_is_a_usage_error(run_tool, tmp_path):
    result = run_tool("frobnicate", str(tmp_path))
    assert result.returncode == 2
    assert result.stdout == b""
    assert b"invalid choice: 'frobnicate'" in result.stderr


def test_missing_milestone_dir_is_a_usage_error(run_tool):
    result = run_tool("create")
    assert result.returncode == 2
    assert result.stdout == b""
    assert b"MILESTONE_DIR" in result.stderr


def test_help_exits_zero_and_lists_the_subcommands(run_tool):
    result = run_tool("--help")
    assert result.returncode == 0
    for subcommand in (b"create", b"list", b"locate", b"lift", b"add", b"strip", b"embed", b"remove", b"walk", b"sort"):
        assert subcommand in result.stdout
    assert result.stderr == b""


def test_a_failure_is_exactly_one_error_line_on_stderr(run_tool, milestone_dir):
    result = run_tool("create", str(milestone_dir("empty")))
    assert result.returncode == 1
    assert result.stdout == b""
    lines = result.stderr.decode("utf-8").split("\n")
    assert len(lines) == 2 and lines[1] == ""
    assert lines[0].startswith("Error: ")
    assert b"Traceback" not in result.stderr


def test_an_operating_system_failure_is_an_error_line_not_a_traceback(run_tool, tmp_path):
    blocker = tmp_path / "not-a-directory"
    blocker.write_text("")
    result = run_tool("create", str(blocker))
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.startswith(b"Error: ")
    assert result.stderr.count(b"\n") == 1
    assert b"Traceback" not in result.stderr
    assert blocker.read_bytes() == b""


def test_main_reports_a_tool_error_as_one_line_and_exit_one(capsys, tmp_path):
    (tmp_path / open_questions.DOCUMENT_NAME).write_bytes(b"<open-questions/>\n")
    assert open_questions.main(["create", str(tmp_path)]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == f"Error: {tmp_path / open_questions.DOCUMENT_NAME} already exists\n"


def test_main_returns_zero_and_prints_nothing_for_a_mutator(capsys, tmp_path):
    assert open_questions.main(["create", str(tmp_path)]) == 0
    captured = capsys.readouterr()
    assert (captured.out, captured.err) == ("", "")


def test_a_malformed_document_fails_as_one_error_line(tmp_path):
    (tmp_path / open_questions.DOCUMENT_NAME).write_text("<open-questions>", encoding="utf-8")
    try:
        open_questions.load_document(str(tmp_path))
    except open_questions.ToolError as error:
        assert "not well-formed XML" in str(error)
        assert "\n" not in str(error)
    else:
        raise AssertionError("a malformed document must raise ToolError")


def test_a_non_utf8_document_fails_as_one_error_line(tmp_path):
    (tmp_path / open_questions.DOCUMENT_NAME).write_bytes(b"<open-questions>\xff</open-questions>")
    try:
        open_questions.load_document(str(tmp_path))
    except open_questions.ToolError as error:
        assert str(error).endswith("is not UTF-8 text")
    else:
        raise AssertionError("a non-UTF-8 document must raise ToolError")


def test_save_replaces_the_document_whole_and_keeps_its_mode(tmp_path):
    path = tmp_path / open_questions.DOCUMENT_NAME
    path.write_bytes(b"old")
    path.chmod(0o640)
    open_questions.save_document(str(tmp_path), open_questions.Document())
    assert path.read_bytes() == b"<open-questions/>\n"
    assert stat.S_IMODE(path.stat().st_mode) == 0o640
    assert sorted(p.name for p in tmp_path.iterdir()) == [open_questions.DOCUMENT_NAME]
