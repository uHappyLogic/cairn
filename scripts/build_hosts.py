"""Build every host plugin tree under hosts/<host>/ from the host-neutral core/.

Usage: uv run scripts/build_hosts.py [<host> ...] [--check]

A host is declared by a definition directory scripts/hosts/<host>/ holding a settings.toml
(plugin_name, the plugin_root literal, prose_drop_patterns, strip_frontmatter_keys, the
[layout] of core/'s top-level directories, renames, and exclude) beside that host's template
files; every file in the directory other than settings.toml is a template rendered to the
same relative path in the host tree with its {{VERSION}} slot filled from the root VERSION
file and its {{NAME}} slot from plugin_name. The build discovers hosts by scanning that
directory and applies the settings uniformly, so no host-specific code exists here and a
definition is validated before any build runs.

With no host argument every discovered host is built; one or more host names build only
those. Each selected host is rendered from core/ into a temporary directory and the whole
render is run through the check set below before anything under hosts/ is touched. The
rendered trees are swapped into hosts/<host>/ only when every selected host passes every
check; otherwise the build exits non-zero listing every failing file and check, and no
hosts/ tree is written.

Checks (every selected host, every failure listed):
  host-name-in-core         core/ names no host: no definition directory name stands as its
                            own word in any core/ file (an identifier that merely contains
                            it, such as CLAUDE.md or a Claude-Session: trailer, is not a
                            mention of the host)
  root-marketplace-version  every plugins[] entry of .claude-plugin/marketplace.json carries
                            exactly the VERSION literal
  frontmatter-missing, frontmatter-invalid, frontmatter-keys
                            every rendered skills/<name>/SKILL.md and agents/<name>.md has
                            YAML frontmatter that yaml.safe_load accepts, with name and
                            description
  description-length        every such description is at or under 25 words
  unfilled-placeholder      no "{{" outside a "${{" expression anywhere in the tree (a "{{"
                            not immediately preceded by "$", so a bare {{VERSION}},
                            {{NAME}}, or {{PLUGIN_ROOT}} slot fails while a GitHub
                            Actions ${{ ... }} expression in a rendered workflow passes)
  foreign-plugin-root       no other host's plugin-root literal anywhere in the tree
  dangling-plugin-root      every occurrence of this host's own plugin-root literal that a
                            /path follows names a file in this tree
  stripped-key-present      no frontmatter key the definition strips is still present
  manifest-json, manifest-version
                            every rendered JSON template parses, and every "version" value
                            in it is exactly the VERSION literal

--check renders and checks the selected hosts the same way, then compares each render
byte-for-byte against the committed hosts/<host>/ tree, writes nothing, and exits non-zero
listing the differing paths. It is the drift gate the release pre-flight runs.

Exit status: 0 on success, 1 when a check or the comparison fails, 2 when the build cannot
run at all (bad argument, unusable definition, missing input). This script reads core/,
scripts/hosts/, VERSION, LICENSE, and the root marketplace, writes only under hosts/, and
never invokes git or gh.
"""

import argparse
import json
import os
import posixpath
import re
import shutil
import sys
import tempfile
import tomllib
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = REPO_ROOT / "core"
DEFINITIONS_DIR = REPO_ROOT / "scripts" / "hosts"
HOSTS_DIR = REPO_ROOT / "hosts"
VERSION_FILE = REPO_ROOT / "VERSION"
LICENSE_FILE = REPO_ROOT / "LICENSE"
ROOT_MARKETPLACE = REPO_ROOT / ".claude-plugin" / "marketplace.json"

SETTINGS_FILE = "settings.toml"
PLUGIN_ROOT_SLOT = "{{PLUGIN_ROOT}}"
VERSION_SLOT = "{{VERSION}}"
NAME_SLOT = "{{NAME}}"
PLACEHOLDER_OPEN = "{{"
DESCRIPTION_WORD_CAP = 25
REQUIRED_FRONTMATTER_KEYS = ("name", "description")

VERSION_PATTERN = re.compile(r"^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)$")

# An unfilled placeholder: a `{{` not immediately preceded by `$`, so the bare {{VERSION}},
# {{NAME}}, and {{PLUGIN_ROOT}} slots trip it while a GitHub Actions `${{ ... }}` expression
# in a rendered workflow does not.
UNFILLED_PLACEHOLDER_RE = re.compile(r"(?<!\$)\{\{")
# A frontmatter block is a leading `---` line, its content, and the next `---` line.
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)^---[ \t]*(?:\n|\Z)", re.S | re.M)
# A top-level frontmatter key: the key at the start of a line, before its colon.
FRONTMATTER_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_.-]*)[ \t]*:")

# The settings every definition must carry, with the TOML type each must have. A key with
# nothing to declare is present and empty, never omitted, so the shape is identical across
# hosts.
SETTINGS_SCHEMA = {
    "plugin_name": str,
    "plugin_root": str,
    "prose_drop_patterns": list,
    "strip_frontmatter_keys": list,
    "renames": list,
    "exclude": list,
    "layout": dict,
}


class BuildError(Exception):
    """The build cannot run: an argument, a definition, or an input is unusable."""


class HostDefinition:
    """One scripts/hosts/<host>/ definition, validated and ready to render."""

    def __init__(self, name, directory, settings, templates):
        self.name = name
        self.directory = directory
        self.plugin_name = settings["plugin_name"]
        self.plugin_root = settings["plugin_root"]
        self.prose_drop_patterns = [re.compile(p) for p in settings["prose_drop_patterns"]]
        self.strip_frontmatter_keys = list(settings["strip_frontmatter_keys"])
        self.renames = [(r["from"], r["to"]) for r in settings["renames"]]
        self.exclude = [e.strip("/") for e in settings["exclude"]]
        self.layout = dict(settings["layout"])
        self.templates = templates


# --- inputs ---------------------------------------------------------------------------


def read_version():
    if not VERSION_FILE.is_file():
        raise BuildError("VERSION not found at the repository root")
    version = VERSION_FILE.read_text(encoding="utf-8").strip()
    if not VERSION_PATTERN.match(version):
        raise BuildError(f"VERSION does not hold a bare MAJOR.MINOR.PATCH literal: {version!r}")
    return version


def decode_text(data):
    """The UTF-8 text of a file's bytes, or None when the file is not UTF-8 text."""
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def walk_files(root):
    """Relative POSIX paths of every file under root, sorted for a deterministic order."""
    paths = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for filename in filenames:
            paths.append(Path(dirpath, filename).relative_to(root).as_posix())
    return sorted(paths)


def core_top_level_dirs():
    if not CORE_DIR.is_dir():
        raise BuildError("core/ not found at the repository root")
    dirs = []
    for entry in sorted(CORE_DIR.iterdir()):
        if entry.is_dir():
            dirs.append(entry.name)
        else:
            raise BuildError(
                f"core/{entry.name} is a file at the top level of core/; the layout maps "
                "top-level directories only"
            )
    if not dirs:
        raise BuildError("core/ holds no top-level directory to render")
    return dirs


def is_relative_path(value):
    """A non-empty relative path that stays inside the tree it is relative to."""
    if value == "" or posixpath.isabs(value):
        return False
    normalized = posixpath.normpath(value)
    return normalized != ".." and not normalized.startswith("../")


def load_definition(directory, core_dirs):
    """Read and validate one definition directory; every problem is a BuildError."""
    name = directory.name
    label = f"scripts/hosts/{name}/{SETTINGS_FILE}"
    settings_path = directory / SETTINGS_FILE
    if not settings_path.is_file():
        raise BuildError(f"{label} not found: every definition directory must carry one")
    try:
        settings = tomllib.loads(settings_path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as e:
        raise BuildError(f"{label}: {e}")

    missing = sorted(set(SETTINGS_SCHEMA) - set(settings))
    unknown = sorted(set(settings) - set(SETTINGS_SCHEMA))
    if missing:
        raise BuildError(f"{label} is missing the key(s) {', '.join(missing)}")
    if unknown:
        raise BuildError(f"{label} carries the unknown key(s) {', '.join(unknown)}")
    for key, kind in SETTINGS_SCHEMA.items():
        if not isinstance(settings[key], kind):
            raise BuildError(f"{label}: {key} must be a {kind.__name__}")

    for key in ("plugin_name", "plugin_root"):
        if not settings[key].strip():
            raise BuildError(f"{label}: {key} must not be empty")
    if PLACEHOLDER_OPEN in settings["plugin_root"]:
        raise BuildError(f"{label}: plugin_root must be a literal, not a placeholder")

    for key in ("prose_drop_patterns", "strip_frontmatter_keys", "exclude"):
        if not all(isinstance(item, str) and item for item in settings[key]):
            raise BuildError(f"{label}: every {key} entry must be a non-empty string")
    for pattern in settings["prose_drop_patterns"]:
        try:
            re.compile(pattern)
        except re.error as e:
            raise BuildError(f"{label}: prose_drop_patterns entry {pattern!r} is not a valid regex: {e}")
    for entry in settings["exclude"]:
        if not is_relative_path(entry):
            raise BuildError(f"{label}: exclude entry {entry!r} must be a path relative to core/")

    for rename in settings["renames"]:
        if (
            not isinstance(rename, dict)
            or set(rename) != {"from", "to"}
            or not all(isinstance(rename[k], str) and is_relative_path(rename[k]) for k in ("from", "to"))
        ):
            raise BuildError(
                f"{label}: every renames entry must be a table with `from` and `to` paths "
                "relative to the host tree root"
            )

    layout = settings["layout"]
    if sorted(layout) != core_dirs:
        raise BuildError(
            f"{label}: [layout] must map exactly the top-level directories of core/ "
            f"({', '.join(core_dirs)}); it maps {', '.join(sorted(layout)) or 'nothing'}"
        )
    for key, value in layout.items():
        if not isinstance(value, str) or (value not in ("", ".") and not is_relative_path(value)):
            raise BuildError(f"{label}: layout.{key} must be a path relative to the host tree root")

    templates = [p for p in walk_files(directory) if p != SETTINGS_FILE]
    return HostDefinition(name, directory, settings, templates)


def discover_definitions(core_dirs):
    if not DEFINITIONS_DIR.is_dir():
        raise BuildError("scripts/hosts/ not found: no host definitions to build")
    directories = [
        entry
        for entry in sorted(DEFINITIONS_DIR.iterdir())
        if entry.is_dir() and not entry.name.startswith(".")
    ]
    if not directories:
        raise BuildError("scripts/hosts/ holds no host definition directory")
    return [load_definition(directory, core_dirs) for directory in directories]


def select_definitions(definitions, requested):
    if not requested:
        return list(definitions)
    by_name = {d.name: d for d in definitions}
    unknown = sorted(set(requested) - set(by_name))
    if unknown:
        raise BuildError(
            f"no host definition named {', '.join(repr(n) for n in unknown)} under scripts/hosts/ "
            f"(available: {', '.join(by_name)})"
        )
    return [d for d in definitions if d.name in set(requested)]


# --- rendering ------------------------------------------------------------------------


def split_frontmatter(text):
    """(frontmatter content, body) when text opens with a frontmatter block, else None."""
    m = FRONTMATTER_RE.match(text)
    if m is None:
        return None
    return m.group(1), text[m.end():]


def strip_frontmatter_keys(text, keys):
    """Delete the given top-level keys (with any continuation lines) from a frontmatter block."""
    if not keys:
        return text
    split = split_frontmatter(text)
    if split is None:
        return text
    frontmatter, body = split
    kept = []
    skipping = False
    for line in frontmatter.split("\n"):
        m = FRONTMATTER_KEY_RE.match(line)
        if m:
            skipping = m.group(1) in keys
        elif not line.startswith((" ", "\t", "-")):
            skipping = False
        if not skipping:
            kept.append(line)
    stripped = "\n".join(kept)
    if stripped == frontmatter:
        return text
    return "---\n" + stripped + "---\n" + body


def is_excluded(core_rel, exclude):
    return any(core_rel == e or core_rel.startswith(e + "/") for e in exclude)


def describe_origin(origin):
    kind, rel = origin
    if kind == "core":
        return f"core/{rel}"
    if kind == "template":
        return f"the template {rel}"
    return "the root LICENSE"


def render_host(defn, version, dest):
    """Render one host into dest; returns {tree path: origin} for every file written."""
    files = {}

    def add(out_rel, data, origin):
        out_rel = posixpath.normpath(out_rel)
        if out_rel in files:
            raise BuildError(
                f"{defn.name}: {describe_origin(files[out_rel][1])} and {describe_origin(origin)} "
                f"both render to hosts/{defn.name}/{out_rel}"
            )
        files[out_rel] = (data, origin)

    for core_rel in walk_files(CORE_DIR):
        if is_excluded(core_rel, defn.exclude):
            continue
        top, _, rest = core_rel.partition("/")
        data = (CORE_DIR / core_rel).read_bytes()
        text = decode_text(data)
        if text is not None:
            text = text.replace(PLUGIN_ROOT_SLOT, defn.plugin_root)
            for pattern in defn.prose_drop_patterns:
                text = pattern.sub("", text)
            text = strip_frontmatter_keys(text, defn.strip_frontmatter_keys)
            data = text.encode("utf-8")
        add(posixpath.join(defn.layout[top], rest), data, ("core", core_rel))

    for src, dst in defn.renames:
        src = posixpath.normpath(src)
        if src not in files:
            raise BuildError(f"{defn.name}: renames entry moves hosts/{defn.name}/{src}, which the layout does not produce")
        data, origin = files.pop(src)
        add(dst, data, origin)

    for tpl_rel in defn.templates:
        data = (defn.directory / tpl_rel).read_bytes()
        text = decode_text(data)
        if text is not None:
            text = text.replace(VERSION_SLOT, version).replace(NAME_SLOT, defn.plugin_name)
            data = text.encode("utf-8")
        add(tpl_rel, data, ("template", tpl_rel))

    add("LICENSE", LICENSE_FILE.read_bytes(), ("license", "LICENSE"))

    for out_rel, (data, _origin) in files.items():
        path = dest / out_rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return {out_rel: origin for out_rel, (_data, origin) in files.items()}


# --- checks ---------------------------------------------------------------------------
# Each check yields (path, check name, detail) triples; the build collects every one before
# deciding, so a failing run lists every failing file and check at once.


def host_name_pattern(name):
    # The host name as its own word: not preceded or followed by an identifier character,
    # so `CLAUDE.md` and `Claude-Session:` (identifiers containing it) are not mentions.
    return re.compile(rf"(?<![A-Za-z0-9_.-]){re.escape(name)}(?![A-Za-z0-9_.-])", re.IGNORECASE)


def check_core_names_no_host(host_names):
    failures = []
    patterns = [(name, host_name_pattern(name)) for name in host_names]
    for core_rel in walk_files(CORE_DIR):
        text = decode_text((CORE_DIR / core_rel).read_bytes())
        if text is None:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for name, pattern in patterns:
                if pattern.search(line):
                    failures.append((f"core/{core_rel}", "host-name-in-core", f'line {lineno} names host "{name}"'))
    return failures


def check_root_marketplace(version):
    label = ".claude-plugin/marketplace.json"
    check = "root-marketplace-version"
    try:
        doc = json.loads(ROOT_MARKETPLACE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return [(label, check, f"cannot be read: {e}")]
    plugins = doc.get("plugins") if isinstance(doc, dict) else None
    if not isinstance(plugins, list) or not plugins:
        return [(label, check, "holds no plugins[] entry")]
    failures = []
    for index, entry in enumerate(plugins):
        found = entry.get("version") if isinstance(entry, dict) else None
        if found != version:
            failures.append((label, check, f'plugins[{index}].version is {found!r}, VERSION is "{version}"'))
    return failures


def requires_frontmatter(core_rel):
    """Whether a core/ file is a skill or agent definition, which must carry frontmatter."""
    parts = core_rel.split("/")
    return (parts[0] == "skills" and len(parts) == 3 and parts[2] == "SKILL.md") or (
        parts[0] == "agents" and len(parts) == 2 and parts[1].endswith(".md")
    )


def json_versions(node, keypath="$"):
    """Every ("keypath", value) for a key named "version" anywhere in a JSON document."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "version":
                yield f"{keypath}.version", value
            yield from json_versions(value, f"{keypath}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from json_versions(value, f"{keypath}[{index}]")


def check_host_tree(defn, tree, origins, definitions, version):
    failures = []
    foreign_roots = [
        (other.name, other.plugin_root)
        for other in definitions
        if other.name != defn.name and other.plugin_root != defn.plugin_root
    ]
    own_reference = re.compile(re.escape(defn.plugin_root) + r"(?:/([A-Za-z0-9_./-]*))?")

    for out_rel in sorted(origins):
        label = f"hosts/{defn.name}/{out_rel}"
        origin_kind, origin_rel = origins[out_rel]
        text = decode_text((tree / out_rel).read_bytes())
        if text is None:
            continue
        lines = text.splitlines()

        for lineno, line in enumerate(lines, 1):
            if UNFILLED_PLACEHOLDER_RE.search(line):
                failures.append((label, "unfilled-placeholder", f"line {lineno}: {line.strip()}"))
            for other_name, other_root in foreign_roots:
                if other_root in line:
                    failures.append(
                        (label, "foreign-plugin-root", f'line {lineno} contains the {other_name} plugin root "{other_root}"')
                    )

        for lineno, line in enumerate(lines, 1):
            for m in own_reference.finditer(line):
                ref = m.group(1)
                if ref is None:
                    continue
                ref = ref.rstrip(".")
                if ref == "":
                    continue
                target = tree / posixpath.normpath(ref)
                if not is_relative_path(ref) or not target.is_file():
                    failures.append(
                        (label, "dangling-plugin-root", f'line {lineno}: "{defn.plugin_root}/{ref}" names no file in this tree')
                    )

        split = split_frontmatter(text)
        required = origin_kind == "core" and requires_frontmatter(origin_rel)
        if split is None:
            if required:
                failures.append((label, "frontmatter-missing", "no YAML frontmatter block"))
        else:
            frontmatter = split[0]
            for key in defn.strip_frontmatter_keys:
                if re.search(rf"^{re.escape(key)}[ \t]*:", frontmatter, re.M):
                    failures.append((label, "stripped-key-present", f'frontmatter still carries "{key}"'))
            if required:
                try:
                    loaded = yaml.safe_load(frontmatter)
                except yaml.YAMLError as e:
                    failures.append((label, "frontmatter-invalid", str(e).splitlines()[0]))
                else:
                    if not isinstance(loaded, dict):
                        failures.append((label, "frontmatter-keys", "frontmatter is not a mapping"))
                    else:
                        for key in REQUIRED_FRONTMATTER_KEYS:
                            value = loaded.get(key)
                            if not isinstance(value, str) or not value.strip():
                                failures.append((label, "frontmatter-keys", f'no "{key}" value'))
                        description = loaded.get("description")
                        if isinstance(description, str):
                            words = len(description.split())
                            if words > DESCRIPTION_WORD_CAP:
                                failures.append(
                                    (label, "description-length", f"description is {words} words, cap is {DESCRIPTION_WORD_CAP}")
                                )

        if origin_kind == "template" and out_rel.endswith(".json"):
            try:
                doc = json.loads(text)
            except json.JSONDecodeError as e:
                failures.append((label, "manifest-json", str(e)))
            else:
                for keypath, value in json_versions(doc):
                    if value != version:
                        failures.append((label, "manifest-version", f'{keypath} is {value!r}, VERSION is "{version}"'))

    return failures


# --- comparison and swap ---------------------------------------------------------------


def compare_trees(rendered, committed):
    """(tree path, status) for every path that differs between the render and hosts/<host>/."""
    rendered_paths = set(walk_files(rendered))
    committed_paths = set(walk_files(committed)) if committed.is_dir() else set()
    differences = []
    for rel in sorted(rendered_paths | committed_paths):
        if rel not in committed_paths:
            differences.append((rel, "missing from the committed tree"))
        elif rel not in rendered_paths:
            differences.append((rel, "not produced by the build"))
        elif (rendered / rel).read_bytes() != (committed / rel).read_bytes():
            differences.append((rel, "differs from the build"))
    return differences


def swap_in(rendered, dest):
    """Replace dest with the rendered tree, staging the copy beside it so the rename is atomic."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    staging = dest.parent / f".{dest.name}.building"
    if staging.exists():
        shutil.rmtree(staging)
    shutil.copytree(rendered, staging)
    if dest.exists():
        shutil.rmtree(dest)
    staging.rename(dest)


# --- entry point ----------------------------------------------------------------------


def unique(failures):
    seen = set()
    for failure in failures:
        if failure not in seen:
            seen.add(failure)
            yield failure


def main(argv):
    parser = argparse.ArgumentParser(
        prog="uv run scripts/build_hosts.py",
        description="Build every host plugin tree under hosts/<host>/ from core/ through its scripts/hosts/<host>/ definition.",
    )
    parser.add_argument(
        "hosts", nargs="*", metavar="host",
        help="definition directory names under scripts/hosts/ to build (default: every one)",
    )
    parser.add_argument(
        "--check", action="store_true",
        help="render and check, then compare byte-for-byte against the committed hosts/<host>/ trees without writing",
    )
    args = parser.parse_args(argv)

    try:
        version = read_version()
        if not LICENSE_FILE.is_file():
            raise BuildError("LICENSE not found at the repository root")
        core_dirs = core_top_level_dirs()
        definitions = discover_definitions(core_dirs)
        selected = select_definitions(definitions, args.hosts)

        failures = check_core_names_no_host([d.name for d in definitions])
        failures += check_root_marketplace(version)

        with tempfile.TemporaryDirectory(prefix="build_hosts-") as tmp:
            renders = []
            for defn in selected:
                rendered = Path(tmp) / defn.name
                origins = render_host(defn, version, rendered)
                failures += check_host_tree(defn, rendered, origins, definitions, version)
                renders.append((defn, rendered, len(origins)))

            failures = list(unique(failures))
            if failures:
                files = {path for path, _check, _detail in failures}
                print(
                    f"{'Check' if args.check else 'Build'} aborted: {len(failures)} check failure(s) "
                    f"in {len(files)} file(s); nothing under hosts/ was written.",
                    file=sys.stderr,
                )
                for path, check, detail in failures:
                    print(f"  {path}: {check}: {detail}", file=sys.stderr)
                return 1

            names = " and ".join(f"hosts/{defn.name}/" for defn, _rendered, _count in renders)
            if args.check:
                drift = []
                for defn, rendered, _count in renders:
                    drift += [(f"hosts/{defn.name}/{rel}", status) for rel, status in compare_trees(rendered, HOSTS_DIR / defn.name)]
                if drift:
                    print(
                        f"Check failed: {len(drift)} path(s) differ between a fresh build of core/ at version "
                        f"{version} and the committed hosts/ trees; nothing was written.",
                        file=sys.stderr,
                    )
                    for path, status in drift:
                        print(f"  {path}: {status}", file=sys.stderr)
                    return 1
                verb = "matches" if len(renders) == 1 else "match"
                print(f"Check passed: {names} {verb} a fresh build of core/ at version {version}.")
                return 0

            for defn, rendered, _count in renders:
                swap_in(rendered, HOSTS_DIR / defn.name)
            counts = ", ".join(f"hosts/{defn.name}/ ({count} files)" for defn, _rendered, count in renders)
            print(f"Built {counts} from core/ at version {version}.")
            return 0
    except (BuildError, OSError) as e:
        print(f"Error: {e}\nNothing under hosts/ was written.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
