"""Fixtures of the host suite, the on-demand pytest directory that drives the installed CLI of
one host, chosen per run, against that host's installed plugin copy.

The directory sits outside pyproject.toml's `testpaths`, so `uv run pytest` and the 3.9
floor run never reach it; it runs only when named, with the host given by the required
`--host` option: `uv run pytest host_tests --host <host>`, <host> exactly one of claude,
antigravity, or codex. Before any test, one up-front check stops the whole run with a
non-zero exit and one line when the run names no host or an unknown one, or when a
prerequisite of the named host is missing; no other host's prerequisites are checked. The
suite drives the copy already installed in the user's real HOME and writes nothing to it
(replacing that copy is the user's own act), runs every agy process at the account's default
model and effort, and lets agy's own print timeout bound each run.
"""

import os
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
# Where each host's definition and its committed built tree live, the paths the build itself
# reads from and writes to.
DEFINITIONS_DIR = REPO_ROOT / "scripts" / "hosts"
HOSTS_DIR = REPO_ROOT / "hosts"
FIXTURE_PROJECT = REPO_ROOT / "tests" / "fixtures" / "host_project"
# The fixture project's milestone container, tracked under a name the milestones tool's
# discovery pattern does not match, so this repository's own `live` never lists the fixture's
# milestone, and the name each seeded copy holds it under, where the installed skills find a
# normal root container.
FIXTURE_CONTAINER = "milestones.fixture"
SEEDED_CONTAINER = "milestones"

# The one fixed bound on a headless run, enforced by agy itself through `--print-timeout`,
# so the suite holds no wall-clock limit of its own.
PRINT_TIMEOUT = "20m"


class Host:
    """One host's entry. The values only the suite needs are given here, at construction:
    `cli`, the command the host's CLI is run by; `installed_root`, the installed copy's root
    as the suite reaches it, or None when the suite holds no fixed path for it; and
    `prerequisites`, the checks run against this host alone before any test, in order, each
    taking the entry and returning None or the reason and remedy of the one that is missing.
    The values the host's definition already declares are read from
    scripts/hosts/<name>/settings.toml with tomllib and never restated: `name`, the
    definition directory's name, which names the host as the build does; `plugin_name`;
    `plugin_dir`; `built_tree`, the committed hosts/<name>/ tree the build renders; and
    `plugin_tree`, the directory plugin_dir names inside it, the one an installed copy
    holds."""

    def __init__(self, name, *, cli, installed_root, prerequisites):
        with open(DEFINITIONS_DIR / name / "settings.toml", "rb") as settings_file:
            settings = tomllib.load(settings_file)
        self.name = name
        self.plugin_name = settings["plugin_name"]
        self.plugin_dir = settings["plugin_dir"]
        self.built_tree = HOSTS_DIR / name
        self.plugin_tree = self.built_tree / self.plugin_dir
        self.cli = cli
        self.installed_root = installed_root
        self.prerequisites = prerequisites


def _tree_files(root):
    """Every file under root, keyed by its path relative to root."""
    files = {}
    for directory, _, names in os.walk(root):
        for name in names:
            path = Path(directory) / name
            files[path.relative_to(root).as_posix()] = path
    return files


def _plugin_tree_label(host):
    """The host's plugin directory in the built tree, repo-relative with its trailing slash."""
    return f"{host.plugin_tree.relative_to(REPO_ROOT).as_posix()}/"


def _cli_on_path(host):
    if shutil.which(host.cli) is None:
        return f"{host.cli} is not resolvable on PATH"
    return None


def _copy_present(host):
    if not Path(os.path.expanduser(host.installed_root)).is_dir():
        return (
            f"no plugin copy at {host.installed_root}; "
            f"extract the release or copy the built {_plugin_tree_label(host)} tree there"
        )
    return None


def _copy_matches_built_tree(host):
    built = _tree_files(host.plugin_tree)
    installed = _tree_files(Path(os.path.expanduser(host.installed_root)))
    for relative in sorted(set(built) | set(installed)):
        if (
            relative not in built
            or relative not in installed
            or built[relative].read_bytes() != installed[relative].read_bytes()
        ):
            return (
                f"the plugin copy at {host.installed_root} differs from "
                f"{_plugin_tree_label(host)} at {relative}; "
                "re-extract the release or copy the built tree there"
            )
    return None


# One entry per host, keyed by the name `--host` takes, in the order the stop line lists them.
HOSTS = {
    "claude": Host(
        "claude",
        cli="claude",
        installed_root=None,
        prerequisites=(_cli_on_path,),
    ),
    "antigravity": Host(
        "antigravity",
        cli="agy",
        installed_root="~/.gemini/config/plugins/cairn",
        prerequisites=(_cli_on_path, _copy_present, _copy_matches_built_tree),
    ),
    "codex": Host(
        "codex",
        cli="codex",
        installed_root=None,
        prerequisites=(_cli_on_path,),
    ),
}

ACCEPTED_HOSTS = f"{', '.join(list(HOSTS)[:-1])}, or {list(HOSTS)[-1]}"


def pytest_addoption(parser):
    parser.addoption(
        "--host",
        action="append",
        nargs="?",
        metavar="HOST",
        help=f"the host whose installed CLI and plugin copy the run drives, exactly one of "
        f"{ACCEPTED_HOSTS}; required, with no default",
    )


def chosen_host(config):
    """The entry of the one host the run names with `--host`, or None when it names none, an
    unknown one, or more than one."""
    named = config.getoption("host")
    if named is None or len(named) != 1 or named[0] not in HOSTS:
        return None
    return HOSTS[named[0]]


def _stop(reason):
    sys.stderr.write(f"host suite prerequisite missing: {reason}\n")
    sys.stderr.flush()
    return 1


def pytest_cmdline_main(config):
    """Read the run's host, then stop the whole run before any test when it names none or an
    unknown one, or when one of that host's prerequisites is missing: one line naming it on
    stderr, a non-zero exit, no per-test outcome, and never a skip. Only the named host's
    prerequisites are checked, in its entry's order, the first missing one stopping the run.
    Returning the exit code from this hook ends the run before pytest configures its
    reporting, so that line is the run's only output; when the host is named and every one of
    its prerequisites holds, returning None lets pytest carry on as usual."""
    host = chosen_host(config)
    if host is None:
        return _stop(f"--host must name exactly one of {ACCEPTED_HOSTS}")
    for check in host.prerequisites:
        missing = check(host)
        if missing is not None:
            return _stop(missing)
    return None


def _git(repository, *args):
    subprocess.run(
        ["git", *args],
        cwd=str(repository),
        stdin=subprocess.DEVNULL,
        capture_output=True,
        check=True,
    )


@pytest.fixture
def seeded_repo(tmp_path):
    """A fresh committed copy of the fixture project for one agy process: seeded_repo() -> Path.
    Each call copies tests/fixtures/host_project to its own directory under tmp_path, renames
    the copy's milestones.fixture/ container to milestones/, runs `git init` there, and makes
    the initial commit, so every agy process starts from the same committed tree, holding the
    fixture's milestone at milestones/<slug>/, and nothing it changes reaches the fixture or
    another process."""

    count = 0

    def build():
        nonlocal count
        count += 1
        repository = tmp_path / f"project{count}"
        shutil.copytree(FIXTURE_PROJECT, repository)
        (repository / FIXTURE_CONTAINER).rename(repository / SEEDED_CONTAINER)
        _git(repository, "init", "-q")
        _git(repository, "config", "user.name", "Host Suite")
        _git(repository, "config", "user.email", "host-suite@example.invalid")
        _git(repository, "config", "commit.gpgsign", "false")
        _git(repository, "add", "-A")
        _git(repository, "commit", "-q", "--no-verify", "-m", "Seed the fixture project")
        return repository

    return build


@pytest.fixture
def run_agy():
    """Run one headless agy process in a seeded repository: run_agy("<prompt>", cwd=repository)
    -> CompletedProcess with decoded stdout and stderr. The line is always
    `agy -p <prompt> --dangerously-skip-permissions --print-timeout <PRINT_TIMEOUT>`, with no
    `--model` and no `--effort` (the account's defaults) and an `--output-format` only when
    one is given. It runs with the user's real HOME, so it drives the installed copy, and
    nothing here bounds it but agy's own print timeout."""

    def run(prompt, *, cwd, output_format=None):
        command = [
            "agy",
            "-p",
            prompt,
            "--dangerously-skip-permissions",
            "--print-timeout",
            PRINT_TIMEOUT,
        ]
        if output_format is not None:
            command += ["--output-format", output_format]
        return subprocess.run(
            command,
            cwd=str(cwd),
            stdin=subprocess.DEVNULL,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

    return run


@pytest.fixture
def plugin_root():
    """Antigravity's installed copy's path in the two forms a run meets it in: (tilde,
    expanded), the tilde literal of its entry's installed root, which every rendered read
    path and python3 command carries, and its expansion under the user's real HOME."""
    tilde = HOSTS["antigravity"].installed_root
    return tilde, Path(os.path.expanduser(tilde))
