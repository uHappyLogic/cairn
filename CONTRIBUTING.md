# Contributing to cairn

## Contributor workflow

A change to cairn arrives as a **contributor-run milestone on a maintainer-reserved slot**: you propose it, the maintainer reserves a milestone for it, and you run that milestone in your fork with cairn's own workflow before opening the pull request. There is no plain-pull-request tier: a small fix is filed as an [issue](https://github.com/uHappyLogic/cairn/issues/new/choose) for the maintainer to make. The design invariants a change must preserve live in [`CLAUDE.md`](CLAUDE.md#invariants-to-preserve-when-editing-skills); read the ones that touch what you are changing before you start.

The handoff, one step per act:

1. **File the proposal issue.** Open a [Milestone proposal](https://github.com/uHappyLogic/cairn/issues/new?template=proposal.yml) with a goal statement in the shape a milestone `## Goal` takes, the motivation, what is in and out of scope, and your commitment to run the milestone yourself. A proposal is a work item in waiting: its acceptance produces a milestone, and your pull request closes it.
2. **The maintainer accepts by reserving a milestone.** On `main`, and only while their own `Current milestone:` line in `milestones/README.md` reads `none`, the maintainer runs `/define-milestone-goal` with the accepted goal. Its `Milestone-definition:` commit creates `milestones/milestone_<N>_<slug>/` — reserving that milestone number and id for you — **without activating it**: `main`'s pointer stays `none` and remains the maintainer's to hold. An abandoned contribution leaves only that defined directory on `main`, and the maintainer reverts its `Milestone-definition:` commit, since `/goto-next-milestone` would otherwise activate it as the lowest-numbered undone milestone.
3. **Fork and branch from that commit.** Fork the repository and start your branch at the `Milestone-definition:` commit that reserved your milestone.
4. **Run `/goto-next-milestone` first.** Before anything else, activate the reserved milestone in your fork: `/goto-next-milestone` points your branch's `Current milestone:` line at `milestones/milestone_<N>_<slug>/`. The activation happens only on your branch, never on `main`.
5. **Run the milestone through `/finish-current-milestone`.** Work the reserved milestone through the full requirements-and-task pipeline — starting state, requirements review and open questions, task derivation, task completion, follow-ups — exactly as the docs' [Workflow pipeline](docs/workflow.md#workflow-pipeline) documents it skill by skill, ending with `/finish-current-milestone`, which records the milestone's history entry in `milestones/README.md` and sets the pointer back to `none`. The branch's net change to the pointer line is nil.
6. **Sync from `main` by merge only, and only while its pointer reads `none`.** Never rebase: a rebase replays your goto commit, whose patch conflicts against any live `main` even after finish. Before a merge, check `main`'s pointer with `git show origin/main:milestones/README.md` and merge only when its `Current milestone:` line reads `none`. A merge attempted while the maintainer's own milestone is live conflicts on exactly that line — abort it (`git merge --abort`) and wait for the next `none` window, which recurs every day or two; never resolve that conflict by hand. After `/finish-current-milestone` your branch reads `none` again and any merge from `main` is safe.
7. **Rebuild `hosts/` and pass the drift gate.** Run `uv run scripts/build_hosts.py`, commit the rebuilt trees, and confirm `uv run scripts/build_hosts.py --check` passes — and, if your milestone touched a tool under `core/tools/`, that both pytest runs under [Development](#development) pass too; the same checks run as the `drift-gate` status on your pull request.
8. **Open the pull request.** Fill in the [template](.github/PULL_REQUEST_TEMPLATE.md) — the reserved milestone id, `Closes #<proposal issue>`, and the finished-milestone checklist. The pull request is merged as a **merge commit** (squash merges are disabled on the repository), so the milestone's commits survive for the release notes and for `/capture-milestone-principle-updates`, which the maintainer runs after the merge.

## Development

This project supports Claude Code, Google Antigravity, and Codex from one source. The runtime layer — skills, agents, shared procedures, and the stdlib-only Python tools under `core/tools/` — is authored **once, host-neutrally, under `core/`**: files there refer to each other through the placeholder `{{PLUGIN_ROOT}}` rather than any host's own syntax, and nothing under `core/` names a host.

Each supported host is a **declarative definition directory** under `scripts/hosts/<host>/` — `scripts/hosts/claude/`, `scripts/hosts/antigravity/`, and `scripts/hosts/codex/` today. It holds a `settings.toml`, which says how `core/` is rendered into that host's tree, beside that host's template files (its manifest, plus a marketplace file where the tree is a marketplace, its `README.md`, `CONTRIBUTING.md` pointer, and traffic workflow), each rendered to the same path in the tree with its version filled from the root `VERSION` file and its plugin name from the settings. Wherever wording differs between hosts, `core/` carries a **named slot**, a `{{SLOT_NAME}}` placeholder, and every definition's `[slots]` table gives that host's text for it: the convention is one value file per slot under the definition's `slots/` subdirectory (`NAME = { file = "slots/NAME.md" }`), and the inline form (`NAME = "text"`) is still accepted. Every definition declares the same slot names. Adding a host means adding a definition directory, not code. The module docstring at the top of `scripts/build_hosts.py` (which `--help` does not print) is the one complete reference for the settings keys, the slot forms and how a value file is read, and the checks — this guide does not repeat them.

Two development rules keep each host's tree about that host alone:

- **Host differences reach `core/` as named slots, not as capability-conditional prose.** A sentence that holds for one host and not another becomes a slot whose value each host fills with its own mechanism; `core/` never describes a capability in prose and leaves the runner to choose a branch at run time.
- **A rendered tree never names another host's mechanism.** This covers every file in the tree — the files rendered from `core/` with their slot values, and the host's own templates — a contrastive mention of what this host does not use included; a link to the source repository is not such a mention. Slot values name no host, their own included: they reach the mechanism through that host's own identifiers (tool names, config keys, file and command names) and otherwise say "this host". This is a rule, not a check: the build's `host-name-in-core` check scans `core/` only, so a slot value or template that breaks it passes the build and must be caught in review.

One generic build script renders every host tree from `core/`:

```bash
uv run scripts/build_hosts.py             # build every host into hosts/<host>/
uv run scripts/build_hosts.py claude      # build only the named host(s)
uv run scripts/build_hosts.py --check     # drift gate: render, validate, compare with the committed trees, write nothing
```

Before writing anything it runs every selected host's render through its full check set (listed in the docstring) and swaps the results into the committed `hosts/claude/`, `hosts/antigravity/`, and `hosts/codex/` trees only when every selected host passes; otherwise it exits non-zero listing every failing file and check. Those trees are generated output, never hand-edited: rebuild after changing `core/` or a host definition and commit the rebuilt trees with that change. `--check` compares a fresh render byte-for-byte against the committed trees and is the first thing a release runs.

The Python tools under `core/tools/` share a pytest suite under the repository-root `tests/` (golden fixtures included), run two ways — once under the pinned interpreter with the locked `dev`-group pytest, and once under the Python 3.9 floor the plugin promises its users:

```bash
uv run pytest                                              # pinned run: the .python-version interpreter, locked pytest
uv run --no-project --python 3.9 --with pytest pytest      # floor run: Python 3.9 with the last pytest that supports it
```

Both must pass before a change to a tool is committed, and the suite stays on the pytest API the two runs share.

The same suite holds one test of the build itself, `tests/test_build_rendering.py`: it imports `scripts/build_hosts.py` in-process, renders a small synthetic `core/` through one synthetic host definition into a temporary directory, and asserts that inline and file-backed slot values land in the rendered files in the build's substitution order, with one case for each refusal of a bad file-backed `[slots]` entry. It runs under the pinned interpreter only: the build needs Python 3.11+ (`tomllib`), so the module skips itself below 3.11 and the floor run reports it skipped. It covers rendering, not the check set or `--check`; run the pinned pytest after changing the build.

CI runs both pytest runs as the two steps after `--check` in the same `drift-gate` job, so one status covers the drift gate and both test runs.

A third suite, `agy_tests/` at the repository root, drives the installed `agy` CLI against the global plugin copy at `~/.gemini/config/plugins/cairn` and sits outside `testpaths`, so neither pytest run above nor CI reaches it: it runs only when named, `uv run pytest agy_tests`, and stops before any test with one line naming the remedy when `agy` is not on `PATH` or that copy is missing or differs from the committed `hosts/antigravity/` tree. Run it and have it pass before committing a change to the Antigravity host integration — `scripts/hosts/antigravity/`, `core/agents/*.md`, `scripts/build_hosts.py`, or `agy_tests/` itself — the same path set the release pre-flight runs it for when any of them changed since the last release.

The root `VERSION` file holds the plugin version and nothing else. `uv run scripts/set_version.py <MAJOR.MINOR.PATCH>` writes it together with its mirrored surfaces (the root `.claude-plugin/marketplace.json` entry, `pyproject.toml`, and `uv.lock`); the version in every host manifest is rendered from `VERSION` by the build, never edited by hand.

Each release publishes every `hosts/<host>/` tree verbatim into its own **distribution repository** — [`cairn-claude`](https://github.com/uHappyLogic/cairn-claude), the recommended install source, [`cairn-antigravity`](https://github.com/uHappyLogic/cairn-antigravity), and [`cairn-codex`](https://github.com/uHappyLogic/cairn-codex) — as one ordinary commit tagged with the release version and carrying a GitHub release with the same notes. Nothing in those repositories is edited by hand, and their issues are disabled: bug reports and pull requests belong here.

The monorepo is not the source users install from — that is `cairn-claude`, as described under [Installation](README.md#installation) — but it is the maintainer's install source: its root `.claude-plugin/marketplace.json` stays a working marketplace, named `cairn` and pointing at `./hosts/claude`, so a checkout can be registered as a **directory marketplace** and the plugin installed from it as usual, for running cairn straight from the working tree while developing it:

```
/plugin marketplace add /path/to/cairn
/plugin install cairn@cairn
```

Claude Code reads that marketplace from the checkout directory, so the `hosts/claude/` tree it points at is what gets installed and updated — no release needed.
