# TASKS DONE

## Neutralize Complete-Task Procedure Language

Sweep `shared/complete-procedure.md` — the single-source completion procedure run by the `complete-task` skill and agent — so it becomes fully work-type-agnostic. Neutralize its software-engineering language, reframe its verification mechanism to check the deliverable against the task's Success criteria however the project defines done (with the recorded fallback), and reword its environment-context read per the milestone's decisions. The procedure's steps, execution-neutral contract, and structure stay intact.

**Provides:**
- The neutral environment-context enumeration wording — "the project's domain context, working conventions, available tools, and how work is verified as done" — used verbatim here; sibling sweep tasks and the CLAUDE.md environment-context invariant reconcile against this exact phrasing.

**Notes:**
- Two recorded decisions pin exact wording — pull it directly rather than paraphrasing. The environment-context read follows the "Environment-context replacement wording" decision (keep the enumerated shape). The reframed verification follows the "Verification fallback without conventions" decision: when the consuming project's CLAUDE.md defines no done-verification convention, verify by direct inspection of the deliverable against the Success section criterion-by-criterion, running a command only where a criterion names one.
- The file is execution-neutral by contract — it must stay silent on committing, the DONE/FAILED return protocol, and follow-up, which live in the wrappers. Neutralizing language must not introduce any of those.
- This is a self-referential edit: the file being rewritten is the very procedure the completer follows, so the step flow (steps 1–5) and their headings must survive the language sweep unchanged.

**Success:**
- No software-engineer-specific phrasing remains in the file — the SE terms it currently carries ("insertion points"/"insertion point", "assertion wording", "the live codebase", "source file(s)", "exports", "build/test commands", "post-edit verification") are gone or neutralized, verifiable by reading the file.
- The environment-context read (step 2) enumerates "the project's domain context, working conventions, available tools, and how work is verified as done", preserving the enumerated shape.
- The verification mechanism (step 4) is reframed from "run the verification command / build & test" to verifying the deliverable against the task's Success criteria however the project's conventions define done, and the recorded fallback (direct criterion-by-criterion inspection of the deliverable, running a command only where a criterion names one, when CLAUDE.md defines no done-verification convention) is present.
- The procedure still has its five numbered steps with the same flow and its `## Rules` section, and remains execution-neutral (no mention of committing, the DONE/FAILED return protocol, or follow-up).

---

