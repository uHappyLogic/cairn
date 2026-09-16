"""Write one MAJOR.MINOR.PATCH version literal into every version surface in this repo.

Usage: uv run scripts/set_version.py MAJOR.MINOR.PATCH

The root VERSION file is the single source of truth for the plugin version. It holds the
bare literal on one newline-terminated line and nothing else, so `cat VERSION`, Python, or
any build reads it without a parser. Every other version literal in the repo is a mirrored
surface that this script keeps in lockstep with it.

Surfaces written:
  - VERSION                          the bare literal (source of truth)
  - .claude-plugin/marketplace.json  "version" on the single plugins[] entry (the monorepo's
                                     hand-held marketplace, mirrored)
  - pyproject.toml                   version under [project] (cairn-tooling, mirrored)
  - uv.lock                          version in the cairn-tooling [[package]] block (mirrored)

Deliberately not written:
  - anything under hosts/            every host manifest (plugin.json, and the dist
                                     marketplace.json for Claude Code) is rendered under
                                     hosts/<host>/ by the host build, scripts/build_hosts.py,
                                     from a template whose version slot is filled from VERSION
  - .claude-plugin/plugin.json       not a surface: no plugin manifest is written by this script

This script only edits files. It never invokes git or gh. All four surfaces are rendered in
memory first, so a failure on any one of them leaves every file untouched.
"""

import json
import os
import re
import sys

VERSION_PATTERN = re.compile(r"^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)$")

VERSION_FILE = "VERSION"
MARKETPLACE_MANIFEST = os.path.join(".claude-plugin", "marketplace.json")
PYPROJECT = "pyproject.toml"
UV_LOCK = "uv.lock"

LOCK_PACKAGE_NAME = "cairn-tooling"


class SurfaceError(Exception):
    """A version surface could not be read or rewritten."""


def fail(message):
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def require_surface(path):
    if not os.path.exists(path):
        raise SurfaceError(f"{path} not found (run this script from the repository root)")


def read_text(path):
    require_surface(path)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def dump_json(data):
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def render_version_file(version):
    # The file's whole content is the literal, so nothing is read back: the existence check
    # is the same repository-root guard every other surface gets.
    require_surface(VERSION_FILE)
    return f"{version}\n"


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
    (VERSION_FILE, render_version_file),
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
