# Cairn for Antigravity

This repository is the Google Antigravity distribution of [Cairn](https://github.com/uHappyLogic/cairn), a plugin that gives your coding agent a milestone-driven development workflow — clarify a goal, resolve every open question, derive an ordered task list, complete the tasks, and close out the milestone before moving on — for any kind of project. It carries the built Antigravity plugin tree exactly as a Cairn release published it: the `plugin.json` manifest beside the plugin's skills, agents, and shared procedures, laid out to be extracted into a workspace's `.agents/plugins/cairn/` directory.

> **Generated — do not edit.** Every file in this repository, this README included, is rendered from the sources of [uHappyLogic/cairn](https://github.com/uHappyLogic/cairn) by its host build and published verbatim by each Cairn release; nothing here is edited by hand, and a change made here would be overwritten by the next release. Issues are disabled in this repository on purpose — report problems and propose changes as issues and pull requests at [uHappyLogic/cairn](https://github.com/uHappyLogic/cairn), never here.

## Installation

### Antigravity

From your project root, extract the latest release into `.agents/plugins/cairn`, the path Antigravity loads the plugin from:

```bash
mkdir -p .agents/plugins/cairn
curl -sL https://github.com/uHappyLogic/cairn-antigravity/archive/refs/heads/main.tar.gz | tar -xz --strip-components=1 -C .agents/plugins/cairn
```

The `main` archive is always the latest release, since `cairn-antigravity` advances only by release snapshots. To pin a release instead of tracking the latest, swap `refs/heads/main` in that URL for `refs/tags/<tag>`, using a tag from the [releases page](https://github.com/uHappyLogic/cairn-antigravity/releases).

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
