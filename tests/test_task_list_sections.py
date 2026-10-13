"""Where a task section ends: a "---" line is the section's separator only when it is the one
standing directly before the next heading or the end of the file (only blank lines between),
every other "---" line is body text, every column-0 "## " line is a heading, and a section
with no qualifying "---" ends at the next heading or the end of the file — in bodies and
**Verified:** bars alike, through every later re-parse."""

import pytest

import task_list
from task_list import parse_sections


def silent(result):
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def titles_and_bodies(text, with_bar=False):
    _, sections = parse_sections(text, with_bar)
    return [(section.title, section.body) for section in sections]


def todo_of(target):
    return (target / task_list.TODO_NAME).read_text(encoding="utf-8")


def done_of(target):
    return (target / task_list.DONE_NAME).read_text(encoding="utf-8")


# --- the separator rule, in process -----------------------------------------------------


def test_a_separator_directly_before_the_next_heading_ends_the_section():
    text = "# TASKS TODO\n\n## A\n\nBody A.\n\n---\n\n## B\n\nBody B.\n\n---\n"
    assert titles_and_bodies(text) == [("A", "Body A."), ("B", "Body B.")]


def test_a_separator_directly_before_the_end_of_the_file_ends_the_section():
    for ending in ("---", "---\n", "---\n\n\n", "--- \n"):
        assert titles_and_bodies("## A\n\nBody A.\n\n" + ending) == [("A", "Body A.")]


def test_a_dash_line_followed_by_prose_is_body_text():
    text = "## A\n\nBefore.\n\n---\n\nAfter.\n\n---\n"
    assert titles_and_bodies(text) == [("A", "Before.\n\n---\n\nAfter.")]


def test_only_the_last_of_several_dash_lines_before_a_heading_is_the_separator():
    text = "## A\n\nBody.\n\n---\n\n---\n\n## B\n\nBody B.\n\n---\n"
    assert titles_and_bodies(text) == [("A", "Body.\n\n---"), ("B", "Body B.")]


def test_a_section_without_a_separator_ends_at_the_next_heading_or_the_end_of_the_file():
    text = "## A\n\nBody A.\n\n## B\n\nBody B.\n"
    assert titles_and_bodies(text) == [("A", "Body A."), ("B", "Body B.")]


def test_every_column_zero_heading_opens_a_section_even_inside_a_code_fence():
    text = "## A\n\n```\n## Not exempt\n```\n\n---\n"
    assert titles_and_bodies(text) == [("A", "```"), ("Not exempt", "```")]


def test_an_indented_heading_or_a_deeper_heading_is_body_text():
    text = "## A\n\n  ## indented\n### Deeper\n\n---\n"
    assert titles_and_bodies(text) == [("A", "  ## indented\n### Deeper")]


def test_a_dash_line_in_a_bar_followed_by_prose_stays_in_the_bar():
    text = "# TASKS DONE\n\n## A\n\nBody.\n\n**Verified:**\n\n- one\n\n---\n\nMore bar.\n\n---\n"
    _, sections = parse_sections(text, with_bar=True)
    assert [(section.title, section.body, section.bar) for section in sections] == [("A", "Body.", "- one\n\n---\n\nMore bar.")]


def test_the_last_verified_line_splits_body_from_bar():
    text = "## A\n\nBody naming **Verified:** inline.\n\n**Verified:**\n\nfirst\n\n**Verified:**\n\n- real bar\n\n---\n"
    _, sections = parse_sections(text, with_bar=True)
    assert (sections[0].body, sections[0].bar) == ("Body naming **Verified:** inline.\n\n**Verified:**\n\nfirst", "- real bar")


# --- through the subcommands and later re-parses ----------------------------------------


def test_a_body_dash_line_written_by_insert_survives_every_later_reparse(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n## First Task\n\nThe first body.\n\n---\n")
    silent(run_task_list("insert", str(target), "Second Task", "--before", "First Task", stdin=b"Before the line.\n\n---\n\nAfter the line.\n"))
    silent(run_task_list("insert", str(target), "Third Task", "--end", stdin=b"The third body.\n"))
    silent(run_task_list("move", str(target), "First Task", stdin=b"- done\n"))
    assert todo_of(target) == (
        "# TASKS TODO\n\n"
        "## Second Task\n\nBefore the line.\n\n---\n\nAfter the line.\n\n---\n\n"
        "## Third Task\n\nThe third body.\n\n---\n"
    )


def test_a_body_ending_in_a_dash_line_keeps_it_as_body_on_the_insert_and_strands_nothing(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n## First Task\n\nThe first body.\n\n---\n")
    silent(run_task_list("insert", str(target), "Dashed Task", "--before", "First Task", stdin=b"Ends in a rule.\n\n---\n"))
    assert todo_of(target) == (
        "# TASKS TODO\n\n"
        "## Dashed Task\n\nEnds in a rule.\n\n---\n\n---\n\n"
        "## First Task\n\nThe first body.\n\n---\n"
    )
    silent(run_task_list("insert", str(target), "Last Task", "--end", stdin=b"The last body.\n"))
    assert "## Dashed Task\n\nEnds in a rule.\n\n---\n\n---\n\n## First Task" in todo_of(target)


def test_a_body_heading_line_written_by_insert_becomes_a_heading_on_the_next_reparse(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n## First Task\n\nThe first body.\n\n---\n")
    silent(run_task_list("insert", str(target), "Second Task", "--end", stdin=b"Some prose.\n\n## Looks Like A Heading\n\nMore prose.\n"))
    assert todo_of(target).endswith("## Second Task\n\nSome prose.\n\n## Looks Like A Heading\n\nMore prose.\n\n---\n")
    silent(run_task_list("insert", str(target), "Third Task", "--end", stdin=b"The third body.\n"))
    assert todo_of(target) == (
        "# TASKS TODO\n\n"
        "## First Task\n\nThe first body.\n\n---\n\n"
        "## Second Task\n\nSome prose.\n\n---\n\n"
        "## Looks Like A Heading\n\nMore prose.\n\n---\n\n"
        "## Third Task\n\nThe third body.\n\n---\n"
    )


def test_a_bar_dash_line_written_by_move_survives_the_next_move(run_task_list, task_list_dir):
    target = task_list_dir(done=b"# TASKS DONE\n\n")
    silent(run_task_list("move", str(target), "Build The Parser First", stdin=b"- one\n\n---\n\n- two\n"))
    silent(run_task_list("move", str(target), "Keep A Body Separator Line", stdin=b"- three\n"))
    _, sections = parse_sections(done_of(target), with_bar=True)
    assert [(section.title, section.bar) for section in sections] == [
        ("Build The Parser First", "- one\n\n---\n\n- two"),
        ("Keep A Body Separator Line", "- three"),
    ]
    assert sections[1].body.startswith("A body may hold a separator line of its own")
    assert "\n---\n\nThe line above stays body text" in sections[1].body


@pytest.mark.parametrize("anchor", ["--before", "--after"])
def test_an_insert_next_to_an_unterminated_section_never_runs_into_it(run_task_list, task_list_dir, anchor):
    target = task_list_dir(todo=b"# TASKS TODO\n\n## First Task\n\nThe first body.\n## Last Task\n\nThe last body.")
    silent(run_task_list("insert", str(target), "New Task", anchor, "First Task", stdin=b"The new body.\n"))
    _, sections = parse_sections(todo_of(target), with_bar=False)
    order = ["New Task", "First Task", "Last Task"] if anchor == "--before" else ["First Task", "New Task", "Last Task"]
    assert [section.title for section in sections] == order
    assert todo_of(target).count("\n---\n") == 3
