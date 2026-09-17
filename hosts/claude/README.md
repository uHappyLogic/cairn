# Cairn for Claude Code

This repository is the Claude Code distribution of [Cairn](https://github.com/uHappyLogic/cairn), a plugin that gives Claude Code a milestone-driven development workflow — clarify a goal, resolve every open question, derive an ordered task list, complete the tasks, and close out the milestone before moving on — for any kind of project. It carries the built Claude Code plugin tree exactly as a Cairn release published it: the `.claude-plugin/` marketplace and manifest beside the plugin's skills, agents, and shared procedures, which makes it the recommended source to add as a marketplace.

> **Generated — do not edit.** Every file in this repository, this README included, is rendered from the sources of [uHappyLogic/cairn](https://github.com/uHappyLogic/cairn) by its host build and published verbatim by each Cairn release; nothing here is edited by hand, and a change made here would be overwritten by the next release. Issues are disabled in this repository on purpose — report problems and propose changes as issues and pull requests at [uHappyLogic/cairn](https://github.com/uHappyLogic/cairn), never here.

## Installation

### Claude Code

In Claude Code, add the `cairn-claude` marketplace and install the plugin from it:

```
/plugin marketplace add uHappyLogic/cairn-claude
/plugin install cairn@cairn
```

**Already installed from `uHappyLogic/cairn`?** Installs pinned to `uHappyLogic/cairn` keep working and updating — that marketplace now serves `./hosts/claude` — but `cairn-claude` is the recommended source. To switch, remove the old marketplace, add the new one, and install again; the plugin id `cairn@cairn` is unchanged, so no project settings need editing:

```
/plugin marketplace remove cairn
/plugin marketplace add uHappyLogic/cairn-claude
/plugin install cairn@cairn
```

### Bootstrap your project

Then, in your project root, create the milestones scaffold once:

```
/init-milestone-base-workflow
```

Run `/init` to document your project — its domain context, working conventions, available tools, and how work is verified as done — in `CLAUDE.md`, so the skills can read that environment context.

## Source

Built from [uHappyLogic/cairn](https://github.com/uHappyLogic/cairn) at release tag [`1.5.0`](https://github.com/uHappyLogic/cairn/releases/tag/1.5.0), whose release page carries the notes for this version. The exact source commit this tree was built from is recorded in the body of this repository's `Release: 1.5.0` commit.

## License

MIT — see [LICENSE](LICENSE).
