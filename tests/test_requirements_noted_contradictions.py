"""A "## Noted contradictions" section standing between "## Decisions" and "## Out of Scope" ends
the decisions section like any other column-0 "## " heading: a subsection the fold creates lands
immediately above that heading, a fold into the last subsection lands there too, a replace of the
last subsection stops at it, and the noted section's bytes are never touched."""

from pathlib import Path

import requirements

FIXTURES = Path(__file__).resolve().parent / "fixtures"
NAME = requirements.REQUIREMENTS_NAME
GOLDEN = (FIXTURES / NAME).read_bytes()

UNICODE_BODY = "Carry `code`, ${VAR}, $(cmd), &amp; entities, and \"quotes\" through untouched, including zażółć gęślą jaźń.\n".encode("utf-8")
NOTED = (
    b"## Noted contradictions\n"
    b"\n"
    b"- \"Prose decision\" (\"The first decision is one prose paragraph\") and \"Topical bullets\" "
    b"(\"Second lead.\"): the first says one thing and the second another, so both cannot hold.\n"
    b"\n"
)
OUT_OF_SCOPE = b"## Out of Scope\n"


def with_noted_section(data):
    """data with the noted section inserted directly before its "## Out of Scope" heading."""
    assert data.count(OUT_OF_SCOPE) == 1
    offset = data.index(OUT_OF_SCOPE)
    return data[:offset] + NOTED + data[offset:]


NOTED_GOLDEN = with_noted_section(GOLDEN)


def run(run_requirements, subcommand, target, section, body):
    result = run_requirements(subcommand, str(target), "--section", section, stdin=body)
    assert (result.returncode, result.stdout, result.stderr) == (0, b"", b"")
    return (target / NAME).read_bytes()


def inserted_after(data, line, inserted):
    assert data.count(line) == 1
    offset = data.index(line) + len(line)
    return data[:offset] + inserted + data[offset:]


def test_the_noted_section_stands_between_decisions_and_out_of_scope():
    assert NOTED_GOLDEN.index(b"\n## Decisions\n") < NOTED_GOLDEN.index(b"\n## Noted contradictions\n") < NOTED_GOLDEN.index(b"\n## Out of Scope\n")


def test_a_created_subsection_lands_immediately_above_the_noted_heading(run_requirements, requirements_dir):
    target = requirements_dir(NOTED_GOLDEN)
    result = run(run_requirements, "fold", target, "A New Subsection", b"Folded.\n")
    assert result == inserted_after(NOTED_GOLDEN, UNICODE_BODY, b"\n### A New Subsection\n\nFolded.\n")
    assert b"### A New Subsection\n\nFolded.\n\n## Noted contradictions\n" in result
    assert result.endswith(NOTED + GOLDEN[GOLDEN.index(OUT_OF_SCOPE):])


def test_a_fold_into_the_last_subsection_lands_above_the_noted_heading(run_requirements, requirements_dir):
    target = requirements_dir(NOTED_GOLDEN)
    result = run(run_requirements, "fold", target, "Render Unicode — Text As Given", b"Folded.\n")
    assert result == inserted_after(NOTED_GOLDEN, UNICODE_BODY, b"\nFolded.\n")
    assert result.endswith(b"Folded.\n\n" + NOTED + GOLDEN[GOLDEN.index(OUT_OF_SCOPE):])


def test_the_fresh_template_with_a_noted_section_takes_a_created_subsection_above_it(run_define, run_requirements, workspace):
    root = workspace()
    defined = run_define("--title", "First", stdin=b"Ship it.\n", cwd=root)
    assert defined.returncode == 0, defined.stderr
    target = root / "milestones" / "milestone_01_first"
    noted = with_noted_section((target / NAME).read_bytes())
    (target / NAME).write_bytes(noted)
    result = run(run_requirements, "fold", target, "Opening Decision", b"The first decision.\n")
    assert result == inserted_after(noted, b"## Decisions\n", b"\n### Opening Decision\n\nThe first decision.\n")
    assert b"## Decisions\n\n### Opening Decision\n\nThe first decision.\n\n## Noted contradictions\n" in result


def test_a_replace_of_the_last_subsection_stops_at_the_noted_heading(run_requirements, requirements_dir):
    target = requirements_dir(NOTED_GOLDEN)
    result = run(run_requirements, "replace", target, "Render Unicode — Text As Given", b"Rewritten.\n")
    offset = NOTED_GOLDEN.index(UNICODE_BODY)
    assert result == NOTED_GOLDEN[:offset] + b"Rewritten.\n" + NOTED_GOLDEN[offset + len(UNICODE_BODY):]
    assert result.endswith(b"Rewritten.\n\n" + NOTED + GOLDEN[GOLDEN.index(OUT_OF_SCOPE):])
