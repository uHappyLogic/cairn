"""The commit tool records exactly the paths it is given, with those paths as the commit's
pathspec: every other staged change stays staged and out of the commit, every other change in
the tree stays where it is, the paths come as arguments or line-exact from a path file, git
reads each one literally relative to the working directory, and the commit carries the given
subject and, when one is given, the body."""

import pytest

FILES = {"README.md": b"# A project\n", "notes/a.md": b"a\n", "notes/b.md": b"b\n"}


@pytest.fixture
def project(repo):
    """A repository whose initial commit holds README.md, notes/a.md, and notes/b.md."""
    return repo({}, files=dict(FILES))


def committed(git, root, environment):
    """The paths the HEAD commit changed, as git names them."""
    output = git(root, environment, "show", "-z", "--name-only", "--format=", "HEAD")
    return sorted(name for name in output.split("\0") if name.strip())


def staged(git, root, environment):
    output = git(root, environment, "diff", "-z", "--cached", "--name-only")
    return sorted(name for name in output.split("\0") if name)


def message(git, root, environment):
    """The HEAD commit's whole message, exactly as recorded."""
    raw = git(root, environment, "cat-file", "commit", "HEAD")
    return raw.split("\n\n", 1)[1]


def assert_landed(result):
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")


def test_the_commit_carries_only_the_named_paths_and_leaves_other_staged_changes_staged(run_commit, project, git, environment):
    (project / "notes" / "a.md").write_bytes(b"a changed\n")
    (project / "notes" / "b.md").write_bytes(b"b changed\n")
    git(project, environment, "add", "--", "notes/b.md")
    (project / "README.md").write_bytes(b"# An edited project\n")
    (project / "untracked.txt").write_bytes(b"left alone\n")
    result = run_commit(project, "--subject", "Only: a", "--", "notes/a.md")
    assert_landed(result)
    assert committed(git, project, environment) == ["notes/a.md"]
    assert staged(git, project, environment) == ["notes/b.md"]
    status = git(project, environment, "status", "--porcelain").splitlines()
    assert sorted(status) == sorted([" M README.md", "M  notes/b.md", "?? untracked.txt"])


def test_a_new_a_modified_and_a_deleted_path_are_all_recorded(run_commit, project, git, environment):
    (project / "notes" / "a.md").write_bytes(b"a changed\n")
    (project / "notes" / "b.md").unlink()
    (project / "notes" / "c.md").write_bytes(b"c\n")
    result = run_commit(project, "--subject", "Three kinds", "--", "notes/a.md", "notes/b.md", "notes/c.md")
    assert_landed(result)
    status = git(project, environment, "show", "--name-status", "--format=", "HEAD").split("\n")
    assert sorted(line for line in status if line) == ["A\tnotes/c.md", "D\tnotes/b.md", "M\tnotes/a.md"]
    assert git(project, environment, "status", "--porcelain") == ""


def test_named_paths_that_did_not_change_are_carried_harmlessly(run_commit, project, git, environment):
    (project / "notes" / "a.md").write_bytes(b"a changed\n")
    result = run_commit(project, "--subject", "Some changed", "--", "README.md", "notes/a.md", "notes/b.md")
    assert_landed(result)
    assert committed(git, project, environment) == ["notes/a.md"]


def test_the_paths_are_read_relative_to_the_working_directory(run_commit, project, git, environment):
    (project / "notes" / "a.md").write_bytes(b"a changed\n")
    (project / "README.md").write_bytes(b"# An edited project\n")
    result = run_commit(project / "notes", "--subject", "From a subdirectory", "--", "a.md")
    assert_landed(result)
    assert committed(git, project, environment) == ["notes/a.md"]


def test_a_path_file_is_read_one_whole_line_per_path(run_commit, project, git, environment):
    (project / "notes" / "a.md").write_bytes(b"a changed\n")
    (project / "notes" / "b.md").write_bytes(b"b changed\n")
    (project / "notes" / "with two  spaces.md").write_bytes(b"new\n")
    (project / "README.md").write_bytes(b"# An edited project\n")
    (project / "paths.txt").write_bytes(b"notes/a.md\n\nnotes/with two  spaces.md\nnotes/b.md")
    result = run_commit(project, "--subject", "From a path file", "--path-file", "paths.txt")
    assert_landed(result)
    assert committed(git, project, environment) == ["notes/a.md", "notes/b.md", "notes/with two  spaces.md"]
    status = git(project, environment, "status", "--porcelain").splitlines()
    assert sorted(status) == sorted([" M README.md", "?? paths.txt"])


@pytest.mark.parametrize("through", ["arguments", "path-file"])
def test_a_path_holding_a_glob_character_names_that_one_file_only(run_commit, project, git, environment, through, tmp_path):
    (project / "notes" / "[draft].md").write_bytes(b"draft\n")
    (project / "notes" / "d.md").write_bytes(b"matched by the pattern, never by the path\n")
    if through == "arguments":
        result = run_commit(project, "--subject", "Literal", "--", "notes/[draft].md")
    else:
        path_file = tmp_path / "paths.txt"
        path_file.write_bytes(b"notes/[draft].md\n")
        result = run_commit(project, "--subject", "Literal", "--path-file", str(path_file))
    assert_landed(result)
    assert committed(git, project, environment) == ["notes/[draft].md"]
    assert git(project, environment, "status", "--porcelain", "--", "notes/d.md") == "?? notes/d.md\n"


def test_the_subject_and_the_body_are_recorded_as_given(run_commit, project, git, environment):
    (project / "README.md").write_bytes(b"# An edited project\n")
    body = "First option — its rationale.\nSecond option — another rationale."
    result = run_commit(project, "--subject", "Recommendation-annotation: milestone_07_slug", "--body", body, "--", "README.md")
    assert_landed(result)
    assert message(git, project, environment) == "Recommendation-annotation: milestone_07_slug\n\n" + body + "\n"


@pytest.mark.parametrize("body", [None, "", "  \n "], ids=["absent", "empty", "whitespace"])
def test_no_body_or_an_empty_one_makes_a_subject_only_commit(run_commit, project, git, environment, body):
    (project / "README.md").write_bytes(b"# An edited project\n")
    extra = () if body is None else ("--body", body)
    result = run_commit(project, "--subject", "Task-completion: A Task", *extra, "--", "README.md")
    assert_landed(result)
    assert message(git, project, environment) == "Task-completion: A Task\n"
