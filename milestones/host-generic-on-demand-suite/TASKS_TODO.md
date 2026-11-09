# TASKS TODO

## Keep Headless Runs From Writing Bytecode

The release pre-flight task's Antigravity run left `tools/__pycache__/open_questions.cpython-313.pyc` in `~/.gemini/config/plugins/cairn`, so the next Antigravity run stops on the installed-copy check until the copy is refreshed: a session the suite started wrote into an installed copy the suite promises to leave untouched. Make the shared run fixture start every host's headless command with `PYTHONDONTWRITEBYTECODE=1` in its environment, so no session it starts writes bytecode into any installed copy, leaving the file-for-file freshness rule, extra files included, as it is, and start by refreshing the Antigravity copy from the built `hosts/antigravity/` tree. It is verified by the composed run's environment carrying the variable, by a run whose session imports a tool module under the installed root leaving no `__pycache__` there, and by two consecutive `uv run pytest host_tests --host antigravity` runs both passing the prerequisite check.

---
