# TASKS TODO

## Write Codex Distribution Repository Templates

Add the root-level templates of `scripts/hosts/codex/`: the `CONTRIBUTING.md` pointer, the `.github/workflows/traffic-badges.yml` copy, and a `README.md` that opens with the badge strip the other two host templates share and names the Codex command-line tool as the supported surface, saying nothing about the desktop app or the IDE extension. The README gives the install commands `codex plugin marketplace add uHappyLogic/cairn-codex` then `codex plugin add cairn@cairn` as the only route, the `$cairn:init-milestone-base-workflow` invocation form with a note that the slash names inside the skills refer to the same skills, `AGENTS.md` as the context file, and the sandbox instructions: workspace-write with on-request approval and no `config.toml` change, every git staging or commit step asking for approval because that sandbox keeps `.git` read-only, and the `python3` tools needing only read access to the installed plugin directory. Verified by a rebuild that lands all three files at the root of `hosts/codex/` beside `LICENSE` and passes `--check`.

---

## Add Codex Installation to Root README

Add a `### Codex` subsection under `## Installation` in the root `README.md` that repeats the Codex README template's installation section word for word, including its `$cairn:init-milestone-base-workflow` form, so the landing page covers the third host. The adoption table gains no `uHappyLogic/cairn-codex` row in this milestone. Verified by comparing the subsection against `scripts/hosts/codex/README.md` and confirming the adoption table is unchanged.

---

## Add Codex to Issue Form Dropdown

Add `codex` as a third option of the required host dropdown in `.github/ISSUE_TEMPLATE/bug.yml` and name Codex, installed from `cairn-codex` with its manifest at `.codex-plugin/plugin.json`, in the field descriptions that enumerate hosts, so a Codex bug can be reported against the right host. Verified by the file loading as YAML with three host options.

---

## Name Codex in Contributing and Security

Change only the sentences that list hosts or repositories: in `CONTRIBUTING.md` (`## Development`) the supported-hosts sentence becomes a three-host sentence, the definition-directory list adds `scripts/hosts/codex/`, the committed-tree list adds `hosts/codex/`, and the distribution-repository sentence adds a `cairn-codex` link; in `SECURITY.md` "both distribution repositories" becomes all three, with a `cairn-codex` link beside the other two. Verified by reading both files and finding no sentence that still enumerates only two hosts or repositories.

---

## Document Codex Headless Runs in Docs

Extend the "Notation and flags" section of `docs/ways-of-using-cairn.md` so Codex is a third binary: `codex exec '$cairn:<skill>'` is the Codex form of a line, the permission bypass maps to `--dangerously-bypass-approvals-and-sandbox`, `--model` has a counterpart in `-m`, `--effort` has no flag, `--add-dir` exists under the same name, and the `<goal>` rule becomes "no single quote" on Codex lines. The one-line swap rule is extended so a line moves to Codex by changing the binary, dropping `--model` and `--effort`, replacing the permission flag, and rewriting `"/cairn:<skill>"` to `'$cairn:<skill>'`. Verified by reading the section against those points and confirming no chain gained a Codex line and the page names no Codex model id or effort level.

---

## Add Traffic Token Check to Release Skill

Add a check that names no host to the step 2f host loop of `.claude/skills/release-plugin/SKILL.md`: for every distribution repository it runs `gh secret list --repo uHappyLogic/cairn-<host>` and, when the `TRAFFIC_TOKEN` secret is missing, stops and prints the maintainer's instructions without running anything, the same way a missing repository is handled. Those instructions say to extend the one token to the new repository, regenerate it, and re-set the secret in every repository, then after publishing to run the repository's `traffic-badges` workflow once by `workflow_dispatch` and add the repository's row to the root README's adoption table in its own commit, apart from the `Release:` commit; the `CLAUDE.md` Development note changes from three repositories to four. Verified by reading the step for the check, the printed instructions, and the absence of any host name.

---

## Verify Codex Install and Agent Dispatches

In a new minimal git repository in a temporary directory outside the cairn checkout, seeded without a model by running the milestone-definition tool and the open-question tool directly so it holds one milestone with one bare open question and one small task, run three live checks exactly once each: add the marketplace from the committed `hosts/codex/` directory and run `codex plugin add cairn@cairn`, then run one dispatch of each agent as a headless `codex exec` run with `--dangerously-bypass-approvals-and-sandbox`, calling Codex by its full path, the alternatives dispatch leaving alternatives embedded in the seed's question. The task passes only when all three pass: a free-tier quota stop leaves it open to resume at the first unrun check with earlier evidence kept as valid, and a result that contradicts a recorded decision is reported as a failure, never fixed or decided here. The three outcomes and the workspace's path are recorded in `TASKS_DONE.md`, the workspace is kept for the interactive check, and no seed or run script is kept.

---

## Confirm Maintainer Interactive Codex Check

The fourth live check is the maintainer's: in an interactive Codex session in the kept verification workspace, under the workspace-write sandbox with on-request approval, they run `$cairn:recommend-all-open-questions` and approve its git steps. This task passes only when the workspace shows that run, such as the `Recommendation-annotation:` commit the skill leaves in the workspace's git history, and the completer must never run the skill itself; without that evidence the task fails and stays open until the maintainer has run the check. On a pass it records the fourth outcome in `TASKS_DONE.md` and deletes the workspace.

---
