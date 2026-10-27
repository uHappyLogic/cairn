"""Every fixed console line the `## Fixed console lines` table of docs/skill-reference.md lists,
checked against the committed host trees: each listed line stands verbatim in the rendered file
of every source its row names, in every tree, as a whole line of a fenced block or as a whole
inline code span, and no line is listed twice. A stop a shared procedure owns is one row under
that procedure, and a success line several skills share is one row naming them all, so the check
that no line repeats is also the check that no two conditions share a line. The lines are a
contract a harness matches a headless run's final message against, so a skill file and its row
change together or this test fails. The test only reads files, so it runs under both
interpreters."""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
REFERENCE = REPO_ROOT / "docs" / "skill-reference.md"
HOSTS = REPO_ROOT / "hosts"
SECTION = "## Fixed console lines"
KINDS = ("success", "no-op", "stop")

CODE_SPAN = re.compile(r"`([^`]+)`")
BACKTICK_RUN = re.compile(r"`+")
PLACEHOLDER = re.compile(r"<[^<>]*>")


# --- the table ---------------------------------------------------------------------------------


def section_lines():
    """The lines of skill-reference.md from the section heading to the next `## ` heading."""
    lines = REFERENCE.read_text(encoding="utf-8").splitlines()
    assert lines.count(SECTION) == 1, f"{REFERENCE.name} holds {lines.count(SECTION)} {SECTION!r} headings, not one"
    start = lines.index(SECTION) + 1
    end = next((index for index in range(start, len(lines)) if lines[index].startswith("## ")), len(lines))
    return lines[start:end]


def table_rows():
    """Every body row of the section's table as (sources, kind, line)."""
    rows = []
    for text in section_lines():
        if not text.startswith("|"):
            continue
        cells = [cell.strip() for cell in text.strip().strip("|").split("|")]
        if cells == ["Source", "Kind", "Line"] or all(set(cell) <= set("-:") for cell in cells):
            continue
        assert len(cells) == 3, f"a table row of {len(cells)} cells, not three: {text}"
        source_cell, kind, line_cell = cells
        line = re.fullmatch(r"`([^`]+)`", line_cell)
        assert line, f"a Line cell that is not one code span: {line_cell}"
        sources = CODE_SPAN.findall(source_cell)
        assert sources, f"a Source cell naming no source: {source_cell}"
        rows.append((tuple(sources), kind, line.group(1)))
    return rows


ROWS = table_rows()


def row_id(row):
    sources, kind, line = row
    return f"{sources[0]}:{kind}:{line}"


# --- the rendered trees ------------------------------------------------------------------------


def plugin_roots():
    """Every rendered plugin root under hosts/: the directory holding a skills/<name>/SKILL.md."""
    return sorted({skill.parents[2] for skill in HOSTS.glob("**/skills/*/SKILL.md")})


def rendered_file(root, source):
    """A row's source in one tree: a shared procedure by its path, a skill by its name."""
    if source.startswith("shared/"):
        return root / source
    return root / "skills" / source / "SKILL.md"


def code_spans(text):
    """Every inline code span of a Markdown text: a run of backticks opens a span that the next
    run of exactly the same length closes, so a span holding a backtick is read whole."""
    spans, position = [], 0
    while True:
        opening = BACKTICK_RUN.search(text, position)
        if opening is None:
            return spans
        closing = re.compile(r"(?<!`)" + re.escape(opening.group()) + r"(?!`)").search(text, opening.end())
        if closing is None:
            position = opening.end()
            continue
        spans.append(text[opening.end() : closing.start()])
        position = closing.end()


def shown_lines(path):
    """Every whole line of a fenced block, and every inline code span of the prose around them,
    of one rendered file, each with its whitespace collapsed as Markdown renders it."""
    shown, prose, fenced = set(), [], False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
            prose.append("")
        elif fenced:
            shown.add(" ".join(line.split()))
        else:
            prose.append(line)
    shown.update(" ".join(span.split()) for span in code_spans("\n".join(prose)))
    return shown


# --- the tests ---------------------------------------------------------------------------------


def test_every_host_tree_is_checked():
    roots = plugin_roots()
    hosts = sorted(path.name for path in HOSTS.iterdir() if path.is_dir())
    assert hosts, "hosts/ holds no host tree"
    assert sorted({root.relative_to(HOSTS).parts[0] for root in roots}) == hosts


def test_table_lists_lines():
    assert ROWS, f"the {SECTION!r} table lists no line"


@pytest.mark.parametrize("row", ROWS, ids=row_id)
def test_line_is_fixed_and_identifier_free(row):
    sources, kind, line = row
    assert kind in KINDS, f"kind {kind!r} is none of {KINDS}"
    assert line == " ".join(line.split()), f"the line carries stray whitespace: {line!r}"
    assert not PLACEHOLDER.search(line), f"the line carries a placeholder: {line!r}"


def test_no_line_repeats():
    seen, repeated = set(), []
    for _, _, line in ROWS:
        if line in seen:
            repeated.append(line)
        seen.add(line)
    assert not repeated, f"lines listed more than once: {repeated}"


@pytest.mark.parametrize("row", ROWS, ids=row_id)
def test_line_stands_in_every_rendered_source(row):
    sources, _, line = row
    missing = []
    for root in plugin_roots():
        for source in sources:
            path = rendered_file(root, source)
            if not path.is_file():
                missing.append(f"{path.relative_to(REPO_ROOT)} does not exist")
            elif line not in shown_lines(path):
                missing.append(f"{path.relative_to(REPO_ROOT)} does not show it")
    assert not missing, f"{line!r}: " + "; ".join(missing)
