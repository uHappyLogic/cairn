"""Write one MAJOR.MINOR.PATCH version literal into every version surface in this repo.

Usage: uv run scripts/set_version.py MAJOR.MINOR.PATCH

Surfaces written:
  - .claude-plugin/plugin.json       "version" on the manifest
  - .claude-plugin/marketplace.json  "version" on the single plugins[] entry (added if absent)
  - pyproject.toml                   version under [project] (cairn-tooling)
  - uv.lock                          version in the cairn-tooling [[package]] block

The generated Antigravity manifest .agents/plugins/cairn/plugin.json is deliberately not
written here: the transpiler copies the version out of .claude-plugin/plugin.json on every
regeneration, so .claude-plugin/plugin.json stays the single source of truth.

This script only edits files. It never invokes git or gh, and it writes nothing under
.agents/. All four files are parsed and rewritten in memory first, so a failure on any one
surface leaves every file untouched.
"""

import json
import os
import re
import sys

VERSION_PATTERN = re.compile(r"^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)$")

PLUGIN_MANIFEST = os.path.join(".claude-plugin", "plugin.json")
MARKETPLACE_MANIFEST = os.path.join(".claude-plugin", "marketplace.json")
PYPROJECT = "pyproject.toml"
UV_LOCK = "uv.lock"

LOCK_PACKAGE_NAME = "cairn-tooling"


class SurfaceError(Exception):
    """A version surface could not be read or rewritten."""


def fail(message):
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def read_text(path):
    if not os.path.exists(path):
        raise SurfaceError(f"{path} not found (run this script from the repository root)")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def dump_json(data):
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def render_plugin_manifest(version):
    data = json.loads(read_text(PLUGIN_MANIFEST))
    if "version" not in data:
        raise SurfaceError(f"{PLUGIN_MANIFEST} has no 'version' key to update")
    data["version"] = version
    return dump_json(data)


def render_marketplace_manifest(version):
    data = json.loads(read_text(MARKETPLACE_MANIFEST))
    plugins = data.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        raise SurfaceError(f"{MARKETPLACE_MANIFEST} does not hold exactly one plugins[] entry")
    plugins[0]["version"] = version
    return dump_json(data)


def render_pyproject(version):
    lines = read_text(PYPROJECT).split("\n")
    in_project = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            in_project = stripped == "[project]"
            continue
        if in_project and re.match(r'^version\s*=\s*"[^"]*"\s*$', line):
            lines[i] = f'version = "{version}"'
            return "\n".join(lines)
    raise SurfaceError(f"{PYPROJECT} has no version line under [project]")


def render_uv_lock(version):
    lines = read_text(UV_LOCK).split("\n")
    in_target_package = False
    for i, line in enumerate(lines):
        if line.strip() == "[[package]]":
            in_target_package = False
            continue
        if line.strip() == f'name = "{LOCK_PACKAGE_NAME}"':
            in_target_package = True
            continue
        if in_target_package and re.match(r'^version\s*=\s*"[^"]*"\s*$', line):
            lines[i] = f'version = "{version}"'
            return "\n".join(lines)
    raise SurfaceError(f"{UV_LOCK} has no version line for the {LOCK_PACKAGE_NAME} package")


RENDERERS = (
    (PLUGIN_MANIFEST, render_plugin_manifest),
    (MARKETPLACE_MANIFEST, render_marketplace_manifest),
    (PYPROJECT, render_pyproject),
    (UV_LOCK, render_uv_lock),
)


def set_version(version):
    rendered = []
    for path, render in RENDERERS:
        rendered.append((path, render(version)))

    for path, content in rendered:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Wrote version {version} to {path}")


def main(argv):
    if len(argv) != 1:
        fail(
            "expected exactly one argument, a bare MAJOR.MINOR.PATCH version literal\n"
            "Usage: uv run scripts/set_version.py MAJOR.MINOR.PATCH"
        )

    version = argv[0]
    if not VERSION_PATTERN.match(version):
        fail(
            f"'{version}' is not a bare MAJOR.MINOR.PATCH version literal "
            "(three dot-separated integers, no 'v' prefix, no suffix, no leading zeros)"
        )

    try:
        set_version(version)
    except (SurfaceError, json.JSONDecodeError, OSError) as e:
        fail(f"{e}\nNo files were changed.")


if __name__ == "__main__":
    main(sys.argv[1:])
