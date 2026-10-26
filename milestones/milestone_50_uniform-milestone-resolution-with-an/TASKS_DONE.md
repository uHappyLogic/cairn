# TASKS DONE

## Add Override Input To Pointer Procedure

`core/shared/get-current-milestone.md` gains its one input, an optional leading `--milestone <milestone_id>` in the skill's invocation text: it states once the rule for recognizing the flag and separating it from the skill's own positional text, takes the value verbatim as the exact milestone directory name under `milestones/` (no bare-number resolution, no stripped `milestones/` prefix or trailing slash) to form `milestones/<milestone_id>/`, and resolves an override without reading the pointer, so it is honoured even when the pointer reads `none`. When `milestones/<milestone_id>/requirements.md` does not exist the procedure stops with no fallback to the pointer, on an error line naming the given value followed by a list of every `milestone_*` directory under `milestones/` and no pointer to `/define-milestone-goal`; with no override the pointer's path stays unchecked and is handed on exactly as today. Verified by reading the rendered procedure in each host tree and by `uv run scripts/build_hosts.py --check` passing after the `hosts/` rebuild.

**Verified:**

- `core/shared/get-current-milestone.md` states one input, an optional leading `--milestone <milestone_id>` in the skill's invocation text, with the rule for recognizing it (first whitespace-separated token exactly `--milestone`, value the next token) and for separating it from the skill's own positional text (both tokens stripped, the rest read as if the flag were never written) stated once, in its `## Recognizing the override` section.
- The override value is taken verbatim as the exact directory name under `milestones/` to form `milestones/<milestone_id>/`, with no bare-number resolution and no stripped `milestones/` prefix or trailing slash.
- An override is resolved without reading `milestones/README.md`, so it is honoured whatever the pointer reads, `none` included.
- When `milestones/<milestone_id>/requirements.md` does not exist the procedure stops without changing anything and with no fallback to the pointer, on the error line `Error: --milestone <milestone_id> matches no milestone directory` naming the given value, followed by every `milestone_*` directory under `milestones/`, and with no pointer to `/define-milestone-goal`.
- With no override the pointer steps are unchanged and the extracted path is handed on as `<MILESTONE_DIR>` with no existence check.
- The rendered procedure in `hosts/claude/shared/`, `hosts/antigravity/shared/`, and `hosts/codex/plugins/cairn/shared/` is byte-identical to the core file and was read to carry the override input.
- `uv run scripts/build_hosts.py --check` passes (exit 0) after the `hosts/` rebuild.

---
