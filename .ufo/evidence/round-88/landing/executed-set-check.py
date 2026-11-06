#!/usr/bin/env python3
"""Round-88 landing corroboration for the wave's T88E2 classes (NOT the frozen
predicate; the frozen counter is unchanged). Written after the wave reported three
runner variants that print the frozen predicate while carrying the real leg:
`parked` / `stub` (the runner does not execute the declared legs) and `dupbase`
(a `./`-aliased path re-declares one gate, so 11 declarations cover 10 gates).

usage: executed-set-check.py <runner-bytes-file> <runner --regression stdout file>

Checks:
  E1 executed set: the `REGRESSION_CASE <name>: PASS` names in the runner's own
     output equal the `regression_case_git` names parsed from its bytes (same
     LEG_RE as the frozen counter), each exactly once;
  E2 blob-distinct: the PIN_ values (blob sha256) of the declared legs are pairwise
     distinct, so two declarations cannot cover one gate under two path spellings.
Prints EXECUTED_SET: declared=<d> executed_pass=<e> missing=<m> extra=<x>
       distinct_pins=<p>/<d> ok|FAIL ; exit 0 only on ok.
"""
import re
import sys

LEG_RE = re.compile(
    r"^  regression_case_git (\S+) \\\n"
    r"\s+'([^']+)' \"\$(PIN_\w+)\" \"\$(REV_\w+)\" \\\n"
    r"\s+\"\$specs/([^\"]+)\.spec\" '([^']*)' \"\$(TABLE_\w+)\" \\\n"
    r"\s+\"\$root/([^\"]+)\"\n", re.M)
VAR_RE = re.compile(r"^(PIN_\w+)=([0-9a-f]+)$", re.M)

runner = open(sys.argv[1], encoding="utf-8").read()
out = open(sys.argv[2], encoding="utf-8", errors="replace").read()
pins = dict(VAR_RE.findall(runner))
legs = [(m.group(1), pins.get(m.group(3))) for m in LEG_RE.finditer(runner)]
names = [n for n, _ in legs]
passed = re.findall(r"^REGRESSION_CASE (\S+): PASS ", out, re.M)
missing = sorted(set(names) - set(passed))
extra = sorted(set(passed) - set(names))
dups = len(passed) != len(set(passed))
pinvals = [p for _, p in legs]
distinct = len(set(pinvals)) if None not in pinvals else 0
ok = not missing and not extra and not dups and len(passed) == len(names) and distinct == len(names)
print("EXECUTED_SET: declared=%d executed_pass=%d missing=%s extra=%s distinct_pins=%d/%d %s" % (
    len(names), len(passed), ",".join(missing) or "-", ",".join(extra) or "-", distinct, len(names),
    "ok" if ok else "FAIL"))
sys.exit(0 if ok else 1)
