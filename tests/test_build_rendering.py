"""The host build's rendering, run in-process against a synthetic core/ and one synthetic host
definition: inline and file-backed slot values both land in the rendered tree, a file-backed
value in the build's substitution order (slots filled first, then {{PLUGIN_ROOT}}, then the
prose drop patterns, then frontmatter-key stripping), and the three refusals the loader
raises for a bad file-backed [slots] entry. The build imports tomllib and PyYAML, so the
module is skipped below Python 3.11: the floor run reports it skipped, the pinned run never
does. main's orchestration and the check set are not exercised here."""

import sys

import pytest

if sys.version_info < (3, 11):
    pytest.skip("the host build needs Python 3.11+ (tomllib)", allow_module_level=True)

import importlib.util
from pathlib import Path

BUILD_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "build_hosts.py"
VERSION = "9.8.7"
PLUGIN_ROOT = "${DEMO_ROOT}"
HOST = "demo"

SETTINGS = """\
plugin_name = "demo-plugin"
plugin_root = "${DEMO_ROOT}"
plugin_dir = ""
prose_drop_patterns = [' \\[drop me\\]']
strip_frontmatter_keys = ["color"]
renames = []
exclude = []

[layout]
shared = "shared"
skills = "skills"

[slots]
INLINE_NOTE = "inline value naming {{PLUGIN_ROOT}}/shared/guide.md"
FILE_NOTE = { file = "slots/FILE_NOTE.md" }
"""

# The value file ends in two newlines: the loader removes exactly one, so the substituted
# value keeps one. It carries {{PLUGIN_ROOT}}, replaced only after the slot fill, and the
# drop pattern's text, removed only after both.
FILE_NOTE_FILE = "File value at {{PLUGIN_ROOT}}/shared/guide.md [drop me]\n\n"

SKILL = """\
---
name: demo
description: A demo skill for the rendering test
color: blue
---
Read {{PLUGIN_ROOT}}/shared/guide.md first.
{{FILE_NOTE}}After the file value.
Inline: {{INLINE_NOTE}}
"""

GUIDE = "Guide kept under {{PLUGIN_ROOT}}.\n"
README_TEMPLATE = "# {{NAME}} {{VERSION}}\n\nInstall under ${DEMO_ROOT}.\n"
LICENSE_TEXT = "Synthetic license text.\n"


@pytest.fixture
def build():
    """The build script imported in-process under its own module name."""
    spec = importlib.util.spec_from_file_location("build_hosts", BUILD_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


@pytest.fixture
def fixture_repo(tmp_path, build, monkeypatch):
    """A synthetic core/, LICENSE, and one host definition under tmp_path, with the build's
    module-level path constants pointed at them."""
    core = tmp_path / "core"
    write(core / "skills" / "demo" / "SKILL.md", SKILL)
    write(core / "shared" / "guide.md", GUIDE)
    write(tmp_path / "LICENSE", LICENSE_TEXT)
    definitions = tmp_path / "definitions"
    definition = definitions / HOST
    write(definition / "settings.toml", SETTINGS)
    write(definition / "slots" / "FILE_NOTE.md", FILE_NOTE_FILE)
    write(definition / "README.md", README_TEMPLATE)
    monkeypatch.setattr(build, "CORE_DIR", core)
    monkeypatch.setattr(build, "LICENSE_FILE", tmp_path / "LICENSE")
    monkeypatch.setattr(build, "DEFINITIONS_DIR", definitions)
    return tmp_path


def test_render_fills_inline_and_file_backed_slots(build, fixture_repo):
    defn = build.load_definition(build.DEFINITIONS_DIR / HOST, build.core_top_level_dirs())
    assert defn.slots == {
        "INLINE_NOTE": "inline value naming {{PLUGIN_ROOT}}/shared/guide.md",
        "FILE_NOTE": "File value at {{PLUGIN_ROOT}}/shared/guide.md [drop me]\n",
    }
    assert defn.templates == ["README.md"]

    dest = fixture_repo / "rendered"
    origins = build.render_host(defn, VERSION, dest)

    expected = {
        "skills/demo/SKILL.md": (
            "---\n"
            "name: demo\n"
            "description: A demo skill for the rendering test\n"
            "---\n"
            "Read ${DEMO_ROOT}/shared/guide.md first.\n"
            "File value at ${DEMO_ROOT}/shared/guide.md\n"
            "After the file value.\n"
            "Inline: inline value naming ${DEMO_ROOT}/shared/guide.md\n"
        ),
        "shared/guide.md": "Guide kept under ${DEMO_ROOT}.\n",
        "README.md": "# demo-plugin 9.8.7\n\nInstall under ${DEMO_ROOT}.\n",
        "LICENSE": LICENSE_TEXT,
    }
    assert set(origins) == set(expected)
    assert build.walk_files(dest) == sorted(expected)
    for rel, text in expected.items():
        assert (dest / rel).read_bytes().decode("utf-8") == text, rel


def write_definition(tmp_path, slot_entry, files=()):
    """A minimal definition directory whose [slots] table holds one entry, BAD_SLOT."""
    definition = tmp_path / HOST
    write(
        definition / "settings.toml",
        "plugin_name = \"demo-plugin\"\n"
        "plugin_root = \"${DEMO_ROOT}\"\n"
        "plugin_dir = \"\"\n"
        "prose_drop_patterns = []\n"
        "strip_frontmatter_keys = []\n"
        "renames = []\n"
        "exclude = []\n"
        "\n"
        "[layout]\n"
        "\n"
        "[slots]\n"
        f"BAD_SLOT = {slot_entry}\n",
    )
    for rel, text in files:
        write(definition / rel, text)
    return definition


@pytest.mark.parametrize(
    "slot_entry, files, refusal",
    [
        ('{ file = "slots/BAD_SLOT.md" }', (), "which does not exist"),
        (
            '{ file = "slots/../settings.toml" }',
            (("slots/OTHER.md", "a value\n"),),
            "outside the definition's slots/ subdirectory",
        ),
        ("42", (), "must be a string or a one-key table"),
    ],
    ids=["missing-value-file", "dotdot-escape", "integer-entry"],
)
def test_loader_refuses_bad_file_backed_slot(build, tmp_path, slot_entry, files, refusal):
    definition = write_definition(tmp_path, slot_entry, files)
    with pytest.raises(build.BuildError) as excinfo:
        build.load_definition(definition, [])
    message = str(excinfo.value)
    assert "slots.BAD_SLOT" in message
    assert refusal in message
