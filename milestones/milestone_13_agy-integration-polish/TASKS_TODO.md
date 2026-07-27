# TASKS TODO

## Enforce Source Frontmatter in Transpilation Script

Update the `scripts/migrate_skills_to_agy.py` script to enforce that every legacy source skill carries YAML frontmatter with both `name` and `description` defined. It must abort with a hard error if either is missing, rather than silently injecting dummy fallbacks, to ensure Antigravity's semantic intent matching works at runtime.

**Notes:**
- The script currently injects dummy frontmatter (`name: {skill_name}`, `description: Transpiled from...`) when it's missing; this fallback logic needs to be removed entirely.
- A missing `name` or `description` key inside an existing frontmatter block must also trigger the hard error.

**Success:**
- Running the script locally against a dummy skill with missing frontmatter aborts with a hard error.
- Running the script locally against a dummy skill with frontmatter but missing a `name` or `description` key aborts with a hard error.
- Running the script against valid skills transpiles them correctly.

---

## Document Transpilation Build Step

Add instructions for running the local transpilation step to both `CLAUDE.md` and a new development section in `README.md` so contributors know how to build the plugin for both platforms.

**Provides:**
- A new development section in `README.md` detailing the build process.

**Notes:**
- The transpilation script is `scripts/migrate_skills_to_agy.py`.

**Success:**
- `CLAUDE.md` contains instructions for running the transpilation step.
- `README.md` contains a new development section with instructions for running the transpilation step.

---

## Update GitHub Project Description

Update the GitHub repository description programmatically using the GitHub CLI to reflect the project's dual-platform support. This is needed to provide a clear, direct signal of dual-support for users searching for either Claude Code or Google Antigravity.

**Notes:**
- The GitHub CLI (`gh`) is already configured locally, so no authentication setup is required before running the edit command.

**Success:**
- Running `gh repo edit --description "Milestone-driven development workflow for Claude Code and Google Antigravity."` executes successfully.
- Running `gh repo view` confirms the description matches the new text.

---
