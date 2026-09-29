"""define_milestone.py slug derivation and title folding: the first five surviving words of
the folded title, each ASCII-folded, lowercased, apostrophe-free, and hyphen-joined inside."""

import pytest

import define_milestone

GOAL = b"Ship it.\n"


@pytest.mark.parametrize(
    ("title", "slug"),
    [
        ("Mechanical milestone definition", "mechanical-milestone-definition"),
        ("One two three four five six seven", "one-two-three-four-five"),
        ("Public Release Preparation", "public-release-preparation"),
        ("Don't Panic", "dont-panic"),
        ("Don’t Panic", "dont-panic"),
        ("Café crème brûlée", "cafe-creme-brulee"),
        ("Multi-Host build", "multi-host-build"),
        ("a/b  c", "a-b-c"),
        ("--edge-- words", "edge-words"),
        ("Add the 3 tools to it now", "add-the-3-tools-to"),
        ("Python 3.9 floor", "python-3-9-floor"),
        ("Fix: the & build", "fix-the-build"),
        ("— — one — two three four five six", "one-two-three-four-five"),
        ("Straße", "stra-e"),
        ("ＡＢＣ wide", "abc-wide"),
    ],
)
def test_derive_slug(title, slug):
    assert define_milestone.derive_slug(title) == slug


def test_words_that_clean_to_nothing_are_filled_from_the_words_that_follow():
    assert define_milestone.derive_slug("! one ? two & three # four % five six") == "one-two-three-four-five"


def test_a_title_no_word_of_which_survives_is_refused():
    with pytest.raises(define_milestone.ToolError) as caught:
        define_milestone.derive_slug("!!! --- —")
    assert "slug" in str(caught.value)


def test_the_slug_names_the_directory_and_the_title_the_heading(run_define, workspace):
    root = workspace()
    title = "Café's   Multi-Host\n  work: über fast, really fast"
    result = run_define("--title", title, stdin=GOAL, cwd=root)
    assert result.returncode == 0, result.stderr
    directory = root / "milestones" / "milestone_01_cafes-multi-host-work-uber-fast"
    requirements = (directory / "requirements.md").read_text(encoding="utf-8")
    assert requirements.startswith("# Milestone 1: Café's Multi-Host work: über fast, really fast\n\n")


def test_the_title_keeps_its_case_and_punctuation_and_has_no_length_cap(run_define, workspace):
    root = workspace()
    title = "A Very LONG title, with (punctuation) & symbols; " + "word " * 60
    result = run_define("--title", title, stdin=GOAL, cwd=root)
    assert result.returncode == 0, result.stderr
    requirements = (root / "milestones" / "milestone_01_a-very-long-title-with" / "requirements.md").read_text(encoding="utf-8")
    assert requirements.splitlines()[0] == "# Milestone 1: " + " ".join(title.split())


@pytest.mark.parametrize(("value", "folded"), [("  a \n\t b  ", "a b"), ("x", "x"), ("line\r\nbreak", "line break")])
def test_read_title_folds_whitespace(value, folded):
    assert define_milestone.read_title(value) == folded


@pytest.mark.parametrize("value", ["", "   ", " \n\t \n "])
def test_an_empty_title_is_refused(run_define, workspace, value):
    root = workspace()
    result = run_define("--title", value, stdin=GOAL, cwd=root)
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr == b"Error: the title given as --title is empty\n"
    assert list((root / "milestones").iterdir()) == []


def test_a_title_without_slug_material_is_refused_end_to_end(run_define, workspace):
    root = workspace()
    result = run_define("--title", "?! ...", stdin=GOAL, cwd=root)
    assert result.returncode == 1
    assert result.stdout == b""
    assert result.stderr.startswith(b"Error: no word of the title")
    assert result.stderr.count(b"\n") == 1
    assert list((root / "milestones").iterdir()) == []
