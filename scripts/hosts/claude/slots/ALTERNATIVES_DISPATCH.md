Use the `Agent` tool with `subagent_type` set to the namespaced registry name of the
`provide-alternatives-to-open-question` agent (singular — the per-question subagent) under this
plugin's namespace, `cairn:provide-alternatives-to-open-question` — one dispatch per surviving
question. Pass it that question's **Short Title**, the `<MILESTONE_DIR>` resolved in step 0, and
the `<scratch dir>` created in sub-step **a**, and nothing else — the three values the
orchestrator already holds:
