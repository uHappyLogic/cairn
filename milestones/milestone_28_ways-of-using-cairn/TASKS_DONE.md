# TASKS DONE

## Write Ways Of Using Cairn Page

Create the tracked `docs/ways-of-using-cairn.md` from the untracked `temp/CAIRN_USAGE.md`: a `#` title and a one-paragraph intro naming the sibling docs pages, then the one `##` legend section (angle-bracket placeholder notation, the `-p "/cairn:<skill>"` line form, one sentence per headless flag — `--dangerously-skip-permissions`, `--model`, `--effort`, `--add-dir` — with its per-host form, and the one-line host swap), then the five ways of the recorded inventory in pipeline order, each under the fixed per-way template (a `##` heading naming the goal, one or two sentences on when to use it and what it yields, the chain as one fenced block) with every line runnable as written and generalized per the Decisions (`<milestone_id>` and `<project-root>` placeholders, a shell comment where each `claude-wait` stood, no `-c`, no argument on `goto-next-milestone`, model and effort values verbatim). Present host, model, and effort mixing as mechanics with no benefit claims, and add the page's entry to the `CLAUDE.md` repository-layout block as milestone 26 did for `docs/design-claims.md`. Verified by the page holding exactly five way sections after the legend, every fenced block closed, no private alias, absolute path, empty-prompt line, or project-specific milestone id remaining, and every chain line otherwise reproduced from the draft snippet that ran it.

**Verified:**

- `docs/ways-of-using-cairn.md` exists, opening with the `#` title `Ways of using Cairn` and one intro paragraph linking the three sibling pages `workflow.md` (and its `#how-skills-commit` anchor), `skill-reference.md`, and `design-claims.md`.
- Exactly one `##` legend section, `Notation and flags`, sits between the intro and the first way, headed for what it holds; it states that angle brackets mark the only substituted text, defines the two placeholders `<milestone_id>` (spelled as the skill reference's `specify-milestone-starting-state <milestone_id>` heading) and `<project-root>`, gives the `-p "/cairn:<skill>"` line form, carries exactly four one-sentence flag bullets (`--dangerously-skip-permissions`, `--model`, `--effort`, `--add-dir`) with each flag's per-host form as `claude --help` and `agy --help` give it (family aliases `opus`/`fable` vs. an id from `agy models`; `low`–`max` vs. `low`–`high`; both remaining flags on both hosts), and ends with the one-sentence host swap presenting the per-host forms.
- Exactly five `##` way sections follow the legend, in pipeline order — Starting a milestone, Running a mixed-agent requirements review, Putting more intelligence into a stuck milestone, Executing tasks, Finishing a milestone — each a goal heading, one or two sentences on when to run it and what it yields, and one fenced block (10 fence lines, every block closed, no two-backtick line).
- All 18 chain lines map back to the draft snippet that ran them under only the mandated generalizations, checked programmatically: `goto-next-milestone` bare, `specify-milestone-starting-state <milestone_id>`, `-c` dropped from the review line, `--add-dir "<project-root>"` on the `agy` line, model and effort values verbatim (`--model "opus"`/`"fable"`, `--effort high`/`xhigh`/`max`), no `--model` or `--effort` added to the `agy` line, the two `claude-wait` positions replaced by the shell comment `# wait until your account's usage window has reset` with both `complete-all-tasks` lines kept and the way's sentences stating the usage-limit resume, and the all-opus first run demoted to one sentence of the first way.
- No `claude-wait`, `/Users/`, `agy -p ""`, `milestone_02_youtube-watch-only`, `milestone_87_gdd-settlement-structure-note`, ` -c `, or session/continuation mention remains anywhere on the page.
- Host, model, and effort mixing is stated as mechanics only (a benefit-word scan for better/stronger/smarter/cheaper/faster/quality/reliability/improvement finds nothing), with what a setting buys routed to `design-claims.md`.
- `CLAUDE.md`'s repository-layout block carries a new `docs/ways-of-using-cairn.md` entry directly after the `docs/design-claims.md` entry, em dash aligned to the same column as the other three `docs/` entries, and the `README.md` entry's count of docs entries reads "the first three entries below".
- `README.md`, `CONTRIBUTING.md`, `docs/workflow.md`, and `docs/skill-reference.md` are untouched (`git diff --stat` empty for all four), and `uv run scripts/build_hosts.py --check` passes.

---

## Link Page From README How It Works

Extend the closing sentence of `README.md`'s `## How it works` section, the one linking `docs/workflow.md` and `docs/skill-reference.md`, with a link to `docs/ways-of-using-cairn.md` beside those two so the README routes readers to the headless command chains, and update the `CLAUDE.md` layout entry for `README.md` that describes that closing sentence. Verified by the section ending with all three links resolving to existing files and `CONTRIBUTING.md` left untouched.

**Verified:**

- The closing sentence of `README.md`'s `## How it works` section — the last paragraph before `## Self-dogfooding` — links `docs/workflow.md`, `docs/skill-reference.md`, and `docs/ways-of-using-cairn.md`, the third link added beside the two existing ones in that single sentence, its clause routing readers to the headless command chains ("how to chain the skills as headless command lines, mixing hosts, models, and effort levels").
- All three link targets in that sentence resolve to existing files (each `docs/…` path extracted from the sentence passes `[ -f ]`; link count is exactly three).
- The `README.md` diff is confined to that one sentence (`git diff --stat`: 1 insertion, 1 deletion, the closing-sentence line only); no other line changed.
- The `CLAUDE.md` layout entry for `README.md` describes `## How it works` as closing with one sentence linking all three pages, naming `docs/ways-of-using-cairn.md` as where the skills are chained as headless command lines.
- `CONTRIBUTING.md` is untouched (`git diff --stat -- CONTRIBUTING.md` empty).
- `uv run scripts/build_hosts.py --check` passes.

---
