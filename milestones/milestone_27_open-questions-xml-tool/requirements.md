# Milestone 27: Open Questions XML Tool

## Goal

Split the `## Open questions` section out of `requirements.md` into a sibling `<MILESTONE_DIR>/open_questions.xml` — a well-formed XML document under one root element, created empty by `define-milestone-goal`, whose "no `<open-question>` child remains" state is the convergence verdict and the `derive-tasks` precondition — and ship one stdlib-only Python tool inside the plugin (rendered into every host tree, invoked via `{{PLUGIN_ROOT}}`, and the file's sole writer) that owns every deterministic operation over that document: list, locate, add, lift, remove, embed with fragment validation replacing the seven-test acceptance gate, `<depends-on>` reconciliation in exact-id mode with transitive strip, dependent-strip on prune, and the answer sweep's dependency-graph walk. Rewire every skill, agent, and shared procedure that touches open questions from the `awk`/`sed`/`grep` boundary-line idiom onto tool invocations so that runtime prose keeps only judgment (authoring text, significance ranking, judgment-mode reconciliation for literal answers) and the entity-escaping, indentation, and whole-block-replacement contracts become the tool's internals — the aim being maximal token efficiency — while `capture-milestone-principle-updates` keeps its diff-line reconstruction, repointed at the new file. Give the tool a pytest suite run under `uv` in CI beside the drift gate, document Python 3.9+ as a prerequisite checked once by `init-milestone-base-workflow`, sync `CLAUDE.md`, `README.md`, and `docs/`, and provide no migration of or compatibility with pre-split milestones.

## Relevant starting state

### The `<open-question>` block and where it lives

Open questions are raw XML blocks under a single `## Open questions` section of `<MILESTONE_DIR>/requirements.md`, beside the four prose sections. `define-milestone-goal`'s template seeds `## Goal`, `## Relevant starting state`, `## Decisions`, and `## Out of Scope` only; `review-milestone-requirements` creates the section the first time it authors a block, so on disk it sits last, after `## Out of Scope`, and its empty heading survives once every block is answered. Every one of the 27 milestone directories holds exactly `requirements.md`, `TASKS_TODO.md`, and `TASKS_DONE.md`; 24 of the `requirements.md` files carry the heading and none carries a live block, so the annotated shape exists only in git history (for example the removed lines of `1cdddec`, `Recommendation-answer: Distribution badge form`). An authored block is three lines — a single-line `<open-question id="Short Title">` opening tag at the base column, one `<question>` child at a 2-space indent, `</open-question>` — and the recommend sweep grows it in a fixed child order: `<alternative id="…">` (what-it-is text, then `<advantage>` and `<drawback>`), `<applied-principle>`, self-closing `<depends-on question="…" option="…"/>`, and one `<recommendation option="…">`. Attribute values and element text are escaped with the five predefined entities, ids are compared case-folded after un-escaping, and no file declares a root element, an XML prolog, or a schema.

### The boundary-line CLI idiom and its runtime restatements

No runtime file invokes an executable today: `core/` holds Markdown only (`find core -type f ! -name '*.md'` returns nothing). Every deterministic operation over the question set is instead prose telling the runner to drive `awk`/`sed`/`grep` over the `<open-question …>`/`</open-question>` boundary lines and never `xmllint`, restated in each consumer: `core/shared/answer-procedure.md` (locate by `id="([^"]*)"`, re-query after the fold, line-range removal, dependent reconciliation with transitive strip), `core/shared/answer-with-recommendation-procedure.md` (locate and lift `<recommendation>`), `answer-open-question-with-alternative` (locate and lift an `<alternative>`), `discuss-open-question` (locate, then read the whole document), `recommend-all-open-questions` (gather once, the seven-test acceptance gate over the returned region with its eight reason strings and one-slot repair template, embed by whole-block-replacement `Edit` at 2-space indents), `answer-all-open-questions-with-recommendation` (gather in document order, drop unresolvable edges, depth walk with origin promotion, per-question re-check that also lifts the commit body), `review-milestone-requirements` (author, prune, dedup, transitive dependent strip), and `derive-tasks` (its precondition is a scan for any `<open-question` line, and its stop message lists the Short Titles). The five-entity un-escaping rule (`&amp;` last) is spelled out in six of those files. The `recommend-open-question` agent renders the child elements itself, indents them, escapes them, and self-checks the two boundary shape tests; the `answer-open-question-with-recommendation` agent stages `<MILESTONE_DIR>/requirements.md` path-scoped and returns bare `DONE`/`FAILED`.

### Indirect readers of the question set

`core/shared/recommend-procedure.md` reads `requirements.md` for the sibling blocks' embedded recommendations and the principle store `milestones/answer_decision_principles.md` in place. `ask-in-milestone-context` lists "any remaining open questions" among what it reads from `requirements.md`, `modify-milestone-goal` reports which open questions a goal change settles, opens, or moots, and `submit-task` and `discuss-new-task` only point at `/discuss-open-question`. `finish-current-milestone` and `goto-next-milestone` never read a question, and `goto-next-milestone` detects a defined milestone by its directory alone.

### Commit and provenance contracts on the question path

`core/shared/commit-procedure.md` takes an explicit PATHS set (guarded by `git status --porcelain -- <PATHS>`, staged by name, never `git add -A`), and every question skill passes `<MILESTONE_DIR>/requirements.md` as its sole path, under `Requirements-review:`, `Recommendation-annotation:`, `Manual-answer:`, `Recommendation-answer:`, and `Alternative-answer:` subjects. `capture-milestone-principle-updates` walks `git log -E --grep='^(Manual-answer|Alternative-answer|Recommendation-answer): ' -- milestones/<milestone_id>/requirements.md`, reads each commit with `git show <hash> --format='%s%n%n%b' -- milestones/<milestone_id>/requirements.md`, and reconstructs the answered block from the diff's removed lines between `-<open-question id="…"` and `-</open-question>` while reading the recorded decision from the added lines; it also treats pre-block-form blockquote answers (`> **Deferred — …:**`) as the no-recommendation case.

### The host build and what a host tree can carry

`scripts/build_hosts.py` walks every file under `core/`, applies `{{PLUGIN_ROOT}}` substitution and `prose_drop_patterns` to every UTF-8 text file whatever its extension, and lands each top-level `core/` directory where the host's `[layout]` maps it — both definitions map exactly `skills`, `agents`, `shared`, a file at the top of `core/` is a `BuildError`, and a layout that does not name every top-level directory fails validation. Its checks run over every rendered file: `unfilled-placeholder` fails on any `{{` not preceded by `$` (so a Python f-string's `{{` would fail), `host-name-in-core` fails on `claude` or `antigravity` as a whole word anywhere in `core/`, `dangling-plugin-root` requires every `<plugin_root>/<path>` (path characters `[A-Za-z0-9_./-]`) to name a file in the rendered tree, and the frontmatter and description checks apply to `skills/<name>/SKILL.md` and `agents/<name>.md` only. The plugin-root literals are `${CLAUDE_PLUGIN_ROOT}` and `.agents/plugins/cairn`, rendered into runtime prose as `${CLAUDE_PLUGIN_ROOT}/shared/answer-procedure.md` and `.agents/plugins/cairn/shared/answer-procedure.md`. `hosts/claude/` (37 files) and `hosts/antigravity/` (36 files) pass `--check` at version 1.5.1; the release skill stages `hosts/` whole, and `CLAUDE.md` enumerates the tree's contents as skills, agents, shared, plus exactly four non-plugin files.

### Python tooling, CI, and the test surface

`pyproject.toml` declares `cairn-tooling` with `requires-python = ">=3.11"` (the build imports `tomllib`), `pyyaml` as its one dependency, and `[tool.uv] package = false`; `.python-version` pins 3.13 and `uv.lock` holds only `cairn-tooling` and `pyyaml`. No `tests/` directory, no `pytest` reference, and no test runner exist anywhere in the repository — the build's validation gate is the only automated check. `.github/workflows/drift-gate.yml` is one job on unfiltered `push` and `pull_request` with `permissions: contents: read`, `actions/checkout@3d3c42e…` (v7.0.1) and `astral-sh/setup-uv@bec219d…` (v10.1.0) pinned by SHA, and the single step `uv run scripts/build_hosts.py --check`; `CONTRIBUTING.md`'s Development section documents those `uv run` commands as the whole build loop. On this machine `uv run` resolves to CPython 3.13.5 under uv 0.11.14; no Python 3.9 interpreter is installed, though uv lists `cpython-3.9.25` and `3.11.15` as downloadable.

### Prerequisites and the bootstrap skill

No document names a runtime prerequisite for the installed plugin: `README.md`'s `## Installation` gives the Claude Code marketplace commands, the Antigravity `curl … | tar -xz` extraction into `.agents/plugins/cairn`, and the bootstrap step, and both distribution README templates under `scripts/hosts/<host>/README.md` repeat the same sections; `uv` appears only in maintainer text. `init-milestone-base-workflow` probes just three things — `milestones/`, `milestones/README.md` with a `Current milestone:` line, and a `## Milestone Workflow` section in `CLAUDE.md` — creates what is missing, stops when all three exist, commits nothing, and runs no environment check; its `milestones/README.md` template describes `requirements.md` as "goal, relevant starting state, decisions, open questions", the line this repository's own `milestones/README.md` carries.

### Documentation surfaces that state the current design

`CLAUDE.md` (mirrored by the `AGENTS.md` symlink) mentions `open-question` 33 times and `boundary-line` 7 times: the "Milestone file structure" section says each milestone contains exactly three files, and the review, answer-procedure, recommend-sweep, answer-sweep, alternative-answer, capture, and dispatched-agent-return invariants each spell out the CLI idiom, the seven-test gate, or the whole-block-replacement embed. `README.md` repeats the three-file list under `## How it works` and, under `## Design principles`, claim 11's line that blocks are "found by their boundary lines, so every answer, cascade, and prune is a deterministic line-range edit"; `docs/design-claims.md` claim 11 gives that as its **Design** with a golden-file-diff **Metric**; `docs/workflow.md`'s "Iterating milestone requirements" paragraph states the query-where-it-pays convention (`awk`/`sed`/`grep`, never `xmllint`); and `docs/skill-reference.md` carries the entries for the eight question skills and agents that describe the same mechanics.

## Decisions

## Out of Scope

## Open questions

<open-question id="Root element shape">
  <question>What is the root element of `open_questions.xml` — its tag name, whether the document opens with an XML declaration, and whether the root carries attributes such as the milestone id?</question>
</open-question>
<open-question id="Empty document creation">
  <question>Does `define-milestone-goal` create the empty `open_questions.xml` by invoking a tool subcommand, keeping the tool the file&apos;s only writer, or by writing a fixed template itself?</question>
</open-question>
<open-question id="Tool directory placement">
  <question>Does the Python tool live in a new top-level `core/` directory that every host `[layout]` maps, such as `tools/`, or under the existing `shared/` directory beside the procedures?</question>
</open-question>
<open-question id="Interpreter command name">
  <question>Which command runs the tool at every invocation site and in the bootstrap check — `python3`, `python`, or a probe that falls back between the two?</question>
</open-question>
<open-question id="Tool file resolution">
  <question>Does every tool invocation take the `open_questions.xml` path or the milestone directory as an argument the caller resolves, or does the tool resolve the current milestone from the `milestones/README.md` pointer itself?</question>
</open-question>
<open-question id="Tool output contract">
  <question>What is the tool&apos;s output and error contract — what each operation prints on success (bare ids, whole blocks, lifted answer text) and how a failure is signalled (exit status and message form)?</question>
</open-question>
<open-question id="Fragment input channel">
  <question>How do `add` and `embed` receive multi-line text — the question text and the agent&apos;s returned fragment — as a command-line argument, on stdin, or from a file path?</question>
</open-question>
<open-question id="Embed extraction ownership">
  <question>Does `embed` accept the recommend agent&apos;s whole final message and extract the `&lt;alternative&gt;`…`&lt;/recommendation&gt;` region itself, or does the orchestrator still extract that region and pass only the fragment for validation?</question>
</open-question>
<open-question id="Escape hatch under sole writer">
  <question>With the tool as the file&apos;s only writer, how does a user clear a stale recommendation to force its regeneration — a `strip` subcommand or a documented hand-edit exception?</question>
</open-question>
<open-question id="Reconciliation command placement">
  <question>Does `remove` run the exact-id `&lt;depends-on&gt;` reconciliation and transitive strip itself when given the recorded option, or is reconciliation a separate subcommand the answer path invokes after the answered block and any mooted siblings are removed?</question>
</open-question>
<open-question id="Judgment-mode verdict application">
  <question>How does the literal-answer path, which judges each dependent&apos;s assumed option in prose, apply its per-dependent outcomes through the tool — per-dependent strip and tag-removal primitives, or one reconcile command that takes the verdicts?</question>
</open-question>
<open-question id="Capture decision source">
  <question>With its commit walk repointed at `open_questions.xml`, does `capture-milestone-principle-updates` read the recorded `## Decisions` entry from the same commit&apos;s `requirements.md` hunk, or from the commit body alone?</question>
</open-question>
<open-question id="Direct XML reads">
  <question>May read-only consumers that need the whole question set — the recommend agent&apos;s grounding, `discuss-open-question`, `ask-in-milestone-context`, `modify-milestone-goal` — read `open_questions.xml` directly, or must every read go through the tool?</question>
</open-question>
<open-question id="Canonical serialization format">
  <question>What on-disk formatting does the tool guarantee when it writes `open_questions.xml` — one element per line at a fixed indent per level, and which entity escapes — so that git diffs and capture&apos;s removed-line reconstruction stay line-oriented?</question>
</open-question>
<open-question id="Test suite location">
  <question>Where does the pytest suite live — in a repository-root `tests/` directory outside `core/` that imports the tool, or beside the tool inside `core/` and excluded from the host render?</question>
</open-question>
<open-question id="Tool test Python versions">
  <question>Which Python versions does CI run the tool&apos;s pytest suite under — a matrix reaching down to the documented 3.9 floor, or only the 3.13 the repository pins — given that `pyproject.toml` requires 3.11 for the build tooling?</question>
</open-question>
<open-question id="Prerequisite check failure mode">
  <question>When `init-milestone-base-workflow` finds no Python 3.9+ interpreter, does it stop the bootstrap or warn and continue creating the scaffold?</question>
</open-question>
