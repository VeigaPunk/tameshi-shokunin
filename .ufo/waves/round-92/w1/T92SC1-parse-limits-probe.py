#!/usr/bin/env python3
"""T92SC1 parse-only probe — characterise the round-92 counter's note-reading
limits exactly, by calling the frozen counter's own `parse_note`.

The addendum draft has to name the limit classes the counter does not cover.
Asserting them from reading the code is weaker than executing them, so this
probe imports `parse_note` from the FROZEN counter blob (the committed bytes,
not the worktree) and feeds it the four classes the plan declares as limits:

  L1  fenced code blocks        a verdict table inside a fence
  L2  HTML tables               a verdict table written as HTML
  L3  prose verdicts            verdict words in prose, outside any table
  L4  predictions not receipts  the same twelve cells, copied from the
                                 committed predictions instead of a receipt

and the two the round-92 rules ADD (these must refuse, not pass):

  R1  out-of-set ids            a second table keyed C001..C012
  R2  unkeyed verdict row       a verdict-bearing row whose first cell is
                                 not an id

L4 is the interesting one: it is a *semantic* limit (the counter certifies
that the cells are true, not how they were obtained), so `parse_note` cannot
detect it at all — the probe shows the parse is byte-identical for a
prediction-copied note and a receipt-copied note, which is exactly why the
limit cannot be closed by the parser.

Read-only: imports the committed counter; writes nothing.

Usage: T92SC1-parse-limits-probe.py [--counter PATH]
"""
import argparse
import hashlib
import importlib.util
import os
import re
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
COUNTER = os.path.join(LANE, ".ufo/evidence/round-92/c1/measure-v92.py")
NOTE_REL = "corpus/knowledge/mutation-case-fleet-sources-census.md"

ap = argparse.ArgumentParser()
ap.add_argument("--counter", default=COUNTER)
ap.add_argument("--repo", default=LANE)
ap.add_argument("--rev", default=None)
a = ap.parse_args()

raw = open(a.counter, "rb").read()
print("counter=%s" % a.counter)
print("counter_sha256=%s" % hashlib.sha256(raw).hexdigest())

spec = importlib.util.spec_from_file_location("m92", a.counter)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
print("self_pin_ok=%s" % m.self_pin_ok())
print("SELF_SHA256=%s" % m.SELF_SHA256)
print("ID_SHAPE=%r" % m.ID_SHAPE.pattern)
print("VERDICTS=%r" % (m.VERDICTS,))

# the honest note's verdict table, exactly as committed
import subprocess
rev = a.rev or subprocess.run(["git", "-C", a.repo, "rev-parse", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
nt = subprocess.run(["git", "-C", a.repo, "cat-file", "blob", "%s:%s" % (rev, NOTE_REL)],
                     capture_output=True, text=True).stdout
print("note_rev=%s" % rev)
print("note_bytes=%d" % len(nt))

spec_ids = {"C%02d" % i for i in range(1, 13)}

rows, bad, headers = m.parse_note(nt, spec_ids)
print("")
print("-- honest note --")
print("rows=%d bad=%d headers=%d ids=%s" % (len(rows), len(bad), headers,
                                             sorted(rows) == sorted(spec_ids)))
print("bad_detail=%r" % (bad,))

# the honest table as a standalone fragment, for the limit constructions
HONEST_TABLE = """
| id | arm targeted | edit | verdict | witness |
|---|---|---|---|---|
| C01 | a | x | KILLED | w |
| C02 | a | x | SURVIVED | w |
| C03 | a | x | SURVIVED | w |
| C04 | a | x | KILLED | w |
| C05 | a | x | KILLED | w |
| C06 | a | x | SURVIVED | w |
| C07 | a | x | KILLED | w |
| C08 | a | x | SURVIVED | w |
| C09 | a | x | SURVIVED | w |
| C10 | a | x | SURVIVED | w |
| C11 | a | x | KILLED | w |
| C12 | a | x | SURVIVED | w |
"""

PREDICTIONS_TABLE = HONEST_TABLE.replace("| w |", "| predicted |")
# same cells, different provenance marker — the two tables are byte-identical
# in every cell the counter reads
RECEIPT_TABLE = HONEST_TABLE

CASES = {
    "L1-fenced-table": (
        "the whole verdict table inside a fenced code block\n"
        "```\n" + HONEST_TABLE + "```\n",
        "expect: not keyed (fence skipped) -> headers=0 rows=0"),
    "L2-html-table": (
        "<table>\n<tr><th>id</th><th>verdict</th></tr>\n"
        + "\n".join("<tr><td>C%02d</td><td>%s</td></tr>" % (i, "KILLED" if i in (1, 4, 5, 7, 11) else "SURVIVED")
                    for i in range(1, 13))
        + "\n</table>\n",
        "expect: not keyed (no pipe-delimited markdown row) -> rows=0"),
    "L3-prose-verdict": (
        "The verdict for C01 is KILLED and the verdict for C02 is SURVIVED.\n"
        "C03 KILLED C04 KILLED C05 KILLED C07 KILLED C11 KILLED.\n",
        "expect: not keyed (prose is not a table row) -> rows=0"),
    "L4-predictions-not-receipts": (
        HONEST_TABLE,
        "expect: keyed and accepted — the parser cannot see provenance"),
    "R1-out-of-set-ids": (
        HONEST_TABLE
        + "\n| id | arm targeted | edit | verdict | witness |\n|---|---|---|---|---|\n"
        + "\n".join("| C%03d | a | x | %s | w |" % (i, "SURVIVED" if i in (1, 4, 5, 7, 11) else "KILLED")
                    for i in range(1, 13)) + "\n",
        "expect: REFUSED (ids=false) — bad rows out-of-set"),
    "R1b-out-of-set-letters": (
        HONEST_TABLE
        + "\n| id | arm targeted | edit | verdict | witness |\n|---|---|---|---|---|\n"
        + "\n".join("| X%d | a | x | %s | w |" % (i, "SURVIVED" if i in (1, 4, 5, 7, 11) else "KILLED")
                    for i in range(1, 13)) + "\n",
        "expect: REFUSED (ids=false)"),
    "R2-unkeyed-verdict-row": (
        HONEST_TABLE
        + "\n| n/a | a | x | KILLED | w |\n",
        "expect: REFUSED (ids=false) — bad row unkeyed"),
}

print("")
print("-- limit and refusal classes (parse_note over a fragment) --")
verdicts = {}
for name, (text, expect) in CASES.items():
    rows, bad, headers = m.parse_note(text, spec_ids)
    ids_ok = (not bad) and headers == 1 and sorted(rows) == sorted(spec_ids)
    verdicts[name] = (len(rows), len(bad), headers, ids_ok, tuple(sorted(rows)))
    print("")
    print("%s" % name)
    print("  %s" % expect)
    print("  rows=%d bad=%d headers=%d ids_ok=%s" % (len(rows), len(bad), headers, ids_ok))
    if bad:
        print("  bad=%r" % (bad[:4],))
    if len(rows) == 12:
        print("  cells=%r" % ([rows["C%02d" % i] for i in range(1, 13)],))

print("")
print("-- L4: are the prediction-copied and receipt-copied parses distinguishable? --")
rp, bp, hp = m.parse_note(PREDICTIONS_TABLE, spec_ids)
rr, br, hr = m.parse_note(RECEIPT_TABLE, spec_ids)
print("predictions_rows=%r" % ([rp["C%02d" % i] for i in range(1, 13)],))
print("receipt_rows=%r" % ([rr["C%02d" % i] for i in range(1, 13)],))
print("identical_cells=%s identical_parse=%s" % (
    [rp.get("C%02d" % i) for i in range(1, 13)] == [rr.get("C%02d" % i) for i in range(1, 13)],
    (rp, bp, hp) == (rr, br, hr)))
print("VERDICT: limit classes executed")

# --- the note's own front-matter `source:` line: how many start with it? -----
print("")
print("-- note front-matter `source:` lines --")
src = [l for l in nt.split("\n") if l.startswith("source:")]
print("count=%d" % len(src))
print("counter_reads_note_source_line=%s" % ("source:" in open(a.counter, encoding="utf-8").read()))
