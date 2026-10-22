#!/usr/bin/env python3
"""tameshi round 26 C2 counter (frozen before any edit it measures): record-vs-repo mismatches.

Usage: python3 .ufo/evidence/round-26/c2-measure.py --repo CLONE_AT_REV

Population: the three lane-record defects routed by the round-25 outside spot-check
(corpus/lessons/round-25-verifier-spotcheck.md:189-199, routed items 1-3). Each label is a
mismatch between what the lane's own record says and the repo bytes at the revision:

  R25-SPOT-1  tools/mte-interop.py returns verdicts but has no registry row. Resolved only when
              tools/registry.json holds an active row whose argv names tools/mte-interop.py AND
              SKILL.md holds a table row starting "| `tools/mte-interop.py` |".
  R25-SPOT-2  the round-25 SCORECARD record and the round-25 lesson omit amendment 3. Resolved
              only when SCORECARD.md, after the line "### Round 25 — measured results
              (TameshiR25)", and corpus/lessons/round-25.md, after its "## Claims" heading, each
              contain "amendment 3" (case-insensitive) and "77302fa", and the SCORECARD text
              also names "before_any_after_measurement".
  R25-SPOT-3  corpus/knowledge/mte-report-interop.md verified-at names a tool run that is not
              the tool at the revision. Resolved only when the verified-at line names
              "tool sha256 <hex>" with <hex> (8-64 hex) a prefix of sha256(tools/mte-interop.py),
              names "selftest N/N", and names a backticked .stdout receipt that exists at the
              revision and contains "MTE_SELFTEST: N/N pass" with the same N.

Lines: C2_ITEM <label>: RESOLVED|MISMATCH (<reason>) then C2_RECORD: mismatches=M/3
Exit: 0 when M == 0 · 1 otherwise · 2 setup · 64 usage.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

SC_HEAD = "### Round 25 — measured results (TameshiR25)"


def item1(repo):
    reg = json.loads((repo / "tools/registry.json").read_text(encoding="utf-8"))
    rows = [r for r in reg.get("rows", []) if r.get("status") == "active"
            and any("tools/mte-interop.py" in str(a) for a in r.get("argv", []))]
    skill = (repo / "SKILL.md").read_text(encoding="utf-8")
    table = re.search(r"^\| `tools/mte-interop\.py` \|", skill, re.M)
    why = []
    if not rows:
        why.append("no active registry.json row runs tools/mte-interop.py")
    if not table:
        why.append("no SKILL.md table row for tools/mte-interop.py")
    return why


def item2(repo):
    why = []
    sc = (repo / "SCORECARD.md").read_text(encoding="utf-8")
    at = sc.find(SC_HEAD)
    if at < 0:
        return ["SCORECARD round-25 measured-results heading missing"]
    tail = sc[at + len(SC_HEAD):]
    for need in ("amendment 3", "77302fa", "before_any_after_measurement"):
        if need.lower() not in tail.lower():
            why.append("SCORECARD after round-25 results lacks %r" % need)
    les = (repo / "corpus/lessons/round-25.md").read_text(encoding="utf-8")
    c = les.find("\n## Claims")
    if c < 0:
        why.append("lesson ## Claims heading missing")
    else:
        lt = les[c:]
        for need in ("amendment 3", "77302fa"):
            if need.lower() not in lt.lower():
                why.append("lesson after ## Claims lacks %r" % need)
    return why


def item3(repo):
    kn = (repo / "corpus/knowledge/mte-report-interop.md").read_text(encoding="utf-8")
    lines = [l for l in kn.splitlines() if l.startswith("verified-at:")]
    if len(lines) != 1:
        return ["expected one verified-at line, found %d" % len(lines)]
    line = lines[0]
    tool = hashlib.sha256((repo / "tools/mte-interop.py").read_bytes()).hexdigest()
    why = []
    m = re.search(r"tool sha256 ([0-9a-f]{8,64})", line)
    if not m or not tool.startswith(m.group(1)):
        why.append("verified-at tool sha256 is not a prefix of sha256(tools/mte-interop.py)=%s" % tool[:12])
    n = re.search(r"selftest (\d+)/(\d+)", line)
    if not n or n.group(1) != n.group(2):
        why.append("verified-at names no selftest N/N")
    receipts = [p for p in re.findall(r"`([^`]+\.stdout)`", line)]
    hit = False
    for p in receipts:
        f = repo / p
        if n and f.is_file() and ("MTE_SELFTEST: %s/%s pass" % (n.group(1), n.group(1))) in f.read_text(encoding="utf-8", errors="replace"):
            hit = True
    if not hit:
        why.append("no named .stdout receipt at the revision carries the verified-at selftest count")
    return why


def main(argv):
    if len(argv) != 2 or argv[0] != "--repo":
        print("usage: c2-measure.py --repo CLONE_AT_REV", file=sys.stderr)
        return 64
    repo = Path(argv[1])
    mism = 0
    for label, fn in (("R25-SPOT-1", item1), ("R25-SPOT-2", item2), ("R25-SPOT-3", item3)):
        try:
            why = fn(repo)
        except (OSError, ValueError) as exc:
            print("C2_RECORD: SETUP (%s: %s)" % (label, exc))
            return 2
        if why:
            mism += 1
            print("C2_ITEM %s: MISMATCH (%s)" % (label, "; ".join(why)))
        else:
            print("C2_ITEM %s: RESOLVED" % label)
    print("C2_RECORD: mismatches=%d/3" % mism)
    return 0 if mism == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
