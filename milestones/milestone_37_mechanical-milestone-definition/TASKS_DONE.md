# TASKS DONE

## Add Milestone Definition Tool

Create `core/tools/define_milestone.py`, a stdlib-only Python 3.9+ tool that takes the title as `--title` and the goal text on stdin and, following the Milestones root, Number scan and padding, Title handling, Slug derivation, Conflict definition, Goal text handling, Markdown template ownership, and Creating open_questions.xml decisions, creates `milestones/milestone_<NN>_<slug>/` with its four files from string constants, importing nothing from `open_questions.py`. On success it prints exactly two unlabeled lines, `Milestone-definition: milestone_<NN>_<slug>` then `milestones/milestone_<NN>_<slug>/`; on any failure it applies the Failure cleanup decision (the directory and its files only, since the tool never creates the root) and the Exit status and stream contract decision through its own `main()` and failure helper copied from the open-question tool's. Verified by hand-running the tool against a scratch `milestones` root through the success, missing-root, conflict, empty-title, and empty-goal paths, and by rebuilding both host trees with `uv run scripts/build_hosts.py` so `--check` passes (no bare `{{`, no host name in the source).

**Verified:**

- `core/tools/define_milestone.py` exists, imports only the standard library (argparse, os, re, sys, tempfile, unicodedata) and nothing from `open_questions.py`, takes the title as a required `--title`, and reads the goal text from stdin.
- The four files are string constants in the tool and written into a freshly created `milestones/milestone_<NN>_<slug>/` in the order `open_questions.xml` (`<open-questions/>` plus newline), `requirements.md` (`# Milestone <N>: <title>`, the goal under `## Goal`, then empty `## Relevant starting state`, `## Decisions`, `## Out of Scope`), `TASKS_TODO.md` (`# TASKS TODO`), `TASKS_DONE.md` (`# TASKS DONE`), each through a temporary file renamed over the target.
- Success path, hand-run against a scratch `milestones` root holding `milestone_09_old`, `milestone_x1_bad`, `milestone_07_`, and a file `milestone_50_file`: exit 0 and exactly the two lines `Milestone-definition: milestone_10_cafes-multi-host-work-uber-fast` and `milestones/milestone_10_cafes-multi-host-work-uber-fast/`, showing the goto-aligned scan, the two-digit padding, the folded title written unchanged into the heading, and the slug rules (apostrophe deleted, NFKD accent fold, hyphenated compound kept as one word, a punctuation-only word skipped, five words); the goal was written with interior blank lines and Markdown kept and outer whitespace trimmed; a root holding `milestone_99_x` yields `milestone_100_…`.
- Missing-root path: with no `milestones` directory the tool exits 1 with one `Error:` line naming `milestones/` and pointing at `/init-milestone-base-workflow`, writes nothing, and never creates the root.
- Conflict path: a dangling symlink at the computed `milestones/milestone_11_same-title` makes the exclusive directory create refuse with one `Error:` line, exit 1, nothing written.
- Empty-title path: a whitespace-and-newline-only `--title` exits 1 with `Error: the title given as --title is empty`; a title no word of which survives slug cleaning is refused with its own `Error:` line.
- Empty-goal path: whitespace-only stdin exits 1 with `Error: the goal text on standard input is empty`; non-UTF-8 stdin is refused with its own `Error:` line; a missing `--title` gets argparse's usage message and exit 2.
- Failure cleanup: a write failure injected on the third file removes the written files and the milestone directory in reverse order and reports one `Error:` line; with a stray file dropped into the directory the cleanup leaves the stray and the directory in place and the `Error:` line gives the original reason followed by the path it could not remove; stdout is empty on every failure path.
- `main()` and `_fail` mirror the open-question tool's contract (UTF-8 stream reconfiguration, `ToolError`/`OSError`/any other exception folded to one `Error:` line with exit 1, no traceback); the tool also runs under Python 3.9.
- `uv run scripts/build_hosts.py` renders the tool byte-identical into `hosts/claude/tools/` and `hosts/antigravity/tools/`, and `uv run scripts/build_hosts.py --check` passes (no bare `{{`, no host name in the source).

---

## Add Definition Tool Test Suite

Add flat per-concern test files under `tests/` for `define_milestone.py`, one per concern named in the Test suite extension decision (numbering and padding, slug derivation, conflicts, failure cleanup, output and exit contract), plus the parity test from the Creating open_questions.xml decision that the written document parses with `open_questions.load_document` and equals `render_document(Document())`. Extend `conftest.py` with a second pinned tool path, a `run_define` subprocess fixture beside `run_tool`, and a helper that builds milestone-root layouts under `tmp_path`, changing no `pyproject.toml` setting. Verified by both suite runs passing, `uv run pytest` and `uv run --no-project --python 3.9 --with pytest pytest`, with no `__pycache__` left under `core/tools/`.

**Verified:**

- `tests/conftest.py` pins a second tool path `DEFINE_TOOL = REPO_ROOT / "core" / "tools" / "define_milestone.py"`, adds a `run_define(*args, stdin=..., cwd=...)` fixture beside `run_tool` (a `sys.executable -B` subprocess run from the given workspace, stdin always piped), and a `workspace(*directories, files=(), root=True)` helper that builds a milestones-root layout under `tmp_path`; `pyproject.toml` is unchanged.
- Flat per-concern test files exist beside the existing ones, one per concern of the Test suite extension decision: `tests/test_define_numbering.py` (numbering and padding), `tests/test_define_slug.py` (slug derivation, with title folding), `tests/test_define_conflicts.py` (conflicts, with the missing root), `tests/test_define_cleanup.py` (failure cleanup), and `tests/test_define_output.py` (output and exit contract, with goal handling).
- `tests/test_define_parity.py` holds the Creating open_questions.xml parity test: the `open_questions.xml` the tool writes equals `render_document(Document())` byte for byte and parses with `open_questions.load_document` to `Document()`.
- `uv run pytest` passes (531 tests, 84 of them in the six new files).
- `uv run --no-project --python 3.9 --with pytest pytest` passes (531 tests).
- `find core/tools -name __pycache__` prints nothing after both runs.

---
