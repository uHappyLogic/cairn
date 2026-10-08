# TASKS DONE

## Agent Writes Scratch File and Returns DONE

Rewrite `core/agents/provide-alternatives-to-open-question.md` so the agent takes the run's scratch directory as a required third prompt value beside the Short Title and `<MILESTONE_DIR>`, writes its self-checked `<alternative>` elements to `<scratch dir>/<Short Title>.xml.part` and renames that file with one `mv` to `<scratch dir>/<Short Title>.xml` (the Short Title exactly as given, a path separator in it failing the write and surfacing as a `FAILED:` skip), and ends its session with the bare token `DONE`, or with `FAILED: <reason>` as before and no file written; its read-only contract toward the project stands with that one file outside the repository as the stated exception, and its two tool calls, grounding, enumeration, and two-anchor self-check stay as they are. The rule is host-neutral and unconditional (no branch on whether the directory value is present), the frontmatter description stays one clause within the 25-word cap, and the change is verified by rebuilding `hosts/` with `uv run scripts/build_hosts.py` and passing `--check`, with the rebuilt trees committed alongside.

**Verified:**

- `core/agents/provide-alternatives-to-open-question.md` states three prompt values (Short Title, Milestone directory, Scratch directory), the scratch directory required and already created by the orchestrator, with no branch on whether it is present.
- Step 4 has the agent write the self-checked `<alternative>` elements to `<scratch dir>/<Short Title>.xml.part` and rename it with one `mv` to `<scratch dir>/<Short Title>.xml`, the Short Title used exactly as given, and a path separator in it failing the write as a `FAILED:` with no directory created.
- On success the agent ends with the bare token `DONE`; on failure with `FAILED: <reason>` and no file at `<scratch dir>/<Short Title>.xml`.
- The read-only contract toward the project stands with the one scratch file outside the repository as the stated exception; the two tool calls (`locate`, `list --with-question`), grounding, enumeration via `alternatives-procedure.md`, and the two-anchor self-check are unchanged.
- The agent file names no host; the frontmatter description is one clause of 22 words, no colon or semicolon, loadable by `yaml.safe_load`.
- `uv run scripts/build_hosts.py` rebuilt the three host trees and `uv run scripts/build_hosts.py --check` passed; the Claude Code and Antigravity agent files differ only in the stripped `color` key; `uv run pytest` passed (544 tests).

---
