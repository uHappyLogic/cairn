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

## Rewrite Define Skill Around Tool

Rewrite `core/skills/define-milestone-goal/SKILL.md` so its single `<overall_goal_description>` argument stays and the model's only work is choosing the title, running `python3 {{PLUGIN_ROOT}}/tools/define_milestone.py --title` with the goal text on stdin as a quoted heredoc, handing the tool's two printed lines unchanged to the commit procedure as PATHS (the directory) and SUBJECT, and printing `Milestone defined.` or the distinct no-change line, while a failure quotes the tool's `Error:` line or the shell's missing-interpreter line verbatim and stops. The number, slug, and conflict steps are gone, the skill names the four files the tool creates and states none of their contents, and its frontmatter description stays one clause of 25 words or fewer. Verified by rebuilding both host trees so `uv run scripts/build_hosts.py --check` passes and by one run of the rewritten steps in a throwaway git repository that ends in a `Milestone-definition:` commit holding exactly the four files.

**Verified:**

- `core/skills/define-milestone-goal/SKILL.md` keeps its single `<overall_goal_description>` argument (Usage and example unchanged) and its steps are now: choose the title; run `python3 {{PLUGIN_ROOT}}/tools/define_milestone.py --title "<title>"` with `<overall_goal_description>` on stdin through a quoted `<<'EOF'` heredoc; hand the tool's two printed lines unchanged to the commit procedure as PATHS (the directory, second line) and SUBJECT (first line); print `Milestone defined.` or the distinct no-change line.
- A failure (missing `python3` or a non-zero exit with one `Error:` line) stops the skill with the shell's or the tool's line quoted verbatim.
- The number, slug, and conflict steps and the `open_questions.py create` call are gone; the skill names the four files the tool creates (`requirements.md`, `open_questions.xml`, `TASKS_TODO.md`, `TASKS_DONE.md`) and states none of their contents (no heading, section, or template text remains).
- The frontmatter description, `Create a new milestone directory with its four starting files from the provided goal description.`, is one clause of 15 words with no colon or semicolon and loads with `yaml.safe_load`.
- `uv run scripts/build_hosts.py` rebuilt both host trees and `uv run scripts/build_hosts.py --check` passes.
- One run of the rewritten steps in a throwaway git repository (a `milestones/` root, pointer `none`) printed `Milestone-definition: milestone_01_getting-started-guide` and `milestones/milestone_01_getting-started-guide/`, and committing that directory under that subject produced a `Milestone-definition:` commit holding exactly the four files, leaving the tree clean.

---

## Remove Create From Open-Question Tool

Remove the `create` subcommand from `core/tools/open_questions.py` (`cmd_create`, its parser registration, and its docstring entry) so the tool works only on documents that already exist, and reword the module docstring's sole-writer claim so `define_milestone.py` creates the document and this tool is its only writer after that. Delete `tests/test_create.py`, keeping only its check that the `empty` fixture is what the serializer renders for no questions, and rewrite the `tests/test_contract.py` cases that drive `create` against a surviving subcommand. Verified by both suite runs passing, `python3 core/tools/open_questions.py --help` no longer listing `create`, and both host trees rebuilt so `--check` passes.

**Verified:**

- `core/tools/open_questions.py` no longer holds `cmd_create`, its `create` parser registration, or its docstring entry, and no longer creates a directory (no `os.makedirs`); every subcommand works only on an existing document.
- The module docstring's sole-writer claim now reads that `define_milestone.py` creates the empty document together with its milestone directory and this module is the document's only writer from then on, no subcommand creating it; the parser description and the MILESTONE_DIR help no longer speak of a directory "to hold" the document.
- `python3 core/tools/open_questions.py --help` lists `list`, `locate`, `lift`, `add`, `strip`, `embed`, `remove`, `walk`, and `sort` and no `create`; `open_questions.py create` is refused by argparse as an invalid choice with exit status 2.
- `tests/test_create.py` is deleted; its check that the `empty` fixture is what the serializer renders for no questions survives as `test_the_empty_fixture_is_what_the_serializer_renders_for_no_questions` in `tests/test_format.py`.
- The `tests/test_contract.py` cases that drove `create` now drive surviving subcommands: the missing-MILESTONE_DIR usage error via `list`, the one-Error-line failure via `locate` of an unknown title, the operating-system failure via `list` on a file standing in for the directory, `main`'s tool-error line via `list` on a missing document, and `main`'s silent mutator via `strip` on the `annotated` fixture; the help test also asserts `create` is absent; the `conftest.py` `run_tool` example no longer names `create`.
- `uv run pytest` passes (527 tests) and `uv run --no-project --python 3.9 --with pytest pytest` passes (527 tests), with no `__pycache__` under `core/tools/`.
- `uv run scripts/build_hosts.py` rebuilt both host trees and `uv run scripts/build_hosts.py --check` passes.

---
