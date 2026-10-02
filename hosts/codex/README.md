<p align="center">
  <a href="https://github.com/uHappyLogic/cairn-codex/tree/traffic-data">
    <img alt="unique views" src="https://raw.githubusercontent.com/uHappyLogic/cairn-codex/traffic-data/views-unique.svg" />
  </a>
  <a href="https://github.com/uHappyLogic/cairn-codex/tree/traffic-data">
    <img alt="unique clones" src="https://raw.githubusercontent.com/uHappyLogic/cairn-codex/traffic-data/clones-unique.svg" />
  </a>
</p>

# Cairn for Codex

Cairn brings all the important questions up to be decided upfront, so you can hand long-running execution to your agent confidently.

This repository is the Codex distribution of [Cairn](https://github.com/uHappyLogic/cairn). It carries the built Codex plugin tree exactly as a Cairn release published it: the `.agents/plugins/marketplace.json` marketplace at its root and, under `plugins/cairn/`, the `.codex-plugin/plugin.json` manifest beside the plugin's skills, agents, and shared procedures, which makes it the source to add as a marketplace.

> **Generated — do not edit.** Every file on `main`, this README included, is rendered from the sources of [uHappyLogic/cairn](https://github.com/uHappyLogic/cairn) by its host build and published verbatim by each Cairn release; nothing here is edited by hand, and a change made here would be overwritten by the next release. The repository's only other branch, `traffic-data`, is not built from anything and no release touches it — the traffic workflow this tree carries, which runs only in this repository and never in an installed copy, writes its per-day data file and badge SVGs there daily for the two badges above this page's title as well as for the adoption table in the root repository's README, and its own daily fetch of that branch counts as one unique clone a day in the clones badge. Issues are disabled in this repository on purpose — report problems and propose changes as issues and pull requests at [uHappyLogic/cairn](https://github.com/uHappyLogic/cairn), never here.

## Installation

Cairn has two runtime prerequisites: **git**, with your project root inside a git work tree that every skill commits into, and a **Python 3.9 or later** interpreter that answers as `python3` on your PATH. The skills drive the plugin's stdlib-only Python tools with it (no packages to install), and `$cairn:init-milestone-base-workflow` checks both once per project, git first, stopping with the remedy when either is missing.

### Codex

Cairn supports the Codex command-line tool. In a terminal, add the `cairn-codex` marketplace and install the plugin from it:

```
codex plugin marketplace add uHappyLogic/cairn-codex
codex plugin add cairn@cairn
```

In a Codex session, invoke a skill by its name under the plugin's namespace, such as `$cairn:init-milestone-base-workflow`. The skills' own text names other skills in the slash form, such as `/derive-tasks`; those slash names refer to the same skills, which you invoke as `$cairn:derive-tasks`.

Codex reads its project instructions from `AGENTS.md`, so on Codex the skills read your project's environment context from `AGENTS.md`, and the bootstrap writes its workflow section there, never to `CLAUDE.md`.

Run your sessions under Codex's workspace-write sandbox with the on-request approval policy; Cairn needs no change to `config.toml`. That sandbox keeps your project's `.git` directory read-only, so every git staging or commit step a skill takes asks for your approval. The plugin's `python3` tools need only read access to the installed plugin directory.

### Bootstrap your project

Then, in your project root, create the milestones scaffold once:

```
$cairn:init-milestone-base-workflow
```

Run Codex's `/init` to document your project — its domain context, working conventions, available tools, and how work is verified as done — in `AGENTS.md`, so the skills can read that environment context.

## Source

Built from [uHappyLogic/cairn](https://github.com/uHappyLogic/cairn) at release tag [`1.8.0`](https://github.com/uHappyLogic/cairn/releases/tag/1.8.0), whose release page carries the notes for this version. The exact source commit this tree was built from is recorded in the body of this repository's `Release: 1.8.0` commit.

## License

MIT — see [LICENSE](LICENSE).
