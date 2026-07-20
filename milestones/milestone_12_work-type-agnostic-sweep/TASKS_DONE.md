# TASKS DONE

## Neutralize Specify-Starting-State Skill Language

Sweep `skills/specify-milestone-starting-state/SKILL.md` — the skill that fills the `## Relevant starting state` section of a milestone's `requirements.md` — so it becomes fully work-type-agnostic. Reframe its code-analysis language ("Analyze the current codebase", "meaningful code", "exported functions/classes/types/interfaces", "schemas, database models", "Source files", "public API") as analyzing the project's existing artifacts and state whatever the work type, and reword its environment-context read per the milestone's decisions. The skill's function — grounding future decisions in what already exists — its seven-step workflow, and its output contract (filling the `## Relevant starting state` section) stay unchanged.

**Notes:**
- The environment-context read (step 3, "Load the environment and explore the codebase") follows the "Environment-context replacement wording" decision: reword the `CLAUDE.md` read from "tech stack or file organization" / "File organization … meaningful code" / "Available MCP tools" to the neutral enumeration "the project's domain context, working conventions, available tools, and how work is verified as done", keeping the enumerated shape. Reconcile against the exact phrasing the sibling "Neutralize Complete-Task Procedure Language" task provides. Retain the generalized `/init` pointer (`/init` documents any project regardless of work type — reword its trigger from "no description of the tech stack or file organization" to the neutral equivalent).
- The frontmatter `description` field currently reads "Analyze the current codebase and fill the … section … with technical context"; it carries SE framing and is in scope — neutralize it in the same pass (unlike the agent-persona task, whose frontmatter describes dispatch role, this line asserts the deliverable is a codebase).
- This skill carries neither a verification mechanism nor the canonical worked example, so neither the "Verification fallback" nor the "Canonical example content" decisions apply here — this is a language + environment-context sweep only.
- Structural elements that must survive the sweep unchanged: the seven numbered workflow steps and their flow, the commit step (step 6, `Starting-state: <milestone_id>` via `${CLAUDE_PLUGIN_ROOT}/shared/commit-procedure.md`), the terse success-reporting step (step 7, the fixed "Starting state recorded." line and its dirty-own-path no-op variant), the `## Relevant starting state` output template, and the `## Rules` section.

**Success:**
- No software-engineer-specific phrasing remains in the file — the code-analysis terms it currently carries ("Analyze the current codebase", "meaningful code", "exported functions/classes/types/interfaces", "schemas, database models", "Source files", "public API", "technical summary/context") are gone or neutralized, verifiable by reading the file (including the frontmatter `description`).
- The environment-context read (step 3) enumerates "the project's domain context, working conventions, available tools, and how work is verified as done", preserving the enumerated shape, with the generalized `/init` pointer retained.
- The seven numbered workflow steps and their flow, the step-6 commit (`Starting-state: <milestone_id>`), the step-7 terse reporting (the "Starting state recorded." line plus its no-op variant), the `## Relevant starting state` output template, and the `## Rules` section are all present and unchanged in function.

---

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

## Neutralize Submit-Task Procedure Language

Sweep `shared/submit-procedure.md` — the single-source task-authoring procedure run by the `submit-task` skill and agent and by `derive-tasks`' bulk dispatch — so it becomes fully work-type-agnostic. Neutralize its code-deliverable framing, reword its environment-context read per the milestone's decisions, and replace its Unity tower-defense worked example and software success-criterion models with the milestone's canonical work-type-neutral worked example. The task body template and the BRIEF+POSITION execution-neutral contract stay intact.

**Notes:**
- Three recorded decisions pin the wording and example — pull them directly rather than paraphrasing. The environment-context read (step 2) follows the "Environment-context replacement wording" decision: replace "tech stack, file organization, available MCP tools, build/test commands, and conventions" item-for-item with "the project's domain context, working conventions, available tools, and how work is verified as done", keeping the enumerated shape and retaining the generalized `/init` pointer (`/init` documents any project regardless of work type). Reconcile this against the exact phrasing the sibling "Neutralize Complete-Task Procedure Language" task provides.
- The canonical worked example, per the "Canonical example content" and "Replacement example strategy" decisions, is a task "Draft the Getting Started section of the user guide": deliverable is a Markdown/document file; `Provides` is the named `## Getting Started` heading later sections cross-link to; the `Notes` gotcha is that the auto-generated table of contents keys off `##` headings so a section added without one is silently dropped; the `Success` bar is inspection-checkable (the guide file exists at its path, contains a `## Getting Started` heading, stays under the agreed length) with an optional command criterion (the doc-lint check passes). This one example replaces the `Creep`/`RegisterWaveStart()`/`AllCreepsDead()` illustration and the "Build command exits with code 0" / "Function Z is exported from W" success-criterion models wherever they appear in the file (the `Notes` guideline's embedded gotcha and the `Success` guideline's example criteria both carry the SE illustrations).
- The file is execution-neutral by contract — it must stay silent on committing, the DONE/FAILED return protocol, triage, and follow-up, which live in the wrappers. Neutralizing language must not introduce any of those.
- This is a self-referential edit: the file being rewritten is the very procedure that authors tasks, so the task body template (`##` title, description, optional `Provides`, optional `Notes`, `Success`, trailing `---`), the BRIEF+POSITION input contract, the five-step flow, and the `## Rules` section must survive the language sweep unchanged — only framing, environment wording, and examples change.

**Success:**
- No software-engineer-specific phrasing remains in the file — the code-deliverable framing it currently carries ("write the code organically", "read from the code", "the public API", "read from the code" in the `Provides`/`Notes` guidelines) is gone or neutralized, verifiable by reading the file.
- The environment-context read (step 2) enumerates "the project's domain context, working conventions, available tools, and how work is verified as done", preserving the enumerated shape, with the generalized `/init` pointer retained.
- The Unity tower-defense worked example (`Creep`, `RegisterWaveStart()`, `AllCreepsDead()`) and the software success-criterion models ("Build command exits with code 0", "Function Z is exported from W") are replaced by the canonical written-guide example (the "Draft the Getting Started section of the user guide" task with its `## Getting Started` Provides, its table-of-contents `##`-heading Notes gotcha, and its inspection-checkable Success bar plus optional doc-lint command criterion).
- The task body template, the BRIEF+POSITION execution-neutral contract, the five numbered steps with the same flow, and the `## Rules` section are all unchanged, and the file remains execution-neutral (no mention of committing, the DONE/FAILED return protocol, triage, or follow-up).

---

## Neutralize Task-Layer Agent Personas

Sweep the two task-layer agent definitions `agents/submit-task.md` and `agents/complete-task.md` so both become work-type-agnostic. Each currently opens with a "You are a **Software Engineer** …" persona statement; replace those with work-type-neutral persona statements, and neutralize any residual software-engineering phrasing elsewhere in the two files in the same pass. This is the shallowest (agent-persona) layer of the sweep; the two shared procedures these agents run are neutralized by their own sibling tasks.

**Notes:**
- The change is confined to persona/framing wording. Each agent's reference to its shared procedure via `${CLAUDE_PLUGIN_ROOT}` (`shared/submit-procedure.md` for the submit agent, `shared/complete-procedure.md` for the complete agent), the `DONE`/`FAILED` return protocol, and the never-commit rule must stay intact — do not reword or restructure them.
- The submit agent's persona line ("turning one high-level task brief into a well-scoped task … your detailed technical reasoning never pollutes the caller's memory") and the complete agent's persona line ("completing one task from the project's task list") are the primary targets; scan the rest of each file for lighter SE-flavored phrasing (e.g. "technical reasoning") and neutralize it too.
- Do not touch the YAML frontmatter's `description` fields' behavioral meaning; these describe the agents' dispatch role, not the user's work type.

**Success:**
- No software-engineer-specific phrasing remains in either `agents/submit-task.md` or `agents/complete-task.md` — neither opens with a "You are a Software Engineer" persona, and no residual SE-flavored wording remains, verifiable by reading both files.
- Each file's shared-procedure reference (via `${CLAUDE_PLUGIN_ROOT}`) and its `DONE`/`FAILED` return protocol are present and unchanged.
- The never-commit rule is still present in both files (submit agent's "Do not commit."; complete agent's "Do not commit — committing is the orchestrator's job.").

---

