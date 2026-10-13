Use the `spawn_agent` tool to spawn one default (generic) subagent per surviving question,
with no custom agent type, and have it act as the plugin's
`provide-alternatives-to-open-question` agent (singular — the per-question subagent) by reading
and following that agent's file, `{{PLUGIN_ROOT}}/agents/provide-alternatives-to-open-question.md`.
Pass it that file's path, that question's **Short Title**, the `<MILESTONE_DIR>` resolved in
step 0, and the `<scratch dir>` created in sub-step **a**, and nothing else — the path, which the
subagent has no other way to learn, and the three values the orchestrator already holds:
