# TASKS TODO

## Rebuild Host Trees After Renderer Change

Run `uv run scripts/build_hosts.py` so both `hosts/claude` and `hosts/antigravity` carry the changed tool source and skill prose, then confirm `uv run scripts/build_hosts.py --check` passes so `main` stays drift-free. Verified by the `--check` run exiting cleanly.

---
