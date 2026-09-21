# TASKS TODO

## Write Ways Of Using Cairn Page

Create the tracked `docs/ways-of-using-cairn.md` from the untracked `temp/CAIRN_USAGE.md`: a `#` title and a one-paragraph intro naming the sibling docs pages, then the one `##` legend section (angle-bracket placeholder notation, the `-p "/cairn:<skill>"` line form, one sentence per headless flag — `--dangerously-skip-permissions`, `--model`, `--effort`, `--add-dir` — with its per-host form, and the one-line host swap), then the five ways of the recorded inventory in pipeline order, each under the fixed per-way template (a `##` heading naming the goal, one or two sentences on when to use it and what it yields, the chain as one fenced block) with every line runnable as written and generalized per the Decisions (`<milestone_id>` and `<project-root>` placeholders, a shell comment where each `claude-wait` stood, no `-c`, no argument on `goto-next-milestone`, model and effort values verbatim). Present host, model, and effort mixing as mechanics with no benefit claims, and add the page's entry to the `CLAUDE.md` repository-layout block as milestone 26 did for `docs/design-claims.md`. Verified by the page holding exactly five way sections after the legend, every fenced block closed, no private alias, absolute path, empty-prompt line, or project-specific milestone id remaining, and every chain line otherwise reproduced from the draft snippet that ran it.

---

## Link Page From README How It Works

Extend the closing sentence of `README.md`'s `## How it works` section, the one linking `docs/workflow.md` and `docs/skill-reference.md`, with a link to `docs/ways-of-using-cairn.md` beside those two so the README routes readers to the headless command chains, and update the `CLAUDE.md` layout entry for `README.md` that describes that closing sentence. Verified by the section ending with all three links resolving to existing files and `CONTRIBUTING.md` left untouched.

---

## Cross-Link Sibling Docs Pages To Ways Page

Add one clause to the routing sentence in the intro paragraph of each of `docs/workflow.md` and `docs/skill-reference.md` pointing at `docs/ways-of-using-cairn.md` as where the skills are chained headlessly, leaving `docs/design-claims.md` linked from the README's Design principles block alone, and update the two `CLAUDE.md` layout entries describing those intros. Verified by each intro linking the new page with the rest of both pages unchanged.

---
