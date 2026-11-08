#!/usr/bin/env python3
"""R95R2 independent provenance probe.

For every manifest row that names a state, print the state, the receipt path,
whether the receipt blob exists at --rev, the first `counter_sha=` line it
carries (or `<absent>`), and whether it equals sha256 of the counter blob at
--rev.  Reads only the object store; never executes the counter; never imports
the checker.
Usage: provenance.py --lane L --rev R --manifest PATH --receipts DIR --counter PATH
"""
import argparse, hashlib, json, subprocess, sys

def git(lane, *a):
    return subprocess.run(["git", "-C", lane, *a], capture_output=True)

def blob(lane, rev, path):
    p = git(lane, "cat-file", "blob", rev + ":" + path)
    return p.stdout if p.returncode == 0 else None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True); ap.add_argument("--rev", required=True)
    ap.add_argument("--manifest", required=True); ap.add_argument("--receipts", required=True)
    ap.add_argument("--counter", required=True)
    a = ap.parse_args()
    cb = blob(a.lane, a.rev, a.counter)
    if cb is None:
        print("PROVENANCE counter-absent-at-rev %s" % a.counter); return 2
    want = hashlib.sha256(cb).hexdigest()
    mb = blob(a.lane, a.rev, a.manifest)
    if mb is None:
        print("PROVENANCE manifest-absent-at-rev %s" % a.manifest); return 2
    rows = json.loads(mb)["rows"]
    n = ok = absent = noc = bad = 0
    print("PROVENANCE counter=%s sha256=%s" % (a.counter, want))
    for key in sorted(rows):
        row = rows[key]
        if not isinstance(row, dict) or "state" not in row:
            continue
        n += 1
        st = row["state"]
        rp = a.receipts + "/" + st + ".out"
        rb = blob(a.lane, a.rev, rp)
        if rb is None:
            absent += 1
            print("ROW %-14s state=%-16s receipt=%s EXISTS=no counter_sha=<absent>" % (key, st, rp))
            continue
        line = None
        for ln in rb.decode("utf-8", "replace").split("\n"):
            if ln.startswith("counter_sha="):
                line = ln.strip(); break
        if line is None:
            noc += 1
            print("ROW %-14s state=%-16s receipt=%s EXISTS=yes counter_sha=<absent> want=%s match=no" % (key, st, rp, want))
        elif line == "counter_sha=" + want:
            ok += 1
            print("ROW %-14s state=%-16s receipt=%s EXISTS=yes %s match=yes" % (key, st, rp, line))
        else:
            bad += 1
            print("ROW %-14s state=%-16s receipt=%s EXISTS=yes %s want=%s match=no" % (key, st, rp, line, want))
    print("PROVENANCE_SUMMARY state_rows=%d match=%d no_counter_sha=%d wrong_counter_sha=%d absent=%d" % (n, ok, noc, bad, absent))
    return 0 if (absent == 0 and noc == 0 and bad == 0) else 1

if __name__ == "__main__":
    sys.exit(main())
