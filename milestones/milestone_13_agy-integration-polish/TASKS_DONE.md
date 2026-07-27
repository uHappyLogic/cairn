# TASKS DONE

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
