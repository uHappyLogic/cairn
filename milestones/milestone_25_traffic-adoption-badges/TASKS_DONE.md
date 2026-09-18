# TASKS DONE

## Relax Build Placeholder Gate For Expressions

Change the build's `unfilled-placeholder` check in `scripts/build_hosts.py` from any `{{` to a `{{` not immediately preceded by `$` (the lookbehind `(?<!\$)\{\{`), so a GitHub Actions `${{ … }}` expression passes in any rendered file of any host while a bare `{{VERSION}}`, `{{NAME}}`, or `{{PLUGIN_ROOT}}` still fails, and reword the script's docstring and the CLAUDE.md clauses that say no `{{` anywhere to no `{{` outside a `${{` expression. The two distribution workflow templates cannot pass the build without this. Verified when `uv run scripts/build_hosts.py --check` still passes on the unchanged trees, a scratch render containing `${{ secrets.X }}` passes the check, and one containing a bare `{{X}}` fails it.

**Verified:**

- `scripts/build_hosts.py`'s `unfilled-placeholder` check matches with the compiled regex `(?<!\$)\{\{` (`UNFILLED_PLACEHOLDER_RE.search(line)`, a `{{` not immediately preceded by `$`) instead of the substring test `"{{" in line`.
- The check stays one uniform test over every rendered text file of every host — no path-scoped exemption, template escape, or new `settings.toml` key — and no `settings.toml` or template file changed; the change set is `scripts/build_hosts.py` and `CLAUDE.md` only.
- The script docstring's `unfilled-placeholder` line reads no `"{{"` outside a `"${{"` expression anywhere in the tree (with the lookbehind and the pass/fail cases in its parenthetical) rather than no `"{{"` anywhere in the tree.
- Both CLAUDE.md clauses — the `scripts/build_hosts.py` layout entry's "no {{ left anywhere" and the Development section's "no `{{` is left anywhere in the tree" — now read no `{{` left anywhere outside a `${{` expression, each with the lookbehind, the uniform-check statement, and the pass/fail cases in a parenthetical; a grep finds no other CLAUDE.md statement of the old rule.
- `uv run scripts/build_hosts.py --check` exits 0 on the unchanged committed trees ("Check passed: hosts/antigravity/ and hosts/claude/ match a fresh build of core/ at version 1.5.0.").
- A scratch render (a temporary copy of the build inputs with a `.github/workflows/scratch.yml` template under both `scripts/hosts/claude/` and `scripts/hosts/antigravity/` containing `${{ secrets.X }}` and `${{ github.token }}`) built with exit 0 and both rendered files carried the expressions byte-for-byte intact.
- A scratch render whose template carried a bare `{{X}}` aborted with exit 1 and an `unfilled-placeholder` failure naming that line for both hosts; a template `{{PLUGIN_ROOT}}` line and a `core/` file's bare `{{VERSION}}` and `{{NAME}}` each tripped the same failure, and a line mixing `${{ ok }}` with a bare `{{X}}` still failed (the lookbehind is per-occurrence, not per-line).

---

## Author Monorepo Traffic Badges Workflow

Add `.github/workflows/traffic-badges.yml` (`name: traffic-badges`) to the monorepo beside `drift-gate.yml`: a `workflow_dispatch` plus one cron `17 3 * * *` commented as daily at 03:17 UTC, `permissions: {}` with a one-line comment that the job token is unused because the action reads the Traffic API and pushes with `TRAFFIC_TOKEN`, and two steps of `albertoarena/github-traffic-badge` pinned to `56f6f3e0ed586f14440561758b197ca57a38f480` with a `# v1.1.4` comment, one for metric `views-unique` and one for `clones-unique`, each passing `token: ${{ secrets.TRAFFIC_TOKEN }}`, `label` `unique views` / `unique clones`, `color` `3b82f6`, `style` `flat`, and `output` `views-unique.svg` / `clones-unique.svg` written out explicitly, with no leading inert-copy comment. This is the monorepo's one of the three hand-kept copies, and CLAUDE.md's description of `drift-gate.yml` as the only workflow is updated to name it. Verified when the file loads as valid YAML, `actionlint` or an equivalent reports no error, and a grep for `github-traffic-badge@` finds the pinned SHA.

**Verified:**

- `.github/workflows/traffic-badges.yml` exists beside `drift-gate.yml`, its first line is `name: traffic-badges`, and the file carries no leading comment (zero `#`-prefixed lines, no inert-copy header).
- Its triggers are `workflow_dispatch` plus exactly one `schedule` entry, `cron: '17 3 * * *'`, followed on the same line by the comment `# daily at 03:17 UTC`.
- Its permissions block is `permissions: {}` followed on the same line by the one-line comment `# job token unused: the action reads the Traffic API and pushes with TRAFFIC_TOKEN`, and no `contents:` grant appears anywhere in the file.
- The one job `badges` has exactly two steps, each `uses: albertoarena/github-traffic-badge@56f6f3e0ed586f14440561758b197ca57a38f480 # v1.1.4`; the input names `token`, `metric`, `label`, `color`, `style`, and `output` match the action's `action.yml` at that SHA, read via `gh api`.
- Step one passes `token: ${{ secrets.TRAFFIC_TOKEN }}`, `metric: views-unique`, `label: unique views`, `color: 3b82f6`, `style: flat`, `output: views-unique.svg`; step two passes the same `token`, `color`, and `style` with `metric: clones-unique`, `label: unique clones`, `output: clones-unique.svg` — every rendering input written explicitly, none inherited from the action's defaults.
- `CLAUDE.md`'s layout entry for `drift-gate.yml` no longer calls it "the one CI workflow" but "the CI workflow, one of the two workflows under .github/workflows/ (the other is traffic-badges.yml below)", and a new layout entry for `.github/workflows/traffic-badges.yml` describes the monorepo's hand-kept copy (triggers, `permissions: {}`, the pinned SHA, both steps' inputs, the traffic-data branch, the by-hand cross-copy grep); a grep finds no remaining only-workflow claim in `CLAUDE.md`, `README.md`, or `CONTRIBUTING.md`, and the "only automated check" sentence stays true because the traffic workflow is not a check.
- `yaml.safe_load` loads the file: `name` is `traffic-badges`, `on` holds `workflow_dispatch` and the one cron, `permissions` is an empty mapping, and every `with:` value of both steps — `color: 3b82f6` included — is a string.
- `actionlint` 1.7.12 (the prebuilt release binary, since Homebrew is blocked by the Xcode licence) reports no error on `.github/workflows/traffic-badges.yml` (exit 0), as it does on `drift-gate.yml`.
- `grep -n 'github-traffic-badge@' .github/workflows/traffic-badges.yml` finds the pinned SHA `56f6f3e0ed586f14440561758b197ca57a38f480` on both step lines (14 and 22).
- `uv run scripts/build_hosts.py --check` still passes ("Check passed: hosts/antigravity/ and hosts/claude/ match a fresh build of core/ at version 1.5.0."); the change set is `.github/workflows/traffic-badges.yml` and `CLAUDE.md` only, touching neither `core/`, `scripts/hosts/`, nor `hosts/`.

---
