# TASKS DONE

## Author Shared Skill-Layer Commit Procedure

Create the single execution-neutral source of truth for the skill-layer commit step — a new file under `shared/` that every committing skill and committing orchestrator will reference via `${CLAUDE_PLUGIN_ROOT}` (never restate), exactly as `complete-task`/`submit-task`/`answer-open-question-with-recommendation` reference their shared procedures today. It is the foundational artifact of this milestone: every later task points downstream skills at this convention rather than duplicating it.

The document must state all four elements of the milestone's committing model as decided in `requirements.md`:

- **Path-scoped staging** — stage only explicitly named paths, never `git add -A`, and decide the path set without content inspection (no diffing to choose what to include).
- **Commit-subject convention** — each committing skill's subject prefix is derived systematically from its distinctive function in the established `<Marker>: <descriptor>` house shape (the `-answer:` family being one instance), with every prefix staying clear of capture's `^Manual-answer:` grep by construction — no ad-hoc per-skill list, no grandfathered exceptions.
- **Dirty-own-path no-op guard** — after a pass, if the skill's own paths did not actually change, stage nothing, commit nothing, report the no-op, and return cleanly (no `--allow-empty`).
- **Layer rule** — user-invoked skills that change files commit; dispatched agents never commit; an orchestrator skill commits its agents' work after they return.

The document takes resolved inputs (the path set and the subject) and holds only the commit logic — no arg-parsing, no skill-specific behavior — mirroring how `shared/answer-procedure.md` is execution-neutral while its wrappers own arg-parsing and committing.

**Provides:**
- `shared/commit-procedure.md` — the execution-neutral shared commit core referenced by every committing skill/orchestrator via `${CLAUDE_PLUGIN_ROOT}`. Its input contract is a resolved path set plus a resolved commit subject; it defines path-scoped staging, the `<Marker>: <descriptor>` subject convention (all prefixes clear of `^Manual-answer:`), the dirty-own-path no-op guard, and the skills-commit/agents-never-commit/orchestrator-commits-after-return layer rule.

**Notes:**
- This is authoring one new Markdown file only — it wires no existing skill onto the procedure (each committer's rewiring is a later task) and changes no other file. It must be written so downstream skills can reference it without restating any of it, following the plugin's `shared/ = single source of truth across ≥2 runners` convention.
- Keep it execution-neutral in the plugin's established sense: it must not mention arg-parsing, the `DONE`/`FAILED` agent return protocol, `<MILESTONE_DIR>` resolution, or any per-skill subject — those belong to the wrapping skills/agents/orchestrators. The layer rule is stated as a rule the wrappers follow, not as behavior this file executes.
- The no-op guard is deliberately `--allow-empty`-free; state the guard as check-own-paths-then-skip, matching the `No-op pass commit` decision in `requirements.md`.

**Success:**
- `shared/commit-procedure.md` exists.
- Its content states all four elements: path-scoped staging (never `git add -A`, no content inspection), the systematic `<Marker>: <descriptor>` subject convention that stays clear of `^Manual-answer:`, the dirty-own-path no-op guard (no `--allow-empty`), and the skills-commit / agents-never-commit / orchestrator-commits-after-return layer rule.
- The document is execution-neutral: it references no specific skill's arguments or subject prefix and describes no arg-parsing, and it is phrased so a skill can reference it via `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md` without restating its steps.

---

