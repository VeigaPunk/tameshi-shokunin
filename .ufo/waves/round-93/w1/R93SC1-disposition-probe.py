#!/usr/bin/env python3
"""R93SC1 probe: what the conjunct-disposition checker actually binds.

Imports the committed checker (tools/conjunct-disposition.py, sha256
1b1c6895ebf1d167900113030beebb071d04ed5e8bbb46988176c82b26764a9a) and calls
its `check()` on synthetic manifest/receipt pairs, to record the facts the
QUALITY draft must state rather than assume:

  A. a row whose receipt shows the conjunct FALSE is accepted (happy path);
  B. a row whose receipt shows the conjunct TRUE is a finding (`no-flip`);
  C. a receipt whose PROVENANCE fields (the `counter_sha=` / `clone_rev=`
     the battery driver writes into every receipt) are absent or wrong is
     STILL accepted -- the checker reads only the receipt's `C1_CONJUNCTS`
     line, so a manifest row is bound to the conjunct VALUE, not to the
     instrument that produced the receipt;
  D. a manifest that declares every conjunct unfalsifiable with a
     mechanism-worded reason produces findings=0 -- so the per-row checker
     ALONE cannot reject it; only the frozen COUNT predicate
     (falsifiable=17 of 19) does. That is why the count must be part of the
     predicate and not a report line.

Read-only: no lane file is written; receipts are built in a temp dir.
"""
import hashlib
import importlib.util
import os
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
CHECKER = os.path.join(LANE, "tools", "conjunct-disposition.py")
REASON = ("the canary reaches its inserted exit under the sealed gate pin, so no "
          "committed lane state can falsify this conjunct")


def load():
    spec = importlib.util.spec_from_file_location("cdisp", CHECKER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    m = load()
    print("checker_sha256=%s" % hashlib.sha256(open(CHECKER, "rb").read()).hexdigest())
    keys = ["selfpin", "green", "canary"]
    with tempfile.TemporaryDirectory() as d:
        # A: a receipt showing selfpin FALSE, with no provenance fields at all
        open(os.path.join(d, "st-a.out"), "w").write(
            "exit=1\nC1_CONJUNCTS selfpin=false green=false canary=true\n")
        # C: a receipt that CLAIMS a different counter digest and clone revision
        open(os.path.join(d, "st-c.out"), "w").write(
            "control=st-c clone_rev=deadbeefdeadbeefdeadbeefdeadbeefdeadbeef "
            "parent=deadbeef\n"
            "counter_sha=" + "0" * 64 + "\n"
            "exit=1\nC1_CONJUNCTS selfpin=false green=false canary=true\n")
        # B: a receipt showing selfpin TRUE
        open(os.path.join(d, "st-b.out"), "w").write(
            "exit=0\nC1_CONJUNCTS selfpin=true green=false canary=true\n")
        base = {"green": {"state": "st-a", "mode": "conjunct-false"},
                "canary": {"unfalsifiable": REASON}}
        allunf = {k: {"unfalsifiable": REASON} for k in keys}
        cases = [
            ("A-happy", dict(base, selfpin={"state": "st-a", "mode": "conjunct-false"}), 0),
            ("C-wrong-provenance", dict(base, selfpin={"state": "st-c",
                                                        "mode": "conjunct-false"}), 0),
            ("B-no-flip", dict(base, selfpin={"state": "st-b", "mode": "conjunct-false"}), 1),
            ("D-all-unfalsifiable", allunf, 0),
        ]
        for name, rows, want in cases:
            f = m.check(keys, rows, d)
            status = "OK" if len(f) == want else "UNEXPECTED"
            print("CASE %-22s findings=%d want=%d %s %s" % (
                name, len(f), want, status, ",".join(x[0] for x in f) if f else "-"))
            for fid, key, detail in f:
                print("     FINDING %s %s: %s" % (fid, key, detail))
        rows = {k: {"state": "st-a", "mode": "conjunct-false"} for k in keys}
        f = m.check(keys, rows, d)
        out = m.report(f, len(keys), rows)
        print("REPORT for 3 falsifiable rows (one wrong): exit=%d" % out)
        f = m.check(keys, allunf, d)
        out = m.report(f, len(keys), allunf)
        print("REPORT for 3 all-unfalsifiable rows: exit=%d "
              "(per-row checker alone ACCEPTS it)" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
