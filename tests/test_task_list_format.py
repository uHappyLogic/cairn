"""The task list's canonical form: parse and render are inverse on the golden task list, and
every write renders the whole file in the one canonical layout, normalizing blank-line drift,
a damaged or missing preamble, and an unterminated section on the first write."""

from pathlib import Path

import pytest

import task_list
from task_list import TODO_HEADING, TaskFile, parse_sections, render_file

FIXTURES = Path(__file__).resolve().parent / "fixtures"
GOLDEN = "task_list_todo.md"


def rendered(text):
    _, sections = parse_sections(text)
    return render_file(TaskFile(TODO_HEADING, sections))


def silent(result):
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def todo_of(target):
    return (target / task_list.TODO_NAME).read_text(encoding="utf-8")


# --- the golden file --------------------------------------------------------------------


def test_parse_render_round_trip_is_the_identity_on_the_golden_file():
    text = (FIXTURES / GOLDEN).read_text(encoding="utf-8")
    assert rendered(text) == text


def test_the_golden_file_uses_lf_and_ends_in_a_separator_and_one_newline():
    data = (FIXTURES / GOLDEN).read_bytes()
    assert b"\r" not in data
    assert data.startswith(TODO_HEADING.encode("utf-8") + b"\n\n")
    assert data.endswith(b"\n---\n")


def test_the_golden_file_parses_into_its_sections():
    _, todo = parse_sections((FIXTURES / GOLDEN).read_text(encoding="utf-8"))
    assert [section.title for section in todo] == [
        "Build The Parser First",
        "Keep A Body Separator Line",
        "Render Unicode — Text As Given",
    ]


def test_an_untouched_section_survives_a_write_byte_for_byte(run_task_list, task_list_dir):
    target = task_list_dir()
    golden = (FIXTURES / "task_list_todo.md").read_text(encoding="utf-8")
    silent(run_task_list("insert", str(target), "Appended Task", "--end", stdin=b"An appended body.\n"))
    assert todo_of(target) == golden + "\n## Appended Task\n\nAn appended body.\n\n---\n"


def test_an_empty_task_list_renders_as_its_heading_and_one_blank_line():
    assert render_file(TaskFile(TODO_HEADING, [])) == "# TASKS TODO\n\n"


def test_a_removal_from_a_one_section_list_leaves_the_bare_heading(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n## Only Task\n\nThe only body.\n\n---\n")
    silent(run_task_list("remove", str(target), "Only Task"))
    assert todo_of(target) == "# TASKS TODO\n\n"


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
    assert rendered(DRIFTED_TODO) == CANONICAL_TODO
    assert rendered(DRIFTED_TODO.replace("\n", "\r\n")) == CANONICAL_TODO


def test_blank_line_drift_is_normalized_silently_on_the_first_write(run_task_list, task_list_dir):
    target = task_list_dir(todo=DRIFTED_TODO.encode("utf-8"))
    silent(run_task_list("insert", str(target), "Third Task", "--end", stdin=b"The third body.\n"))
    assert todo_of(target) == CANONICAL_TODO + "\n## Third Task\n\nThe third body.\n\n---\n"


def test_blank_line_drift_is_normalized_silently_by_a_removal(run_task_list, task_list_dir):
    target = task_list_dir(todo=DRIFTED_TODO.encode("utf-8"))
    silent(run_task_list("remove", str(target), "First Task"))
    assert todo_of(target) == "# TASKS TODO\n\n## Second Task\n\nThe second body,\non two lines.\n\n---\n"


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


def test_a_damaged_preamble_is_replaced_by_the_fixed_heading_on_a_removal(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# Tasks todo (old)\n\nnotes\n## First Task\n\nOne.\n\n---\n\n## Second Task\n\nTwo.\n\n---\n")
    silent(run_task_list("remove", str(target), "First Task"))
    assert todo_of(target) == "# TASKS TODO\n\n## Second Task\n\nTwo.\n\n---\n"


def test_an_unterminated_section_gains_its_separator_on_the_first_write(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n## First Task\n\nThe first body.\n\n## Second Task\n\nThe second body.\n")
    silent(run_task_list("insert", str(target), "Third Task", "--after", "Second Task", stdin=b"The third body.\n"))
    assert todo_of(target) == (
        "# TASKS TODO\n\n"
        "## First Task\n\nThe first body.\n\n---\n\n"
        "## Second Task\n\nThe second body.\n\n---\n\n"
        "## Third Task\n\nThe third body.\n\n---\n"
    )


def test_an_unterminated_section_gains_its_separator_on_a_removal(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n## First Task\n\nThe first body.\n\n## Second Task\n\nThe second body.\n\n## Third Task\n\nThe third body.\n")
    silent(run_task_list("remove", str(target), "Second Task"))
    assert todo_of(target) == (
        "# TASKS TODO\n\n"
        "## First Task\n\nThe first body.\n\n---\n\n"
        "## Third Task\n\nThe third body.\n\n---\n"
    )


@pytest.mark.parametrize(
    "text",
    [
        DRIFTED_TODO,
        "stray\n## Old Task\nOld body.\n\n\n## Next Task\nNext body.\n---\n\n---\n",
    ],
)
def test_rendering_a_drifted_file_is_idempotent(text):
    once = rendered(text)
    assert rendered(once) == once
