"""define_milestone.py conflicts: the exclusive create of the milestone directory is the only
check, anything already at that path refuses the call before a write, and a missing
milestones root is refused without being created."""

import io
import sys

import define_milestone

GOAL = b"Ship it.\n"
CONFLICT = b"Error: milestones/milestone_02_same-title already exists; nothing was written\n"


def entries(root):
    return sorted(path.name for path in (root / "milestones").iterdir())


def test_a_file_at_the_computed_path_is_a_conflict(run_define, workspace):
    root = workspace("milestone_01_one", files=("milestone_02_same-title",))
    blocker = root / "milestones" / "milestone_02_same-title"
    blocker.write_bytes(b"keep me")
    result = run_define("--title", "Same title", stdin=GOAL, cwd=root)
    assert (result.returncode, result.stdout, result.stderr) == (1, b"", CONFLICT)
    assert blocker.read_bytes() == b"keep me"
    assert entries(root) == ["milestone_01_one", "milestone_02_same-title"]


def test_a_dangling_symlink_at_the_computed_path_is_a_conflict(run_define, workspace, tmp_path):
    root = workspace("milestone_01_one")
    link = root / "milestones" / "milestone_02_same-title"
    link.symlink_to(tmp_path / "missing")
    result = run_define("--title", "Same title", stdin=GOAL, cwd=root)
    assert (result.returncode, result.stdout, result.stderr) == (1, b"", CONFLICT)
    assert link.is_symlink() and not (tmp_path / "missing").exists()
    assert entries(root) == ["milestone_01_one", "milestone_02_same-title"]


def test_a_symlink_to_a_file_at_the_computed_path_is_a_conflict(run_define, workspace, tmp_path):
    root = workspace("milestone_01_one")
    target = tmp_path / "target.txt"
    target.write_bytes(b"untouched")
    (root / "milestones" / "milestone_02_same-title").symlink_to(target)
    result = run_define("--title", "Same title", stdin=GOAL, cwd=root)
    assert (result.returncode, result.stdout, result.stderr) == (1, b"", CONFLICT)
    assert target.read_bytes() == b"untouched"


def test_a_directory_at_the_computed_path_is_a_conflict(workspace, monkeypatch, capsys):
    # A counted directory always holds a number below the computed one, so only a directory
    # appearing between the scan and the create can collide; pin the scan to stage that race.
    root = workspace("milestone_01_one")
    existing = root / "milestones" / "milestone_02_same-title"
    existing.mkdir()
    (existing / "requirements.md").write_bytes(b"theirs")
    monkeypatch.chdir(root)
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(GOAL)))
    monkeypatch.setattr(define_milestone, "next_number", lambda root: 2)
    assert define_milestone.main(["--title", "Same title"]) == 1
    captured = capsys.readouterr()
    assert (captured.out, captured.err) == ("", CONFLICT.decode("utf-8"))
    assert sorted(path.name for path in existing.iterdir()) == ["requirements.md"]
    assert (existing / "requirements.md").read_bytes() == b"theirs"


def test_a_slug_reused_under_another_number_is_allowed(run_define, workspace):
    root = workspace("milestone_01_same-title")
    result = run_define("--title", "Same title", stdin=GOAL, cwd=root)
    assert result.returncode == 0, result.stderr
    assert entries(root) == ["milestone_01_same-title", "milestone_02_same-title"]


def test_a_number_held_twice_is_not_a_conflict(run_define, workspace):
    root = workspace("milestone_03_a", "milestone_03_b")
    result = run_define("--title", "Next", stdin=GOAL, cwd=root)
    assert result.returncode == 0, result.stderr
    assert entries(root) == ["milestone_03_a", "milestone_03_b", "milestone_04_next"]


def test_a_missing_milestones_root_is_refused_and_not_created(run_define, workspace):
    root = workspace(root=False)
    result = run_define("--title", "First", stdin=GOAL, cwd=root)
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == (
        b"Error: the milestones root milestones/ does not exist in the working directory; "
        b"run /init-milestone-base-workflow first\n"
    )
    assert list(root.iterdir()) == []


def test_a_file_where_the_root_should_be_is_refused(run_define, workspace):
    root = workspace(root=False)
    (root / "milestones").write_bytes(b"not a directory")
    result = run_define("--title", "First", stdin=GOAL, cwd=root)
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.startswith(b"Error: the milestones root milestones/ does not exist")
    assert (root / "milestones").read_bytes() == b"not a directory"
