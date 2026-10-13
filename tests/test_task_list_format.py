"""The task files' canonical form: parse and render are inverse on the golden task files, and
every write renders the whole file in the one canonical layout, normalizing blank-line drift,
a damaged or missing preamble, and an unterminated section on the first write."""

from pathlib import Path

import pytest

import task_list
from task_list import DONE_HEADING, TODO_HEADING, TaskFile, parse_sections, render_file

FIXTURES = Path(__file__).resolve().parent / "fixtures"
GOLDEN = [
    ("task_list_todo.md", TODO_HEADING, False),
    ("task_list_done.md", DONE_HEADING, True),
]


def rendered(text, heading, with_bar):
    _, sections = parse_sections(text, with_bar)
    return render_file(TaskFile(heading, sections, with_bar))


def silent(result):
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def todo_of(target):
    return (target / task_list.TODO_NAME).read_text(encoding="utf-8")


def done_of(target):
    return (target / task_list.DONE_NAME).read_text(encoding="utf-8")


# --- the golden files -------------------------------------------------------------------


@pytest.mark.parametrize("name, heading, with_bar", GOLDEN)
def test_parse_render_round_trip_is_the_identity_on_a_golden_file(name, heading, with_bar):
    text = (FIXTURES / name).read_text(encoding="utf-8")
    assert rendered(text, heading, with_bar) == text


@pytest.mark.parametrize("name, heading, with_bar", GOLDEN)
def test_golden_files_use_lf_and_end_in_a_separator_and_one_newline(name, heading, with_bar):
    data = (FIXTURES / name).read_bytes()
    assert b"\r" not in data
    assert data.startswith(heading.encode("utf-8") + b"\n\n")
    assert data.endswith(b"\n---\n")


def test_the_golden_files_parse_into_their_sections():
    _, todo = parse_sections((FIXTURES / "task_list_todo.md").read_text(encoding="utf-8"), with_bar=False)
    assert [section.title for section in todo] == [
        "Build The Parser First",
        "Keep A Body Separator Line",
        "Render Unicode — Text As Given",
    ]
    assert all(section.bar is None for section in todo)
    _, done = parse_sections((FIXTURES / "task_list_done.md").read_text(encoding="utf-8"), with_bar=True)
    assert [section.title for section in done] == ["Ship The Initial Tool", "Record A Prose Bar"]
    assert done[0].bar == "- The tool exists as one self-contained file\n- Both test runs pass"


def test_an_untouched_section_survives_a_write_byte_for_byte(run_task_list, task_list_dir):
    target = task_list_dir()
    golden = (FIXTURES / "task_list_todo.md").read_text(encoding="utf-8")
    silent(run_task_list("insert", str(target), "Appended Task", "--end", stdin=b"An appended body.\n"))
    assert todo_of(target) == golden + "\n## Appended Task\n\nAn appended body.\n\n---\n"


def test_an_empty_task_file_renders_as_its_heading_and_one_blank_line():
    assert render_file(TaskFile(TODO_HEADING, [], with_bar=False)) == "# TASKS TODO\n\n"
    assert render_file(TaskFile(DONE_HEADING, [], with_bar=True)) == "# TASKS DONE\n\n"


def test_a_move_out_of_a_one_section_list_leaves_the_bare_heading(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n## Only Task\n\nThe only body.\n\n---\n", done=b"# TASKS DONE\n\n")
    silent(run_task_list("move", str(target), "Only Task", stdin=b"- it was done\n"))
    assert todo_of(target) == "# TASKS TODO\n\n"
    assert done_of(target) == "# TASKS DONE\n\n## Only Task\n\nThe only body.\n\n**Verified:**\n\n- it was done\n\n---\n"


# --- normalization on the first write ---------------------------------------------------

DRIFTED_TODO = (
    "# TASKS TODO\n"
    "## First Task\n"
    "The first body.\n"
    "---\n"
    "\n\n\n"
    "## Second Task\n"
    "\n\n"
    "The second body,\n"
    "on two lines.\n"
    "\n\n"
    "---"
)
CANONICAL_TODO = (
    "# TASKS TODO\n\n"
    "## First Task\n\nThe first body.\n\n---\n\n"
    "## Second Task\n\nThe second body,\non two lines.\n\n---\n"
)


def test_blank_line_drift_is_normalized_in_process():
    assert rendered(DRIFTED_TODO, TODO_HEADING, False) == CANONICAL_TODO
    assert rendered(DRIFTED_TODO.replace("\n", "\r\n"), TODO_HEADING, False) == CANONICAL_TODO


def test_blank_line_drift_is_normalized_silently_on_the_first_write(run_task_list, task_list_dir):
    target = task_list_dir(todo=DRIFTED_TODO.encode("utf-8"))
    silent(run_task_list("insert", str(target), "Third Task", "--end", stdin=b"The third body.\n"))
    assert todo_of(target) == CANONICAL_TODO + "\n## Third Task\n\nThe third body.\n\n---\n"


def test_blank_line_drift_in_the_done_file_is_normalized_by_a_move(run_task_list, task_list_dir):
    drifted = "# TASKS DONE\n## Old Task\nOld body.\n**Verified:**\n- old criterion\n---\n\n\n"
    target = task_list_dir(done=drifted.encode("utf-8"))
    silent(run_task_list("move", str(target), "Build The Parser First", stdin=b"- parsed\n"))
    assert done_of(target).startswith(
        "# TASKS DONE\n\n## Old Task\n\nOld body.\n\n**Verified:**\n\n- old criterion\n\n---\n\n## Build The Parser First\n\n"
    )


@pytest.mark.parametrize(
    "preamble",
    [
        "",
        "#  tasks todo damaged\n\n",
        "# TASKS TODO\n\nA note someone left above the first section.\n\n",
        "Stray text with no heading at all.\n",
        "# TASKS DONE\n\n",
    ],
)
def test_a_damaged_or_missing_preamble_is_replaced_by_the_fixed_heading(run_task_list, task_list_dir, preamble):
    target = task_list_dir(todo=(preamble + "## First Task\n\nThe first body.\n\n---\n").encode("utf-8"))
    silent(run_task_list("insert", str(target), "Second Task", "--end", stdin=b"The second body.\n"))
    assert todo_of(target) == "# TASKS TODO\n\n## First Task\n\nThe first body.\n\n---\n\n## Second Task\n\nThe second body.\n\n---\n"


def test_a_damaged_done_preamble_is_replaced_by_its_fixed_heading(run_task_list, task_list_dir):
    target = task_list_dir(done=b"# Tasks done (old)\n\nnotes\n")
    silent(run_task_list("move", str(target), "Build The Parser First", stdin=b"- parsed\n"))
    assert done_of(target).startswith("# TASKS DONE\n\n## Build The Parser First\n\n")


def test_an_unterminated_section_gains_its_separator_on_the_first_write(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n## First Task\n\nThe first body.\n\n## Second Task\n\nThe second body.\n")
    silent(run_task_list("insert", str(target), "Third Task", "--after", "Second Task", stdin=b"The third body.\n"))
    assert todo_of(target) == (
        "# TASKS TODO\n\n"
        "## First Task\n\nThe first body.\n\n---\n\n"
        "## Second Task\n\nThe second body.\n\n---\n\n"
        "## Third Task\n\nThe third body.\n\n---\n"
    )


def test_an_unterminated_done_entry_gains_its_separator_on_the_first_move(run_task_list, task_list_dir):
    target = task_list_dir(done=b"# TASKS DONE\n\n## Old Task\n\nOld body.\n\n**Verified:**\n\n- old criterion\n")
    silent(run_task_list("move", str(target), "Build The Parser First", stdin=b"- parsed\n"))
    assert done_of(target).startswith("# TASKS DONE\n\n## Old Task\n\nOld body.\n\n**Verified:**\n\n- old criterion\n\n---\n\n## Build")


@pytest.mark.parametrize(
    "text, heading, with_bar",
    [
        (DRIFTED_TODO, TODO_HEADING, False),
        ("stray\n## Old Task\nOld body.\n**Verified:**\n- old criterion\n\n\n## Next Task\nNext body.\n**Verified:**\nprose\n---\n", DONE_HEADING, True),
    ],
)
def test_rendering_a_drifted_file_is_idempotent(text, heading, with_bar):
    once = rendered(text, heading, with_bar)
    assert rendered(once, heading, with_bar) == once
