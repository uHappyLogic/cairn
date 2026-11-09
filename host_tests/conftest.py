"""Fixtures of the host suite, the on-demand pytest directory that drives the installed CLI of
one host, chosen per run, against that host's installed plugin copy.

The directory sits outside pyproject.toml's `testpaths`, so `uv run pytest` and the 3.9
floor run never reach it; it runs only when named, with the host given by the required
`--host` option: `uv run pytest host_tests --host <host>`, <host> exactly one of claude,
antigravity, or codex. Before any test, one up-front check stops the whole run with a
non-zero exit and one line when the run names no host or an unknown one, or when a
prerequisite of the named host is missing: its CLI on PATH, the installed copy that CLI
reports (Antigravity's at its fixed global path), and that copy equal, file for file, to the
host's plugin directory in the built tree. No other host's prerequisites are checked. The
suite drives the copy already installed in the user's real HOME and writes nothing to any
installation (bringing a copy up to date is the user's own act, by the host's documented
install, which the stop line names), runs every headless process at the account's default
model and effort, and bounds each by one wall-clock limit of its own, the same on every host:
a run that exceeds it is killed with its whole process group and fails its test.
"""

import json
import os
import shutil
import signal
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

# The suite's one wall-clock bound on a headless run, in seconds: 20 minutes, one value for
# every host, passed by the run fixture to the subprocess it starts. No host's own time limit
# is passed on its command line, so this is the only bound on every host.
RUN_TIMEOUT = 20 * 60

# The id Claude Code's and Codex's plugin listings give the plugin installed from its own
# marketplace, both named cairn.
PLUGIN_ID = "cairn@cairn"
# Antigravity's install location, the one fixed in the repository: the global path its
# plugin root renders as, which the host loads the plugin from in every project.
ANTIGRAVITY_ROOT = "~/.gemini/config/plugins/cairn"


class CopyNotLocated(Exception):
    """The host's CLI reported no installed copy; the one argument says why."""


class Host:
    """One host's entry. The values only the suite needs are given here, at construction:
    `cli`, the command the host's CLI is run by; `locate_copy`, taking the entry and returning
    where the installed copy the host loads stands, as the host's CLI reports it (Antigravity's
    at its fixed global path), or raising CopyNotLocated; and `remedy`, taking the entry and
    returning how the user brings that copy up to date by the host's documented install, the
    text the entry then holds as `remedy` and every one of the host's stop lines carries; and
    `headless`, taking the entry and a prompt and returning the command line of one headless
    run of the host's CLI with that prompt, in the machine-readable output mode whose records
    the tests read, or None while the entry gives no such command, which fails any test that
    starts a run. `installed_root` is None until the prerequisite check has located the copy,
    and then that copy's root as the suite reaches it. The values the host's definition
    already declares are read from scripts/hosts/<name>/settings.toml with tomllib and never
    restated: `name`, the definition directory's name, which names the host as the build
    does; `plugin_name`; `plugin_dir`; `built_tree`, the committed hosts/<name>/ tree the
    build renders; and `plugin_tree`, the directory plugin_dir names inside it, the one an
    installed copy holds."""

    def __init__(self, name, *, cli, locate_copy, remedy, headless=None):
        with open(DEFINITIONS_DIR / name / "settings.toml", "rb") as settings_file:
            settings = tomllib.load(settings_file)
        self.name = name
        self.plugin_name = settings["plugin_name"]
        self.plugin_dir = settings["plugin_dir"]
        self.built_tree = HOSTS_DIR / name
        self.plugin_tree = self.built_tree / self.plugin_dir
        self.cli = cli
        self.locate_copy = locate_copy
        self.remedy = remedy(self)
        self.headless = headless
        self.installed_root = None


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


def _plugin_listing(host):
    """What `<cli> plugin list --json` prints, parsed: the listing Claude Code and Codex both
    give in JSON, never read from their text tables."""
    command = [host.cli, "plugin", "list", "--json"]
    shown = " ".join(command)
    completed = subprocess.run(
        command,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode != 0:
        detail = " ".join(completed.stderr.split()) or f"exit code {completed.returncode}"
        raise CopyNotLocated(f"`{shown}` failed: {detail}")
    try:
        return json.loads(completed.stdout)
    except ValueError:
        raise CopyNotLocated(f"`{shown}` printed no JSON listing") from None


def _claude_copy(host):
    """The copy Claude Code loads in a repository outside any recorded project: the
    cairn@cairn entry of its listing that records no projectPath, since the project and local
    scopes each record the project they apply to, read from its readFromFolder when that is
    set (a directory-marketplace install) and otherwise from its installPath."""
    listing = _plugin_listing(host)
    for entry in listing if isinstance(listing, list) else []:
        if not isinstance(entry, dict):
            continue
        if entry.get("id") == PLUGIN_ID and "projectPath" not in entry:
            root = entry.get("readFromFolder") or entry.get("installPath")
            if root:
                return root
    raise CopyNotLocated(
        f"`{host.cli} plugin list --json` reports no {PLUGIN_ID} install "
        "at a scope outside any project"
    )


def _codex_copy(host):
    """The copy Codex loads: the cache directory of the cairn@cairn version its listing reports
    installed, ~/.codex/plugins/cache/cairn/cairn/<version>."""
    listing = _plugin_listing(host)
    installed = listing.get("installed") if isinstance(listing, dict) else None
    for entry in installed if isinstance(installed, list) else []:
        if not isinstance(entry, dict):
            continue
        if entry.get("pluginId") == PLUGIN_ID and entry.get("installed", True):
            version = entry.get("version")
            if version:
                return f"~/.codex/plugins/cache/cairn/cairn/{version}"
    raise CopyNotLocated(f"`{host.cli} plugin list --json` reports no {PLUGIN_ID} installed")


def _antigravity_copy(host):
    """The copy Antigravity loads, at the fixed global path its CLI lists the plugin under."""
    return ANTIGRAVITY_ROOT


def _cli_on_path(host):
    if shutil.which(host.cli) is None:
        return f"{host.cli} is not resolvable on PATH; put {host.cli} on PATH and {host.remedy}"
    return None


def _copy_located(host):
    try:
        host.installed_root = host.locate_copy(host)
    except CopyNotLocated as reason:
        return f"{reason}; {host.remedy}"
    return None


def _copy_present(host):
    if not Path(os.path.expanduser(host.installed_root)).is_dir():
        return f"no plugin copy at {host.installed_root}; {host.remedy}"
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
                f"{_plugin_tree_label(host)} at {relative}; {host.remedy}"
            )
    return None


# The checks run against the chosen host alone before any test, in order, each taking its
# entry and returning None or the one line's reason and remedy, the first missing one
# stopping the run: the CLI found on PATH, the CLI asked where the installed copy is, that
# copy present, and that copy equal to the host's plugin directory in the built tree file for
# file, a missing or extra file included. The comparison is made even when the copy the host
# loads is the built tree itself, as on a directory-marketplace install of this checkout.
PREREQUISITES = (_cli_on_path, _copy_located, _copy_present, _copy_matches_built_tree)

# One entry per host, keyed by the name `--host` takes, in the order the stop line lists them.
HOSTS = {
    "claude": Host(
        "claude",
        cli="claude",
        locate_copy=_claude_copy,
        remedy=lambda host: (
            "refresh the directory-marketplace install by running "
            f"`claude plugin marketplace add {REPO_ROOT}` and "
            f"`claude plugin install {PLUGIN_ID}`"
        ),
    ),
    "antigravity": Host(
        "antigravity",
        cli="agy",
        locate_copy=_antigravity_copy,
        remedy=lambda host: (
            f"copy the built {_plugin_tree_label(host)} tree, or extract the release, "
            f"into {ANTIGRAVITY_ROOT}"
        ),
        headless=lambda host, prompt: [
            host.cli,
            "-p",
            prompt,
            "--dangerously-skip-permissions",
            "--output-format",
            "stream-json",
        ],
    ),
    "codex": Host(
        "codex",
        cli="codex",
        locate_copy=_codex_copy,
        remedy=lambda host: (
            f"re-run `codex plugin marketplace add {host.built_tree}` and "
            f"`codex plugin add {PLUGIN_ID}`"
        ),
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
    prerequisites are checked, in PREREQUISITES' order, the first missing one stopping the run.
    Returning the exit code from this hook ends the run before pytest configures its
    reporting, so that line is the run's only output; when the host is named and every one of
    its prerequisites holds, returning None lets pytest carry on as usual."""
    host = chosen_host(config)
    if host is None:
        return _stop(f"--host must name exactly one of {ACCEPTED_HOSTS}")
    for check in PREREQUISITES:
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
    """A fresh committed copy of the fixture project for one headless process: seeded_repo() ->
    Path. Each call copies tests/fixtures/host_project to its own directory under tmp_path,
    renames the copy's milestones.fixture/ container to milestones/, runs `git init` there, and
    makes the initial commit, so every headless process starts from the same committed tree,
    holding the fixture's milestone at milestones/<slug>/, and nothing it changes reaches the
    fixture or another process."""

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


def _kill_group(process):
    """Kill every process of the run's group, the CLI and whatever it started, and reap the
    CLI; a group already gone is nothing to kill."""
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait()


def run_bounded(command, *, cwd, limit):
    """Run one command to its end within `limit` seconds -> CompletedProcess with decoded
    stdout and stderr. The command starts in a session of its own, so it leads a process group
    of its own that everything it starts joins. A run still going at the limit has that whole
    group killed and fails the calling test, and so does a run the test is interrupted during,
    which is killed the same way before the interruption goes on, so no run outlives the
    test that started it."""
    process = subprocess.Popen(
        command,
        cwd=str(cwd),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
        start_new_session=True,
    )
    try:
        stdout, stderr = process.communicate(timeout=limit)
    except subprocess.TimeoutExpired:
        _kill_group(process)
        _, stderr = process.communicate()
        overran = True
    except BaseException:
        _kill_group(process)
        raise
    else:
        overran = False
    if overran:
        pytest.fail(
            f"`{command[0]}` ran past the suite's run limit of {limit} seconds and was killed "
            f"with its whole process group; its stderr until then:\n{stderr}",
            pytrace=False,
        )
    return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)


@pytest.fixture
def run_host(request):
    """Run one headless process of the chosen host's CLI in a seeded repository:
    run_host("<prompt>", cwd=repository) -> CompletedProcess with decoded stdout and stderr.
    The command line is the one the chosen host's entry composes for the prompt, with no model
    or effort flag (the account's defaults), and the run is bounded by RUN_TIMEOUT, the one
    limit for every host, which no flag of the host's own adds to. It runs with the user's
    real HOME, so it drives the installed copy. A run past the limit is killed with its whole
    process group and fails its test, and an entry giving no headless command fails the test
    before any process starts."""
    host = chosen_host(request.config)

    def run(prompt, *, cwd):
        if host.headless is None:
            pytest.fail(f"the {host.name} entry gives no headless command", pytrace=False)
        return run_bounded(host.headless(host, prompt), cwd=cwd, limit=RUN_TIMEOUT)

    return run


@pytest.fixture
def plugin_root():
    """Antigravity's installed copy's path in the two forms a run meets it in: (tilde,
    expanded), the tilde literal of its fixed global path, which every rendered read path and
    python3 command carries, and its expansion under the user's real HOME."""
    return ANTIGRAVITY_ROOT, Path(os.path.expanduser(ANTIGRAVITY_ROOT))
