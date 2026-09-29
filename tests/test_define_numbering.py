"""define_milestone.py numbering: max-plus-one over the milestone directories directly under
the root, leading zeros stripped, at least two digits, and every other entry skipped."""

GOAL = b"Ship it.\n"


def defined_name(result):
    assert result.returncode == 0, result.stderr
    subject, directory = result.stdout.decode("utf-8").splitlines()
    return subject.split(": ", 1)[1]


def test_a_cold_start_is_milestone_01(run_define, workspace):
    root = workspace()
    result = run_define("--title", "First", stdin=GOAL, cwd=root)
    assert defined_name(result) == "milestone_01_first"
    assert (root / "milestones" / "milestone_01_first").is_dir()


def test_the_number_is_the_maximum_plus_one_regardless_of_gaps(run_define, workspace):
    root = workspace("milestone_01_a", "milestone_05_b", "milestone_03_c")
    assert defined_name(run_define("--title", "Next", stdin=GOAL, cwd=root)) == "milestone_06_next"


def test_leading_zeros_are_stripped_before_comparing(run_define, workspace):
    root = workspace("milestone_009_nine", "milestone_10_ten")
    assert defined_name(run_define("--title", "Next", stdin=GOAL, cwd=root)) == "milestone_11_next"


def test_a_padded_number_counts_as_its_integer(run_define, workspace):
    root = workspace("milestone_007_seven")
    assert defined_name(run_define("--title", "Next", stdin=GOAL, cwd=root)) == "milestone_08_next"


def test_the_number_is_padded_to_two_digits(run_define, workspace):
    root = workspace("milestone_08_eight")
    assert defined_name(run_define("--title", "Next", stdin=GOAL, cwd=root)) == "milestone_09_next"


def test_ninety_nine_is_followed_by_one_hundred(run_define, workspace):
    root = workspace("milestone_99_last-two-digit")
    result = run_define("--title", "Next", stdin=GOAL, cwd=root)
    assert defined_name(result) == "milestone_100_next"
    assert (root / "milestones" / "milestone_100_next").is_dir()


def test_the_width_grows_without_a_cap(run_define, workspace):
    root = workspace("milestone_1234_big")
    assert defined_name(run_define("--title", "Next", stdin=GOAL, cwd=root)) == "milestone_1235_next"


def test_entries_that_are_not_milestone_directories_are_skipped(run_define, workspace):
    root = workspace(
        "milestone_02_counted",
        "milestone_x1_non-digit",
        "milestone_07_",
        "milestone_40",
        "Milestone_30_capital",
        "notes",
        files=("milestone_50_file", "README.md"),
    )
    result = run_define("--title", "Next", stdin=GOAL, cwd=root)
    assert defined_name(result) == "milestone_03_next"
    assert result.stderr == b""


def test_non_ascii_digits_do_not_count(run_define, workspace):
    root = workspace("milestone_01_one", "milestone_٣٣_arabic-indic", "milestone_９９_fullwidth")
    assert defined_name(run_define("--title", "Next", stdin=GOAL, cwd=root)) == "milestone_02_next"


def test_a_symlink_to_a_directory_counts_but_a_dangling_one_does_not(run_define, workspace, tmp_path):
    root = workspace("milestone_01_one")
    target = tmp_path / "elsewhere"
    target.mkdir()
    (root / "milestones" / "milestone_04_linked").symlink_to(target, target_is_directory=True)
    (root / "milestones" / "milestone_09_dangling").symlink_to(tmp_path / "missing")
    assert defined_name(run_define("--title", "Next", stdin=GOAL, cwd=root)) == "milestone_05_next"


def test_nested_milestone_directories_do_not_count(run_define, workspace):
    root = workspace("milestone_01_one", "archive")
    (root / "milestones" / "archive" / "milestone_60_old").mkdir()
    assert defined_name(run_define("--title", "Next", stdin=GOAL, cwd=root)) == "milestone_02_next"


def test_the_heading_carries_the_integer_number(run_define, workspace):
    root = workspace("milestone_06_six")
    run_define("--title", "Seventh", stdin=GOAL, cwd=root)
    requirements = (root / "milestones" / "milestone_07_seventh" / "requirements.md").read_text(encoding="utf-8")
    assert requirements.startswith("# Milestone 7: Seventh\n")
