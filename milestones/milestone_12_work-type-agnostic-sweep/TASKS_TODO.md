# TASKS TODO

## Neutralize Goal-Skill Examples

Replace the remaining game-flavored illustrations in the two goal skills — `skills/define-milestone-goal/SKILL.md` and `skills/modify-milestone-goal/SKILL.md` — with work-type-neutral goal examples, closing re-audit findings 1–4. `define-milestone-goal` carries a shooting-mechanic `## Usage` example and a matching `player-shooting` slug-derivation example; `modify-milestone-goal` carries a shooting-mechanic `## Usage` example and an "offline playback" delta example on its argument line. These four survived the milestone's sweep because neither file was in scope of any neutralization task.

**Notes:**
- Per the recorded "Canonical example content" and "Replacement example strategy" decisions, reuse the milestone's one canonical written-guide example rather than inventing a second neutral example. The sibling `skills/discuss-milestone-goal/SKILL.md` already anchors this after its own sweep with `/discuss-milestone-goal add a getting-started guide that walks a new user through their first session` — keep the two goal-skill `## Usage` examples consistent with that user-guide-drafting goal, and derive the `define-milestone-goal` slug example from the same goal (a `getting-started-guide`-style slug in place of `player-shooting`).
- `modify-milestone-goal`'s delta example must stay a *delta* (a described change folded into an existing goal, not a full replacement) to keep illustrating that argument mode — reword "also support offline playback" to a neutral delta consistent with the guide example (e.g. broadening or narrowing the guide's scope), naming no software/game specifics.
- Examples-only sweep: neither file carries a verification mechanism or an environment-context read, so the "Verification fallback" and "Environment-context replacement wording" decisions do not apply. Touch only the illustrative example content — each skill's workflow, steps, argument contracts, and structure stay unchanged.

**Success:**
- No shooting/spline/projectile or offline-playback content remains in either file, verifiable by reading both — the `## Usage` examples, the `define-milestone-goal` slug-derivation example, and the `modify-milestone-goal` delta example are all work-type-neutral and name no software or game specifics.
- The replacement examples are consistent with the milestone's canonical written-guide example (the getting-started-guide goal `discuss-milestone-goal` already uses); no second neutral example is introduced.
- `modify-milestone-goal`'s argument-line example still illustrates a *delta* change (not a full replacement goal), preserving what that example teaches.
- Each skill's workflow, numbered steps, argument contracts, and structure are otherwise unchanged in function.

---
