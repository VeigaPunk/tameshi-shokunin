#!/usr/bin/env python3
"""R93M1 independent cross-check of the C2 conjunct disposition.

Reads the committed battery receipts and the committed C2 manifest and confirms,
without running tools/conjunct-disposition.py, that every one of the counter's 19
conjunct keys is either false in the named receipt (mode conjunct-false), present
as the named C1_SETUP token (mode setup-refusal), or declared unfalsifiable with a
reason of >=40 chars naming a pin/seal mechanism.

This is the cross-check behind the report's "literal QUALITY 158" paragraph. It
does not replace the C2 checker; it is an independent read of the same bytes.
"""
import json
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
REV = "855f0c1c59ee2af7f184d8de62d02cdd576eb94e"
RECEIPTS = os.path.join(LANE, ".ufo/evidence/round-93/pre-freeze/controls")
MANIFEST = os.path.join(LANE, "tools/conjunct-disposition.json")
COUNTER = ".ufo/evidence/round-93/c1/measure-v93.py"
MIN_REASON = 40
MECHANISM = ("pin", "sealed", "seal", "gate bytes", "GIT_", "pinned", "replace")


def blob(rev, path):
    return subprocess.run(["git", "-C", LANE, "cat-file", "blob", rev + ":" + path],
                          capture_output=True, check=True).stdout.decode()


def latest_receipt(name):
    cands = [name + ".out"] + ["%s.rerun-%d.out" % (name, i) for i in range(1, 50)]
    found = [c for c in cands if os.path.exists(os.path.join(RECEIPTS, c))]
    return os.path.join(RECEIPTS, found[-1]) if found else None


def conj_of(body):
    for line in body.split("\n"):
        if line.startswith("C1_CONJUNCTS "):
            return {kv.split("=", 1)[0]: kv.split("=", 1)[1] == "true"
                    for kv in line.split()[1:]}
    return {}


def main():
    src = blob(REV, COUNTER)
    m = re.search(r"CONJUNCT_KEYS = \((.*?)\)\n", src, re.S)
    keys = re.findall(r'"([a-z0-9_]+)"', m.group(1))
    manifest = json.load(open(MANIFEST))
    rows = manifest["rows"]
    findings = []
    fals = {}
    for k in keys:
        row = rows.get(k)
        if row is None:
            findings.append("missing-row " + k)
            continue
        if "unfalsifiable" in row:
            reason = str(row["unfalsifiable"]).strip()
            if len(reason) < MIN_REASON or not any(t in reason.lower() for t in MECHANISM):
                findings.append("bad-unfalsifiable " + k)
            continue
        path = latest_receipt(row["state"])
        if not path:
            findings.append("no-receipt " + k)
            continue
        body = open(path, encoding="utf-8", errors="replace").read()
        if row["mode"] == "setup-refusal":
            if ("C1_SETUP " + row.get("token", "")) not in body:
                findings.append("token-absent " + k)
        else:
            conj = conj_of(body)
            if conj.get(k) is not False:
                findings.append("no-flip %s %s" % (k, path))
            else:
                fals.setdefault(k, []).append(os.path.basename(path))
    for k in rows:
        if k not in keys:
            findings.append("unknown-key " + k)
    print("COUNTER_KEYS", " ".join(keys))
    for k in keys:
        if k in fals:
            print("FALSE_IN %-16s %s" % (k, ",".join(fals[k])))
        else:
            row = rows.get(k, {})
            print("DECLARED %-15s %s" % (k, "unfalsifiable" if "unfalsifiable" in row else row.get("mode")))
    fals_n = sum(1 for k in keys
                 if "unfalsifiable" not in rows.get(k, {})
                 and (k in fals or rows.get(k, {}).get("mode") == "setup-refusal"))
    unf_n = sum(1 for k in keys if "unfalsifiable" in rows.get(k, {}))
    print("INDEPENDENT_CONJUNCT_CHECK rows=%d falsifiable=%d unfalsifiable=%d findings=%d" % (
        len(keys), fals_n, unf_n, len(findings)))
    for f in findings:
        print("FINDING", f)
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
