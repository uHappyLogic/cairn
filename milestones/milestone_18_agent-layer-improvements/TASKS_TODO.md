# TASKS TODO

## Rewrite Plugin Root References For Antigravity

Make `scripts/migrate_skills_to_agy.py` rewrite every `${CLAUDE_PLUGIN_ROOT}/shared/<name>.md` reference in the copied skills, agents, and shared files to a path resolvable relative to the generated `.agents/plugins/cairn/` tree, then regenerate that tree, closing the milestone-15 follow-up under which those references are copied verbatim and resolve nowhere. Verified when no file under `.agents/plugins/cairn/` contains the literal `${CLAUDE_PLUGIN_ROOT}` and every rewritten reference names a file that exists in the generated tree.

---
