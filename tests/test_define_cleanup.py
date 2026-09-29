"""define_milestone.py failure cleanup: a failure after the milestone directory exists removes
exactly what the call created, in reverse creation order, with unlink and non-recursive
rmdir, and a removal that fails stops the cleanup and is named in the one Error line."""

import errno
import io
import os
import sys

import pytest

import define_milestone

GOAL = b"Ship it.\n"
DIRECTORY = os.path.join("milestones", "milestone_01_first")


def no_space(path):
    return OSError(errno.ENOSPC, "No space left on device", path)


@pytest.fixture
def define_in_process(workspace, monkeypatch, capsys):
    """Run main() in a fresh workspace with the goal on stdin: returns (status, out, err, root)."""

    def run(title="First"):
        root = workspace()
        monkeypatch.chdir(root)
        monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(GOAL)))
        status = define_milestone.main(["--title", title])
        captured = capsys.readouterr()
        return status, captured.out, captured.err, root

    return run


@pytest.fixture
def fail_on(monkeypatch):
    """Make the write of the named file fail, running `before` first when given."""

    def install(name, before=None, error=no_space):
        real = define_milestone.write_new_file

        def write(path, text):
            if os.path.basename(path) == name:
                if before is not None:
                    before(path)
                raise error(path)
            real(path, text)

        monkeypatch.setattr(define_milestone, "write_new_file", write)

    return install


@pytest.fixture
def removals(monkeypatch):
    """Record every unlink and rmdir, in call order, as (operation, path) pairs."""
    calls = []
    real_unlink, real_rmdir = os.unlink, os.rmdir

    def unlink(path, *args, **kwargs):
        calls.append(("unlink", os.fspath(path)))
        return real_unlink(path, *args, **kwargs)

    def rmdir(path, *args, **kwargs):
        calls.append(("rmdir", os.fspath(path)))
        return real_rmdir(path, *args, **kwargs)

    monkeypatch.setattr(os, "unlink", unlink)
    monkeypatch.setattr(os, "rmdir", rmdir)
    return calls


def test_a_failure_on_the_third_file_removes_what_was_written_in_reverse(define_in_process, fail_on, removals):
    fail_on("TASKS_TODO.md")
    status, out, err, root = define_in_process()
    assert (status, out) == (1, "")
    assert err == f"Error: No space left on device: {os.path.join(DIRECTORY, 'TASKS_TODO.md')}\n"
    assert removals == [
        ("unlink", os.path.join(DIRECTORY, "requirements.md")),
        ("unlink", os.path.join(DIRECTORY, "open_questions.xml")),
        ("rmdir", DIRECTORY),
    ]
    assert list((root / "milestones").iterdir()) == []


def test_a_failure_on_the_first_file_removes_only_the_directory(define_in_process, fail_on, removals):
    fail_on("open_questions.xml")
    status, out, err, root = define_in_process()
    assert (status, out) == (1, "")
    assert err.startswith("Error: No space left on device: ")
    assert removals == [("rmdir", DIRECTORY)]
    assert list((root / "milestones").iterdir()) == []


def test_a_failure_on_the_last_file_removes_all_three_written_files(define_in_process, fail_on, removals):
    fail_on("TASKS_DONE.md")
    status, out, err, root = define_in_process()
    assert (status, out) == (1, "")
    assert [path for _, path in removals] == [
        os.path.join(DIRECTORY, "TASKS_TODO.md"),
        os.path.join(DIRECTORY, "requirements.md"),
        os.path.join(DIRECTORY, "open_questions.xml"),
        DIRECTORY,
    ]
    assert list((root / "milestones").iterdir()) == []


def test_the_milestones_root_is_never_removed(define_in_process, fail_on):
    fail_on("requirements.md")
    status, _, _, root = define_in_process()
    assert status == 1
    assert (root / "milestones").is_dir()


def test_a_failed_rename_leaves_no_temporary_file(define_in_process, monkeypatch):
    real_replace = os.replace

    def replace(source, target):
        if os.path.basename(target) == "requirements.md":
            raise OSError(errno.EIO, "Input/output error", target)
        return real_replace(source, target)

    monkeypatch.setattr(os, "replace", replace)
    status, out, err, root = define_in_process()
    assert (status, out) == (1, "")
    assert err == f"Error: Input/output error: {os.path.join(DIRECTORY, 'requirements.md')}\n"
    assert list((root / "milestones").iterdir()) == []


def test_a_stray_file_stops_the_cleanup_and_is_left_in_place(define_in_process, fail_on):
    def drop_stray(path):
        with open(os.path.join(os.path.dirname(path), "stray.txt"), "wb") as handle:
            handle.write(b"someone else's")

    fail_on("TASKS_TODO.md", before=drop_stray)
    status, out, err, root = define_in_process()
    assert (status, out) == (1, "")
    assert err == (
        f"Error: No space left on device: {os.path.join(DIRECTORY, 'TASKS_TODO.md')}; "
        f"the cleanup could not remove {DIRECTORY}\n"
    )
    directory = root / DIRECTORY
    assert sorted(path.name for path in directory.iterdir()) == ["stray.txt"]
    assert (directory / "stray.txt").read_bytes() == b"someone else's"


def test_a_removal_that_fails_stops_the_cleanup_and_names_every_path_left(define_in_process, fail_on, monkeypatch):
    real_unlink = os.unlink

    def unlink(path, *args, **kwargs):
        if os.path.basename(os.fspath(path)) == "requirements.md":
            raise PermissionError(errno.EACCES, "Permission denied", path)
        return real_unlink(path, *args, **kwargs)

    fail_on("TASKS_TODO.md")
    monkeypatch.setattr(os, "unlink", unlink)
    status, out, err, root = define_in_process()
    assert (status, out) == (1, "")
    left = ", ".join([DIRECTORY, os.path.join(DIRECTORY, "open_questions.xml"), os.path.join(DIRECTORY, "requirements.md")])
    assert err == (
        f"Error: No space left on device: {os.path.join(DIRECTORY, 'TASKS_TODO.md')}; the cleanup could not remove {left}\n"
    )
    assert sorted(path.name for path in (root / DIRECTORY).iterdir()) == ["open_questions.xml", "requirements.md"]


def test_an_already_missing_path_does_not_stop_the_cleanup(define_in_process, fail_on):
    fail_on("TASKS_TODO.md", before=lambda path: os.remove(os.path.join(os.path.dirname(path), "requirements.md")))
    status, out, err, root = define_in_process()
    assert (status, out) == (1, "")
    assert "cleanup" not in err
    assert list((root / "milestones").iterdir()) == []


def test_an_unexpected_exception_is_cleaned_up_and_reported(define_in_process, fail_on):
    fail_on("requirements.md", error=lambda path: ValueError("bad\nvalue"))
    status, out, err, root = define_in_process()
    assert (status, out) == (1, "")
    assert err == "Error: ValueError: bad value\n"
    assert list((root / "milestones").iterdir()) == []


def test_an_interrupt_is_cleaned_up_and_propagated(define_in_process, fail_on):
    fail_on("requirements.md", error=lambda path: KeyboardInterrupt())
    with pytest.raises(KeyboardInterrupt):
        define_in_process()
    assert list(os.scandir("milestones")) == []
