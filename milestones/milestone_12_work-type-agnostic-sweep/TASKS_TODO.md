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

## Neutralize Code-Construct Task Vocabulary

Reword the residual code/OOP-construct vocabulary in `skills/derive-tasks/SKILL.md` and `shared/complete-procedure.md` to work-type-neutral equivalents, closing re-audit findings 5–7. Both files were already swept by earlier milestone tasks ("Neutralize Derive-Tasks Skill Language", "Neutralize Complete-Task Procedure Language"), but this specific vocabulary survived: `derive-tasks` twice frames a brief's excluded low-level detail as "method names" (the intro's "if you get lost in file-paths and method names" and step 3's "does not contain file paths, method names, contract surface, or success criteria"), and `complete-procedure`'s step-3 Provides guidance lists the named surface as "files, methods, classes, fields, thresholds" — "methods, classes, fields" being OOP constructs that assume a code deliverable.

**Notes:**
- Preserve the exact meaning of each spot while removing the code assumption — this is a like-for-like vocabulary swap, not a rewrite. In `derive-tasks`, both occurrences distinguish the *high-level brief* from the *low-level per-piece detail* that is the completer's job; the neutral wording must keep that altitude contrast (the point is that decomposition breaks when you drop into fine-grained specifics, whatever their form). In `complete-procedure`, the list names the kinds of things a `Provides` entry pins as a fixed contract for sibling tasks; the neutral wording must still read as concrete named surface (a project of any work type still has files/sections/named artifacts and thresholds — drop only the OOP-specific "methods, classes, fields").
- `shared/complete-procedure.md` is execution-neutral by contract — it must stay silent on committing, the DONE/FAILED return protocol, and follow-up. This vocabulary swap must not disturb that or the procedure's step flow.

**Success:**
- No code-construct vocabulary remains in either file — "method names" is gone from both `derive-tasks` spots (intro and step 3), and "methods, classes, fields" is gone from `complete-procedure`'s Provides list, verifiable by reading both files.
- The reworded phrasing preserves the original meaning at each spot: `derive-tasks` still contrasts the high-level brief against low-level per-piece detail, and `complete-procedure`'s Provides guidance still names concrete shared surface other tasks depend on.
- Each file's workflow, contracts, structure, and (for `complete-procedure`) execution-neutrality are otherwise unchanged in function.

---
