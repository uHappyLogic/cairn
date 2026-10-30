"""define_milestone.py placement: the required --at scope, normalized lexically and printed in its
canonical repo-relative form, the root spelled "." or "./"; an empty, absolute, or climbing scope
and one missing from the working tree or not a directory refused on one Error line naming it as
given; only the scope's milestones/ container created when missing; and no number, the
directory named by its slug alone."""

import os

import pytest

import define_milestone

GOAL = b"Ship it.\n"


def printed(result):
    """The two printed lines of a successful call: (subject, path)."""
    assert result.returncode == 0, result.stderr
    assert result.stderr == b""
    subject, path = result.stdout.decode("utf-8").splitlines()
    return subject, path


def tree(root):
    """Every path under root, relative and sorted, directories with a trailing slash."""
    entries = []
    for directory, names, files in os.walk(root):
        relative = os.path.relpath(directory, root)
        for name in names:
            entries.append(os.path.normpath(os.path.join(relative, name)) + "/")
        for name in files:
            entries.append(os.path.normpath(os.path.join(relative, name)))
    return sorted(entries)


# --- the canonical path -----------------------------------------------------------------


@pytest.mark.parametrize("scope", [".", "./", ".//", "./.", "pkg/..", "pkg/sub/../.."])
def test_every_spelling_of_the_root_prints_the_root_container_path(run_define, workspace, scope):
    root = workspace(root=False)
    (root / "pkg" / "sub").mkdir(parents=True)
    subject, path = printed(run_define("--at", scope, "--title", "Root work", stdin=GOAL, cwd=root))
    assert (subject, path) == ("Milestone-definition: milestones/root-work/", "milestones/root-work/")
    assert (root / "milestones" / "root-work" / "requirements.md").is_file()


@pytest.mark.parametrize(
    "scope",
    [
        "packages/ledger",
        "packages/ledger/",
        "./packages/ledger",
        "packages//ledger",
        "./packages/./ledger//",
        "packages/other/../ledger",
    ],
)
def test_every_spelling_of_a_package_prints_one_canonical_path(run_define, workspace, scope):
    root = workspace(root=False)
    (root / "packages" / "ledger").mkdir(parents=True)
    (root / "packages" / "other").mkdir()
    subject, path = printed(run_define("--at", scope, "--title", "Ledger import", stdin=GOAL, cwd=root))
    assert path == "packages/ledger/milestones/ledger-import/"
    assert subject == "Milestone-definition: " + path
    assert (root / path / "requirements.md").is_file()


def test_the_printed_path_is_the_directory_the_files_were_written_into(run_define, workspace):
    root = workspace(root=False)
    (root / "a" / "b" / "c").mkdir(parents=True)
    _, path = printed(run_define("--at", "a/b/c", "--title", "Deep core", stdin=GOAL, cwd=root))
    assert path == "a/b/c/milestones/deep-core/"
    assert sorted(entry.name for entry in (root / path).iterdir()) == ["TASKS_TODO.md", "open_questions.xml", "requirements.md"]
    assert tree(root) == [
        "a/",
        "a/b/",
        "a/b/c/",
        "a/b/c/milestones/",
        "a/b/c/milestones/deep-core/",
        "a/b/c/milestones/deep-core/TASKS_TODO.md",
        "a/b/c/milestones/deep-core/open_questions.xml",
        "a/b/c/milestones/deep-core/requirements.md",
    ]


@pytest.mark.parametrize(
    ("value", "scope"),
    [
        (".", "."),
        ("./", "."),
        ("pkg", "pkg"),
        ("pkg/", "pkg"),
        ("./pkg", "pkg"),
        ("pkg//sub///", "pkg/sub"),
        ("./pkg/./sub/.", "pkg/sub"),
        ("pkg/..", "."),
        ("a/b/../c", "a/c"),
        ("a space/b", "a space/b"),
    ],
)
def test_normalize_scope_collapses_lexically(value, scope):
    assert define_milestone.normalize_scope(value) == scope


def test_normalization_reads_no_filesystem(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert define_milestone.normalize_scope("nowhere/../at/./all/") == "at/all"
    assert list(tmp_path.iterdir()) == []


# --- refusals -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("scope", "reason"),
    [
        ("", "the scope given as --at is empty"),
        ("/", "the scope / given as --at is an absolute path; name a directory relative to the workspace root"),
        ("/tmp", "the scope /tmp given as --at is an absolute path; name a directory relative to the workspace root"),
        ("//pkg", "the scope //pkg given as --at is an absolute path; name a directory relative to the workspace root"),
        ("..", "the scope .. given as --at climbs out of the workspace root with .."),
        ("../", "the scope ../ given as --at climbs out of the workspace root with .."),
        ("../elsewhere", "the scope ../elsewhere given as --at climbs out of the workspace root with .."),
        ("pkg/../..", "the scope pkg/../.. given as --at climbs out of the workspace root with .."),
        ("./pkg/../../pkg", "the scope ./pkg/../../pkg given as --at climbs out of the workspace root with .."),
    ],
)
def test_an_empty_absolute_or_climbing_scope_is_refused_naming_it_as_given(run_define, workspace, scope, reason):
    root = workspace(root=False)
    (root / "pkg").mkdir()
    result = run_define("--at", scope, "--title", "First", stdin=GOAL, cwd=root)
    assert (result.returncode, result.stdout) == (1, b"")
    assert result.stderr == f"Error: {reason}\n".encode("utf-8")
    assert tree(root) == ["pkg/"]


@pytest.mark.parametrize("scope", ["missing", "missing/", "./pkg/missing", "pkg//missing/./"])
def test_a_scope_missing_from_the_working_tree_is_refused_naming_it_as_given(run_define, workspace, scope):
    root = workspace(root=False)
    (root / "pkg").mkdir()
    result = run_define("--at", scope, "--title", "First", stdin=GOAL, cwd=root)
    assert (result.returncode, result.stdout) == (1, b"")
    assert result.stderr == (
        f"Error: the scope {scope} given as --at does not exist in the working tree; nothing was written\n".encode("utf-8")
    )
    assert tree(root) == ["pkg/"]


def test_a_scope_naming_a_file_is_refused_naming_it_as_given(run_define, workspace):
    root = workspace(root=False)
    (root / "pkg").mkdir()
    (root / "pkg" / "module.py").write_bytes(b"code")
    result = run_define("--at", "./pkg/module.py", "--title", "First", stdin=GOAL, cwd=root)
    assert (result.returncode, result.stdout) == (1, b"")
    assert result.stderr == b"Error: the scope ./pkg/module.py given as --at is not a directory; nothing was written\n"
    assert tree(root) == ["pkg/", "pkg/module.py"]


def test_a_scope_that_is_a_dangling_symlink_is_refused(run_define, workspace, tmp_path):
    root = workspace(root=False)
    (root / "gone").symlink_to(tmp_path / "missing")
    result = run_define("--at", "gone", "--title", "First", stdin=GOAL, cwd=root)
    assert (result.returncode, result.stdout) == (1, b"")
    assert result.stderr == b"Error: the scope gone given as --at is not a directory; nothing was written\n"
    assert not (tmp_path / "missing").exists()


def test_a_scope_that_is_a_symlink_to_a_directory_is_accepted(run_define, workspace, tmp_path):
    root = workspace(root=False)
    target = tmp_path / "real"
    target.mkdir()
    (root / "linked").symlink_to(target, target_is_directory=True)
    _, path = printed(run_define("--at", "linked", "--title", "Linked core", stdin=GOAL, cwd=root))
    assert path == "linked/milestones/linked-core/"
    assert (target / "milestones" / "linked-core" / "requirements.md").is_file()


def test_the_scope_is_never_created(run_define, workspace):
    root = workspace(root=False)
    result = run_define("--at", "packages/new-core", "--title", "First", stdin=GOAL, cwd=root)
    assert result.returncode == 1
    assert list(root.iterdir()) == []


# --- the container ------------------------------------------------------------------------


def test_a_missing_root_container_is_created(run_define, workspace):
    root = workspace(root=False)
    _, path = printed(run_define("--at", ".", "--title", "First", stdin=GOAL, cwd=root))
    assert path == "milestones/first/"
    assert tree(root) == [
        "milestones/",
        "milestones/first/",
        "milestones/first/TASKS_TODO.md",
        "milestones/first/open_questions.xml",
        "milestones/first/requirements.md",
    ]


def test_a_missing_package_container_is_created_and_nothing_else(run_define, workspace):
    root = workspace(root=False)
    (root / "pkg").mkdir()
    (root / "pkg" / "module.py").write_bytes(b"code")
    printed(run_define("--at", "pkg", "--title", "First", stdin=GOAL, cwd=root))
    assert tree(root) == [
        "pkg/",
        "pkg/milestones/",
        "pkg/milestones/first/",
        "pkg/milestones/first/TASKS_TODO.md",
        "pkg/milestones/first/open_questions.xml",
        "pkg/milestones/first/requirements.md",
        "pkg/module.py",
    ]
    assert not (root / "milestones").exists()


def test_an_existing_container_is_kept_with_everything_in_it(run_define, workspace):
    root = workspace("live-one", files=("answer_decision_principles.md",))
    printed(run_define("--at", ".", "--title", "Second", stdin=GOAL, cwd=root))
    assert sorted(entry.name for entry in (root / "milestones").iterdir()) == [
        "answer_decision_principles.md",
        "live-one",
        "second",
    ]


@pytest.mark.parametrize("scope", [".", "pkg"])
def test_a_file_where_the_container_should_be_is_refused(run_define, workspace, scope):
    root = workspace(root=False)
    (root / "pkg").mkdir()
    container = root / "milestones" if scope == "." else root / "pkg" / "milestones"
    container.write_bytes(b"not a directory")
    label = "milestones/" if scope == "." else "pkg/milestones/"
    result = run_define("--at", scope, "--title", "First", stdin=GOAL, cwd=root)
    assert (result.returncode, result.stdout) == (1, b"")
    assert result.stderr == f"Error: {label} exists and is not a directory; nothing was written\n".encode("utf-8")
    assert container.read_bytes() == b"not a directory"


# --- no number ----------------------------------------------------------------------------


def test_the_directory_is_named_by_the_slug_alone(run_define, workspace):
    root = workspace("milestone_07_seven", "milestone_99_last")
    subject, path = printed(run_define("--at", ".", "--title", "Next", stdin=GOAL, cwd=root))
    assert (subject, path) == ("Milestone-definition: milestones/next/", "milestones/next/")
    assert sorted(entry.name for entry in (root / "milestones").iterdir()) == ["milestone_07_seven", "milestone_99_last", "next"]


def test_the_heading_carries_the_title_alone(run_define, workspace):
    root = workspace("milestone_06_six")
    printed(run_define("--at", ".", "--title", "Seventh", stdin=GOAL, cwd=root))
    requirements = (root / "milestones" / "seventh" / "requirements.md").read_text(encoding="utf-8")
    assert requirements.startswith("# Seventh\n\n## Goal\n")


def test_two_scopes_take_two_milestones(run_define, workspace):
    root = workspace(root=False)
    (root / "app").mkdir()
    (root / "lib").mkdir()
    first = printed(run_define("--at", "app", "--title", "Parser rework", stdin=GOAL, cwd=root))
    second = printed(run_define("--at", "lib", "--title", "Parser rework", stdin=GOAL, cwd=root))
    third = printed(run_define("--at", ".", "--title", "Parser rework", stdin=GOAL, cwd=root))
    assert [path for _, path in (first, second, third)] == [
        "app/milestones/parser-rework/",
        "lib/milestones/parser-rework/",
        "milestones/parser-rework/",
    ]
