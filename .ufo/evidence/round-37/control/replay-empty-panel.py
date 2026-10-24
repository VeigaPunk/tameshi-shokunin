#!/usr/bin/env python3
"""Replay the frozen r35/r36 predicates against the committed r37 empty-panel tree.

Only the public-panel path is redirected. The frozen counter source, runner, tool,
sealed files, scoring code, and revision all come from committed Git objects at REV.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile

SOURCE_PANEL = ".ufo/evidence/round-35/c1/panel"
EMPTY_PANEL = ".ufo/evidence/round-37/control/empty-panel"
COUNTERS = {
    "v1": ".ufo/evidence/round-35/c1/c1-measure.py",
    "v2": ".ufo/evidence/round-36/c1/c1-measure-v2.py",
}


def git_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1", PYTHONDONTWRITEBYTECODE="1")
    return env


def git(lane, *args):
    return subprocess.run(["git", "-C", lane, *args], env=git_env(), capture_output=True)


def manifest_at(lane, rev):
    p = git(lane, "show", "%s:%s/manifest.json" % (rev, EMPTY_PANEL))
    if p.returncode:
        raise RuntimeError("empty-panel manifest missing at rev")
    return json.loads(p.stdout.decode("utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--panel-rev")
    ap.add_argument("--work-root", required=True)
    ap.add_argument("--sealed", default=".ufo/evidence/round-35/c1/sealed")
    a = ap.parse_args()
    lane = os.path.abspath(a.lane)
    rev_result = git(lane, "rev-parse", "--verify", a.rev)
    if rev_result.returncode:
        print("EMPTY_PANEL_REPLAY: SETUP rev_unresolved=%s" % a.rev)
        return 2
    rev = rev_result.stdout.decode().strip()
    panel_rev_result = git(lane, "rev-parse", "--verify", a.panel_rev or rev)
    if panel_rev_result.returncode:
        print("EMPTY_PANEL_REPLAY: SETUP panel_rev_unresolved=%s" % (a.panel_rev or rev))
        return 2
    panel_rev = panel_rev_result.stdout.decode().strip()
    try:
        manifest = manifest_at(lane, panel_rev)
    except (RuntimeError, ValueError, UnicodeDecodeError) as exc:
        print("EMPTY_PANEL_REPLAY: SETUP manifest_error=%s" % type(exc).__name__)
        return 2

    source_rev = manifest.get("source_revision", "")
    source_path = manifest.get("source_panel_path", "")
    source_tree = git(lane, "rev-parse", "%s:%s" % (source_rev, source_path))
    if (source_tree.returncode or source_tree.stdout.decode().strip() != manifest.get("source_panel_tree")
            or manifest.get("source_specimen_count") != 9 or manifest.get("expected_specimen_count") != 0):
        print("EMPTY_PANEL_REPLAY: SETUP source_tree_mismatch")
        return 2
    source_names_result = git(lane, "ls-tree", "-r", "--name-only", source_rev, "--", source_path)
    if source_names_result.returncode:
        print("EMPTY_PANEL_REPLAY: SETUP source_tree_unreadable")
        return 2
    source_names = [n.rsplit("/", 1)[-1] for n in source_names_result.stdout.decode().splitlines() if n]
    expected_names = manifest.get("source_specimens")
    if sorted(source_names) != sorted(expected_names) or len(source_names) != 9:
        print("EMPTY_PANEL_REPLAY: SETUP source_specimen_set_mismatch")
        return 2
    empty_paths_result = git(lane, "ls-tree", "-r", "--name-only", panel_rev, "--", EMPTY_PANEL)
    empty_paths = [n for n in empty_paths_result.stdout.decode().splitlines() if n]
    if empty_paths != [EMPTY_PANEL + "/manifest.json"]:
        print("EMPTY_PANEL_REPLAY: SETUP mutant_tree_not_empty paths=%d" % len(empty_paths))
        return 2

    work_root = os.path.abspath(a.work_root)
    os.makedirs(work_root, exist_ok=True)
    env = git_env()
    os.environ.clear()
    os.environ.update(env)
    results = {}
    for kind, counter_path in COUNTERS.items():
        raw = git(lane, "show", "%s:%s" % (rev, counter_path))
        if raw.returncode:
            print("EMPTY_PANEL_REPLAY: SETUP counter_missing=%s" % kind)
            return 2
        namespace = {"__name__": "tameshi_r37_frozen_" + kind, "__file__": counter_path}
        try:
            exec(compile(raw.stdout, counter_path + "@" + rev, "exec"), namespace)
        except Exception as exc:
            print("EMPTY_PANEL_REPLAY: SETUP counter_load_error=%s" % type(exc).__name__)
            return 2
        original_loader = namespace.get("load_copies_rev")
        if not callable(original_loader):
            print("EMPTY_PANEL_REPLAY: SETUP counter_loader_missing=%s" % kind)
            return 2

        def committed_panel_loader(lane_arg, rev_arg, reldir, original=original_loader):
            if reldir == SOURCE_PANEL:
                return original(lane_arg, panel_rev, EMPTY_PANEL)
            return original(lane_arg, rev_arg, reldir)

        namespace["load_copies_rev"] = committed_panel_loader
        work = os.path.join(work_root, "work-" + kind)
        os.makedirs(work, exist_ok=True)
        if os.listdir(work):
            print("EMPTY_PANEL_REPLAY: SETUP work_not_empty=%s" % kind)
            return 2
        sys.argv = [counter_path, "--lane", lane, "--rev", rev, "--work", work,
                    "--sealed", a.sealed]
        from io import StringIO
        import contextlib
        stdout = StringIO()
        stderr = StringIO()
        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                rc = namespace["main"]()
        except SystemExit as exc:
            rc = int(exc.code or 0)
        output = stdout.getvalue()
        results[kind] = (rc, output, hashlib.sha256(raw.stdout).hexdigest())
        print("COUNTER_SOURCE %s sha256=%s" % (kind, results[kind][2]))
        for line in output.splitlines():
            print(line)

    v1_ok = (results["v1"][0] == 0 and "C1_R35_PASS=true" in results["v1"][1]
             and "tool_sha_ok=1" in results["v1"][1] and "pub_kill=0/0" in results["v1"][1]
             and "pub_accept=0/0" in results["v1"][1])
    v2_ok = (results["v2"][0] == 1 and "C1_R36V2_PASS=false" in results["v2"][1]
             and "tool_sha_ok=1" in results["v2"][1] and "pub_kill=0/0" in results["v2"][1]
             and "pub_accept=0/0" in results["v2"][1] and "pub_slots=0" in results["v2"][1]
             and "pub_distinct=0" in results["v2"][1])
    ok = v1_ok and v2_ok
    print("EMPTY_PANEL_REPLAY: source_tree=%s source_specimens=9 empty_specimens=0 counter_rev=%s panel_rev=%s v1_pass=%d v2_reject=%d EMPTY_PANEL_REPLAY_PASS=%s"
          % (manifest["source_panel_tree"], rev, panel_rev, int(v1_ok), int(v2_ok), "true" if ok else "false"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
