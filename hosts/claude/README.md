<p align="center">
  <a href="https://github.com/uHappyLogic/cairn-claude/tree/traffic-data">
    <img alt="unique views" src="https://raw.githubusercontent.com/uHappyLogic/cairn-claude/traffic-data/views-unique.svg" />
  </a>
  <a href="https://github.com/uHappyLogic/cairn-claude/tree/traffic-data">
    <img alt="unique clones" src="https://raw.githubusercontent.com/uHappyLogic/cairn-claude/traffic-data/clones-unique.svg" />
  </a>
</p>

# Cairn for Claude Code

Milestone-driven development for your coding agent — any kind of work, one milestone at a time.

This repository is the Claude Code distribution of [Cairn](https://github.com/uHappyLogic/cairn). It carries the built Claude Code plugin tree exactly as a Cairn release published it: the `.claude-plugin/` marketplace and manifest beside the plugin's skills, agents, and shared procedures, which makes it the recommended source to add as a marketplace.

> **Generated — do not edit.** Every file on `main`, this README included, is rendered from the sources of [uHappyLogic/cairn](https://github.com/uHappyLogic/cairn) by its host build and published verbatim by each Cairn release; nothing here is edited by hand, and a change made here would be overwritten by the next release. The repository's only other branch, `traffic-data`, is not built from anything and no release touches it — the traffic workflow this tree carries, which runs only in this repository and never in an installed copy, writes its per-day data file and badge SVGs there daily for the two badges above this page's title as well as for the adoption table in the root repository's README, and its own daily fetch of that branch counts as one unique clone a day in the clones badge. Issues are disabled in this repository on purpose — report problems and propose changes as issues and pull requests at [uHappyLogic/cairn](https://github.com/uHappyLogic/cairn), never here.

## Installation

Cairn has one runtime prerequisite: a **Python 3.9 or later** interpreter that answers as `python3` on your PATH. The skills drive the plugin's stdlib-only open-question tool with it (no packages to install), and `/init-milestone-base-workflow` checks it once per project, stopping with the remedy when it is missing.

### Claude Code

In Claude Code, add the `cairn-claude` marketplace and install the plugin from it:

```
/plugin marketplace add uHappyLogic/cairn-claude
/plugin install cairn@cairn
```

**Already installed from `uHappyLogic/cairn`?** That install keeps working — see [Migrating from the old marketplace](#migrating-from-the-old-marketplace) to switch to this source.

### Bootstrap your project

Then, in your project root, create the milestones scaffold once:

```
/init-milestone-base-workflow
```

Run `/init` to document your project — its domain context, working conventions, available tools, and how work is verified as done — in `CLAUDE.md`, so the skills can read that environment context.

## Migrating from the old marketplace

**Already installed from `uHappyLogic/cairn`?** Installs pinned to `uHappyLogic/cairn` keep working and updating — that marketplace now serves `./hosts/claude` — but `cairn-claude` is the recommended source. To switch, remove the old marketplace, add the new one, and install again; the plugin id `cairn@cairn` is unchanged, so no project settings need editing:

```
/plugin marketplace remove cairn
/plugin marketplace add uHappyLogic/cairn-claude
/plugin install cairn@cairn
```

## Source

Built from [uHappyLogic/cairn](https://github.com/uHappyLogic/cairn) at release tag [`1.7.0`](https://github.com/uHappyLogic/cairn/releases/tag/1.7.0), whose release page carries the notes for this version. The exact source commit this tree was built from is recorded in the body of this repository's `Release: 1.7.0` commit.

## License

MIT — see [LICENSE](LICENSE).
