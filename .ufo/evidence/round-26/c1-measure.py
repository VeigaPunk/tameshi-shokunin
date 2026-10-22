#!/usr/bin/env python3
"""tameshi round 26 C1 counter (frozen before any mutant run): wired recorded ledger legs.

Usage: python3 .ufo/evidence/round-26/c1-measure.py --repo CLONE_AT_REV

Reads CLONE_AT_REV/tools/mutate-and-run.sh (a lane clone checked out at the measured
revision). recorded_cases is scorecard command D (ledger comment lines). A recorded leg
counts as wired only when the runner also carries, for that leg name:
  - an embedded spec heredoc  cat >"$d/<leg>.spec"
  - a regression replay call  regression_case_git <leg>
  - a leg-check entry          '<leg>:<leg>.spec:TABLE_<X>:<n>:<k>'
  - the TABLE_<X>='...' line that entry names, with exactly <n> defects and <k> KILLED
depth_score = min(10, recorded_cases, wired_legs).

Lines: C1_LEG <leg>: WIRED|UNWIRED (<missing parts>) per recorded leg, then
C1_DEPTH: recorded_cases=N wired_legs=W depth_score=S
Exit: 0 when depth_score >= 9 (the round-26 target) · 1 below target · 2 setup · 64 usage.
"""
import re
import sys
from pathlib import Path

LEDGER_RE = re.compile(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+", re.M)
LEG_RE = re.compile(r"^#   ((?:js|bash)-\S+)\s+\S+\s+\d+/\d+", re.M)
TARGET = 9


def main(argv):
    if len(argv) != 2 or argv[0] != "--repo":
        print("usage: c1-measure.py --repo CLONE_AT_REV", file=sys.stderr)
        return 64
    runner = Path(argv[1]) / "tools" / "mutate-and-run.sh"
    try:
        text = runner.read_text(encoding="utf-8")
    except OSError as exc:
        print("C1_DEPTH: SETUP (%s)" % exc)
        return 2
    recorded = len(LEDGER_RE.findall(text))
    legs = LEG_RE.findall(text)
    if len(set(legs)) != len(legs):
        print("C1_DEPTH: SETUP (duplicate ledger leg names)")
        return 2
    wired = 0
    for leg in legs:
        missing = []
        if ('cat >"$d/%s.spec"' % leg) not in text:
            missing.append("spec-heredoc")
        if not re.search(r"^\s*regression_case_git %s \\$" % re.escape(leg), text, re.M):
            missing.append("regression-call")
        m = re.search(r"'%s:%s\.spec:(TABLE_[A-Z0-9_]+):(\d+):(\d+)'" % (re.escape(leg), re.escape(leg)), text)
        if not m:
            missing.append("leg-check-entry")
        else:
            var, n, k = m.group(1), int(m.group(2)), int(m.group(3))
            t = re.search(r"^%s='([^']*)'$" % var, text, re.M)
            if not t:
                missing.append("table-line")
            else:
                pairs = [p.split(":", 1) for p in t.group(1).split(",") if p]
                if len(pairs) != n or sum(1 for p in pairs if p[-1] == "KILLED") != k:
                    missing.append("table-counts")
        if missing:
            print("C1_LEG %s: UNWIRED (%s)" % (leg, ",".join(missing)))
        else:
            wired += 1
            print("C1_LEG %s: WIRED" % leg)
    score = min(10, recorded, wired)
    print("C1_DEPTH: recorded_cases=%d wired_legs=%d depth_score=%d" % (recorded, wired, score))
    return 0 if score >= TARGET else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
