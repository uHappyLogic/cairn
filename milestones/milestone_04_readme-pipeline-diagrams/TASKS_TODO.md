# TASKS TODO

## Fix Stale Self-Dogfooding Milestone Reference

Correct the one factually-wrong milestone reference in `README.md`'s `## Self-dogfooding` section. That section names the active milestone directory as `milestones/milestone_01_public-release-prep/`, but three milestones have since completed and the current active milestone is `milestone_04`. Update the reference to `milestones/milestone_04_readme-pipeline-diagrams/`. This is the single mandated polish edit for the whole milestone (per `requirements.md` `## Decisions` → Polish scope); make no other discretionary polish edits.

**Notes:**
- Two tasks in this milestone edit `README.md`; this one is the mirror of the diagram-rewrite task — it must touch **only** the `## Self-dogfooding` section and leave `## Workflow pipeline` and `## Skill reference` untouched. Locate the section by its `## Self-dogfooding` heading, not by line numbers (they drift once the sibling diagram task lands).

**Success:**
- The `## Self-dogfooding` section no longer contains the string `milestone_01_public-release-prep` and instead references `milestone_04_readme-pipeline-diagrams` as the active milestone directory.
- The sentence naming the active milestone directory remains grammatical and accurate.
- No README section other than `## Self-dogfooding` is modified.

---
