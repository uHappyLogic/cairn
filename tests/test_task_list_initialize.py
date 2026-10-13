"""The initialize subcommand: TASKS_TODO.md replaced whole by its heading and the ordered list
read from standard input in the file's own section form, with no flag and no refusal for
what the file held before, silent on success; every section validated first, so any refusal
is one Error line with both task files byte-for-byte unchanged."""

import pytest

import task_list

LIST = (
    b"## Derive The First Task\n\nThe first brief.\n\n---\n\n"
    b"## Derive The Second Task\n\nThe second brief,\nwrapped.\n\n---\n\n"
    b"## Derive The Third Task\n\nThe third brief.\n\n---\n"
)
CANONICAL = (
    "# TASKS TODO\n\n"
    "## Derive The First Task\n\nThe first brief.\n\n---\n\n"
    "## Derive The Second Task\n\nThe second brief,\nwrapped.\n\n---\n\n"
    "## Derive The Third Task\n\nThe third brief.\n\n---\n"
)


def silent(result):
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def snapshot(target):
    return (target / task_list.TODO_NAME).read_bytes(), (target / task_list.DONE_NAME).read_bytes()


def todo_of(target):
    return (target / task_list.TODO_NAME).read_text(encoding="utf-8")


def refused(result, target, before):
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.startswith(b"Error: ") and result.stderr.count(b"\n") == 1
    assert snapshot(target) == before
    return result.stderr.decode("utf-8")


def test_initialize_replaces_a_fresh_file_with_the_heading_and_the_list_in_order(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n", done=b"# TASKS DONE\n\n")
    silent(run_task_list("initialize", str(target), stdin=LIST))
    assert todo_of(target) == CANONICAL
    assert (target / task_list.DONE_NAME).read_bytes() == b"# TASKS DONE\n\n"


def test_initialize_replaces_whatever_the_file_held_with_no_flag(run_task_list, task_list_dir):
    target = task_list_dir()
    done_before = (target / task_list.DONE_NAME).read_bytes()
    silent(run_task_list("initialize", str(target), stdin=LIST))
    assert todo_of(target) == CANONICAL
    assert "Build The Parser First" not in todo_of(target)
    assert (target / task_list.DONE_NAME).read_bytes() == done_before


def test_initialize_keeps_a_title_the_done_file_already_holds(run_task_list, task_list_dir):
    target = task_list_dir()
    silent(run_task_list("initialize", str(target), stdin=b"## Ship The Initial Tool\n\nFollow-up work reuses a done title.\n\n---\n"))
    assert todo_of(target) == "# TASKS TODO\n\n## Ship The Initial Tool\n\nFollow-up work reuses a done title.\n\n---\n"


def test_initialize_normalizes_the_list_into_the_canonical_layout(run_task_list, task_list_dir):
    target = task_list_dir()
    drifted = b"\n\n## Derive The First Task\nThe first brief.\n---\n## Derive The Second Task\n\n\nThe second brief,\nwrapped.\n\n\n---\n\n\n\n## Derive The Third Task\nThe third brief."
    silent(run_task_list("initialize", str(target), stdin=drifted))
    assert todo_of(target) == CANONICAL


def test_initialize_keeps_a_body_dash_line_and_writes_a_missing_last_separator(run_task_list, task_list_dir):
    target = task_list_dir()
    silent(run_task_list("initialize", str(target), stdin=b"## Only Task\n\nAbove.\n\n---\n\nBelow."))
    assert todo_of(target) == "# TASKS TODO\n\n## Only Task\n\nAbove.\n\n---\n\nBelow.\n\n---\n"


def test_initialize_writes_bodies_verbatim_without_checking_the_task_format(run_task_list, task_list_dir):
    target = task_list_dir()
    body = "a lower-case title-less brief with `code`, ${VAR}, $(cmd), &amp; — and four sentences. Two. Three. Four."
    silent(run_task_list("initialize", str(target), stdin=f"## x\n\n{body}\n\n---\n".encode("utf-8")))
    assert todo_of(target) == f"# TASKS TODO\n\n## x\n\n{body}\n\n---\n"


@pytest.mark.parametrize(
    "stdin, reason",
    [
        (b"## Same Title\n\nOne.\n\n---\n\n## same   TITLE\n\nTwo.\n\n---\n", "fold to the same title"),
        (b"## First Task\n\nOne.\n\n---\n\n## \n\nTwo.\n\n---\n", "section 2 of the task list on standard input has an empty title"),
        (b"## First Task\n\nOne.\n\n---\n\n## Empty Body\n\n\n---\n", 'the section titled "Empty Body" on standard input has an empty body'),
        (b"A preamble line.\n\n## First Task\n\nOne.\n\n---\n", "holds text before its first"),
        (b"Just prose, no heading.\n", "holds text before its first"),
        (b"", 'holds no "## " section'),
        (b"\n\n  \n", 'holds no "## " section'),
    ],
)
def test_initialize_refuses_the_whole_list_and_leaves_both_files_unchanged(run_task_list, task_list_dir, stdin, reason):
    target = task_list_dir()
    before = snapshot(target)
    message = refused(run_task_list("initialize", str(target), stdin=stdin), target, before)
    assert reason in message


def test_a_refusal_late_in_the_list_writes_none_of_the_earlier_sections(run_task_list, task_list_dir):
    target = task_list_dir(todo=b"# TASKS TODO\n\n")
    before = snapshot(target)
    stdin = LIST + b"\n## Derive The First Task\n\nRepeated.\n\n---\n"
    message = refused(run_task_list("initialize", str(target), stdin=stdin), target, before)
    assert 'titles two sections "Derive The First Task" and "Derive The First Task"' in message


def test_initialize_refuses_a_missing_todo_file(run_task_list, task_list_dir):
    target = task_list_dir()
    (target / task_list.TODO_NAME).unlink()
    result = run_task_list("initialize", str(target), stdin=LIST)
    assert result.returncode == 1
    assert b"does not exist" in result.stderr
    assert sorted(path.name for path in target.iterdir()) == [task_list.DONE_NAME]
