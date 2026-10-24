#!/usr/bin/env python3
"""Count the one r36 control-input mismatch until an append-only repair resolves it."""
import argparse
import json
import os
import subprocess
import sys

OLD_MUTANT = "91373d55557fe26c431e9e3dd9e8fa4a00d7b57f"
ERRATUM_MARKER = "### Round 36 control-input erratum (round 37)"
MANIFEST = ".ufo/evidence/round-37/control/empty-panel/manifest.json"
REPLAY_RECEIPT = ".ufo/evidence/round-37/control/replay-at-final.stdout"


def git_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1", PYTHONDONTWRITEBYTECODE="1")
    return env


def git(lane, *args):
    return subprocess.run(["git", "-C", lane, *args], env=git_env(), capture_output=True)


def show(lane, rev, path):
    p = git(lane, "show", "%s:%s" % (rev, path))
    return p.stdout if p.returncode == 0 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    lane = os.path.abspath(a.lane)
    resolved = git(lane, "rev-parse", "--verify", a.rev)
    if resolved.returncode:
        print("C1_R37: SETUP rev_unresolved=%s" % a.rev)
        return 2
    rev = resolved.stdout.decode().strip()
    scorecard = show(lane, rev, "SCORECARD.md")
    manifest_bytes = show(lane, rev, MANIFEST)
    replay = show(lane, rev, REPLAY_RECEIPT)
    if scorecard is None:
        print("C1_R37: SETUP scorecard_unresolved")
        return 2

    correction = ERRATUM_MARKER.encode() in scorecard
    manifest_ok = False
    if manifest_bytes is not None:
        try:
            doc = json.loads(manifest_bytes.decode("utf-8"))
            source_rev = doc["source_revision"]
            source_path = doc["source_panel_path"]
            expected_tree = doc["source_panel_tree"]
            tree = git(lane, "rev-parse", "%s:%s" % (source_rev, source_path))
            empty_paths = git(lane, "ls-tree", "-r", "--name-only", rev, "--",
                              ".ufo/evidence/round-37/control/empty-panel")
            got_paths = [p for p in empty_paths.stdout.decode().splitlines() if p]
            manifest_ok = (tree.returncode == 0 and tree.stdout.decode().strip() == expected_tree
                           and doc["source_specimen_count"] == 9
                           and doc["expected_specimen_count"] == 0
                           and got_paths == [MANIFEST])
        except (KeyError, ValueError, UnicodeDecodeError):
            manifest_ok = False

    def receipt_ok(raw, label, wanted):
        if raw is None:
            return False
        text = raw.decode("utf-8", "replace")
        return (label in text and wanted in text and "rev=" + rev in text)

    receipts_ok = (receipt_ok(replay, "C1_R35_PASS=true", "pub_kill=0/0")
                   and receipt_ok(replay, "C1_R36V2_PASS=false", "pub_kill_slots=0"))
    old_commit = git(lane, "cat-file", "-e", OLD_MUTANT + "^{commit}")
    old_unresolved_superseded = old_commit.returncode != 0 and correction and manifest_ok and receipts_ok
    mismatches = 0 if old_unresolved_superseded else 1
    print("C1_R37: unresolved_control_inputs=%d old_mutant_resolves=%d correction=%d manifest_ok=%d receipts_ok=%d rev=%s C1_R37_PASS=%s"
          % (mismatches, int(old_commit.returncode == 0), int(correction), int(manifest_ok),
             int(receipts_ok), rev, "true" if mismatches == 0 else "false"))
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
