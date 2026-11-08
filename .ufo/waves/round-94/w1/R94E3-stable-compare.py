#!/usr/bin/env python3
"""R94E3 — stable-line comparator for the round-94 C1 control battery replay.

Compares receipt sets pairwise on the STABLE lines only
(C1_ROW, C1_CONJUNCTS, C1_SUMMARY, C1_SOURCE, C1_R94_PASS, C1_SETUP), ignoring
the driver header (control=/clone_rev=/parent=/mutant=/counter_sha=) and exit=.

The one volatile token inside a STABLE line is the 40-hex `rev=<hash>` field of
C1_SUMMARY: it is the fixture clone's own commit, whose hash necessarily changes
between two runs of the same edit because the committer timestamp changes. This
script reports the comparison twice — strict (no scrub) and rev-normalized — and
proves that whenever the two readings disagree, the only differing bytes are one
`rev=<40 hex>` token, so the scrub cannot hide a real measurement change.

Usage:
  python3 -I R94E3-stable-compare.py [--produced DIR] [--committed DIR]
"""
import argparse
import difflib
import pathlib
import re
import sys

STABLE_PREFIX = ("C1_ROW", "C1_CONJUNCTS", "C1_SUMMARY", "C1_SOURCE",
                 "C1_R94_PASS", "C1_SETUP")
REV = re.compile(r"^rev=[0-9a-f]{40}$")


def stable_lines(path):
    """Return [(prefix, raw_line)] for stable lines, order preserved."""
    out = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if s.startswith(STABLE_PREFIX):
            out.append(s)
    return out


def scrub(line):
    """Replace only the whole-token `rev=<40hex>` field of a C1_SUMMARY line."""
    if not line.startswith("C1_SUMMARY "):
        return line
    parts = line.split(" ")
    parts = ["rev=<fixture-commit>" if REV.match(p) else p for p in parts]
    return " ".join(parts)


def scrub_is_token_only(a, b):
    """True iff a != b but they agree on every whitespace-separated token
    except one, and that token in each is `rev=<40 hex>`."""
    if a == b:
        return False
    ta, tb = a.split(), b.split()
    if len(ta) != len(tb):
        return False
    bad = [(x, y) for x, y in zip(ta, tb) if x != y]
    if len(bad) != 1:
        return False
    x, y = bad[0]
    return bool(REV.match(x)) and bool(REV.match(y))


def compare(label, a_path, b_path, report):
    a_raw, b_raw = stable_lines(a_path), stable_lines(b_path)
    a_scr = [scrub(x) for x in a_raw]
    b_scr = [scrub(x) for x in b_raw]

    strict_same = a_raw == b_raw
    scr_same = a_scr == b_scr

    diff_idx = [i for i, (x, y) in enumerate(zip(a_raw, b_raw)) if x != y]
    length_diff = len(a_raw) - len(b_raw)
    token_only = (not strict_same and scr_same and length_diff == 0
                  and all(scrub_is_token_only(a_raw[i], b_raw[i]) for i in diff_idx))

    if strict_same:
        status = "IDENTICAL"
    elif token_only:
        status = "REV-ONLY"
    else:
        status = "DRIFT"

    report.append(
        "%-9s %-32s lines=%2d raw_diff=%d scrubbed_diff=%d%s"
        % (status, label, len(a_scr),
           len(diff_idx) + abs(length_diff),
           sum(1 for x, y in zip(a_scr, b_scr) if x != y) + abs(length_diff),
           "" if token_only or strict_same else "  <-- non-token difference"))

    if status == "DRIFT":
        for line in difflib.unified_diff(a_scr, b_scr, "produced", "committed",
                                         lineterm="", n=0):
            report.append("      " + line[:240])
    return status


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--produced", default="/fast/scratch/hyaku/tameshi-r94/R94E3/receipts")
    ap.add_argument("--committed",
                    default="/home/vgpnk/Projects/shokunin/tameshi-shokunin/"
                            ".ufo/evidence/round-94/pre-freeze/controls")
    a = ap.parse_args()
    produced, committed = pathlib.Path(a.produced), pathlib.Path(a.committed)

    report = []
    drift = []

    # --- pass 1 (produced *.out, excluding reruns) vs the committed receipts ---
    report.append("== A. pass-1 receipts vs committed receipts (stable lines) ==")
    pass1 = sorted(p for p in produced.glob("*.out") if ".rerun-" not in p.name)
    for p in pass1:
        c = committed / p.name
        if not c.exists():
            report.append("MISSING-COMMITTED %s" % p.name)
            drift.append(p.name)
            continue
        if compare(p.name, p, c, report) == "DRIFT":
            drift.append(p.name)
    for c in sorted(committed.glob("*.out")):
        if not (produced / c.name).exists():
            report.append("MISSING-PRODUCED %s" % c.name)
            drift.append(c.name)
    report.append("   pass-1 receipts compared: %d" % len(pass1))

    # --- pass 2 (rerun-1) vs pass 1, and vs committed ---
    reruns = sorted(produced.glob("*.rerun-1.out"))
    report.append("")
    report.append("== B. rerun-1 receipts vs pass-1 receipts (stable lines) ==")
    for p in reruns:
        base = p.name[: -len(".rerun-1.out")] + ".out"
        other = produced / base
        if not other.exists():
            report.append("NO-PASS1 %s" % p.name)
            drift.append(p.name)
            continue
        if compare(p.name, p, other, report) == "DRIFT":
            drift.append(p.name)
    report.append("   rerun receipts compared: %d" % len(reruns))

    report.append("")
    report.append("== C. rerun-1 receipts vs committed receipts (stable lines) ==")
    for p in reruns:
        base = p.name[: -len(".rerun-1.out")] + ".out"
        other = committed / base
        if not other.exists():
            report.append("NO-COMMITTED %s" % p.name)
            drift.append(p.name)
            continue
        if compare(p.name, p, other, report) == "DRIFT" and p.name not in drift:
            drift.append(p.name)

    report.append("")
    report.append("differing_receipts=" + (",".join(sorted(set(drift))) if drift else "none"))
    report.append("VERDICT: " + ("reproduced" if not drift else "drift"))

    text = "\n".join(report) + "\n"
    sys.stdout.write(text)
    return 0 if not drift else 1


if __name__ == "__main__":
    sys.exit(main())
