"""define_milestone.py conflicts: the exclusive create of the milestone directory is the only
check, anything already at that path refuses the call before a write, a title whose slug a
milestone of the same scope already holds is refused, and the same slug stands in two scopes."""

import io
import sys

import define_milestone

GOAL = b"Ship it.\n"
CONFLICT = b"Error: milestones/same-title already exists; nothing was written\n"


def entries(root):
    return sorted(path.name for path in (root / "milestones").iterdir())


def test_a_file_at_the_computed_path_is_a_conflict(run_define, workspace):
    root = workspace("one", files=("same-title",))
    blocker = root / "milestones" / "same-title"
    blocker.write_bytes(b"keep me")
    result = run_define("--at", ".", "--title", "Same title", stdin=GOAL, cwd=root)
    assert (result.returncode, result.stdout, result.stderr) == (1, b"", CONFLICT)
    assert blocker.read_bytes() == b"keep me"
    assert entries(root) == ["one", "same-title"]


def test_a_dangling_symlink_at_the_computed_path_is_a_conflict(run_define, workspace, tmp_path):
    root = workspace("one")
    link = root / "milestones" / "same-title"
    link.symlink_to(tmp_path / "missing")
    result = run_define("--at", ".", "--title", "Same title", stdin=GOAL, cwd=root)
    assert (result.returncode, result.stdout, result.stderr) == (1, b"", CONFLICT)
    assert link.is_symlink() and not (tmp_path / "missing").exists()
    assert entries(root) == ["one", "same-title"]


def test_a_symlink_to_a_file_at_the_computed_path_is_a_conflict(run_define, workspace, tmp_path):
    root = workspace("one")
    target = tmp_path / "target.txt"
    target.write_bytes(b"untouched")
    (root / "milestones" / "same-title").symlink_to(target)
    result = run_define("--at", ".", "--title", "Same title", stdin=GOAL, cwd=root)
    assert (result.returncode, result.stdout, result.stderr) == (1, b"", CONFLICT)
    assert target.read_bytes() == b"untouched"


def test_a_directory_at_the_computed_path_is_a_conflict(run_define, workspace):
    root = workspace("one")
    existing = root / "milestones" / "same-title"
    existing.mkdir()
    (existing / "requirements.md").write_bytes(b"theirs")
    result = run_define("--at", ".", "--title", "Same title", stdin=GOAL, cwd=root)
    assert (result.returncode, result.stdout, result.stderr) == (1, b"", CONFLICT)
    assert sorted(path.name for path in existing.iterdir()) == ["requirements.md"]
    assert (existing / "requirements.md").read_bytes() == b"theirs"


def test_defining_the_same_title_twice_in_one_scope_is_a_conflict(run_define, workspace):
    root = workspace()
    first = run_define("--at", ".", "--title", "Same title", stdin=GOAL, cwd=root)
    assert first.returncode == 0, first.stderr
    requirements = (root / "milestones" / "same-title" / "requirements.md").read_bytes()
    second = run_define("--at", "./", "--title", "Same  TITLE", stdin=b"Another goal.\n", cwd=root)
    assert (second.returncode, second.stdout, second.stderr) == (1, b"", CONFLICT)
    assert (root / "milestones" / "same-title" / "requirements.md").read_bytes() == requirements
    assert entries(root) == ["same-title"]


def test_a_conflict_in_a_package_names_the_package_path(run_define, workspace):
    root = workspace(root=False)
    (root / "pkg" / "milestones" / "same-title").mkdir(parents=True)
    result = run_define("--at", "pkg/", "--title", "Same title", stdin=GOAL, cwd=root)
    assert (result.returncode, result.stdout) == (1, b"")
    assert result.stderr == b"Error: pkg/milestones/same-title already exists; nothing was written\n"
    assert list((root / "pkg" / "milestones" / "same-title").iterdir()) == []


def test_a_conflict_raced_in_after_the_container_was_created_removes_the_container(workspace, monkeypatch, capsys):
    root = workspace(root=False)
    real = define_milestone.create_container

    def create_then_race(container):
        made = real(container)
        (root / "milestones" / "same-title").mkdir()
        return made

    monkeypatch.chdir(root)
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(GOAL)))
    monkeypatch.setattr(define_milestone, "create_container", create_then_race)
    assert define_milestone.main(["--at", ".", "--title", "Same title"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == (
        "Error: milestones/same-title already exists; nothing was written; "
        "the cleanup could not remove milestones\n"
    )
    assert entries(root) == ["same-title"]


def test_the_same_slug_in_two_scopes_is_not_a_conflict(run_define, workspace):
    root = workspace("same-title")
    (root / "pkg").mkdir()
    result = run_define("--at", "pkg", "--title", "Same title", stdin=GOAL, cwd=root)
    assert result.returncode == 0, result.stderr
    assert entries(root) == ["same-title"]
    assert (root / "pkg" / "milestones" / "same-title" / "requirements.md").is_file()


def test_a_numbered_directory_holding_the_slug_is_not_a_conflict(run_define, workspace):
    root = workspace("milestone_03_same-title")
    result = run_define("--at", ".", "--title", "Same title", stdin=GOAL, cwd=root)
    assert result.returncode == 0, result.stderr
    assert entries(root) == ["milestone_03_same-title", "same-title"]
