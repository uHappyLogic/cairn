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
