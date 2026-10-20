#!/usr/bin/env python3
"""Measure whether registered selftests honor inherited Git environment.

Each selected registry selftest runs from a detached /tmp clone of the exact
requested revision. Its GIT_DIR, GIT_WORK_TREE, and GIT_INDEX_FILE point only
at a throwaway canary repository. The canary verdict records changes to its
HEAD, refs, index, and object database; it never uses a real repository as the
canary.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

DEFAULT_ROOT = Path(__file__).resolve().parents[3]
HEX40 = re.compile(r"^[0-9a-f]{40}$")


class CannotEvaluate(Exception):
    pass


def git_environment(extra=None):
    """Return a Git environment without inherited repository selectors."""
    env = {key: value for key, value in os.environ.items()
           if not key.startswith("GIT_")}
    env.update({
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_PAGER": "cat",
    })
    if extra:
        env.update(extra)
    return env


def git(args, *, env=None, timeout=300):
    try:
        proc = subprocess.run(
            ["git", *map(str, args)], env=env or git_environment(),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CannotEvaluate("git " + str(args[0]) + ": " + str(exc)) from exc
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", "replace").strip()
        raise CannotEvaluate(
            "git {} failed (exit {}): {}".format(args[0], proc.returncode, detail)
        )
    return proc.stdout


def resolve_revision(root, rev):
    raw = git(["-C", root, "rev-parse", "--verify", "--quiet",
               "--end-of-options", rev + "^{commit}"])
    resolved = raw.decode("ascii", "strict").strip()
    if not HEX40.fullmatch(resolved):
        raise CannotEvaluate("revision did not resolve to a full commit id: " + repr(resolved))
    return resolved


def make_fleet_clone(root, revision, scratch):
    source = root.resolve()
    fleet = scratch / "fleet"
    fleet.mkdir()
    try:
        siblings = sorted(source.parent.iterdir(), key=lambda path: path.name)
    except OSError as exc:
        raise CannotEvaluate("cannot enumerate fleet siblings: " + str(exc)) from exc
    for sibling in siblings:
        if not sibling.name.endswith("-shokunin"):
            continue
        if sibling.resolve() == source:
            continue
        link = fleet / sibling.name
        if not link.exists() and not link.is_symlink():
            link.symlink_to(sibling, target_is_directory=True)
    clone = fleet / source.name
    git(["clone", "-q", "--no-hardlinks", "-c", "core.hooksPath=/dev/null",
         source, clone])
    git(["-C", clone, "checkout", "-q", "--detach", revision])
    observed = git(["-C", clone, "rev-parse", "HEAD"]).decode("ascii").strip()
    if observed != revision:
        raise CannotEvaluate("clone HEAD mismatch: expected {}, got {}".format(
            revision, observed))
    return clone


def initialize_canary(path):
    path.mkdir()
    (path / "seed.txt").write_text("round-18 git-env-canary\n", encoding="utf-8")
    env = git_environment({
        "GIT_AUTHOR_NAME": "Tameshi round-18 canary",
        "GIT_AUTHOR_EMAIL": "canary@example.invalid",
        "GIT_COMMITTER_NAME": "Tameshi round-18 canary",
        "GIT_COMMITTER_EMAIL": "canary@example.invalid",
    })
    git(["init", "-q", path], env=env)
    git(["-C", path, "add", "seed.txt"], env=env)
    git(["-C", path, "commit", "-q", "-m", "canary baseline"], env=env)


def file_fingerprint(path):
    try:
        info = path.lstat()
    except FileNotFoundError:
        return None
    if path.is_symlink():
        return ("symlink", info.st_mode, os.readlink(path))
    if path.is_dir():
        return ("directory", info.st_mode)
    if not path.is_file():
        return ("other", info.st_mode, info.st_size)
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return ("file", info.st_mode, info.st_size, digest.hexdigest())


def tree_fingerprint(root):
    """Map every relative path and file identity below root to its fingerprint."""
    if not root.exists():
        return None
    result = {".": file_fingerprint(root)}
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        kept_dirs = []
        for name in sorted(dirs):
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            result[rel] = file_fingerprint(path)
            if not path.is_symlink():
                kept_dirs.append(name)
        dirs[:] = kept_dirs
        for name in sorted(files):
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            result[rel] = file_fingerprint(path)
    return result


def component_snapshot(git_dir):
    return {
        "head": file_fingerprint(git_dir / "HEAD"),
        "refs": (tree_fingerprint(git_dir / "refs"),
                 file_fingerprint(git_dir / "packed-refs")),
        "index": (file_fingerprint(git_dir / "index"),
                  file_fingerprint(git_dir / "index.lock")),
        "objects": tree_fingerprint(git_dir / "objects"),
    }


def changed_components(before, after):
    return [name for name in ("head", "refs", "index", "objects")
            if before[name] != after[name]]


def selected_rows(registry_path):
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CannotEvaluate("cannot read registry {}: {}".format(registry_path, exc)) from exc
    if not isinstance(registry, dict) or not isinstance(registry.get("rows"), list):
        raise CannotEvaluate("registry must contain a rows list")
    selected = []
    for number, row in enumerate(registry["rows"]):
        if not isinstance(row, dict):
            raise CannotEvaluate("registry row {} is not an object".format(number))
        argv = row.get("argv")
        if not isinstance(argv, list) or not all(isinstance(arg, str) for arg in argv):
            raise CannotEvaluate("registry row {} has invalid argv".format(number))
        if (row.get("kind") == "selftest" or "--selftest" in argv
                or (argv and argv[-1] == "selftest")):
            if not row.get("name") or not argv:
                raise CannotEvaluate("registry row {} lacks name or argv".format(number))
            timeout = row.get("timeout_s")
            if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or timeout <= 0:
                raise CannotEvaluate("registry row {} has invalid timeout_s".format(number))
            selected.append(row)
    if not selected:
        raise CannotEvaluate("registry has no selftest rows")
    return selected


def tool_label(argv):
    for arg in argv[1:]:
        if "/" in arg or arg.endswith((".py", ".sh")):
            return arg
    return argv[0]


def kill_process_group(proc):
    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        proc.communicate(timeout=3)
    except subprocess.TimeoutExpired:
        pass
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def run_row(row, clone, canary):
    git_dir = canary / ".git"
    env = {key: value for key, value in os.environ.items()
           if not key.startswith("GIT_")}
    env.update({
        "GIT_DIR": str(git_dir),
        "GIT_WORK_TREE": str(canary),
        "GIT_INDEX_FILE": str(git_dir / "index"),
        "PYTHONDONTWRITEBYTECODE": "1",
    })
    before = component_snapshot(git_dir)
    started = time.monotonic()
    try:
        proc = subprocess.Popen(
            row["argv"], cwd=clone, env=env, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True,
        )
    except OSError as exc:
        raise CannotEvaluate("cannot start {}: {}".format(row["name"], exc)) from exc
    timed_out = False
    try:
        stdout, stderr = proc.communicate(timeout=float(row["timeout_s"]))
        exit_value = str(proc.returncode)
    except subprocess.TimeoutExpired:
        timed_out = True
        kill_process_group(proc)
        stdout, stderr = proc.communicate()
        exit_value = "timeout"
    after = component_snapshot(git_dir)
    return {
        "name": row["name"],
        "tool": tool_label(row["argv"]),
        "argv": row["argv"],
        "exit": exit_value,
        "timed_out": timed_out,
        "changed": changed_components(before, after),
        "elapsed_s": round(time.monotonic() - started, 3),
        "stdout_bytes": len(stdout or b""),
        "stderr_bytes": len(stderr or b""),
    }


def execute(root, requested_rev):
    if not root.is_dir():
        raise CannotEvaluate("lane root does not exist: " + str(root))
    resolved = resolve_revision(root, requested_rev)
    scratch = Path(tempfile.mkdtemp(prefix="tameshi-r18w1-X09GitEnvCanary-", dir="/tmp"))
    try:
        clone = make_fleet_clone(root, resolved, scratch)
        rows = selected_rows(clone / "tools" / "registry.json")
        results = []
        canary_root = scratch / "canaries"
        canary_root.mkdir()
        for index, row in enumerate(rows):
            canary = canary_root / "row-{:02d}".format(index + 1)
            initialize_canary(canary)
            results.append(run_row(row, clone, canary))
        return resolved, results
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT,
                        help="lane Git worktree (default: this tool's lane)")
    parser.add_argument("--rev", required=True,
                        help="commit to clone and measure")
    args = parser.parse_args(argv)
    try:
        revision, results = execute(args.root.resolve(), args.rev)
    except (CannotEvaluate, UnicodeError, OSError) as exc:
        print("GIT_ENV_CANARY: CANNOT-EVALUATE ({})".format(exc), file=sys.stderr)
        return 2

    print("REV {}".format(revision))
    print("SELFTEST_ROWS {}".format(len(results)))
    by_tool = {}
    any_timeout = False
    for result in results:
        facets = ",".join(result["changed"]) or "none"
        print("ROW {} tool={} command={} exit={} canary={} facets={} elapsed_s={}".format(
            result["name"], result["tool"], json.dumps(result["argv"]),
            result["exit"], "touched" if result["changed"] else "clean",
            facets, result["elapsed_s"],
        ))
        state = by_tool.setdefault(result["tool"], {"touched": False, "rows": []})
        state["touched"] = state["touched"] or bool(result["changed"])
        state["rows"].append(result["name"])
        any_timeout = any_timeout or result["timed_out"]
    for tool, state in by_tool.items():
        print("CANARY {} {}".format(tool, "touched" if state["touched"] else "clean"))
    touched = [tool for tool, state in by_tool.items() if state["touched"]]
    print("TOUCHED_TOOLS {}".format(",".join(touched) if touched else "none"))
    return 2 if any_timeout else 0


if __name__ == "__main__":
    raise SystemExit(main())
