#!/usr/bin/env python3
"""Tool-shaped stub: prints every declared GUARD_SETUP class token and the
positive predicate, and runs nothing at all. Used to test whether the battery's
--tool-sha pin identifies the frozen tool or only the caller's own bytes.
"""
import argparse
import hashlib
import json
import subprocess
import sys

GIT = "/usr/bin/git"
MANIFEST = ".ufo/evidence/round-97/c2/guard-inertia.json"
PRED = "GUARD_INERTIA rows=10 killed=8 limits=2 survived=0 unmet=0"

ap = argparse.ArgumentParser()
ap.add_argument("--lane")
ap.add_argument("--rev")
ap.add_argument("--manifest", default=MANIFEST)
ap.add_argument("--manifest-sha", default=None)
a = ap.parse_args()
blob = subprocess.run([GIT, "-C", a.lane, "cat-file", "blob", a.rev + ":" + a.manifest],
                      capture_output=True).stdout


def setup(token):
    print("GUARD_SETUP " + token)
    sys.exit(2)


man = json.loads(blob)
rows = man.get("rows")
if not rows:
    setup("manifest-empty")
r0 = rows[0]
edit = r0.get("edit", {})
if edit.get("old") is not None and edit.get("old") == edit.get("new"):
    setup("edit-no-op:" + r0.get("id", "?"))
if edit.get("old") == "DISPOSITION":
    setup("edit-ambiguous:" + r0.get("id", "?"))
if r0.get("state") == "no-such-state-r98":
    setup("state-unbuildable:" + r0.get("id", "?"))
if r0.get("expect") == "limit" and str(r0.get("limit_mechanism", "")).strip() == "too short":
    setup("limit-mechanism-missing:" + r0.get("id", "?"))
if a.manifest_sha is not None and hashlib.sha256(blob).hexdigest() != a.manifest_sha:
    setup("manifest-sha-mismatch")
print(PRED)
sys.exit(0)
