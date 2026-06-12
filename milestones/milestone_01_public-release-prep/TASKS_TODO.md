# TASKS TODO








## Rewrite README for Public Adoption

Replace `README.md` with a complete, freshly authored adoption-focused rewrite that serves as both the landing page and the user manual. The current file is maintainer/developer-facing with no installation section, no "why use this" framing, and no marketplace-add instructions; this task makes it a public-facing document. The rewrite splits existing content by audience — carrying forward the condensed pipeline overview and skill reference, and dropping the maintainer-only content that already lives in `CLAUDE.md`.

**Notes:**
- This is a full rewrite, not a patch. The existing content is split by audience: adoption-relevant content (pipeline overview, skill reference) is condensed and carried forward; maintainer-only content (deep file-structure docs, altitude/invariant rules from `CLAUDE.md`'s Invariants section) is dropped entirely and must NOT be relocated.
- The self-dogfooding setup (the repo runs its own workflow on itself — `milestones/` and the active milestone directory are live workflow artifacts) must remain visible as a credibility showcase.
- By the time this task runs, `.claude-plugin/plugin.json` already carries `name: "cairn"` and `.claude-plugin/marketplace.json` already exists — so the install command and naming are consistent and can be referenced directly.
- No `CONTRIBUTING.md` and no `docs/` directory are created; the milestone produces exactly one public README.

**Success:**
- `README.md` opens with `# Cairn`, followed by the tagline **"Mark the path from idea to shipped."** and the subtitle **"Milestone-driven development for any stack."**
- `README.md` contains an installation section whose install command is `/plugin marketplace add uHappyLogic/cairn`.
- `README.md` contains a "what problem this solves / why use it" section aimed at a first-time visitor.
- `README.md` contains a condensed pipeline overview (the ordered skill sequence from bootstrap through milestone archival).
- `README.md` contains a skill reference section.
- `README.md` contains no deep file-structure documentation (no table or prose describing the `.claude-plugin/`, `skills/`, `agents/`, `shared/` layout as a maintainer reference) and no altitude/invariant rules.
- No `CONTRIBUTING.md` file exists in the repo after this task runs.
- No `docs/` directory exists in the repo after this task runs.
- No files other than `README.md` are modified by this task.

---
