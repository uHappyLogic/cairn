"""The remove subcommand: the TASKS_TODO.md section whose heading equals the title (exact
whitespace-folded, case-folded match) taken out of the list, its heading, body, and "---"
together, with the rest of the file rendered in the canonical layout; it reads nothing from
standard input, renders the removed section nowhere, and never reads or writes the done file
a milestone completed before the bar moved into commits keeps beside its list; silent on
success; a partial, shared, or unknown title refused with one Error line and the list
byte-for-byte unchanged."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

import task_list
from task_list import parse_sections

TOOL = Path(task_list.__file__).resolve()

FIRST = "Build The Parser First"
SECOND = "Keep A Body Separator Line"
THIRD = "Render Unicode — Text As Given"

# The done file a milestone completed before the bar moved into commits keeps beside its list,
# named as the list is with DONE for TODO, in the form its entries were written in.
DONE_NAME = task_list.TODO_NAME.replace("TODO", "DONE")
STANDING_DONE = (
    b"# TASKS DONE\n\n"
    b"## Ship The Initial Tool\n\nAdd the first version of the tool.\n\n"
    b"**Verified:**\n\n- The tool exists as one self-contained file\n\n---\n"
)


def silent(result):
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def snapshot(target):
    return (target / task_list.TODO_NAME).read_bytes()


def todo_of(target):
    return (target / task_list.TODO_NAME).read_text(encoding="utf-8")


def todo_titles(target):
    _, sections = parse_sections(todo_of(target))
    return [section.title for section in sections]


def refused(result, target, before):
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.startswith(b"Error: ") and result.stderr.count(b"\n") == 1
    assert snapshot(target) == before
    return result.stderr.decode("utf-8")


# --- the removal ------------------------------------------------------------------------


def test_remove_takes_the_section_out_and_keeps_the_rest_of_the_list(run_task_list, task_list_dir):
    target = task_list_dir()
    silent(run_task_list("remove", str(target), SECOND))
    assert todo_of(target) == (
        "# TASKS TODO\n\n"
        "## Build The Parser First\n\nWrite the parser that reads the whole file into its heading and sections, so every "
        "later write renders from one model. Verified by its round trip on the golden files.\n\n---\n\n"
        "## Render Unicode — Text As Given\n\nCarry `code`, ${VAR}, $(cmd), &amp; entities, and \"quotes\" through "
        "untouched, including non-ASCII text like zażółć gęślą jaźń.\n\n---\n"
    )


@pytest.mark.parametrize(
    "title, remaining",
    [
        (FIRST, [SECOND, THIRD]),
        (SECOND, [FIRST, THIRD]),
        (THIRD, [FIRST, SECOND]),
    ],
)
def test_remove_takes_out_exactly_the_named_section_wherever_it_stands(run_task_list, task_list_dir, title, remaining):
    target = task_list_dir()
    _, before = parse_sections(todo_of(target))
    silent(run_task_list("remove", str(target), title))
    _, after = parse_sections(todo_of(target))
    assert [section.title for section in after] == remaining
    assert after == [section for section in before if section.title != title]


def test_a_body_with_a_dash_line_goes_whole_and_strands_nothing(run_task_list, task_list_dir):
    target = task_list_dir()
    silent(run_task_list("remove", str(target), SECOND))
    text = todo_of(target)
    assert "A body may hold a separator line" not in text
    assert "The line above stays body text" not in text
    assert todo_titles(target) == [FIRST, THIRD]


def test_a_section_without_its_separator_is_removed_silently(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n## First Task\n\nThe first body.\n## Second Task\n\nThe second body.\n\n---\n")
    silent(run_task_list("remove", str(target), "First Task"))
    assert todo_of(target) == "# TASKS TODO\n\n## Second Task\n\nThe second body.\n\n---\n"


def test_removing_the_last_section_leaves_the_bare_heading(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n## Only Task\n\nThe only body.\n\n---\n")
    silent(run_task_list("remove", str(target), "Only Task"))
    assert todo_of(target) == "# TASKS TODO\n\n"


def test_successive_removals_empty_the_list(run_task_list, task_list_dir):
    target = task_list_dir()
    for title in (THIRD, FIRST, SECOND):
        silent(run_task_list("remove", str(target), title))
    assert todo_of(target) == "# TASKS TODO\n\n"


def test_the_rest_of_the_list_is_rendered_in_the_canonical_layout(run_task_list, task_list_dir):
    drifted = b"stray preamble\n## First Task\nThe first body.\n---\n\n\n\n## Second Task\n\n\nThe second body.\n---"
    target = task_list_dir(todo=drifted)
    silent(run_task_list("remove", str(target), "First Task"))
    assert todo_of(target) == "# TASKS TODO\n\n## Second Task\n\nThe second body.\n\n---\n"


# --- what remove never touches ----------------------------------------------------------


def test_remove_reads_nothing_from_standard_input(run_task_list, task_list_dir):
    target = task_list_dir()
    silent(run_task_list("remove", str(target), FIRST, stdin=b"- a bar the tool never reads\n"))
    assert "a bar the tool never reads" not in todo_of(target)
    assert todo_titles(target) == [SECOND, THIRD]


def test_remove_runs_on_a_terminal_stdin_without_blocking(task_list_dir):
    pty = pytest.importorskip("pty")
    target = task_list_dir()
    master, slave = pty.openpty()
    try:
        result = subprocess.run(
            [sys.executable, "-B", str(TOOL), "remove", str(target), FIRST],
            stdin=slave,
            capture_output=True,
            check=False,
            timeout=30,
        )
    finally:
        os.close(slave)
        os.close(master)
    silent(result)
    assert todo_titles(target) == [SECOND, THIRD]


def test_a_done_file_standing_beside_the_list_is_never_read_or_written(run_task_list, task_list_dir):
    target = task_list_dir()
    (target / DONE_NAME).write_bytes(STANDING_DONE)
    silent(run_task_list("remove", str(target), FIRST))
    assert (target / DONE_NAME).read_bytes() == STANDING_DONE
    assert todo_titles(target) == [SECOND, THIRD]
    assert sorted(path.name for path in target.iterdir()) == [DONE_NAME, task_list.TODO_NAME]


def test_an_unreadable_done_file_beside_the_list_does_not_stop_a_removal(run_task_list, task_list_dir):
    target = task_list_dir()
    (target / DONE_NAME).write_bytes(b"# TASKS DONE\n\n## Bad \xff bytes\n")
    silent(run_task_list("remove", str(target), FIRST))
    assert (target / DONE_NAME).read_bytes() == b"# TASKS DONE\n\n## Bad \xff bytes\n"


def test_no_done_file_is_created(run_task_list, task_list_dir):
    target = task_list_dir()
    silent(run_task_list("remove", str(target), FIRST))
    assert sorted(path.name for path in target.iterdir()) == [task_list.TODO_NAME]


# --- exact-match refusals ---------------------------------------------------------------


@pytest.mark.parametrize("title", ["build the parser first", "  BUILD the   parser\tFIRST  "])
def test_the_title_is_matched_whitespace_folded_and_case_folded(run_task_list, task_list_dir, title):
    target = task_list_dir()
    silent(run_task_list("remove", str(target), title))
    assert todo_titles(target) == [SECOND, THIRD]


@pytest.mark.parametrize("title", ["Build The Parser", "Parser", "Build The Parser First Now", "No Such Task"])
def test_a_partial_or_unknown_title_is_refused(run_task_list, task_list_dir, title):
    target = task_list_dir()
    before = snapshot(target)
    message = refused(run_task_list("remove", str(target), title), target, before)
    assert f'no section of {target / task_list.TODO_NAME} is titled "{title}"' in message
    assert f'"{FIRST}", "{SECOND}", "{THIRD}"' in message


def test_a_title_two_sections_share_is_refused(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n## Twin\n\nOne.\n\n---\n\n## twin\n\nTwo.\n\n---\n")
    before = snapshot(target)
    message = refused(run_task_list("remove", str(target), "Twin"), target, before)
    assert "Error: 2 sections of" in message and "the title names no single section" in message


def test_a_title_only_a_done_file_beside_the_list_holds_is_refused(run_task_list, task_list_dir):
    target = task_list_dir()
    (target / DONE_NAME).write_bytes(STANDING_DONE)
    before = snapshot(target)
    refused(run_task_list("remove", str(target), "Ship The Initial Tool"), target, before)
    assert (target / DONE_NAME).read_bytes() == STANDING_DONE


def test_removing_from_an_empty_list_is_refused(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n")
    before = snapshot(target)
    message = refused(run_task_list("remove", str(target), FIRST), target, before)
    assert "it holds no section" in message
