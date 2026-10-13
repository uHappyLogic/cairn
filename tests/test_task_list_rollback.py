"""The move's failure state, exercised in-process by a monkeypatched replace: both new contents
are rendered before either file is touched, TASKS_DONE.md is replaced first and TASKS_TODO.md
second, and a failed second replace writes TASKS_DONE.md's original bytes back so the call
ends with one Error line, exit 1, and both files as they were; only when that restore fails
too does the superset remain, and the Error line says so."""

import io
import os
import sys

import pytest

import task_list

TITLE = "Build The Parser First"
BAR = b"- The parser reads the whole file\n"


def snapshot(target):
    return (target / task_list.TODO_NAME).read_bytes(), (target / task_list.DONE_NAME).read_bytes()


def run_move(monkeypatch, target, title=TITLE, bar=BAR):
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(bar)))
    return task_list.main(["move", str(target), title])


@pytest.fixture
def replaces(monkeypatch):
    """Record every os.replace the tool makes, failing those whose (target name, nth time that
    target is replaced) pair is listed: replaces({("TASKS_TODO.md", 1)}) -> the call log."""

    def install(failing):
        real = os.replace
        calls = []

        def replace(source, destination, *args, **kwargs):
            name = os.path.basename(str(destination))
            calls.append(name)
            if (name, calls.count(name)) in failing:
                raise PermissionError(13, "Permission denied", str(destination))
            return real(source, destination, *args, **kwargs)

        monkeypatch.setattr(os, "replace", replace)
        return calls

    return install


def test_a_failed_todo_replace_restores_the_done_file_and_ends_with_both_files_unchanged(capsys, monkeypatch, replaces, task_list_dir):
    target = task_list_dir()
    before = snapshot(target)
    calls = replaces({(task_list.TODO_NAME, 1)})
    assert run_move(monkeypatch, target) == 1
    assert calls == [task_list.DONE_NAME, task_list.TODO_NAME, task_list.DONE_NAME]
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == f"Error: Permission denied: {target / task_list.TODO_NAME}\n"
    assert snapshot(target) == before
    assert sorted(path.name for path in target.iterdir()) == [task_list.DONE_NAME, task_list.TODO_NAME]


def test_a_failed_restore_reports_the_superset_in_the_one_error_line(capsys, monkeypatch, replaces, task_list_dir):
    target = task_list_dir()
    todo_before, done_before = snapshot(target)
    calls = replaces({(task_list.TODO_NAME, 1), (task_list.DONE_NAME, 2)})
    assert run_move(monkeypatch, target) == 1
    assert calls == [task_list.DONE_NAME, task_list.TODO_NAME, task_list.DONE_NAME]
    captured = capsys.readouterr()
    assert captured.out == ""
    lines = captured.err.split("\n")
    assert len(lines) == 2 and lines[1] == ""
    assert lines[0] == (
        f"Error: replacing {target / task_list.TODO_NAME} failed (Permission denied: {target / task_list.TODO_NAME}) "
        f"and restoring {target / task_list.DONE_NAME} failed too (Permission denied: {target / task_list.DONE_NAME}); "
        f'the section "{TITLE}" now stands in both files'
    )
    todo_after, done_after = snapshot(target)
    assert todo_after == todo_before
    _, todo_sections = task_list.parse_sections(todo_after.decode("utf-8"), with_bar=False)
    _, done_sections = task_list.parse_sections(done_after.decode("utf-8"), with_bar=True)
    assert todo_sections[0].title == TITLE
    assert (done_sections[-1].title, done_sections[-1].body, done_sections[-1].bar) == (
        TITLE,
        todo_sections[0].body,
        "- The parser reads the whole file",
    )
    assert done_after.startswith(done_before)
    assert sorted(path.name for path in target.iterdir()) == [task_list.DONE_NAME, task_list.TODO_NAME]


def test_a_failed_first_replace_touches_neither_file(capsys, monkeypatch, replaces, task_list_dir):
    target = task_list_dir()
    before = snapshot(target)
    calls = replaces({(task_list.DONE_NAME, 1)})
    assert run_move(monkeypatch, target) == 1
    assert calls == [task_list.DONE_NAME]
    assert capsys.readouterr().err == f"Error: Permission denied: {target / task_list.DONE_NAME}\n"
    assert snapshot(target) == before
    assert sorted(path.name for path in target.iterdir()) == [task_list.DONE_NAME, task_list.TODO_NAME]


def test_both_contents_are_rendered_before_either_file_is_touched(capsys, monkeypatch, task_list_dir):
    target = task_list_dir()
    before = snapshot(target)
    order = []
    real_render = task_list.render_file
    real_write = task_list.write_bytes

    def render(task_file):
        order.append(("render", task_file.heading))
        return real_render(task_file)

    def write(path, data):
        order.append(("write", os.path.basename(path)))
        return real_write(path, data)

    monkeypatch.setattr(task_list, "render_file", render)
    monkeypatch.setattr(task_list, "write_bytes", write)
    assert run_move(monkeypatch, target) == 0
    assert capsys.readouterr() == ("", "")
    assert order == [
        ("render", task_list.DONE_HEADING),
        ("render", task_list.TODO_HEADING),
        ("write", task_list.DONE_NAME),
        ("write", task_list.TODO_NAME),
    ]
    assert snapshot(target) != before


def test_a_rerun_after_a_clean_failure_is_an_ordinary_move(capsys, monkeypatch, replaces, task_list_dir):
    target = task_list_dir()
    replaces({(task_list.TODO_NAME, 1)})
    assert run_move(monkeypatch, target) == 1
    capsys.readouterr()
    monkeypatch.undo()
    assert run_move(monkeypatch, target) == 0
    assert capsys.readouterr() == ("", "")
    todo, done = (data.decode("utf-8") for data in snapshot(target))
    assert f"## {TITLE}" not in todo
    assert done.count(f"## {TITLE}") == 1
    assert done.endswith("**Verified:**\n\n- The parser reads the whole file\n\n---\n")
