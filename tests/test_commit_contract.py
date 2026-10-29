"""The output and error contract of the commit tool, driven as a subprocess in a temporary git
repository built on the conftest git fixtures: nothing printed when a commit lands, its one
fixed line on stdout with exit 0 when none of the paths changed, one Error line with exit 1
and nothing committed for every refusal and git failure, argparse's own exit 2 for a
malformed invocation, and never a traceback."""

import pytest

import commit

NO_OP_LINE = "Nothing committed — none of the paths changed."
FILES = {"README.md": b"# A project\n", "notes/a.md": b"a\n"}


@pytest.fixture
def project(repo):
    """A repository whose initial commit holds README.md and notes/a.md."""
    return repo({}, files=dict(FILES))


def head(git, root, environment):
    return git(root, environment, "rev-parse", "HEAD").strip()


def staged(git, root, environment):
    return git(root, environment, "diff", "--cached", "--name-only").split()


def assert_one_error_line(result):
    assert result.returncode == 1
    assert result.stdout == b""
    lines = result.stderr.decode("utf-8").split("\n")
    assert len(lines) == 2 and lines[1] == ""
    assert lines[0].startswith("Error: ")
    assert b"Traceback" not in result.stderr


def assert_usage_error(result):
    assert result.returncode == 2
    assert result.stdout == b""
    assert b"usage: commit.py" in result.stderr
    assert b"Traceback" not in result.stderr


def assert_nothing_recorded(git, root, environment, before):
    assert head(git, root, environment) == before
    assert staged(git, root, environment) == []


# --- malformed invocations --------------------------------------------------------------


def test_no_arguments_is_a_usage_error(run_commit, project):
    result = run_commit(project)
    assert_usage_error(result)
    assert result.stderr.startswith(b"usage: commit.py")


def test_a_missing_subject_is_a_usage_error_with_nothing_recorded(run_commit, project, git, environment):
    before = head(git, project, environment)
    (project / "README.md").write_bytes(b"# A changed project\n")
    result = run_commit(project, "--", "README.md")
    assert_usage_error(result)
    assert b"the following arguments are required: --subject" in result.stderr
    assert_nothing_recorded(git, project, environment, before)


def test_a_subject_flag_without_its_value_is_a_usage_error(run_commit, project):
    result = run_commit(project, "--subject")
    assert_usage_error(result)
    assert b"expected one argument" in result.stderr


def test_paths_given_both_ways_is_a_usage_error_with_nothing_recorded(run_commit, project, git, environment):
    before = head(git, project, environment)
    (project / "README.md").write_bytes(b"# A changed project\n")
    (project / "paths.txt").write_bytes(b"README.md\n")
    result = run_commit(project, "--subject", "Both", "--path-file", "paths.txt", "README.md")
    assert_usage_error(result)
    assert b"not both" in result.stderr
    assert_nothing_recorded(git, project, environment, before)


def test_an_option_overriding_the_schedule_is_a_usage_error(run_commit, project):
    result = run_commit(project, "--subject", "Retry", "--attempts", "3", "README.md")
    assert_usage_error(result)
    assert b"unrecognized arguments: --attempts" in result.stderr


def test_the_parser_takes_no_input_beyond_the_subject_the_body_and_the_paths():
    options = {option for action in commit.build_parser()._actions for option in action.option_strings}
    assert options == {"-h", "--help", "--subject", "--body", "--path-file"}


def test_help_exits_zero_and_names_every_input(run_commit, project):
    result = run_commit(project, "--help")
    assert result.returncode == 0
    for text in (b"--subject SUBJECT", b"--body BODY", b"--path-file FILE", b"PATH"):
        assert text in result.stdout
    assert result.stderr == b""


# --- refusals ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "arguments, reason",
    [
        (("--subject", "No paths"), b"no path is given"),
        (("--subject", "Empty path", "--", ""), b"a path given as an argument is empty"),
        (("--subject", "   ", "--", "README.md"), b"the subject given as --subject is empty"),
        (("--subject", "Two\nlines", "--", "README.md"), b"holds a line break"),
        (("--subject", "Missing file", "--path-file", "absent.txt"), b"does not exist"),
    ],
    ids=["no-path", "empty-path", "empty-subject", "multi-line-subject", "missing-path-file"],
)
def test_a_refused_input_is_one_error_line_with_nothing_recorded(run_commit, project, git, environment, arguments, reason):
    before = head(git, project, environment)
    (project / "README.md").write_bytes(b"# A changed project\n")
    result = run_commit(project, *arguments)
    assert_one_error_line(result)
    assert reason in result.stderr
    assert_nothing_recorded(git, project, environment, before)


@pytest.mark.parametrize(
    "data, reason",
    [(b"", b"names no path"), (b"\n\n\n", b"names no path"), (b"README\xff.md\n", b"is not UTF-8 text")],
    ids=["empty", "blank-lines-only", "not-utf8"],
)
def test_a_path_file_naming_no_usable_path_is_refused(run_commit, project, git, environment, data, reason):
    before = head(git, project, environment)
    (project / "README.md").write_bytes(b"# A changed project\n")
    (project / "paths.txt").write_bytes(data)
    result = run_commit(project, "--subject", "Bad path file", "--path-file", "paths.txt")
    assert_one_error_line(result)
    assert reason in result.stderr
    assert_nothing_recorded(git, project, environment, before)


def test_a_git_failure_is_one_error_line_carrying_gits_message(run_commit, tmp_path):
    plain = tmp_path / "plain"
    plain.mkdir()
    (plain / "README.md").write_bytes(b"# Not a repository\n")
    result = run_commit(plain, "--subject", "Outside", "--", "README.md")
    assert_one_error_line(result)
    assert result.stderr.startswith(b"Error: git status exited 128: ")
    assert b"not a git repository" in result.stderr
    assert b"attempts" not in result.stderr


def test_an_operating_system_failure_is_an_error_line_not_a_traceback(run_commit, project, environment, tmp_path):
    empty = tmp_path / "no-git"
    empty.mkdir()
    (project / "README.md").write_bytes(b"# A changed project\n")
    result = run_commit(project, "--subject", "No git", "--", "README.md", env=dict(environment, PATH=str(empty)))
    assert_one_error_line(result)


# --- success ----------------------------------------------------------------------------


def test_a_commit_that_lands_prints_nothing(run_commit, project, git, environment):
    before = head(git, project, environment)
    (project / "README.md").write_bytes(b"# A changed project\n")
    result = run_commit(project, "--subject", "Landed: README", "--", "README.md")
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    assert head(git, project, environment) != before
    assert git(project, environment, "log", "-1", "--format=%s").strip() == "Landed: README"


def test_a_no_op_prints_its_one_fixed_line_on_stdout_and_exits_zero(run_commit, project, git, environment):
    before = head(git, project, environment)
    result = run_commit(project, "--subject", "Nothing: README", "--", "README.md", "notes/a.md")
    assert (result.returncode, result.stderr) == (0, b"")
    assert result.stdout == (NO_OP_LINE + "\n").encode("utf-8")
    assert commit.NO_OP_LINE == NO_OP_LINE
    assert_nothing_recorded(git, project, environment, before)


def test_a_no_op_through_a_path_file_prints_the_same_line(run_commit, project, git, environment):
    before = head(git, project, environment)
    (project / "paths.txt").write_bytes(b"README.md\nnotes/a.md\n")
    result = run_commit(project, "--subject", "Nothing: from file", "--path-file", "paths.txt")
    assert (result.returncode, result.stdout, result.stderr) == (0, (NO_OP_LINE + "\n").encode("utf-8"), b"")
    assert_nothing_recorded(git, project, environment, before)
