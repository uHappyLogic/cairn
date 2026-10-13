"""The move subcommand: the TASKS_TODO.md section whose heading equals the title (exact
whitespace-folded, case-folded match) appended to TASKS_DONE.md with the **Verified:**
label, the bar from standard input verbatim with only its leading and trailing blank lines
trimmed, and the "---"; silent on success; a partial, shared, or unknown title or an empty
bar refused with one Error line and both task files byte-for-byte unchanged."""

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


def done_of(target):
    return (target / task_list.DONE_NAME).read_text(encoding="utf-8")


def todo_titles(target):
    _, sections = parse_sections(todo_of(target), with_bar=False)
    return [section.title for section in sections]


def done_sections(target):
    _, sections = parse_sections(done_of(target), with_bar=True)
    return sections


def refused(result, target, before):
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.startswith(b"Error: ") and result.stderr.count(b"\n") == 1
    assert snapshot(target) == before
    return result.stderr.decode("utf-8")


# --- the Verified rendering -------------------------------------------------------------


def test_move_appends_the_entry_with_the_verified_label_the_bar_and_the_separator(run_task_list, task_list_dir):
    target = task_list_dir()
    done_before = done_of(target)
    silent(run_task_list("move", str(target), FIRST, stdin=b"- The parser reads the whole file\n- The round trip holds\n"))
    assert done_of(target) == done_before + (
        "\n## Build The Parser First\n\n"
        "Write the parser that reads the whole file into its heading and sections, so every later write renders from "
        "one model. Verified by its round trip on the golden files.\n\n"
        "**Verified:**\n\n"
        "- The parser reads the whole file\n- The round trip holds\n\n"
        "---\n"
    )
    assert todo_titles(target) == [SECOND, THIRD]


def test_move_cuts_the_section_and_keeps_the_rest_of_the_todo_file(run_task_list, task_list_dir):
    target = task_list_dir()
    silent(run_task_list("move", str(target), SECOND, stdin=b"- kept\n"))
    assert todo_of(target) == (
        "# TASKS TODO\n\n"
        "## Build The Parser First\n\nWrite the parser that reads the whole file into its heading and sections, so every "
        "later write renders from one model. Verified by its round trip on the golden files.\n\n---\n\n"
        "## Render Unicode — Text As Given\n\nCarry `code`, ${VAR}, $(cmd), &amp; entities, and \"quotes\" through "
        "untouched, including non-ASCII text like zażółć gęślą jaźń.\n\n---\n"
    )


def test_move_carries_a_body_with_a_dash_line_whole(run_task_list, task_list_dir):
    target = task_list_dir()
    silent(run_task_list("move", str(target), SECOND, stdin=b"- kept\n"))
    entry = done_sections(target)[-1]
    assert entry.title == SECOND
    assert entry.body == (
        "A body may hold a separator line of its own that is not the section's end.\n\n---\n\n"
        "The line above stays body text, because the next non-blank line is this prose rather than a heading."
    )
    assert entry.bar == "- kept"


def test_the_bar_is_trimmed_of_leading_and_trailing_blank_lines_only(run_task_list, task_list_dir):
    target = task_list_dir(done=b"# TASKS DONE\n\n")
    silent(run_task_list("move", str(target), FIRST, stdin=b"\n\n  \n- one\n\n  - nested two\n\n\n"))
    assert done_of(target).endswith("**Verified:**\n\n- one\n\n  - nested two\n\n---\n")


def test_the_bar_is_opaque_markdown_never_split_or_given_bullets(run_task_list, task_list_dir):
    target = task_list_dir(done=b"# TASKS DONE\n\n")
    bar = "The bar is prose; nothing adds a bullet.\nSecond line `code` ${VAR} — zażółć."
    silent(run_task_list("move", str(target), FIRST, stdin=bar.encode("utf-8")))
    assert done_sections(target)[0].bar == bar
    assert done_of(target).endswith(f"**Verified:**\n\n{bar}\n\n---\n")


def test_a_title_the_done_file_already_holds_is_moved_without_a_check(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n## Ship The Initial Tool\n\nThe follow-up.\n\n---\n")
    silent(run_task_list("move", str(target), "  ship the   INITIAL tool ", stdin=b"- again\n"))
    assert [section.title for section in done_sections(target)] == ["Ship The Initial Tool", "Record A Prose Bar", "Ship The Initial Tool"]
    assert todo_of(target) == "# TASKS TODO\n\n"


def test_a_section_without_its_separator_moves_silently_and_gains_one(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n## First Task\n\nThe first body.\n## Second Task\n\nThe second body.\n\n---\n", done=b"# TASKS DONE\n\n")
    silent(run_task_list("move", str(target), "First Task", stdin=b"- done\n"))
    assert done_of(target) == "# TASKS DONE\n\n## First Task\n\nThe first body.\n\n**Verified:**\n\n- done\n\n---\n"
    assert todo_of(target) == "# TASKS TODO\n\n## Second Task\n\nThe second body.\n\n---\n"


def test_successive_moves_append_in_order(run_task_list, task_list_dir):
    target = task_list_dir(done=b"# TASKS DONE\n\n")
    for title in (THIRD, FIRST, SECOND):
        silent(run_task_list("move", str(target), title, stdin=f"- {title} done\n".encode("utf-8")))
    assert [(section.title, section.bar) for section in done_sections(target)] == [
        (THIRD, f"- {THIRD} done"),
        (FIRST, f"- {FIRST} done"),
        (SECOND, f"- {SECOND} done"),
    ]
    assert todo_of(target) == "# TASKS TODO\n\n"


# --- exact-match refusals ---------------------------------------------------------------


@pytest.mark.parametrize("title", ["build the parser first", "  BUILD the   parser\tFIRST  "])
def test_the_title_is_matched_whitespace_folded_and_case_folded(run_task_list, task_list_dir, title):
    target = task_list_dir()
    silent(run_task_list("move", str(target), title, stdin=b"- matched\n"))
    assert done_sections(target)[-1].title == FIRST


@pytest.mark.parametrize("title", ["Build The Parser", "Parser", "Build The Parser First Now", "No Such Task"])
def test_a_partial_or_unknown_title_is_refused(run_task_list, task_list_dir, title):
    target = task_list_dir()
    before = snapshot(target)
    message = refused(run_task_list("move", str(target), title, stdin=b"- a criterion\n"), target, before)
    assert f'no section of {target / task_list.TODO_NAME} is titled "{title}"' in message


def test_a_title_two_sections_share_is_refused(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n## Twin\n\nOne.\n\n---\n\n## twin\n\nTwo.\n\n---\n")
    before = snapshot(target)
    message = refused(run_task_list("move", str(target), "Twin", stdin=b"- a criterion\n"), target, before)
    assert 'Error: 2 sections of' in message and 'the title names no single section' in message


def test_a_title_only_the_done_file_holds_is_refused(run_task_list, task_list_dir):
    target = task_list_dir()
    before = snapshot(target)
    refused(run_task_list("move", str(target), "Ship The Initial Tool", stdin=b"- a criterion\n"), target, before)


@pytest.mark.parametrize("bar", [b"", b"\n\n", b"  \n\t\n"])
def test_an_empty_bar_is_refused(run_task_list, task_list_dir, bar):
    target = task_list_dir()
    before = snapshot(target)
    message = refused(run_task_list("move", str(target), FIRST, stdin=bar), target, before)
    assert message == "Error: the acceptance bar on standard input is empty\n"


def test_moving_out_of_an_empty_list_is_refused(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n")
    before = snapshot(target)
    message = refused(run_task_list("move", str(target), FIRST, stdin=b"- a criterion\n"), target, before)
    assert "it holds no section" in message
