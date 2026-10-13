"""The insert subcommand: one section composed from the title argument and the body on
standard input, landed at exactly the one position its required flag names (--end,
--before, --after), the body written verbatim, silent on success; an empty title or body, a
folded title TASKS_TODO.md already holds, or an anchor naming no single section refused
with one Error line and both task files byte-for-byte unchanged."""

import pytest

import task_list
from task_list import parse_sections

FIRST = "Build The Parser First"
SECOND = "Keep A Body Separator Line"
THIRD = "Render Unicode — Text As Given"


def silent(result):
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def snapshot(target):
    return (target / task_list.TODO_NAME).read_bytes(), (target / task_list.DONE_NAME).read_bytes()


def todo_of(target):
    return (target / task_list.TODO_NAME).read_text(encoding="utf-8")


def titles_of(target):
    _, sections = parse_sections(todo_of(target), with_bar=False)
    return [section.title for section in sections]


def section_of(target, title):
    _, sections = parse_sections(todo_of(target), with_bar=False)
    return next(section for section in sections if section.title == title)


def refused(result, target, before):
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.startswith(b"Error: ") and result.stderr.count(b"\n") == 1
    assert snapshot(target) == before
    return result.stderr.decode("utf-8")


# --- the three positions ----------------------------------------------------------------


def test_end_puts_the_section_after_the_last_section(run_task_list, task_list_dir):
    target = task_list_dir()
    silent(run_task_list("insert", str(target), "New Task", "--end", stdin=b"The new body.\n"))
    assert titles_of(target) == [FIRST, SECOND, THIRD, "New Task"]


def test_end_on_an_empty_list_puts_the_only_section(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n")
    silent(run_task_list("insert", str(target), "New Task", "--end", stdin=b"The new body.\n"))
    assert todo_of(target) == "# TASKS TODO\n\n## New Task\n\nThe new body.\n\n---\n"


@pytest.mark.parametrize(
    "anchor, expected",
    [
        (FIRST, ["New Task", FIRST, SECOND, THIRD]),
        (SECOND, [FIRST, "New Task", SECOND, THIRD]),
        (THIRD, [FIRST, SECOND, "New Task", THIRD]),
    ],
)
def test_before_puts_the_section_ahead_of_the_named_section(run_task_list, task_list_dir, anchor, expected):
    target = task_list_dir()
    silent(run_task_list("insert", str(target), "New Task", "--before", anchor, stdin=b"The new body.\n"))
    assert titles_of(target) == expected


@pytest.mark.parametrize(
    "anchor, expected",
    [
        (FIRST, [FIRST, "New Task", SECOND, THIRD]),
        (SECOND, [FIRST, SECOND, "New Task", THIRD]),
        (THIRD, [FIRST, SECOND, THIRD, "New Task"]),
    ],
)
def test_after_puts_the_section_behind_the_named_section(run_task_list, task_list_dir, anchor, expected):
    target = task_list_dir()
    silent(run_task_list("insert", str(target), "New Task", "--after", anchor, stdin=b"The new body.\n"))
    assert titles_of(target) == expected


def test_an_anchor_is_matched_whitespace_folded_and_case_folded(run_task_list, task_list_dir):
    target = task_list_dir()
    silent(run_task_list("insert", str(target), "New Task", "--before", "  keep a   BODY separator\tline ", stdin=b"The new body.\n"))
    assert titles_of(target) == [FIRST, "New Task", SECOND, THIRD]


def test_the_other_sections_keep_their_order_and_text(run_task_list, task_list_dir):
    target = task_list_dir()
    _, before = parse_sections(todo_of(target), with_bar=False)
    silent(run_task_list("insert", str(target), "New Task", "--after", FIRST, stdin=b"The new body.\n"))
    _, after = parse_sections(todo_of(target), with_bar=False)
    assert [section for section in after if section.title != "New Task"] == before


# --- the body verbatim ------------------------------------------------------------------


def test_the_tool_composes_heading_body_and_separator(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n")
    silent(run_task_list("insert", str(target), "New Task", "--end", stdin=b"\n\nThe new body.\n\n\n"))
    assert todo_of(target) == "# TASKS TODO\n\n## New Task\n\nThe new body.\n\n---\n"


def test_the_body_is_written_verbatim(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n")
    body = "Carry `code`, ${VAR}, $(cmd), 'quotes', \"quotes\", &amp; and zażółć — a backslash \\n too.\n  Indented line kept.\n\n**Verified:** in a body stays text."
    silent(run_task_list("insert", str(target), "New Task", "--end", stdin=(body + "\n").encode("utf-8")))
    assert todo_of(target) == f"# TASKS TODO\n\n## New Task\n\n{body}\n\n---\n"


def test_structure_like_body_lines_are_written_as_body_by_the_insert(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n")
    silent(run_task_list("insert", str(target), "New Task", "--end", stdin=b"## Not A Heading Here\n\n---\n\nTail.\n"))
    assert todo_of(target) == "# TASKS TODO\n\n## New Task\n\n## Not A Heading Here\n\n---\n\nTail.\n\n---\n"


def test_the_title_is_folded_to_one_line(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n")
    silent(run_task_list("insert", str(target), "  New \n  Task  ", "--end", stdin=b"The new body.\n"))
    assert todo_of(target) == "# TASKS TODO\n\n## New Task\n\nThe new body.\n\n---\n"


def test_no_task_format_rule_is_checked(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n")
    body = "One. Two. Three. Four. Five sentences.\n\n### Steps\n\n- a step"
    silent(run_task_list("insert", str(target), "x", "--end", stdin=body.encode("utf-8")))
    assert section_of(target, "x").body == body


def test_a_title_the_done_file_already_holds_is_inserted(run_task_list, task_list_dir):
    target = task_list_dir()
    silent(run_task_list("insert", str(target), "Ship The Initial Tool", "--end", stdin=b"Follow-up work.\n"))
    assert titles_of(target)[-1] == "Ship The Initial Tool"


# --- refusals ---------------------------------------------------------------------------


@pytest.mark.parametrize("title", ["", "   ", "\n\t"])
def test_an_empty_title_is_refused(run_task_list, task_list_dir, title):
    target = task_list_dir()
    before = snapshot(target)
    message = refused(run_task_list("insert", str(target), title, "--end", stdin=b"A body.\n"), target, before)
    assert message == "Error: the task title is empty\n"


@pytest.mark.parametrize("body", [b"", b"\n", b"   \n\t\n"])
def test_an_empty_body_is_refused(run_task_list, task_list_dir, body):
    target = task_list_dir()
    before = snapshot(target)
    message = refused(run_task_list("insert", str(target), "New Task", "--end", stdin=body), target, before)
    assert message == "Error: the task body on standard input is empty\n"


@pytest.mark.parametrize("title", [FIRST, "build the parser first", "  BUILD  the\tparser FIRST "])
def test_a_folded_title_the_todo_file_already_holds_is_refused(run_task_list, task_list_dir, title):
    target = task_list_dir()
    before = snapshot(target)
    message = refused(run_task_list("insert", str(target), title, "--end", stdin=b"A body.\n"), target, before)
    assert message == f'Error: {target / task_list.TODO_NAME} already holds a section titled "{FIRST}"\n'


@pytest.mark.parametrize("flag", ["--before", "--after"])
@pytest.mark.parametrize("anchor", ["No Such Task", "Build The Parser", "Build The Parser First Of All"])
def test_an_anchor_naming_no_section_is_refused(run_task_list, task_list_dir, flag, anchor):
    target = task_list_dir()
    before = snapshot(target)
    message = refused(run_task_list("insert", str(target), "New Task", flag, anchor, stdin=b"A body.\n"), target, before)
    assert f'no section of {target / task_list.TODO_NAME} is titled "{anchor}"' in message
    assert f'"{FIRST}", "{SECOND}", "{THIRD}"' in message


def test_an_anchor_on_an_empty_list_is_refused(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n")
    before = snapshot(target)
    message = refused(run_task_list("insert", str(target), "New Task", "--after", "Anything", stdin=b"A body.\n"), target, before)
    assert "it holds no section" in message


@pytest.mark.parametrize("flag", ["--before", "--after"])
def test_an_anchor_two_sections_share_is_refused(run_task_list, task_list_dir, flag):
    target = task_list_dir(todo=b"# TASKS TODO\n\n## Twin\n\nOne.\n\n---\n\n## twin\n\nTwo.\n\n---\n")
    before = snapshot(target)
    message = refused(run_task_list("insert", str(target), "New Task", flag, "TWIN", stdin=b"A body.\n"), target, before)
    assert 'are titled "TWIN"; the title names no single section' in message
