# Gurita

A naming draft, written 2026-10-30, revised 2026-11-10 to rename the unit of work as well, and split the same day from the draft that also named the orchestrator, whose half is now `ideas/kepala.md`. A review of its gaps that day corrected the collision check, settled that the rename keeps nothing of the old vocabulary and reads nothing recorded under it, and added two open questions. It renames the plugin **Gurita**, Indonesian for octopus. The unit the plugin works on, today a milestone, becomes a **mission**, and its directory leaves the `milestones/` container to stand directly in its scope as `mission_<slug>/`. The draft records why the image holds, which names it rules out, what was checked for collisions and when, and how the names land in the repository. It says mission wherever it describes the renamed plugin and milestone only for what stands today, the rename work included, since that work is defined and finished under the current word. It precedes that work, and the closing section names what the work decides.

## Why rename

`Cairn` was chosen for what it means, a pile of stones marking a path, which is what a milestone is. It is shared by hundreds of frameworks and tools, so it marks nothing on its own. The replacement is chosen with the orchestrator `ideas/kepala.md` outlines in view: a second product sitting on top of the plugin will need a name that says how it relates to the first, so the plugin takes a name a second one can join. That second name is that draft's subject, and nothing in this rename waits on it.

`Milestone` is the other half of the stone image, the thing a cairn marks, and it does not survive the name it came with. It was also never exact: a milestone is a point passed on the way, while the unit the plugin works on is a piece of work with a goal, a scope, tasks, and an end. `Mission` says that, and it fits the new image where milestone does not: an arm carries a mission out, and the head `ideas/kepala.md` names is what would set one.

## The image

The octopus is the right animal, and for a more exact reason than "many arms". An octopus has about 500 million neurons and two thirds of them sit in the arms, grouped in ganglia along each arm. An arm senses and starts actions on its own; the central brain sets the goal and does not track each sucker. That is how a mission already works: it resolves its own implementation-level questions, through the open-question loop, before its tasks are derived, and whoever set its goal holds none of that detail. The arms also work in parallel and independently of one another, which is what path-addressed missions make possible: several missions worked at once, sequenced only where one scope encloses another (the scope gate, `core/shared/check-scope-gate.md`). The other half of the image, the head that sets the goals, is `ideas/kepala.md`'s.

One more fit, for the announcement rather than the design: an octopus piles shells and stones at the mouth of its den. The animal builds a cairn.

Two corrections to the image as first pitched:

- **Arms, not tentacles.** An octopus has eight arms and no tentacles; squid and cuttlefish carry the two tentacles. The plugin is the arms.
- **Octopus Deploy owns the English vocabulary.** It is a deployment orchestrator and its per-machine agent is called Tentacle, which is the head-and-arms split this image leads to, already named, in developer tooling. So octopus, octo-, tentacle, and kraken are all unusable, and the image has to be carried by anatomy or by another language.

## The names

**Gurita** is Indonesian and Malay for octopus. Pronounced gu-RI-ta. It carries the plugin's sense natively: the verb `menggurita`, per the KBBI, means to wrap around something strongly, like the arms of an octopus, and is the Indonesian press's word for a business that has spread into many sectors. A plugin whose missions reach into every scope of a project is doing exactly that.

**Mission** is the unit of work, in place of milestone: one goal, placed at one scope, decided question by question, executed task by task, and finished. It stays English on purpose. Gurita is a name, explained once, while the unit's word is typed in every command (`--mission <path>`) and read in every console line, so it has to say what it is without the landing page.

Gurita says nothing to most English speakers, as `cairn` said nothing to many; the meaning is one sentence away on the landing page. It carries no cultural-use expectation of the kind that ruled out the Māori word below.

### Collision check

Checked first on 2026-10-30 through web search of GitHub, npm, PyPI, and crates.io, which found nothing named `gurita`. That check was a search, not a registry query, and its result was wrong: looking the slug up directly on 2026-11-10 found three uses.

- **npm holds a package `gurita`.** One version, 1.0.0, published 2024-05-15, with no README, no repository, and no description, and 6 downloads in the month to 2026-11-09. It reads as a placeholder, not a tool.
- **GitHub holds `bjpop/gurita`**, a command-line tool for data analytics and plotting, with 6 stars and last pushed on 2026-08-20, so it is small and alive. It is a developer tool in another niche.
- **The GitHub owner names `gurita` and `gurita-dev` are taken**, the first by an account with no public repository, the second by one holding 41, its most starred being Apache Wicket helper libraries last pushed in 2018. A repository search for the word in a name lists 86.

PyPI and crates.io hold nothing under the name. None of the three blocks the rename: the plugin is published to no package registry, its repositories stay under `uHappyLogic`, and the one live tool shares neither the niche nor a namespace with it. They are recorded as a cost of the name, and the name stays, because next to the hundreds that share `cairn` three small uses still leave it marking something. The rename work looks the slug up once more before anything is published.

`mission` is a word of the vocabulary, never a package, repository, or plugin name, so no registry entry can block it. One use in the same niche was found on 2026-11-10, through web search and in talk coverage only, not in the vendor's own documentation: Factory calls its long-running multi-agent runs Missions, each with an orchestrator, workers, and validators, managed from a Mission Control view. That mission is the whole multi-day run, which here would be the orchestrator's loop (`ideas/kepala.md`), not one arm's unit, so a reader arriving from Factory will first read the word one level too high. It is recorded as a cost of the word, not as a reason against it.

## How the names land

| Site | Today | After |
|---|---|---|
| Plugin name and marketplace name | `cairn` | `gurita` |
| Skill and agent namespace | `cairn:derive-tasks` | `gurita:derive-tasks` |
| Source repository | `uHappyLogic/cairn` | `uHappyLogic/gurita` |
| Distribution repositories | `uHappyLogic/cairn-<host>` | `uHappyLogic/gurita-<host>` |
| Antigravity global install | `~/.gemini/config/plugins/cairn` | `~/.gemini/config/plugins/gurita` |
| Codex plugin directory | `plugins/cairn` | `plugins/gurita` |
| Build tooling project | `cairn-tooling` | `gurita-tooling` |

In prose the name is capitalised, Gurita; as a slug it is lowercase. The source repository is renamed with the plugin, decided on 2026-11-10 with the breaking of web references to its old name accepted, so no link to `uHappyLogic/cairn` is kept working on purpose. The repositories stay under `uHappyLogic`; whether the plugin and the orchestrator later share an organisation is left to `ideas/kepala.md`.

The name's surface, measured on 2026-10-30 outside the `hosts/` build output and `uv.lock`:

| What | Count |
|---|---|
| Files mentioning the name | 111 |
| Occurrences | 1817 |

Most of it is prose in `docs/`, the README, the milestones' own records, and the idea drafts. The identifier sites are not only the ones in the table above, and they are not each held in one place, as this draft first said. Beyond `.claude-plugin/marketplace.json`, `pyproject.toml`, and the three `settings.toml` host definitions, from which the build regenerates every host tree, a check on 2026-11-10 found the sites the open questions list.

### How the mission lands

The earlier version of this draft left the milestone vocabulary alone, because it names what the plugin works on, not the plugin. That is reversed: every site that says milestone says mission, the word mission is lowercase in prose like milestone before it, and the sites below are the ones where the word is an identifier rather than prose.

| Site | Today | After |
|---|---|---|
| Mission directory | `<scope>/milestones/<slug>/` | `<scope>/mission_<slug>/`, with no container |
| Discovery pattern | `**/milestones/*/requirements.md` | `**/mission_*/requirements.md` |
| The flag every per-mission skill takes | `--milestone <path>` | `--mission <path>` |
| Ten skill names | `define-milestone-goal`, `finish-milestone`, `review-milestone-requirements`, and seven more | `define-mission-goal`, `finish-mission`, `review-mission-requirements`, and so on |
| Tools | `milestones.py`, `define_milestone.py` | `missions.py`, `define_mission.py` |
| The read-only tool's query and flags | `milestones`, `--milestone`, `since --milestones` | `missions`, `--mission`, `since --missions` |
| Shared procedure | `resolve-milestone.md` | `resolve-mission.md` |
| Commit markers | `Milestone-definition:`, `Milestone-finish:` | `Mission-definition:`, `Mission-finish:` |
| Commit descriptors | `Workflow-bootstrap: milestones`, `Workflow-migration: milestones` | `Workflow-bootstrap: missions`, `Workflow-migration: missions` |
| Context file section | `## Milestone Workflow` | `## Mission Workflow` |
| Dispatch prompt line | `Milestone directory: <MILESTONE_DIR>` | `Mission directory: <MISSION_DIR>` |
| Principle store | `milestones/answer_decision_principles.md` | no home yet, see the open questions |
| Fixed console lines | 22 of the 94 listed lines carry the word | each reworded together with its row in `docs/skill-reference.md` |

The container goes with the word, a change of shape rather than of spelling, decided on 2026-11-10. A mission is `<scope>/mission_<slug>/`, a directory standing directly in its scope and told apart by its prefix, `mission_<slug>/` when the scope is the root. The container was kept until now for two reasons, and the prefix meets both: a mission still has a scope the gate can compare, now the directory holding the mission directory where it was the directory holding the container, and every runner still has one discovery pattern rather than a tree walk. What changes with it:

- The path a mission is addressed by is one level shorter, and the directory's own name says what it is wherever it is listed, in a tree view, a diff, or a commit subject.
- The definition tool creates one directory and no container, and the gate's lexical refusal of a path with no `milestones/` container becomes a refusal of a path whose last component does not open with `mission_`.
- A scope's missions are no longer grouped behind one entry: they stand among the scope's own directories, the root's included, sorted together by their prefix, and anything that walks the tree, a packaging glob or a test collector, now walks them too. A mission holds one Markdown file, one XML file, and one task list, so this is clutter rather than breakage.
- The pattern matches any directory so prefixed that holds a tracked `requirements.md`, whoever made it. The host suite's fixture project, kept today under `milestones.fixture/` so the pattern does not match it, needs a new name of the same kind for its mission directory.
- The principle store loses the directory it lives in.

What does not carry the word stays as it is: `requirements.md`, `open_questions.xml`, `TASKS_TODO.md`, the commit markers without it (`Task-completion:`, `Starting-state:`, the three answer markers, and the rest), and the 72 other fixed console lines. What is history stays as written too: the CHANGELOG's entries, which are each release's notes verbatim, the commits already in the log, and the `milestone_01` to `milestone_54` directory names the invariants cite.

The word's surface, measured on 2026-11-10 over tracked files outside `hosts/` and `uv.lock`, any capitalisation:

| What | Count |
|---|---|
| Files mentioning the word | 134 |
| Occurrences | 5529 |
| of them in `tests/` | 1931 |
| of them in `core/` | 1519 |
| of them in `docs/` | 660 |
| of them in `CLAUDE.md` | 442 |
| Files and directories named with it | 10 skill directories, 2 tools, 1 shared procedure, 15 test files, 1 fixture container |

That is three times the name's surface, and unlike the name it is not held in a few places from which the build regenerates the rest: the word is in tool code, in the tests' fixtures and expected output, and in strings that are read back from the git log.

## Checked and rejected

| Name | Why not |
|---|---|
| Octopus, Octo | Octopus Deploy; GitHub's octo- prefix |
| Tentacle | Octopus Deploy's agent |
| Kraken, Hydra, Nautilus | saturated |
| Tako | Japanese for octopus; three developer tools carry it, a deploy CLI, a CLI framework, and a Go framework |
| Wheke | Māori for octopus, clean, but Māori words carry cultural-use expectations the project should not take on |

The head words that were checked, and Argo, which was weighed as a pair, are in `ideas/kepala.md`.

### Alternatives kept on record

Names for the plugin alone, in case the chosen one fails a later check, none with a head word found that joins it: **Brachia**, the Latin for arms and the anatomical term for an octopus's arm set, as in brachial crown and interbrachial web, clean but pronounced two ways; **Pweza**, Swahili for octopus, clean, with an unusual onset; **Eledone**, an octopus genus, clean and melodic; **Lonkero**, Finnish for tentacle, clean, also a drink.

The pairs that were weighed, each a head word and an octopus word that merge, are in `ideas/kepala.md`. They are an alternative only until this rename is released: after that the plugin's half is fixed, and a head word has to join Gurita.

## Carrying it out

The rename is one release, carried out ahead of the orchestrator and waiting on nothing in `ideas/kepala.md`, so that the orchestrator, when it ships, never refers to the plugin as Cairn and matches fixed console lines that already say mission. It has two parts of different kinds. The name is mostly mechanical: the identifier sites change first, the build regenerates the host trees, the drift gate and both test runs pass, the prose follows, and `/release-plugin` publishes. The word is not: it changes the pattern live work is discovered by and the markers finished work is read back by, and what happens to everything already recorded under the old word, in this repository and in every project that uses the plugin, is settled in the hard cut below. Both parts are root-scoped, so if they are two milestones the scope gate runs them one after the other. Whether they are one milestone or two is settled when the goal is discussed; the rest is listed below for the work itself to decide.

### A hard cut

Decided on 2026-11-10, on one ground: Cairn was not widely adopted, so the rename pivots hard instead of carrying the old forms along for the projects that hold them.

- **Nothing of the old vocabulary is kept.** The renamed plugin answers to the new names only: no `cairn:` alias for a skill or an agent, no `--milestone` flag beside `--mission`, and one discovery pattern, `**/mission_*/requirements.md`, with no second one for a `milestones/` container. A project or a harness that used the old names changes them or stays on the last Cairn release.
- **The record starts at the rename.** The read-only tool reads `Mission-finish:` subjects and joins a task to its mission through `**/mission_*/TASKS_TODO.md`, and reads nothing else. A milestone finished before the rename, each of this repository's 57 `Milestone-finish: milestones/<slug>/` commits and every other project's own, is printed by no query, not by `record .`, by `summary`, or by the overview the starting-state procedure and the review pass read, and stands in the git log alone, where `git show` still reaches it. History is not rewritten and the tool does not read both forms. The limit is documented, as the record's start at the first `Task-completion:` commit already is.
- **The rename and the path-addressed redesign are one release, and its notes are the rebranding.** `VERSION` reads 1.9.0 and the redesign is on `main` unreleased, so the release that carries the rename carries the redesign too and a user upgrades once. `/release-plugin` writes its notes from finish summaries the renamed tool no longer prints, and that loss is accepted: the notes announce the rebranding, and everything else the release changed is described in the documentation, not itemised in the notes.

## Open questions

- **Whether the distribution repositories are renamed or recreated.** A renamed GitHub repository redirects its old URL for clones and the web, so existing installs keep resolving while the marketplace entry moves; a recreated one breaks them cleanly. The traffic-badge workflow and its `TRAFFIC_TOKEN`, scoped to exactly the four repositories by name, follow whichever is chosen. The fourth of those repositories, the source repository, is not part of this question: it is renamed to `uHappyLogic/gurita`, as the table of sites above records, and the token's scope follows its new name.
- **What the rename means for an installed copy.** A user who installed `cairn` invokes `/cairn:...`; after the rename those skills are `/gurita:...` and the plugin has a new name in the marketplace, so the user installs again rather than updates, and the hard cut leaves no alias behind. Whether that is a major version, and what the CHANGELOG entry and the old README say to the user who arrives at the old name, is the milestone's to settle.
- **What a project does with what it holds under the old word.** The hard cut rules out a tool that discovers both forms, so a milestone live at the upgrade is invisible to the renamed plugin until it stands at `mission_<slug>/`. Moving it there, one level up, is not a free rename: the tool's log reads follow no rename, so a moved mission loses its `Starting-state:` anchor, and its task list reads as added, not modified, at the new path, which turns a started mission back into a defined one that holds no scope until its list is next written. Two choices are left: a migration that moves the directories and re-establishes what the log no longer shows, or an upgrade rule that every live milestone is finished under the last Cairn release first. The same answer covers `/migrate-milestones`, which is on `main` unreleased and so ships in this release or never. Its re-finished `Milestone-finish: milestones/<dir>/` commits exist to be printed by `summary` and `record`, which after the rename print none of them, and it leaves a live milestone where it stands, under a path the new pattern does not match. What is left of it is cleanup, removing the pointer-era directories and `milestones/README.md` and rewriting the context file's workflow section, so it is cut down to that under a name that fits, replaced by whichever migration the live milestones get, or dropped with a rule that a pointer-era project starts clean. The context file's `## Milestone Workflow` section is rewritten with whichever is chosen. This repository had no live milestone on 2026-11-10, while other projects on the maintainer's machine, running the unreleased path-addressed form, did.
- **Where the principle store lives.** `milestones/answer_decision_principles.md` sits in the root container, which no longer exists once missions carry a prefix instead. It is one project-wide file read by the recommendation pass and written only by capture, at a fixed path both name literally, so it needs a fixed path that depends on no mission: a file at the project root, a file under a directory of the plugin's own, or the root `milestones/` directory kept for this one file. The last keeps every existing project's store where it is and keeps the old word in the tree.
- **How the word's rename is known to be complete.** A search that finds nothing cannot be the bar, because some occurrences stay by decision: the CHANGELOG's entries, 122 occurrences on 2026-11-10, the `milestone_NN` directory names and the numbered milestones the invariants in `CLAUDE.md` cite for their measurements, and whatever the answer on the old state, above, leaves in a migration skill. Nothing tells a leftover from one of those. The suites do not: they pin behaviour, not vocabulary, and the 1931 occurrences in `tests/` are fixtures and expected output that change together with the code they test, so a leftover in runtime prose, in the docs, or in a help text no test quotes fails nothing. The choices are a listed residue checked by a test, as `tests/test_fixed_console_lines.py` checks the console lines against their table, a listed residue checked once by hand when the work ends, or no bar beyond the drift gate and the suites.
- **Which sites carry the name as an identifier, and what verifies a change to them.** The table of sites above is short of what a check on 2026-11-10 found outside `hosts/`:
  - the source repository, now in the table but named as `uHappyLogic/cairn` in twelve files: the README, CONTRIBUTING, SECURITY, the CHANGELOG, the issue-template configuration, the release skill, and each host's README and CONTRIBUTING templates;
  - the marketplace name, written literally in `scripts/hosts/claude/.claude-plugin/marketplace.json` and `scripts/hosts/codex/.agents/plugins/marketplace.json`, where only the plugin's own name is the build's `{{NAME}}`;
  - the Codex template directory `scripts/hosts/codex/plugins/cairn/`, and in the Codex `settings.toml` the `plugin_dir` and the four layout paths beside `plugin_name`;
  - three Claude Code slot values that write the namespaced agent names out, `COMPLETE_TASK_DISPATCH.md`, `ALTERNATIVES_DISPATCH.md`, and `ALTERNATIVES_REPAIR.md`;
  - the host suite: `PLUGIN_ID = "cairn@cairn"`, the Antigravity root, and the Codex cache path in `host_tests/conftest.py`, and the `/cairn:` invocations in two of its tests;
  - `scripts/set_version.py`, which holds `cairn-tooling` as the lock package it rewrites;
  - `.claude/skills/release-plugin/SKILL.md`, which names the distribution repositories, creates them with the topic `cairn`, and carries the name in its description;
  - two file names, `docs/ways-of-using-cairn.md`, referenced from six files, and `ideas/benchmark_for_cairn.md`;
  - one runtime file, `core/skills/ask-in-milestone-context/SKILL.md`, whose prose says "the right cairn skill";
  - the dated hands-on check blocks heading the three `settings.toml` files, which quote install commands, invocations, and cache paths under the old name.

  The work needs the whole list before it starts, since a missed identifier is a broken install or dispatch, not a stale sentence. It also has to say what verifies the change. The plan above names the drift gate and both test runs, none of which exercises an installed copy, while the plugin's name, its namespace, its install paths, and ten skill names are what the host suite and each host's hands-on check cover, on all three hosts.
- **Under which word the rename's own work is recorded, and by which copy it is run.** The work is defined under `milestones/` and run by the copy of the plugin the maintainer's sessions load, so its finish commit is the last `Milestone-finish:` unless that copy changes before it finishes, in which case its directory is the first one the answer on the old state, above, is applied to. That copy is not a fixed install. The marketplace is a directory source at this repository, and on 2026-11-10 the sessions on the maintainer's machine, in this project and in others, ran the unreleased path-addressed skills, while the cache directory labelled 1.9.0 still held the released pointer-era ones: the copy in use is read from the working tree's `hosts/claude`. Whether a session reads it once at its start or again at each skill call was not tested. Either way a task that renames the plugin and rebuilds `hosts/claude` takes `cairn:complete-task`, `--milestone`, and the old discovery pattern away from the tasks after it, and from every other project's session running on the same machine, so the work pins the copy for its length, for one by running from a separate checkout, or makes the switch in its last task.

## Sources

- Octopus neuron distribution and arm autonomy: https://www.sciencealert.com/here-s-how-octopus-arms-make-decisions-without-input-from-the-brain
- Arms versus tentacles: https://livescience.com/difference-arms-tentacles
- Octopus Deploy's Tentacle agent: https://docs.octopusdeploy.com
- KBBI entry for `gurita` and `menggurita`: https://typoonline.com/kbbi/gurita
- The `gurita` uses found on 2026-11-10: https://www.npmjs.com/package/gurita , https://github.com/bjpop/gurita , https://github.com/gurita-dev
- Factory's Missions, talk coverage only: https://sozai.app/transcript/multi-agent-architecture-luke-alvoeiro-factory/index.md , https://www.startuphub.ai/news/missions-ai-agents-that-ship-for-days
- Tako collisions: https://github.com/redentordev/tako-cli , https://jsr.io/@takojs/tako , https://pkg.go.dev/gettako.dev/tako
